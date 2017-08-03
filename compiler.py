import erblexer
import erbparser
import pprint

code = """

/* Recursive fibonacci sequence generator! */

fib = (int n) -> int {
    if n < 2 {
        ret n
    }
    ret fib(n - 2) + fib(n - 1)
}

fib(10) /* should return 55 */

"""

erblexer.Lexer().build()
p = erbparser.Parser(debug=True)
result = p.parse('a = "abcdef"')
pprint.pprint(result)
