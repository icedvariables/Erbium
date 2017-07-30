import ply.yacc as yacc
import alltokens

class Parser:
    def __init__(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        self.scopes = {"global":{}}
        self.ast = ()

    tokens = alltokens.tokensKeywords

    # CHUNK

    def p_chunk(self, p):
        "chunk : statement chunk"
        p[0] = (p[1],) + p[2]

    def p_chunk_statement(self, p):
        "chunk : statement"
        p[0] = (p[1],)

    # BLOCK

    def p_block(self, p):
        "block : LCURLY chunk RCURLY"
        p[0] = ("block", p[2])

    # STATEMENT

    def p_stat_if(self, p):
        "statement : IF expression block ELSE block"
        condition = p[2]
        block = p[3]
        elseBlock = p[5]
        p[0] = ("if", condition, block, elseBlock)

    def p_stat_assign_with_type(self, p):
        "statement : typename EQUALS expression"
        name = p[1]
        value = p[3]
        p[0] = ("assign", name, value)

    # EXPRESSION

    def p_expr_num(self, p):
        "expression : NUM"
        p[0] = ("number", p[1])

    def p_expr_decimalnum(self, p):
        "expression : DECIMALNUM"
        p[0] = ("decimal-number", p[1])

    # TYPENAME

    def p_typename(self, p):
        "typename : type ID"
        dataType = p[1]
        name = p[2]
        p[0] = ("typename", dataType, name)

    # TYPENAMELIST

    def p_typenamelist_typename(self, p):
        "typenamelist : typename"
        p[0] = (p[1],)

    def p_typenamelist(self, p):
        "typenamelist : typename COMMA typenamelist"
        p[0] = (p[1],) + p[3]

    # TYPE

    def p_type_function(self, p):
        "type :  onetype ARROW onetype"
        p[0] = ("type-function", p[1], p[3])

    def p_type(self, p):
        "type : onetype"
        p[0] = ("type", p[1])

    # ONETYPE

    def p_onetype_array(self, p):
        "onetype : ID LSQUARE NUM RSQUARE"
        p[0] = ("onetype-array", p[1], p[3])

    def p_onetype(self, p):
        "onetype : ID"
        p[0] = ("onetype", p[1])

    def p_error(self, p):
        print "SYNTAX ERROR: invalid syntax: " + str(p)

    def parse(self, code):
        self.ast = self.parser.parse(code)
        return self.ast
