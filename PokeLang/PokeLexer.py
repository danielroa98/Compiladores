
'''
Antonio Junco de Haas - A01339695
Luis Daniel Roa González - A01021960
Sergio Hernández Castillo - A01025210
Sebastián Gonzalo Vives Faus - A01025211

'''

from sly import Lexer
import sys

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {FLOAT, INTEGER, ID, BOOL, ARR, WHILE, IF, ELSE, PRINT,
              PLUS, MINUS, TIMES, DIVIDE, ASSIGN, MOD, VOID,
              EQ, LT, LE, GT, GE, NE, FOR, CHAR,
              PRINT_IN_LINE, PRINT_IN_NEW_LINE, FUNC,
              START, FINISH, INT_TYPE, CHAR_TYPE, FLOAT_TYPE, BOOL_TYPE, STRUCT}

    literals = {'{', '}', '[', ']', ',', ';', '(', ')'}

    # String containing ignored characters
    ignore = ' \t'

    @_(r"[-+]?\d+\.\d*")
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    # Regular expression rules for tokens
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    EQ = r'=='
    ASSIGN = r'='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='

    @_(r"[-+]?\d+")
    def INTEGER(self, t):
        t.value = int(t.value)
        return t

    @_(r'green|red')
    def BOOL(self, t):
        if t.value == 'green':
            t.value = True
            return t
        elif t.value == 'red':
            t.value = False
            return t

    # Identifiers and keywords
    #BOOLEAN = r'green|red'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    CHAR = r'"[a-zA-Z]"'
    ID['if_i_choose_you'] = IF
    ID['else'] = ELSE
    ID['whilepokemon'] = WHILE
    ID['forpokemon'] = FOR
    ID['print'] = PRINT
    ID['battle_start'] = START
    ID['battle_end'] = FINISH
    ID['pikachu'] = INT_TYPE
    ID['squirtle'] = FLOAT_TYPE
    ID['bulbasaur'] = BOOL_TYPE
    ID['charmander'] = CHAR_TYPE
    ID['pokebelt'] = ARR
    ID['move'] = FUNC
    ID['pokemon'] = STRUCT
    ID['pokehabla'] = PRINT_IN_LINE
    ID['pokehabla_nl'] = PRINT_IN_NEW_LINE
    ID['shadow'] = VOID

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Error Léxico: En la línea %d: Con el caracter %r' %
              (self.lineno, t.value[0]))
        sys.exit(2)
        self.index += 1


def lexerStart(fileContents):
    data = fileContents
    lexer = CalcLexer()
    return lexer.tokenize(data)
