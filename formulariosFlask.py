from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario: ', validators=[Required()])
    password = PasswordField('Contraseña: ', validators=[Required()])
    enviar = SubmitField('Enviar')

class ClienteForm(FlaskForm):
    cliente = StringField('Ingrese el nombre del cliente', validators=[Required()])
    enviar = SubmitField('Enviar')

class ProductForm(FlaskForm):
    producto = StringField('Ingrese el nombre del producto', validators=[Required()])
    enviar = SubmitField('Enviar')

class CrearUsuario(FlaskForm):
	usuario_n = StringField('Nombre de usuario: ', validators=[Required()])
	password_n = PasswordField('Contraseña: ', validators=[Required()])
	enviar = SubmitField('Enviar')




