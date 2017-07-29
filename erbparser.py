import ply.yacc as yacc
import alltokens

class Parser:
    def __init__(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        self.scopes = {"global":{}}
        self.ast = ()
    
    tokens = alltokens.tokensKeywords
    
    # PROGRAM
    
    def p_program(self, p):
        "program : chunk"
        p[0] = p[1]
    
    # BLOCK
    
    def p_block(self, p):
        "block : LCURLY chunk RCURLY"
        p[0] = ("block", p[2])
    
    # CHUNK
    
    def p_chunk(self, p):
        "chunk : statement chunk"
        p[0] = (p[1],) + p[2]
    
    def p_chunk_statement(self, p):
        "chunk : statement"
        p[0] = (p[1],)
    
    # STATEMENT
    
    def p_stat_if(self, p):
        "statement : IF expression block ELSE block"
        condition = p[2]
        block = p[3]
        elseBlock = p[5]
        p[0] = ("if", condition, block, elseBlock)
    
    def p_stat_assign(self, p):
        "statement : ID EQUALS expression"
        p[0] = ("assign", p[1], p[3])
    
    # EXPRESSION
    
    def p_expr_num(self, p):
        "expression : NUM"
        p[0] = ("number", p[1])
    
    def p_expr_decimalnum(self, p):
        "expression : DECIMALNUM"
        p[0] = ("decimal-number", p[1])

    def p_error(self, p):
        print "SYNTAX ERROR: invalid syntax: " + str(p)
    
    def parse(self, code):
        self.ast = self.parser.parse(code)
        return self.ast