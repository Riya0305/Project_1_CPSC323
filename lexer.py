# regular expression lib -> re
import re

class TokenType:
    KEYWORD = "kEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    REAL = "REAL"
    OPERATOR = "OPERATOR"
    SEPERATOR = "SEPERATOR"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"

class Token:
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

    def __str__(self) -> str:
        return f"Token({self.type}, {self.lexeme})"

class Lexer:
    KEYWORDS = {'while'}
    OPERATORS = {'+', '-', '*', ''}