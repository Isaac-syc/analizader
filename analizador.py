import ply.lex as lex
import tkinter as tk
from tkinter import ttk
from parseador import parsear

# Definición de tokens
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

t_ASIGNACION = r'='
t_PARENTESIS_ABRIR = r'\('
t_PARENTESIS_CERRAR = r'\)'
t_LLAVE_I = r'\{'
t_LLAVE_F = r'\}'
t_COMA = r','
t_OPERADOR_RELACIONAL = r'[<>]=?|!=|=='
t_PALABRA_RESERVADA = r'FOR|IF|MAIN|FUNC'

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_IDENTIFICADOR(t):
    r'[a-z]+'
    t.type = 'IDENTIFICADOR'
    return t

# def t_CARACTER_NO_RECONOCIDO(t):
#     r'[^a-z\d\s"=(){}<>,!+-]'
#     t.value = (t.value[0],)
#     return t

t_ignore = ' \n\t'

def t_error(t):
    error_message = f"Caracter no reconocido: '{t.value[0]}'"
    t.value = ('CARACTER_NO_RECONOCIDO', error_message)
    return t

lexer = lex.lex()

def analyze_text(text):
    lexer.input(text)
    tokens_result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_result.append((tok.type, tok.value))
    return tokens_result

def on_analyze():
    input_text = text_entry.get("1.0", tk.END)
    tokens_result = analyze_text(input_text)
    print("tokens_result:", tokens_result)

    result = parsear(input_text)
    print("result de analizador:", result)
    if result == True:
        result_text = "Cadena válida."
    else:
        result_text = "Cadena inválida."

    for item in tree.get_children():
        tree.delete(item)

    for i, (token_type, lexeme) in enumerate(tokens_result, start=1):
        tree.insert("", "end", values=(i, token_type, lexeme))

    # Muestra el resultado en la interfaz gráfica
    tree.insert("", "end", values=("Resultado", result_text))

root = tk.Tk()
root.title("Lexer GUI")

root.geometry("320x400")

text_entry = tk.Text(root, height=3, width=40)
text_entry.pack(pady=10)

analyze_button = tk.Button(root, text="Analyze", command=on_analyze)
analyze_button.pack()

columns = ("#", "Tipo de Token", "Lexema")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack()
root.mainloop()
