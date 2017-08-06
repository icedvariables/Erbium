keywords = {
    "if": "IF",
	"else": "ELSE",
	"mutable": "MUTABLE",
    "public": "PUBLIC",
    "true": "TRUE",
    "false": "FALSE",
    "null": "NULL"
}

tokens = [
    "ID",

    "NUM",
    "DECIMALNUM",
    "CHARACTER",
    "STRING",

    "EQUALS",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "ARROW",
    "LEFTARROW",
    "COMMA",
    "GREATERTHAN",
    "LESSTHAN",
    "GREATERTHANOREQUAL",
    "LESSTHANOREQUAL",
    "EQUALTO",

    "LBRACKET",
    "RBRACKET",
    "LCURLY",
    "RCURLY",
    "LSQUARE",
    "RSQUARE"
]

tokensKeywords = tokens + list(keywords.values())
