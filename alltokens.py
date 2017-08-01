keywords = {
    "if": "IF",
	"else": "ELSE",
	"mutable": "MUTABLE",
    "public": "PUBLIC",
    "true": "TRUE",
    "false": "FALSE",
    "null": "NULL",
    "ret": "RETURN"
}

tokens = [
    "ID",

    "NUM",
    "DECIMALNUM",
    "CHARACTER",

    "EQUALS",
    "PLUS",
    "MINUS",
    "STAR",
    "SLASH",
    "ARROW",
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
