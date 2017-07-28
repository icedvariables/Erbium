import ply.yacc as yacc
import alltokens

class Parser:
    tokens = alltokens.tokensKeywords

    def __init__(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_error(self, p):
        print("PARSING ERROR: invalid syntax.")