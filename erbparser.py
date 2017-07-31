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
        "statement : type ID EQUALS expression"
        dataType = p[1]
        name = p[2]
        value = p[4]
        p[0] = ("assign", dataType, name, value)

    def p_stat_assign_function(self, p): # TODO: Add functions with multiple arguments.
        "statement : functiontype ID EQUALS LBRACKET ID RBRACKET block"
        dataType = p[1]
        name = p[2]
        arg = p[5]
        block = p[7]
        p[0] = ("assign-function", dataType, name, arg, block)

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

    # TYPE

    def p_functiontype(self, p):
        "functiontype : type ARROW type"
        arg = p[1]
        ret = p[3]

        p[0] = ("functiontype", arg, ret)

    def p_type_array(self, p):
        "type : ID LSQUARE NUM RSQUARE"
        dataType = p[1]
        amount = p[3]

        print "Data type " + dataType + "[" + str(amount) + "] " + ("exists." if self.isExistingType(dataType) else "does not exist!")

        p[0] = ("type-array", dataType, amount)

    def p_one_id(self, p):
        "type : ID"
        dataType = p[1]

        print "Data type " + dataType + " " + ("exists." if self.isExistingType(dataType) else "does not exist!")

        p[0] = ("type", dataType)

    def p_error(self, p):
        print "SYNTAX ERROR: invalid syntax: " + str(p)

    def parse(self, code):
        self.ast = self.parser.parse(code)
        return self.ast

    def isExistingType(self, dataType):
        return dataType in self.types.keys()
