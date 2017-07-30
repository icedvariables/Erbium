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

    "EQUALS",
    "PLUS",
    "MINUS",
    "STAR",
    "SLASH",
    "ARROW",
    "COMMA",

    "LBRACKET",
    "RBRACKET",
    "LCURLY",
    "RCURLY",
    "LSQUARE",
    "RSQUARE"
]

tokensKeywords = tokens + list(keywords.values())
