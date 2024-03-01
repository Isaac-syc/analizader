import ply.yacc as yacc

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
]

def p_statement(p):
    '''statement : assignment_statement
                    | for_loop
                    | if_statement
                    | main_function
                    | function_call'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : IDENTIFICADOR ASIGNACION CADENA'''
    p[0] = True

def p_for_loop(p):
    '''for_loop : PALABRA_RESERVADA PARENTESIS_ABRIR IDENTIFICADOR COMA ENTERO COMA ENTERO PARENTESIS_CERRAR LLAVE_I LLAVE_F'''
    if p[1] == 'FOR':
        p[0] = True
    else:
        p[0] = False

def p_if_statement(p):
    '''if_statement : PALABRA_RESERVADA PARENTESIS_ABRIR IDENTIFICADOR OPERADOR_RELACIONAL ENTERO PARENTESIS_CERRAR LLAVE_I LLAVE_F'''
    if p[1] == 'IF':
        p[0] = True
    else:
        p[0] = False

def p_main_function(p):
    '''main_function : PALABRA_RESERVADA PARENTESIS_ABRIR PARENTESIS_CERRAR LLAVE_I LLAVE_F'''
    if p[1] == 'MAIN':
        p[0] = True
    else:
        p[0] = False

def p_function_call(p):
    '''function_call : PALABRA_RESERVADA IDENTIFICADOR PARENTESIS_ABRIR parametros PARENTESIS_CERRAR LLAVE_I LLAVE_F'''
    if p[1] == 'FUNC':
        p[0] = True
    else:
        p[0] = False
    
def p_parametros(p):
    '''parametros : IDENTIFICADOR
                    | ENTERO'''
    p[0] = True

def p_error(p):
    print("Error de sintaxis")

parser = yacc.yacc()

def parsear(input_text):
    try:
        result = parser.parse(input_text)
        print("result:", result)
        return result
    except Exception as e:
        print("Error:", e)
        return False
