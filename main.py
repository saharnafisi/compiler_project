import ply
tokens = (
    'STR', 'ID', 'MINUS',
    'PLUS', 'LPAR', 'RPAR',
    'NEWLINE', 'ASSIGN',
    'SEMICOL', 'MUL', 'DIV',
    'NUMBER', 'COLON', 'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE', 'MCOMMENT',
    'EQ', 'NEQ', 'GT', 'LT')
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
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQ = r'\='
t_NEQ = r'<>'
t_LT = r'<'
t_GT = r'>'
t_ignore = ' \t'


def t_MCOMMENT(t):
    r'\/\*(\*(?!\/)|[^*])*\*\/'
    t.lexer.lineno += t.value.count("\n")
    return t


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


def p_start(p):
    """start : comment LBRACE newline stmts newline RBRACE comment
            |
    """


def p_newline(p):
    """newline : NEWLINE
                | """

def p_stmts(p):
    """
    stmts : stmt SEMICOL newline stmts
            | comment stmts
            | stmts comment
            |
    """


def p_comment(p):
    """comment : MCOMMENT newline
                | """


def p_stmt1(p):
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


def p_expr1(p):
    """expr : term
            | expr LBRACKET NUMBER RBRACKET
            | expr LBRACKET NUMBER COLON RBRACKET
            | expr LBRACKET NUMBER COLON NUMBER RBRACKET"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = p[1][p[3]]
    elif len(p) == 6:
        p[0] = p[1][p[3]:]
    else:
        p[0] = p[1][p[3]:p[5]]


def p_expr2(p):
    """expr : expr PLUS term
            | expr LBRACKET COLON NUMBER RBRACKET"""
    if len(p) == 4:
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1][:p[4]]


def p_expr3(p):
    """expr : expr MINUS term"""
    if len(p) == 4:
        p[0] = p[1] - p[3]
    else:
        p[0] = p[1]


def p_expr4(p):
    """expr : expr EQ expr"""
    if p[1] == p[3]:
        p[0] = True
    else:
        p[0] = False


def p_expr5(p):
    """expr : expr NEQ expr"""
    if p[1] != p[3]:
        p[0] = True
    else:
        p[0] = False


def p_expr6(p):
    """expr : expr GT expr"""
    if p[1] > p[3]:
        p[0] = True
    else:
        p[0] = False


def p_expr7(p):
    """expr : expr LT expr"""
    if p[1] < p[3]:
        p[0] = True
    else:
        p[0] = False


def p_term1(p):
    """term : term MUL factor
            | factor
    """
    if len(p) == 4:
        p[0] = p[1] * p[3]
    else:
        p[0] = p[1]


def p_term2(p):
    """term : term DIV factor
    """
    p[0] = p[1] / p[3]


def p_factor1(p):
    """factor : primary
                | PLUS factor
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_factor2(p):
    """factor : MINUS factor"""
    p[0] = -1 * p[2]


def p_primary1(p):
    """primary : STR
            | LPAR expr RPAR
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_primary2(p):
    """primary : ID """
    p[0] = symt[p[1]]


def p_primary3(p):
    """primary : NUMBER"""
    p[0] = p[1]


def p_error(t):
    print("syntax error at '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()

with open('test_input1.txt') as input_file:
    data = input_file.read()
    parser.parse(data)
