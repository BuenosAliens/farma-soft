#!/usr/bin/env python


# Importamos los módulos y paquetes necesarios
import csv
import preparaCsv
import validacion
from datetime import datetime

# Módulo necesario para realizar las búsquedas y tenerlas listas para mostrar
import busqueda 

# Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask import Flask, render_template, redirect, request, url_for, flash, session

# Formularios Flask
from formulariosFlask import LoginForm, ProductForm, ClienteForm, CrearUsuario

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

# Validacion del archivo csv
nombre_de_archivo = 'farmacia.csv'
validacion.validar(nombre_de_archivo)
registros = preparaCsv.genera_clase(nombre_de_archivo)

# Bootstrap local
app.config['SECRET_KEY'] = 'palabra'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# Templates de errores
@app.errorhandler(404)
def no_encontrado(e):
    if 'username' in session:
        return render_template('404.html'), 404
    else:
        flash('No se han encontrado registros.')
        return redirect(url_for('ingresar'))

@app.errorhandler(500)
def error_interno(e):
    if 'username' in session:
        return render_template('500.html'), 500
    else:
        flash('Error en el servidor.')
        return redirect(url_for('ingresar'))


# Routes de las páginas del sitio/app

# Inicio
@app.route('/')
def index():
    return render_template('index.html')


# Intro
@app.route('/bienvenida')
def bienvenida():
    if 'username' in session:
        return render_template('bienvenida.html')
    else:
        flash('Para acceder debe estar logeado.')
        return redirect(url_for('ingresar'))

# Pantalla de log-in
@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():

    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios.csv') as archivo:
            archivo_csv = csv.reader(archivo)
            register = next(archivo_csv)
            while register:
                if formulario.usuario.data == register[0] and formulario.password.data == register[1]:
                    flash('Bienvenido '+ formulario.usuario.data)
                    session['username'] = formulario.usuario.data
                    return redirect(url_for('ultimas_ventas'))
                register = next(archivo_csv, None)
            else:
                flash('Nombre de usuario y/o contraseña equivocados.')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


# Pantalla de log-out
@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logout.html')
    else:
        return redirect(url_for('index'))

# Mostrar las últimas ventas
@app.route('/ultimas_ventas', methods=['GET', 'POST'])
def ultimas_ventas():
    if 'username' in session:   
        ultimos = 5
        last_s = []
        last_s=busqueda.listar_ventas(registros, ultimos)
        return render_template('ultimas_ventas.html',last_s=last_s)
    else:
        flash('Para acceder debe estar logueado.')
        return redirect(url_for('ingresar'))


# Productos buscados por cliente
@app.route('/pXclientes', methods=['GET', 'POST'])
def pXclientes():
    if 'username' in session:
        formulario = ClienteForm()
        if formulario.validate_on_submit():
            cliente = formulario.cliente.data.upper()
            if len(cliente) < 3:
                flash('Debe tipear 3 caracteres como mínimo para poder realizar la busqueda')
                return render_template('pXclientes.html', form = formulario)
            else:
                val = busqueda.encontrar_clientes(registros,cliente)#llama a funcion para validar si exiten los clientes
                if len(val) == 0:
                    flash('No seencontraron registros')
                elif len(val) == 1:
                    listar = busqueda.listar_productos_cliente(registros,cliente)
                    return render_template('pXclientes.html', form = formulario, listar = listar, cliente= formulario.cliente.data.upper())
                else:
                    flash('Se encontraron registros, seleccione uno.')
                    return render_template('pXclientes.html', form = formulario, clientes = val)
        return render_template('pXclientes.html', form = formulario)
    else:
        flash('Para poder ingresar debeestar logueado.')
        return redirect(url_for('ingresar'))


# Selección de clientes (cuando el resultado es mayor a 1)
@app.route('/pXclientes/<clientes>', methods=['GET', 'POST'])
def pXclientes2(clientes):
    if 'username' in session:
        formulario = ClienteForm()
        if formulario.validate_on_submit():
            cliente = formulario.cliente.data.upper()
            if len(cliente) < 3:
                flash('Debe tipear 3 caracteres como mínimo para realizar la búsqueda.')
                return redirect(url_for('pXclientes'))
            else:
                val = busqueda.encontrar_clientes(registros,cliente)
                if len(val) == 0:
                    flash('No se encontraron registros.')
                    return redirect(url_for('pXclientes'))                   
                elif len(val) == 1:
                    listar = busqueda.listar_productos_cliente(registros,cliente)
                    return render_template('pXclientes.html', form = formulario, listar = listar, cliente= formulario.cliente.data.upper())
                else:
                    flash('Se encontraron registros, seleccione uno.')
                    return render_template('pXclientes.html', form = formulario, clientes = val)
        else:
            cliente = clientes
            val = busqueda.encontrar_clientes(registros,cliente)
            listar = busqueda.listar_productos_cliente(registros,cliente)
            return render_template('pXclientes.html', form = formulario, listar = listar, cliente= cliente)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))

# Clientes buscados por productos
@app.route('/clientes_prod', methods=['GET', 'POST'])
def clientes_prod():
    if 'username' in session:
        formulario = ProductForm()
        if formulario.validate_on_submit():
            producto = formulario.producto.data.upper()
            if len(producto) < 3:
                flash('Debe tipear al menos tres caracteres para poder realizar la búsqueda.')
                return render_template('clientes_prod.html', form=formulario)
            else:
                val = busqueda.encontrar_productos(registros, producto)
                if len(val) == 0:
                    flash('No se encontraron registros.')
                elif len(val) == 1:
                    listar = busqueda.listar_clientes_producto(registros,producto)
                    return render_template('clientes_prod.html', form = formulario, listar = listar, producto= formulario.producto.data.upper())
                else:
                    flash('Se encontraron registros, seleccione uno.')
                    return render_template('clientes_prod.html', form = formulario, productos = val)
        return render_template('clientes_prod.html', form=formulario)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))

# selección de producto cuando el resultado es mayor que 1
@app.route('/clientes_prod/<productos>', methods=['GET', 'POST'])
def cliente_prod2(productos):
    if 'username' in session:
        formulario = ProductForm()
        if formulario.validate_on_submit():
            producto = formulario.producto.data.upper()
            if len(producto) < 3:
                flash('Debe tipear como mínimo 3 caracteres para poder realizar la busqueda')
                return redirect(url_for('clientes_prod'))
            else:
                val = busqueda.encontrar_productos(registros,producto)
                if len(val) == 0:
                    flash('No se encontraron registros.')
                    return redirect(url_for('clientes_prod'))                   
                elif len(val) == 1:
                    listar = busqueda.listar_clientes_producto(registros,producto)
                    return render_template('clientes_prod.html', form = formulario, listar = listar, producto= formulario.producto.data.upper())
                else:
                    flash('Se encontraron registros, seleccione uno.')
                    return render_template('clientes_prod.html', form = formulario, productos = val)
        else:
            producto = productos
            val = busqueda.encontrar_productos(registros,producto)
            listar = busqueda.listar_clientes_producto(registros,producto)
            return render_template('clientes_prod.html', form = formulario, listar = listar, producto = producto)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))



# Listado de productos
@app.route('/mas_vendidos', methods=['GET', 'POST'])
def mas_vendidos():
    if 'username' in session:
        producto_res = []
        cantidad = 5
        producto_res = busqueda.mas_vendidos(registros = registros, cantidad=cantidad)
        return render_template('mas_vendidos.html', producto_res = producto_res)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))


# Clientes que más gastaron en compras
@app.route('/mejoresClientes', methods=['GET', 'POST'])
def mejoresClientes():
    if 'username' in session:
        producto_res = []
        cantidad = 5
        producto_res = busqueda.mas_gastaron(registros = registros, cantidad=cantidad)
        return render_template('mejoresClientes.html', producto_res = producto_res)
    else:
        flash('Para poder acceder debe estar logueado.')
        return redirect(url_for('ingresar'))

#Creación de usuarios
@app.route('/nuevoUsuario', methods=['GET', 'POST'])
def nuevoUsuario():
    formulario = CrearUsuario()
    if formulario.validate_on_submit():
        usuario = formulario.usuario_n.data
        password = formulario.password_n.data
        busqueda.agregar(usuario, password)
    return render_template('nuevoUsuario.html', formulario = formulario)

if __name__ == "__main__":
    manager.run()
