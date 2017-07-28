keywords = {
    "if": "IF",
	"else": "ELSE",
	"mut": "MUTABLE"
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