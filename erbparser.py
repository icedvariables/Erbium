import ply.yacc as yacc
import alltokens

class Parser:
    tokens = alltokens.tokensKeywords
    BUILTIN_TYPES = {
        "int": ("number"),
        "long": ("number"),
        "float": ("number", "decimal-number"),
        "char": ("character")
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
    
    def p_stat_assign(self, p):
        "statement : ID EQUALS expression"
        dataType = "unknown-type" # TODO: Infer data type.
        name = p[1]
        value = p[3]
        p[0] = ("assign", dataType, name, value)

    def p_stat_assign_with_type(self, p): # TODO: Check if value is valid based on the type given.
        "statement : type ID EQUALS expression"
        dataType = p[1]
        name = p[2]
        value = p[4]
        p[0] = ("assign", dataType, name, value)

    def p_stat_functioncall(self, p):
        "statement : functioncall"
        p[0] = p[1]

    # EXPRESSION

    def p_expr_num(self, p):
        "expression : NUM"
        p[0] = ("number", p[1])

    def p_expr_decimalnum(self, p):
        "expression : DECIMALNUM"
        p[0] = ("decimal-number", p[1])

    def p_expr_id(self, p):
        "expression : ID"
        p[0] = ("id", p[1])
    
    def p_expr_character(self, p):
        "expression : CHARACTER"
        p[0] = ("character", p[1])
    
    def p_expr_functioncall(self, p):
        "expression : functioncall"
        p[0] = p[1]
    
    def p_expr_functiondef(self, p):
        "expression : functiondefine"
        p[0] = p[1]

    # EXPRESSIONLIST

    def p_exprlist(self, p):
        "expressionlist : expression COMMA expressionlist"
        p[0] = (p[1],) + p[3]

    def p_exprlist_expr(self, p):
        "expressionlist : expression"
        p[0] = (p[1],)

    # FUNCTIONCALL

    def p_functioncall(self, p):
        "functioncall : ID LBRACKET expressionlist RBRACKET"
        name = p[1]
        args = p[3]
        p[0] = ("functioncall", name, args)

    def p_functioncall_no_args(self, p):
        "functioncall : ID LBRACKET RBRACKET"
        name = p[1]
        p[0] = ("functioncall", name, ())
    
    # FUNCTIONDEFINE
    
    def p_functiondef(self, p):
        "functiondefine : LBRACKET typeidlist RBRACKET ARROW type block"
        args = p[2]
        ret = p[5]
        block = p[6]
        p[0] = ("functiondefine", args, ret, block)
    
    def p_functiondef_no_args(self, p):
        "functiondefine : LBRACKET RBRACKET ARROW type block"
        args = ()
        ret = p[4]
        block = p[5]
        p[0] = ("functiondefine", args, ret, block)

    # TYPE
    
    def p_type(self, p):
        """type : singletype
                | functiontype"""
        p[0] = p[1]

    def p_functiontype(self, p):
        "functiontype : singletype ARROW singletype"
        arg = p[1]
        ret = p[3]

        p[0] = ("functiontype", arg, ret)

    def p_singletype_array(self, p):
        "singletype : ID LSQUARE NUM RSQUARE"
        dataType = p[1]
        amount = p[3]

        print "Data type " + dataType + "[" + str(amount) + "] " + ("exists." if self.isExistingType(dataType) else "does not exist!")

        p[0] = ("singletype-array", dataType, amount)

    def p_singletype_id(self, p):
        "singletype : ID"
        dataType = p[1]

        print "Data type " + dataType + " " + ("exists." if self.isExistingType(dataType) else "does not exist!")

        p[0] = ("singletype", dataType)
    
    # TYPEID
    
    def p_typeid(self, p):
        "typeid : type ID"
        dataType = p[1]
        name = p[2]
        p[0] = ("typeid", dataType, name)
    
    def p_typeidlist(self, p):
        "typeidlist : typeid COMMA typeidlist"
        p[0] = (p[1],) + p[3]
    
    def p_typeidlist_typeid(self, p):
        "typeidlist : typeid"
        p[0] = (p[1],)



    def p_error(self, p):
        print "SYNTAX ERROR: invalid syntax: " + str(p)

    def parse(self, code):
        self.ast = self.parser.parse(code)
        return self.ast

    def isExistingType(self, dataType):
        return dataType in self.types.keys()
