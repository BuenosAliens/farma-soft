#!/usr/bin/python3

# Prepara a los campos obtenidos de la base de datos "farmacia.csv" para ser mostrados cuando sea requerido
import csv
def genera_clase(nombre_archivo):
    class Csv:
        def __init__ (self, cliente, codigo, producto, cantidad, precio):
            self.cliente = cliente
            self.codigo = codigo
            self.producto = producto
            self.cantidad = cantidad
            self.precio = precio
        def __str__ (self):
            return '{}, {}, {}, {}, {}'.format(self.cliente, self.codigo, self.producto, self.cantidad, self.precio)
        def __repr__ (self):
            return '{}, {}, {}, {}, {}'.format(self.cliente, self.codigo, self.producto, self.cantidad, self.precio)
        def __gt__ (self, otro):
            return self.cantidad > otro.cantidad
        def compra (self):
            return self.cantidad * self.precio

    cl = 0
    cd = 0
    cpro = 0
    cc = 0
    cpre = 0
    registros = []

    with open(nombre_archivo, 'r', encoding = 'latin-1') as archivo:
        archivo_csv = csv.reader(archivo)
        a = 0
        for linea in archivo_csv:
            if a == 0:
                b = 0
                for b in range(5):
                    fields = linea[b].strip(' ')
                    fields = fields.upper()
                    if fields == 'CLIENTE':
                        cl = b
                    elif fields == 'CODIGO':
                        cd = b
                    elif fields == 'PRODUCTO':
                        cpro = b
                    elif fields == 'CANTIDAD':
                        cc = b
                    else:
                        cpre = b
                    b = b + 1
                a = a + 1

            else:
                registros.append(Csv(cliente = linea[cl].strip(' ').upper(), codigo = linea[cd].strip(' '), producto = linea[cpro].strip(' ').upper(), cantidad = int(float(linea[cc].strip(' '))), precio = float(linea[cpre].strip(' '))))
    return (registros)

                

            
    

