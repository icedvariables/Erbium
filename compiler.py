from erbparser import Parser
from executeast import ExecuteAst
import pprint

code = """

/* Recursive fibonacci sequence generator! */

(n) -> {
    if n < 2
        <- n
    <- fib(n - 2) + fib(n - 1)
}(10) /* Call the anonymous function immediately after defining it. */

"""

p = Parser(debug=True)
ast = p.parse("a = 5")
pprint.pprint(ast)
executer = ExecuteAst(ast)
print executer.execute()
