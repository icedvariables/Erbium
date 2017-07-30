import erblexer
import erbparser
import pprint

code = """

/* Assign x to a function that takes a 32-bit signed integer called y and returns a 32-bit signed integer equal to y + 1. */

x = (int32 y) -> int32 {
    z = 5
}

"""

erblexer.Lexer().build()
p = erbparser.Parser(debug=True)
result = p.parse("float x = 5.5")
pprint.pprint(result)
