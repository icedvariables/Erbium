import erblexer
import erbparser
import pprint

code = """

/* Assign x to a function that takes a 32-bit signed integer called y and returns a 32-bit signed integer equal to y + 1. */

int32->int32 a = (x){
    int32 y = 10
}

"""

erblexer.Lexer().build()
p = erbparser.Parser(debug=True)
result = p.parse(code)
pprint.pprint(result)
