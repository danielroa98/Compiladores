from sly import Lexer
import sys

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {FLOAT, INTEGER, ID, BOOLEAN, ARR, WHILE, IF, ELSE, PRINT,
              PLUS, MINUS, TIMES, DIVIDE, ASSIGN, MOD,
              EQ, LT, LE, GT, GE, NE, FOR,
              START, FINISH, INT_TYPE, CHAR_TYPE, FLOAT_TYPE, BOOL_TYPE, STRUCT}

    literals = {'{', '}', '[', ']', ',', ';'}

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

    # Identifiers and keywords
    BOOLEAN = r'green|red'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
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
    ID['pokemon'] = STRUCT

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
