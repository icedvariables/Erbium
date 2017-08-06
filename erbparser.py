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

    def __init__(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
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
        name = p[1]
        value = p[3]
        p[0] = ("assign", name, value)

    def p_stat_functioncall(self, p):
        "statement : functioncall"
        p[0] = p[1]

    def p_stat_return(self, p):
        "statement : LEFTARROW expression"
        p[0] = ("return", p[2])

    # EXPRESSION

    def p_expr_num(self, p):
        "expression : NUM"
        p[0] = ("int", p[1])

    def p_expr_decimalnum(self, p):
        "expression : DECIMALNUM"
        p[0] = ("float", p[1])

    def p_expr_character(self, p):
        "expression : CHARACTER"
        p[0] = ("char", p[1])

    def p_expr_id(self, p):
        "expression : ID"
        p[0] = ("id", p[1])

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
        "expression : expression LSQUARE NUM RSQUARE"
        p[0] = ("arrayaccess", p[1], p[3])

    def p_expr_string(self, p):
        "expression : STRING"
        p[0] = ("array", tuple(p[1]))

    def p_expr_binop(self, p):
        """expression : expression GREATERTHAN expression
                      | expression LESSTHAN expression
                      | expression GREATERTHANOREQUAL expression
                      | expression LESSTHANOREQUAL expression
                      | expression EQUALTO expression
                      | expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression"""

        left = p[1]
        operation = p[2]
        right = p[3]
        p[0] = ("binop", operation, left, right)

    # EXPRESSIONLIST

    def p_exprlist(self, p):
        "expressionlist : expression COMMA expressionlist"
        p[0] = (p[1],) + p[3]

    def p_exprlist_expr(self, p):
        "expressionlist : expression"
        p[0] = (p[1],)

    # FUNCTIONCALL

    def p_functioncall(self, p):
        "functioncall : expression LBRACKET expressionlist RBRACKET"
        name = p[1]
        args = p[3]
        p[0] = ("functioncall", name, args)

    def p_functioncall_no_args(self, p):
        "functioncall : expression LBRACKET RBRACKET"
        name = p[1]
        p[0] = ("functioncall", name, ())

    # FUNCTIONDEFINE

    def p_functiondef(self, p):
        "functiondefine : LBRACKET idlist RBRACKET ARROW block"
        args = p[2]
        block = p[5]
        p[0] = ("functiondefine", args, block)

    def p_functiondef_no_args(self, p):
        "functiondefine : LBRACKET RBRACKET ARROW block"
        args = ()
        block = p[4]
        p[0] = ("functiondefine", args, block)

    # IDLIST

    def p_idlist(self, p):
        "idlist : ID COMMA idlist"
        p[0] = (p[1],) + p[3]

    def p_idlist_id(self, p):
        "idlist : ID"
        p[0] = (p[1])



    def p_error(self, p):
        if(p):
            print "SYNTAX ERROR:" + str(p.lineno) + ":" + str(p.lexpos) + ": Invalid syntax: " + str(p.value)
        else:
            print "SYNTAX ERROR: Unexpected end of input."
        sys.exit()

    def parse(self, code):
        self.ast = self.parser.parse(code)
        return self.ast
