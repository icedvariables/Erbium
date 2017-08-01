import erblexer
import erbparser
import pprint

code = """

/* Assign x to a function that takes a 32-bit signed integer called y and returns a 32-bit signed integer equal to y + 1. */

a = (int x, int y) -> char {
    char z = '@'
}

char b = foo(5, 10.5, f, 'g')

"""

erblexer.Lexer().build()
p = erbparser.Parser(debug=True)
result = p.parse(code)
pprint.pprint(result)
