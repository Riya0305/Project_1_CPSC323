import re
import os

# Token types for RAT24 language 
class TokenType:
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    REAL = "REAL"
    OPERATOR = "OPERATOR"
    SEPARATOR = "SEPARATOR"
    COMMENT = "COMMENT"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"

# Class to represent token and lexeme
class Token:
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

    def __str__(self) -> str:
        return f"Token({self.type}, {self.lexeme})"

# Lexer class that handles the tokenization of the RAT24 source code. 
class Lexer:
    KEYWORDS = {'while', 'if', 'else', 'for', 'return', 'get', 'put', 'function', 'integer'}
    OPERATORS = {'+', '-', '*', '/', '=', '<=', '>=', '==', '!=', '<', '>'}
    SEPARATORS = {'(', ')', ';', '{', '}', '"', ',', '@'}

    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = 0
        self.length = len(source_code)

    # This function runs until the source code is over and it tokenizes the entire source code
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

        while self.pos < self.length and self.source_code[self.pos].isdigit():
            lexeme += self.source_code[self.pos]
            self.pos += 1

        if self.pos < self.length and self.source_code[self.pos] == '.':
            is_real = True
            lexeme += '.'
            self.pos += 1
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
        return ch in {'+', '-', '*', '/', '=', '<', '>', '!', '&', '|'}

    # Check if character is a separator
    def is_separator(self, ch):
        return ch in Lexer.SEPARATORS

def test_case():
    test_files = ["test_case1.txt", "test_case2.txt", "test_case3.txt"]

    for test_file in test_files:
        print(f"Processing {test_file}...")
        
        # Check if the test file exists before trying to read it
        if not os.path.isfile(test_file):
            print(f"File {test_file} does not exist.")
            continue

        with open(test_file, "r") as file:
            source_code = file.read()
        
        # Initialize lexer with the current source code
        lexer = Lexer(source_code)
        # Tokenize the source code
        tokens = lexer.tokenize()

        # Define output file name
        output_file_name = f"output_{test_file.split('.')[0]}.txt"
        try:
            with open(output_file_name, "w") as output_file:
                output_file.write(f"Processing {test_file}\n")
                output_file.write(f"{'Token':<15} {'Lexeme':<20}\n")
                output_file.write("-" * 35 + "\n")

                for token in tokens:
                    output_file.write(f"{token.type:<15} {token.lexeme:<20}\n")

                output_file.write("\n" + "=" * 35 + "\n")

            print(f"Output written to {output_file_name}")

        except IOError as e:
            print(f"Error writing to {output_file_name}: {e}")

if __name__ == "__main__":
    test_case()









































# #importing regular expression library
# import re

# #token types for RAT24 language 
# class TokenType:
#     KEYWORD = "KEYWORD"
#     IDENTIFIER = "IDENTIFIER"
#     INTEGER = "INTEGER"
#     REAL = "REAL"
#     OPERATOR = "OPERATOR"
#     SEPARATOR = "SEPARATOR"
#     COMMENT = "COMMENT"
#     #end of file
#     EOF = "EOF" 
#     #adding to take away errors
#     UNKNOWN = "UNKNOWN"

# #used to represent token and lexeme
# class Token:
#     def __init__(self, type, lexeme):
#         self.type = type
#         self.lexeme = lexeme

#     def __str__(self) -> str:
#         return f"Token({self.type}, {self.lexeme})"

# #lexer class that handles the tokenization of the RAT24 source code. 
# class Lexer:
#     # Sets of keywords, operators, and separators for Rat24F
#     KEYWORDS = {'while', 'if', 'else', 'for', 'return', 'get', 'put'}
#     OPERATORS = {'+', '-', '*', '/', '=', '<=', '>=', '==', '!=', '<', '>'}
#     SEPARATORS = {'(', ')', ';', '{', '}', '"', ',', '@'}
#     COMMENT_START = {'[*'}
#     COMMENT_END = {'*]'}

#     def __init__(self, source_code):
#         self.source_code = source_code
#         self.pos = 0
#         self.length = len(source_code)

#     #this function runs till the source code is over and it tokenizes the entire source code
#     def tokenize(self):
#         #initilaizing tokens as an empty array
#         tokens = []
#         #loop that runs till we reach till the end of the source code
#         while self.pos < self.length:
#             current_char = self.source_code[self.pos]
#             if current_char.isspace():
#                 self.pos += 1
#                 continue
#             elif current_char.isalpha() or current_char == '_':
#                 tokens.append(self.fsm_identifier())
#             elif current_char.isdigit():
#                 tokens.append(self.fsm_integer_or_real())
#             elif self.is_operator(current_char):
#                 tokens.append(self.fsm_operator())
#             elif self.is_separator(current_char):
#                 tokens.append(Token(TokenType.SEPARATOR, current_char))
#                 self.pos += 1
#             else:
#                 tokens.append(Token(TokenType.UNKNOWN, current_char))
#                 self.pos += 1

#         tokens.append(Token(TokenType.EOF, "EOF"))
#         return tokens
    
#     #checking if the position marks the beginning or end of the source code
#     def is_comment_start(self):
#         return self.source_code[self.pos:self.pos+2] == self.COMMENT_START
    
#     def is_comment_end(self):
#         return self.source_code[self.pos:self.pos+2] == self.COMMENT_END
    
#     #holding the content of the comment
#     def fsm_comments(self):
#         lexeme = ''
    
#         while self.pos < self.length and not self.is_comment_end():
#             lexeme += self.source_code[self.pos]
#             self.pos += 1

#         if self.is_comment_end():
#             lexeme += self.source_code[self.pos:self.pos+2]
#             self.pos += 1

#         return Token(TokenType.COMMENT, lexeme)
    
#     # FSM for Identifiers (Regex: [a-zA-Z_][a-zA-Z0-9_]*)
#     def fsm_identifier(self):
#         lexeme = ''
#         while self.pos < self.length and (self.source_code[self.pos].isalnum() or self.source_code[self.pos] == '_'):
#             lexeme += self.source_code[self.pos]
#             self.pos += 1
        
#         if lexeme in Lexer.KEYWORDS:
#             return Token(TokenType.KEYWORD, lexeme)
        
#         if lexeme[0].isalpha() and lexeme[-1].isalpha():
#             return Token(TokenType.IDENTIFIER, lexeme)
#         else:
#             return Token(TokenType.UNKNOWN, lexeme)

#     # FSM for Integers and Reals (Integer Regex: [0-9]+, Real Regex: [0-9]+\.[0-9]+)
#     def fsm_integer_or_real(self):
#         lexeme = ''
#         is_real = False

#         # Handle digits before potential decimal point
#         while self.pos < self.length and self.source_code[self.pos].isdigit():
#             lexeme += self.source_code[self.pos]
#             self.pos += 1

#         # Check if it's a real number
#         if self.pos < self.length and self.source_code[self.pos] == '.':
#             is_real = True
#             lexeme += '.'
#             self.pos += 1
#             # Handle digits after the decimal point
#             while self.pos < self.length and self.source_code[self.pos].isdigit():
#                 lexeme += self.source_code[self.pos]
#                 self.pos += 1

#         if is_real:
#             return Token(TokenType.REAL, lexeme)
#         else:
#             return Token(TokenType.INTEGER, lexeme)

#     # FSM for Operators (handles multi-character operators like <=, >=, ==, !=)
#     def fsm_operator(self):
#         lexeme = self.source_code[self.pos]
#         self.pos += 1
        
#         if self.pos < self.length and self.source_code[self.pos] == '=':
#             lexeme += '='
#             self.pos += 1

#         if lexeme in Lexer.OPERATORS:
#             return Token(TokenType.OPERATOR, lexeme)
        
#         return Token(TokenType.UNKNOWN, lexeme)

#     # Check if character is an operator
#     def is_operator(self, ch):
#         return ch in {'+', '-', '*', '/', '=','<', '>', '!', '&', '|'}

#     # Check if character is a separator
#     def is_separator(self, ch):
#         return ch in Lexer.SEPARATORS


# # Main program to test the lexer
# def main():
#     test_files =["test_case1.txt", "test_case2.txt", "test_case3.txt"]

#     for test_file in test_files:
#         with open(test_file, "r") as file:
#             source_code = file.read()
#         # Initialize lexer with the current source code
#         lexer = Lexer(source_code)
#         # Tokenize the source code
#         tokens = lexer.tokenize()
        
#         # Print output
#         output_file_name = f"output_{test_file}"
#         with open(output_file_name, "w") as output_file:
#             # Write test case header
#             output_file.write(f"Processing {test_file}\n")
#             output_file.write(f"{'Token':<15} {'Lexeme':<20}\n")
#             output_file.write("-" * 35 + "\n")
#             # Write tokens and lexemes with proper alignment
            
#             for token in tokens:
#                 output_file.write(f"{token.type:<15} {token.lexeme:<20}\n")
#             output_file.write("\n" + "=" * 35 + "\n")  # Separator between test cases

#         print("Tokenization complete. Check the output files.")
    
    
    
    
# #     source_code = """
# #     [* this is comment for this sample code which
# #     converts Fahrenheit into Celcius *]
# #     function convert (fahr integer)
# #     {
# #     return 5 * (fahr -32) / 9;
# #     }
# #     @
# #     integer low, high, step; [* declarations *]
# #     get (low, high, step);
# #     while (low <= high )
# #     { put (low);
# #     put (convert (low));
# #     low = low + step;
# #     }
# #     @
# #     """

# #     # Initialize the lexer with source code
# #     lexer = Lexer(source_code)

# #     # Tokenize the source code
# #     tokens = lexer.tokenize()

# #     # Print tokens and lexemes
# #     print("Token\tLexeme")
# #     for token in tokens:
# #         print(f"{token.type}\t{token.lexeme}")


#     if __name__ == "__main__":
#         main()