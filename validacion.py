#!/usr/bin/python3

# validar csv
def validar(nombre_archivo):
    import csv
    class RegistroExcede(Exception):
        pass

    class MiError(Exception):
        pass
    CAMPOS = 5 
    try:
        with open(nombre_archivo, 'r', encoding='latin-1') as archivo:
            archivo_csv=csv.reader(archivo)
            registro = 1
            campo = 1
            for linea in archivo_csv:
                if len (linea) != CAMPOS:
                    raise RegistroExcede()
                else:
                    x=0
                    for x in range(CAMPOS):
                        campo = x + 1
                        if linea[x] == '':
                            error= 'El registro {} se encuentrea vacío en: {}'.format(campo, registro)
                            raise MiError(error)
                        else:
                            pass
                        if registro == 1:
                            w_column = linea[x].strip(' ')
                            w_column = w_column.upper()
                            if w_column == 'PRECIO':
                                colum_precio = x
                            elif w_column =='CANTIDAD':
                                colum_cantidad = x
                            else:
                                pass                 
                        else:
                            if x == colum_cantidad:
                                val_columa=int(float(linea[x]))
                            elif x == colum_precio:
                                w_column = linea[x].strip(' ')
                                if w_column.isdigit() == True:
                                    raise ValueError()
                                else:
                                    f=float(linea[x])                            
                            else:
                                pass
           
                registro = registro + 1
            print('Archivo Ok!!')                 
    except FileNotFoundError:
        print('No se encuentra el archivo')
    except PermissionError:
        print('No tiene los permisos necesarios')
    except RegistroExcede:
        mensaje='{} Los registros no son los correctos'.format(linea)
        print(mensaje)
        with open('Error.log','w') as error_file:
            error_file.write(mensaje)
    except ValueError:
        if x == colum_cantidad:
            print('El registro {} un valor incorrecto en CANTIDAD'.format(registro))
        else:
            print('El registro {} un valor incorrecto en PRECIO'.format(registro, x))







