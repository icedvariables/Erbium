import ply.yacc as yacc

from lexer import Lexer

class Parser:
    tokens = Lexer.tokens

    def __init__(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_error(self, p):
        print("PARSING ERROR: invalid syntax.")
