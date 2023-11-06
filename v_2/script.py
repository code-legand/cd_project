# Define reserved keywords
reserved = {
    'int': 'INT',
    'main': 'MAIN',
    'begin': 'BEGINS',
    'end': 'ENDS',
    'while': 'WHILE',
    'return': 'RETURN',
}

# Define tokens
tokens = [
    'OPENPARAN', 'CLOSEPARAN', 'GREATER', 'EQUAL', 'PLUS', 'DIVIDE',
    'NUM', 'ID', 'SEMICOL', 'NL', 'SP'
] + list(reserved.values())

# Define token patterns
t_OPENPARAN = r'\('
t_CLOSEPARAN = r'\)'
t_GREATER = r'>'
t_EQUAL = r'='
t_PLUS = r'\+'
t_DIVIDE = r'/'
t_NUM = r'[0-9]+'
t_SEMICOL = r';'
t_NL = r'\n'
t_SP = r'[ \t]+'

# Define the lexer functions
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Ignored characters
t_ignore = ''


# Initialize variables
var = None
num = None

# Define the lexer functions
def t_error(t):
    print(f"Invalid token: {t.value[0]}")
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Define the parser rules
counterVar = None
n = None
numVar = None

def p_program(p):
    '''program : INT SP MAIN OPENPARAN CLOSEPARAN NL BEGINS NL stmt ENDS'''
    print("Valid")

def p_stmt(p):
    '''stmt : declstmt whilestmt returnstmt'''
    pass

def p_declstmt(p):
    '''declstmt : SP INT SP ID EQUAL NUM SEMICOL NL'''
    global counterVar, n
    counterVar = var
    n = num

def p_whilestmt(p):
    '''whilestmt : SP WHILE OPENPARAN ID GREATER NUM CLOSEPARAN NL whilebody SP ENDS SP WHILE NL'''
    global numVar
    numVar = var

def p_whilebody(p):
    '''whilebody : SP ID EQUAL ID PLUS NUM SEMICOL NL SP ID EQUAL ID DIVIDE NUM SEMICOL NL'''
    pass

def p_returnstmt(p):
    '''returnstmt : SP RETURN SP ID NL'''
    pass

def p_error(p):
    print("Invalid syntax")

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()

# Main function to read input file and parse the program
def main(input_file):
    with open(input_file, 'r') as file:
        data = file.read()
        lexer.input(data)
        parser.parse(data)

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("USAGE: python script.py <input file>")
        sys.exit(1)

    main(sys.argv[1])
