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
        self.tokens = iter(tokens)  # Ensure tokens are an iterator
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

    def parse_rat24f(self):
        log_rule("<Rat24F> ::= <Opt Function Definitions> @ <Opt Declaration List> <Statement List> @")
        self.parse_opt_function_definitions()
        self.match('@')
        self.parse_opt_declaration_list()
        self.parse_statement_list()
        self.match('@')

    def parse_opt_function_definitions(self):
        log_rule("<Opt Function Definitions> ::= <Function Definitions> | <Empty>")
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.lexeme == 'function':
            self.parse_function_definitions()
        else:
            self.parse_empty()

    def parse_function_definitions(self):
        log_rule("<Function Definitions> ::= <Function> | <Function> <Function Definitions>")
        self.parse_function()
        while self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.lexeme == 'function':
            self.parse_function()

    def parse_function(self):
        log_rule("<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
        self.match('KEYWORD')  # Matches 'function'
        self.match('IDENTIFIER')  # Matches function name
        self.match('SEPARATOR')  # Matches '('
        self.parse_opt_parameter_list()
        self.match('SEPARATOR')  # Matches ')'
        self.parse_opt_declaration_list()
        self.parse_body()

    def parse_opt_parameter_list(self):
        log_rule("<Opt Parameter List> ::= <Parameter List> | <Empty>")
        if self.current_token and self.current_token.type == 'IDENTIFIER':
            self.parse_parameter_list()
        else:
            self.parse_empty()

    def parse_parameter_list(self):
        log_rule("<Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>")
        self.parse_parameter()
        while self.current_token and self.current_token.lexeme == ',':
            self.match('SEPARATOR')  # Matches ','
            self.parse_parameter()

    def parse_parameter(self):
        log_rule("<Parameter> ::= <IDs> <Qualifier>")
        self.parse_ids()
        self.parse_qualifier()

    def parse_qualifier(self):
        log_rule("<Qualifier> ::= integer | boolean | real")
        if self.current_token.lexeme in ['integer', 'boolean', 'real']:
            self.match('KEYWORD')
        else:
            self.error("Expected a qualifier (integer, boolean, real)")

    def parse_ids(self):
        log_rule("<IDs> ::= <Identifier> | <Identifier>, <IDs>")
        self.match('IDENTIFIER')  # Matches the identifier
        while self.current_token and self.current_token.lexeme == ',':
            self.match('SEPARATOR')  # Matches ','
            self.match('IDENTIFIER')

    def parse_opt_declaration_list(self):
        log_rule("<Opt Declaration List> ::= <Declaration List> | <Empty>")
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.lexeme in ['integer', 'boolean', 'real']:
            self.parse_declaration_list()
        else:
            self.parse_empty()

    def parse_declaration_list(self):
        log_rule("<Declaration List> ::= <Declaration> ; | <Declaration> ; <Declaration List>")
        self.parse_declaration()
        self.match('SEPARATOR')  # Match ';' at the end of a declaration
        while self.current_token and self.current_token.lexeme in ['integer', 'boolean', 'real']:
            self.parse_declaration()
            self.match('SEPARATOR')  # Match ';' after each declaration

    def parse_declaration(self):
        log_rule("<Declaration> ::= <Qualifier> <IDs>")
        self.parse_qualifier()
        self.parse_ids()

    def parse_body(self):
        log_rule("<Body> ::= { <Statement List> }")
        self.match('SEPARATOR')  # Match '{'
        self.parse_statement_list()
        self.match('SEPARATOR')  # Match '}'

    def parse_statement_list(self):
        log_rule("<Statement List> ::= <Statement> | <Statement> <Statement List>")
        self.parse_statement()
        while self.current_token and (self.current_token.type in ['IDENTIFIER', 'KEYWORD']):
            self.parse_statement()

    def parse_statement(self):
        log_rule("<Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
        if self.current_token.type == 'IDENTIFIER':
            self.parse_assign()
        elif self.current_token.type == 'KEYWORD' and self.current_token.lexeme == 'if':
            self.parse_if()
        # Additional parsing logic for other statements (Return, Print, etc.)

    def parse_assign(self):
        log_rule("<Assign> ::= <Identifier> = <Expression> ;")
        self.match('IDENTIFIER')  # Matches the identifier in the assignment
        self.match('OPERATOR')  # Matches '='
        self.parse_expression()
        self.match('SEPARATOR')  # Matches ';'

    def parse_expression(self):
        log_rule("<Expression> ::= <Term> <Expression Prime>")
        self.parse_term()
        self.parse_expression_prime()

    def parse_expression_prime(self):
        log_rule("<Expression Prime> ::= + <Term> <Expression Prime> | - <Term> <Expression Prime> | ε")
        if self.current_token and self.current_token.lexeme in ['+', '-']:
            self.match('OPERATOR')
            self.parse_term()
            self.parse_expression_prime()

    def parse_term(self):
        log_rule("<Term> ::= <Factor> <Term Prime>")
        self.parse_factor()
        self.parse_term_prime()

    def parse_term_prime(self):
        log_rule("<Term Prime> ::= * <Factor> <Term Prime> | / <Factor> <Term Prime> | ε")
        if self.current_token and self.current_token.lexeme in ['*', '/']:
            self.match('OPERATOR')
            self.parse_factor()
            self.parse_term_prime()

    def parse_factor(self):
        log_rule("<Factor> ::= - <Primary> | <Primary>")
        if self.current_token.lexeme == '-':
            self.match('OPERATOR')
        self.parse_primary()

    def parse_primary(self):
        log_rule("<Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | <Real> | true | false")
        if self.current_token.type == 'IDENTIFIER':
            self.match('IDENTIFIER')
            if self.current_token and self.current_token.lexeme == '(':
                self.match('SEPARATOR')
                self.parse_ids()
                self.match('SEPARATOR')
        elif self.current_token.type == 'INTEGER' or self.current_token.type == 'REAL':
            self.match(self.current_token.type)
        elif self.current_token.lexeme == 'true' or self.current_token.lexeme == 'false':
            self.match('KEYWORD')
        elif self.current_token.lexeme == '(':
            self.match('SEPARATOR')
            self.parse_expression()
            self.match('SEPARATOR')
        else:
            self.error("Expected an identifier, integer, real, or boolean literal")

    def parse_empty(self):
        log_rule("<Empty> ::= ε")

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
