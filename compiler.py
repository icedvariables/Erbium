from lexer import Lexer
from parser import Parser

code = """

/* Assign x to a function that takes a 32-bit signed integer called y and returns a 32-bit signed integer equal to y + 1. */

x = (int32 y) -> int32 {
    y + 1
}

mut a = 5
a = a + 10

"""

l = Lexer()
p = Parser()
tokens = l.input(code)
for token in tokens:
    print token
