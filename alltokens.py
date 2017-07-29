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

    "REAL",
    "NUMBER",

    "EQUALS",
    "PLUS",
    "MINUS",
    "STAR",
    "SLASH",
    "ARROW",

    "LBRACKET",
    "RBRACKET",
    "LCURLY",
    "RCURLY"
]

tokensKeywords = tokens + list(keywords.values())