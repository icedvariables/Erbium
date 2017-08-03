import ply.lex as lex
import alltokens
import sys

class Lexer:
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    tokens = alltokens.tokensKeywords

    t_EQUALS            = r"="
    t_PLUS              = r"\+"
    t_MINUS             = r"-"
    t_TIMES             = r"\*"
    t_DIVIDE            = r"/"
    t_ARROW             = r"->"
    t_COMMA             = r","
    t_GREATERTHAN       =r">"
    t_LESSTHAN          = r"<"
    t_GREATERTHANOREQUAL= r">="
    t_LESSTHANOREQUAL   = r"<="
    t_EQUALTO           = r"=="

    t_LBRACKET  = r"\("
    t_RBRACKET  = r"\)"
    t_LCURLY    = r"\{"
    t_RCURLY    = r"\}"
    t_LSQUARE   = r"\["
    t_RSQUARE   = r"\]"

    t_ignore = " \t"
    t_ignore_COMMENT = r"\/\*.*\*\/" # Discard anthing between /* and */

    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"

        # Check if this is actually a keyword instead of an id
        t.type = alltokens.keywords.get(t.value, "ID")

        return t

    def t_DECIMALNUM(self, t): # Match a decimal value
        r"\d+\.\d*"
        t.value = float(t.value)
        return t

    def t_NUM(self, t): # Match an integer value
        r"\d+"
        t.value = int(t.value)
        return t

    def t_CHARACTER(self, t): # Match a single character between single quotes
        r"'[^']?'"
        t.value = t.value[1:-1] # Remove the two quotes around the character
        return t

    def t_STRING(self, t): # Match a string of characters between double quotes
        r'"[^"]*"'
        t.value = t.value[1:-1] # Remove the two quotes around the string
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value) # Count line numbers

    def t_error(self, t):
        print "LEXICAL ERROR:" + str(t.lineno) + ":" + str(t.lexpos) + ": Unexpected character: " + t.value[0]
        sys.exit()

    def input(self, data):
        self.lexer.input(data)

        # Generate an array of tokens
        tokens = []
        while(True):
            t = self.lexer.token()
            if not(t):
                break
            tokens.append(t)

        return tokens
