from lexer import Lexer  # Import the Lexer class from lexer.py

debug = True  # Switch for enabling/disabling production rule logging
output_file = "parser_output.txt"  # File to write output

def log_to_file(message):
    """Logs output to a specified file."""
    with open(output_file, "a") as file:
        file.write(message + "\n")

def log_rule(rule):
    """Logs the production rule if debug mode is on."""
    if debug:
        print(rule)
        log_to_file(rule)

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = iter(tokens)  # Make sure tokens are an iterator
        self.current_token = None
        self.next_token()

    def next_token(self):
        """Advance to the next token."""
        self.current_token = next(self.tokens, None)

    def error(self, message):
        """Handles syntax errors and logs a meaningful error message."""
        error_message = (f"Syntax Error: {message} "
                         f"(Token: {self.current_token.type}, Lexeme: {self.current_token.lexeme})")
        print(error_message)
        log_to_file(error_message)

    def match(self, expected_token_type):
        """Match the current token with the expected token type."""
        if self.current_token and self.current_token.type == expected_token_type:
            log_to_file(f"Token: {self.current_token.type}, Lexeme: {self.current_token.lexeme}")
            self.next_token()
        else:
            self.error(f"Expected token type {expected_token_type}")

    # Parsing functions for each grammar rule, logging production rules
    def parse_rat24f(self):
        log_rule("<Rat24F> ::= <Opt Function Definitions> @ <Opt Declaration List> <Statement List> @")
        self.parse_opt_function_definitions()
        self.match('@')
        self.parse_opt_declaration_list()
        self.parse_statement_list()
        self.match('@')

    def parse_opt_function_definitions(self):
        log_rule("<Opt Function Definitions> ::= <Function Definitions> | <Empty>")
        if self.current_token.type == 'function':
            self.parse_function_definitions()
        else:
            self.parse_empty()

    def parse_empty(self):
        log_rule("<Empty> ::= ε")

    # Add similar parsing functions for other grammar rules here

# Clear the output file at the start
open(output_file, "w").close()

# Read source code from file
with open("source_code_input.txt", "r") as file:
    source_code = file.read()

# Tokenize the source code using Lexer
lexer_instance = Lexer(source_code)
tokens = lexer_instance.tokenize()  # Retrieve tokens using the tokenize() method

# Initialize parser with tokens and parse
parser = SyntaxAnalyzer(tokens)
parser.parse_rat24f()
