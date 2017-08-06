import erbparser
import pprint

code = """

/* Recursive fibonacci sequence generator! */

(n) -> {
    if n < 2
        <- n
    else
        <- fib(n - 2) + fib(n - 1)
}(10) /* Call the anonymous function immediately after defining it. */

"""

p = erbparser.Parser(debug=True)
result = p.parse(code)
pprint.pprint(result)
