import ply.yacc as yacc
import io
import contextlib
import sys

def ejecutar_cadena(cadena):
    # Crea un buffer para la salida del código ejecutado
    buffer = io.StringIO()
    # Variable para almacenar el resultado de la ejecución
    resultado = None
    # Captura la salida estándar actual para restaurarla más tarde
    stdout_original = sys.stdout
    try:
        # Redirige la salida estándar al buffer
        sys.stdout = buffer
        # Ejecuta el código
        exec(cadena)
        # Lee el resultado del buffer
        resultado = buffer.getvalue()
    except Exception as e:
        # Imprime el error en la salida estándar actual (la consola)
        print("Error de ejecución:", e)
        resultado = False
    finally:
        # Asegurarse de restaurar la salida estándar a su valor original
        sys.stdout = stdout_original
        # Cierra el buffer
        buffer.close()
    return resultado


def parsear(texto):
    tokens = [
        'IDENTIFICADOR',
        'ASIGNACION',
        'ENTERO',
        'CADENA',
        'PALABRA_RESERVADA',
        'PARENTESIS_ABRIR',
        'PARENTESIS_CERRAR',
        'LLAVE_I',
        'LLAVE_F',
        'COMA',
        'OPERADOR_RELACIONAL',
        'CONTENIDO',
        'DOS_PUNTOS',
    ]

    def p_statement(p):
        '''statement : assignment_statement
                        | for_loop
                        | if_statement
                        | main_function'''
        p[0] = p[1]

    def p_assignment_statement(p):
        '''assignment_statement : IDENTIFICADOR ASIGNACION CADENA'''
        cadena = texto
        respuesta = ejecutar_cadena(cadena)
        p[0] = {'resultado': True, 'output': respuesta}

    def p_for_loop(p):
        '''for_loop : PALABRA_RESERVADA PARENTESIS_ABRIR IDENTIFICADOR COMA ENTERO COMA ENTERO PARENTESIS_CERRAR LLAVE_I CONTENIDO LLAVE_F'''
        if p[1] == 'FOR':
            p[0] = {'resultado': True, 'output': ''}
            print(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11])
            nueva_cadena = 'for ' + p[3] + ' in range(' + str(p[5]) + ', ' + str(p[7]) + '): ' + p[10]
            respuesta = ejecutar_cadena(nueva_cadena)
            p[0]['output'] = respuesta
            
        else:
            p[0] = {'resultado': False, 'output': ''}

    def p_if_statement(p):
        '''if_statement : PALABRA_RESERVADA PARENTESIS_ABRIR ENTERO OPERADOR_RELACIONAL ENTERO PARENTESIS_CERRAR LLAVE_I CONTENIDO LLAVE_F'''
        if p[1] == 'IF':
            p[0] = {'resultado': True, 'output': ''}

            print(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])
            nueva_cadena = 'if ' + str(p[3]) + ' ' + p[4] + ' ' + str(p[5]) + ': ' + p[8]
            respuesta = ejecutar_cadena(nueva_cadena)
            p[0]['output'] = respuesta
        else:
            p[0] = False

    def p_main_function(p):
        '''main_function : PALABRA_RESERVADA PARENTESIS_ABRIR PARENTESIS_CERRAR LLAVE_I CONTENIDO LLAVE_F'''
        if p[1] == 'MAIN':
            p[0] = {'resultado': True, 'output': ''}
            respuesta = ejecutar_cadena(p[5])
            p[0]['output'] = respuesta
        else:
            p[0] = False


    def p_parametros(p):
        '''parametros :  ENTERO'''
        p[0] = True

    def p_error(p):
        print("Error de sintaxis")

    parser = yacc.yacc()
    try:
        informacion = parser.parse(texto)
        resultado = informacion['resultado']
        output = informacion['output']
        print(f"Resultado: {resultado}")
        print(f"Output: {output}")
        return resultado, output
    except Exception as e:
        print("Errorrrr:", e)
        return False, ''
