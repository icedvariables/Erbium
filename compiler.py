import erblexer
import erbparser
import pprint

code = """

/* Assign x to a function that takes a 32-bit signed integer called y and returns a 32-bit signed integer equal to y + 1. */

x = (int32 y) -> int32 {
    z = x + 5
}

"""

code1 = """
if 5 {
    a = 5
} else {
    z = 10
}
"""

erblexer.Lexer().build()
p = erbparser.Parser()
result = p.parse(code1)
pprint.pprint(result)