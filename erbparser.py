import ply.yacc as yacc
import alltokens
import sys

class Parser:
    tokens = alltokens.tokensKeywords
    
    # Multiplication and division have higher precedence than addition and subtraction:
    # 5 + 10 * 8 would become 5 + (10 * 8) and not (5 + 10) * 8
    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE")
    )
    
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
    
    def p_block_empty(self, p):
        "block : LCURLY RCURLY"
        p[0] = ("block", ())

    # STATEMENT

    def p_stat_ifelse(self, p):
        "statement : IF expression block ELSE block"
        condition = p[2]
        block = p[3]
        elseBlock = p[5]
        p[0] = ("ifelse", condition, block, elseBlock)
    
    def p_stat_if(self, p):
        "statement : IF expression block"
        condition = p[2]
        block = p[3]
        p[0] = ("if", condition, block)
    
    def p_stat_assign(self, p):
        "statement : ID EQUALS expression"
        typeid = ("unknown-type", p[1])
        value = p[3]
        p[0] = ("assign", typeid, value)

    def p_stat_assign_with_type(self, p): # TODO: Check if value is valid based on the type given.
        "statement : typeid EQUALS expression"
        typeid = p[1]
        value = p[3]
        p[0] = ("assign", typeid, value)

    def p_stat_functioncall(self, p):
        "statement : functioncall"
        p[0] = p[1]
        
    def p_stat_return(self, p):
        "statement : RETURN expression"
        p[0] = ("return", p[2])

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
    
    def p_expr_array(self, p):
        "expression : LSQUARE expressionlist RSQUARE"
        p[0] = ("array", p[2])
    
    def p_expr_array_empty(self, p):
        "expression : LSQUARE RSQUARE"
        p[0] = ("array", ())
    
    def p_expr_arrayaccess(self, p):
        "expression : ID LSQUARE NUM RSQUARE"
        p[0] = ("arrayaccess", p[1], p[3])
    
    def p_expr_string(self, p):
        "expression : STRING"
        p[0] = ("array", tuple(p[1]))
    
    def p_expr_greaterthan(self, p):
        "expression : expression GREATERTHAN expression"
        p[0] = ("greaterthan", p[1], p[3])
    
    def p_expr_lessthan(self, p):
        "expression : expression LESSTHAN expression"
        p[0] = ("lessthan", p[1], p[3])
    
    def p_expr_greaterthanorequal(self, p):
        "expression : expression GREATERTHANOREQUAL expression"
        p[0] = ("greaterthanorequal", p[1], p[3])
    
    def p_expr_lessthanorequal(self, p):
        "expression : expression LESSTHANOREQUAL expression"
        p[0] = ("lessthanorequal", p[1], p[3])
    
    def p_expr_equalto(self, p):
        "expression : expression EQUALTO expression"
        p[0] = ("equalto", p[1], p[3])
    
    def p_expr_add(self, p):
        "expression : expression PLUS expression"
        p[0] = ("add", p[1], p[3])
    
    def p_expr_subtract(self, p):
        "expression : expression MINUS expression"
        p[0] = ("subtract", p[1], p[3])
    
    def p_expr_multiply(self, p):
        "expression : expression TIMES expression"
        p[0] = ("multiply", p[1], p[3])
    
    def p_expr_divide(self, p):
        "expression : expression DIVIDE expression"
        p[0] = ("divide", p[1], p[3])

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
                | arraytype
                | functiontype"""
        p[0] = p[1]

    def p_functiontype(self, p):
        "functiontype : type ARROW type"
        arg = p[1]
        ret = p[3]

        p[0] = ("functiontype", arg, ret)

    def p_singletype_id(self, p):
        "singletype : ID"
        dataType = p[1]

        print "Data type " + dataType + " " + ("exists." if self.isExistingType(dataType) else "does not exist!")

        p[0] = ("singletype", dataType)
    
    def p_arraytype(self, p):
        "arraytype : ID LSQUARE RSQUARE"
        dataType = p[1]

        print "Data type " + dataType + "[] " + ("exists." if self.isExistingType(dataType) else "does not exist!")

        p[0] = ("arraytype", dataType)
    
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
        if(p):
            print "SYNTAX ERROR:" + str(p.lineno) + ":" + str(p.lexpos) + ": Invalid syntax: " + str(p.value)
        else:
            print "SYNTAX ERROR: Unexpected end of input."
        sys.exit()

    def parse(self, code):
        self.ast = self.parser.parse(code)
        return self.ast

    def isExistingType(self, dataType):
        return dataType in self.types.keys()
