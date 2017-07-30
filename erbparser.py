import ply.yacc as yacc
import alltokens

class Parser:
    tokens = alltokens.tokensKeywords
    BUILTIN_TYPES = {
        "int32": ("number"),
        "int16": ("number"),
        "float": ("number", "decimal-number")
    }

    def __init__(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        self.types = Parser.BUILTIN_TYPES
        self.ast = ()

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

    def p_stat_assign_with_type(self, p): # TODO: Check if value is valid based on the type given.
        "statement : typename EQUALS expression"
        typeName = p[1]
        value = p[3]
        p[0] = ("assign", typeName, value)

    # EXPRESSION

    def p_expr_value(self, p):
        "expression : value"
        p[0] = ("value", p[1])

    # VALUE

    def p_value_num(self, p):
        "value : NUM"
        p[0] = ("number", p[1])

    def p_value_decimalnum(self, p):
        "value : DECIMALNUM"
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
        dataType = p[1]
        amount = p[3]

        print "Data type " + dataType + "[" + str(amount) + "] is " + ("valid" if self.isExistingType(dataType) else "invalid")

        p[0] = ("onetype-array", dataType, amount)

    def p_onetype(self, p):
        "onetype : ID"
        dataType = p[1]

        print "Data type " + dataType + " is " + ("valid" if self.isExistingType(dataType) else "invalid")

        p[0] = ("onetype", dataType)

    def p_error(self, p):
        print "SYNTAX ERROR: invalid syntax: " + str(p)

    def parse(self, code):
        self.ast = self.parser.parse(code)
        return self.ast

    def isExistingType(self, dataType):
        return dataType in self.types.keys()
