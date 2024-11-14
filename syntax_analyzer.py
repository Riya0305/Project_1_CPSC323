class SyntaxAnalyzer:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def match(self, expected_type):
        if self.current_token.type == expected_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected token type {expected_type} (Token: {self.current_token.type}, Lexeme: {self.current_token.lexeme})")

    def error(self, message):
        print(f"Syntax Error: {message}")
        exit(1)

    def parse_rat24f(self):
        print("<Rat24F> ::= <Opt Function Definitions> @ <Opt Declaration List> <Statement List> @")
        self.parse_opt_function_definitions()
        self.match('SEPARATOR')  # Match '@'
        self.parse_opt_declaration_list()
        self.parse_statement_list()
        self.match('SEPARATOR')  # Match '@'

    def parse_opt_function_definitions(self):
        print("<Opt Function Definitions> ::= <Function Definitions> | <Empty>")
        if self.current_token.lexeme == "function":
            self.parse_function_definitions()
        else:
            self.parse_empty()

    def parse_function_definitions(self):
        print("<Function Definitions> ::= <Function> | <Function> <Function Definitions>")
        self.parse_function()
        if self.current_token.lexeme == "function":
            self.parse_function_definitions()

    def parse_function(self):
        print("<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
        self.match('KEYWORD')  # Match 'function'
        self.match('IDENTIFIER')  # Match function name
        self.match('SEPARATOR')  # Match '('
        self.parse_opt_parameter_list()
        self.match('SEPARATOR')  # Match ')'
        self.parse_opt_declaration_list()
        self.parse_body()

    def parse_body(self):
        print("<Body> ::= { <Statement List> }")
        self.match('SEPARATOR')  # Match '{'
        self.parse_statement_list()
        self.match('SEPARATOR')  # Match '}'

    def parse_statement_list(self):
        print("<Statement List> ::= <Statement> | <Statement> <Statement List>")
        self.parse_statement()
        while self.current_token.type in {'IDENTIFIER', 'KEYWORD'}:
            self.parse_statement()

    def parse_statement(self):
        print("<Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
        if self.current_token.type == 'IDENTIFIER':
            self.parse_assign()
        elif self.current_token.lexeme == "if":
            self.parse_if()
        # Add cases for other statement types as needed

    def parse_if(self):
        print("<If> ::= if ( <Condition> ) <Statement> fi | if ( <Condition> ) <Statement> else <Statement> fi")
        self.match('KEYWORD')  # Match 'if'
        self.match('SEPARATOR')  # Match '('
        self.parse_condition()
        self.match('SEPARATOR')  # Match ')'
        self.parse_statement()
        if self.current_token.lexeme == "else":
            self.match('KEYWORD')  # Match 'else'
            self.parse_statement()
        self.match('KEYWORD')  # Match 'fi'

    # New Method to Parse Conditions
    def parse_condition(self):
        print("<Condition> ::= <Expression> <Relational Operator> <Expression>")
        self.parse_expression()  # Parse the first expression
        self.parse_relational_operator()  # Parse the relational operator (e.g., ==, !=, <, >)
        self.parse_expression()  # Parse the second expression

    # New Method to Parse Relational Operators
    def parse_relational_operator(self):
        print("<Relational Operator> ::= == | != | < | > | <= | >=")
        if self.current_token.lexeme in ['==', '!=', '<', '>', '<=', '>=']:
            self.match('OPERATOR')  # Match a relational operator
        else:
            self.error("Expected a relational operator (==, !=, <, >, <=, >=)")

    def parse_expression(self):
        print("<Expression> ::= <Term> <Expression Prime>")
        self.parse_term()
        self.parse_expression_prime()

    def parse_term(self):
        print("<Term> ::= <Factor> <Term Prime>")
        self.parse_factor()
        self.parse_term_prime()

    def parse_factor(self):
        print("<Factor> ::= - <Primary> | <Primary>")
        if self.current_token.lexeme == '-':
            self.match('OPERATOR')
        self.parse_primary()

    def parse_primary(self):
        print("<Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | <Real> | true | false")
        if self.current_token.type == 'IDENTIFIER':
            self.match('IDENTIFIER')
        elif self.current_token.type == 'INTEGER':
            self.match('INTEGER')
        # Additional cases for primary types

    def parse_empty(self):
        print("<Empty> ::= ε")

# Additional methods such as parse_assign, parse_opt_parameter_list, etc., would go here