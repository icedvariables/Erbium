from erbparser import Parser
from executeast import ExecuteAst
import pprint

code = """

/* Recursive fibonacci sequence generator! */

fib = (n) -> {
    if n < 2
        <- n
    <- fib(n - 2) + fib(n - 1)
}

"""

p = Parser(debug=True)
ast = p.parse(code)
pprint.pprint(ast)
