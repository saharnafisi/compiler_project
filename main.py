import ply
tokens = (
    'STR', 'ID', 'MINUS',
    'PLUS', 'LPAR', 'RPAR',
    'NEWLINE', 'ASSIGN',
    'SEMICOL', 'MUL', 'DIV',
    'NUMBER','COLON', 'LBRACKET', 'RBRACKET')
t_MINUS = r'\-'
t_LPAR = r'\('
t_RPAR = r'\)'
t_ASSIGN = r'\=:'
t_PLUS = r'\+'
t_SEMICOL = r';'
t_MUL = r'\*'
t_DIV = r'/'
t_COLON = r':'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ignore = ' \t'


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z]+[a-zA-Z0-9]*'
    return t


def t_STR(t):
    r'\"(?:[^\\"]|\\.)*\"'
    t.value = t.value.replace('"', '')
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex
lexer = lex.lex()


"""lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
"""

symt = {}


def p_stmts(p):
    """
    stmts : stmt SEMICOL
            | stmt SEMICOL NEWLINE stmts
            |
    """


def p_stmt(p):
    """stmt : ID LPAR expr RPAR
            | ID ASSIGN ID LPAR RPAR
            | ID ASSIGN expr"""

    if len(p) == 5:
        if p[1] == 'print':
            print(p[3])
        else:
            print("syntax error: only 'print'")
    if len(p) == 6:
        if p[3] == 'input':
            symt[p[1]] = input()
        else:
            print("syntax error: only 'input'")
    if len(p) == 4:
        symt[p[1]] = p[3]


def p_stmt2(p):
    """
    stmt : ID ASSIGN ID LPAR expr RPAR
    """
    if p[3] == 'input':
        symt[p[1]] = input(p[5])
    else:
        print("syntax error: only 'input'")


def p_expr2(p):
    """expr : term
            | expr LBRACKET NUMBER RBRACKET """
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = p[1][p[3]]


def p_expr3(p):
    """expr : expr PLUS term"""
    p[0] = p[1] + p[3]

def p_expr5(p):
    """expr : expr MINUS term"""
    if len(p)==4:
        p[0] = p[1] - p[3]
    else:
        p[0]=p[1]


def p_term(p):
    """term : term MUL factor
            | factor
    """
    if len(p)==4:
        p[0] = p[1] * p[3]
    else:
        p[0]=p[1]

def p_term2(p):
    """term : term DIV factor
    """
    p[0] = p[1] / p[3]

def p_factor0(p):
    """factor : NUMBER
    """
    p[0] = p[1]

def p_factor(p):
    """factor : STR
            | LPAR expr RPAR
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_factor2(p):
    """factor : ID """
    p[0] = symt[p[1]]


def p_error(t):
    print("syntax error at '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()

with open('test_input1.txt') as input_file:
    data = input_file.read()
    parser.parse(data)
