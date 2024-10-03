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
    OPERATORS = {'+', '-', '*', '/', '=', '<=', '>=', '==', '!=', '<', '>'}
    SEPARATORS = {'(', ')', ';'}

    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = 0
        self.length = len(source_code)

    def tokenize(self):
        tokens = []
        while self.pos < self.length:
            current_char = self.source_code[self.pos]

            if current_char.isspace():
                self.pos += 1
                continue
            elif current_char.isalpha() or current_char == '_':
                tokens.append(self.fsm_identifier())
            elif current_char.isdigit():
                tokens.append(self.fsm_integer_or_real())
            elif self.is_operator(current_char):
                tokens.append(self.fsm_operator())
            elif self.is_separator(current_char):
                tokens.append(Token(TokenType.SEPARATOR, current_char))
                self.pos += 1
            else:
                tokens.append(Token(TokenType.UNKNOWN, current_char))
                self.pos += 1

        tokens.append(Token(TokenType.EOF, "EOF"))
        return tokens

    # FSM for Identifiers
    def fsm_identifier(self):
        lexeme = ''
        while self.pos < self.length and (self.source_code[self.pos].isalnum() or self.source_code[self.pos] == '_'):
            lexeme += self.source_code[self.pos]
            self.pos += 1
        
        if lexeme in Lexer.KEYWORDS:
            return Token(TokenType.KEYWORD, lexeme)
        return Token(TokenType.IDENTIFIER, lexeme)

    # FSM for Integers and Reals
    def fsm_integer_or_real(self):
        lexeme = ''
        is_real = False

        # Handle digits before potential decimal point
        while self.pos < self.length and self.source_code[self.pos].isdigit():
            lexeme += self.source_code[self.pos]
            self.pos += 1

        # Check if it's a real number
        if self.pos < self.length and self.source_code[self.pos] == '.':
            is_real = True
            lexeme += '.'
            self.pos += 1
            # Handle digits after the decimal point
            while self.pos < self.length and self.source_code[self.pos].isdigit():
                lexeme += self.source_code[self.pos]
                self.pos += 1

        if is_real:
            return Token(TokenType.REAL, lexeme)
        else:
            return Token(TokenType.INTEGER, lexeme)

    # FSM for Operators
    def fsm_operator(self):
        lexeme = self.source_code[self.pos]
        self.pos += 1
        if self.pos < self.length and self.source_code[self.pos] == '=':
            lexeme += '='
            self.pos += 1

        if lexeme in Lexer.OPERATORS:
            return Token(TokenType.OPERATOR, lexeme)
        return Token(TokenType.UNKNOWN, lexeme)

    # Check if character is an operator
    def is_operator(self, ch):
        return ch in {'+', '-', '*', '/', '=', '>', '<', '!', '&', '|'}

    # Check if character is a separator
    def is_separator(self, ch):
        return ch in Lexer.SEPARATORS


# Main program to test the lexer
def main():
    # Source code to tokenize (can read from a file as well)
    source_code = """
    while (fahr <= upper) a = 23.00;
    """

    # Initialize lexer
    lexer = Lexer(source_code)

    # Tokenize the source code
    tokens = lexer.tokenize()

    # Print tokens and lexemes
    print("Token\tLexeme")
    for token in tokens:
        print(f"{token.type}\t{token.lexeme}")

if __name__ == "__main__":
    main()