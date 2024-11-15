class Lexer:
    def __init__(self, input_code, output):
        self.input_code = input_code
        self.tokens = []
        self.current_pos = 0
        self.output = output
        self.tokenize()

    def write_output(self, text):
        self.output.write(text + "\n")

    def tokenize(self):
        keywords = {'function', 'integer', 'if', 'else', 'while', 'put'}
        operators = {'+', '-', '=', '<', '>', '*', '/'}
        separators = {'(', ')', '{', '}', ';'}

        while self.current_pos < len(self.input_code):
            char = self.input_code[self.current_pos]

            if char in [' ', '\t', '\n']:
                self.current_pos += 1
                continue

            if char.isalpha():
                start_pos = self.current_pos
                while self.current_pos < len(self.input_code) and self.input_code[self.current_pos].isalnum():
                    self.current_pos += 1
                lexeme = self.input_code[start_pos:self.current_pos]
                token_type = 'KEYWORD' if lexeme in keywords else 'IDENTIFIER'
                self.tokens.append((token_type, lexeme))
                self.write_output(f"Token: {token_type} Lexeme: {lexeme}")
                continue

            if char.isdigit():
                start_pos = self.current_pos
                while self.current_pos < len(self.input_code) and self.input_code[self.current_pos].isdigit():
                    self.current_pos += 1
                lexeme = self.input_code[start_pos:self.current_pos]
                self.tokens.append(('NUMBER', lexeme))
                self.write_output(f"Token: NUMBER Lexeme: {lexeme}")
                continue

            if char in operators:
                self.tokens.append(('OPERATOR', char))
                self.write_output(f"Token: OPERATOR Lexeme: {char}")
                self.current_pos += 1
                continue

            if char in separators:
                self.tokens.append(('SEPARATOR', char))
                self.write_output(f"Token: SEPARATOR Lexeme: {char}")
                self.current_pos += 1
                continue

            self.tokens.append(('MISMATCH', char))
            self.write_output(f"Token: MISMATCH Lexeme: {char}")
            self.current_pos += 1

    def get_next_token(self):
        if self.tokens:
            return self.tokens.pop(0)
        return None


class Parser:
    def __init__(self, lexer, output):
        self.lexer = lexer
        self.current_token = None
        self.output = output
        self.advance()

    def write_output(self, text):
        self.output.write(text + "\n")

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def syntax_error(self, message):
        self.write_output(f"Syntax Error: {message}")
        raise Exception(message)

    def parse_identifier(self):
        token_type, lexeme = self.current_token
        if token_type == "IDENTIFIER":
            self.write_output(f"<Identifier> -> {lexeme}")
            self.advance()
        else:
            self.syntax_error(f"Expected identifier, but found {token_type} Lexeme: {lexeme}")

    def parse_function_declaration(self):
        self.write_output("<Function Declaration> -> function <Identifier> ( <Parameters> ) <Body>")
        self.advance()  # Skip 'function'

        token_type, lexeme = self.current_token
        if token_type != "IDENTIFIER":
            self.syntax_error(f"Expected function name (identifier), found {token_type} Lexeme: {lexeme}")

        self.parse_identifier()
        self.advance()  # Skip '('
        self.parse_parameters()
        self.advance()  # Skip ')'
        self.parse_body()

    def parse_parameters(self):
        token_type, lexeme = self.current_token
        if token_type == "KEYWORD" and lexeme == "integer":
            self.write_output(f"Parameter: {lexeme}")
            self.advance()
            self.parse_identifier()

    def parse_body(self):
        token_type, lexeme = self.current_token
        if token_type == "SEPARATOR" and lexeme == "{":
            self.write_output("<Body> -> { <Statements> }")
            self.advance()
            self.parse_statement()
            self.advance()  # Skip '}'

    def parse_statement(self):
        token_type, lexeme = self.current_token
        if token_type == "IDENTIFIER":
            self.write_output("<Statement> -> <Assign>")
            self.advance()
            token_type, lexeme = self.current_token
            if token_type == "OPERATOR" and lexeme == "=":
                self.write_output("<Assign> -> <Identifier> = <Expression> ;")
                self.advance()
                self.parse_expression()
                self.advance()
                token_type, lexeme = self.current_token
                if token_type == "SEPARATOR" and lexeme == ";":
                    self.write_output(f"Token: {token_type} Lexeme: {lexeme}")
                    self.advance()
                else:
                    self.syntax_error(f"Expected ';', but found {token_type} Lexeme: {lexeme}")

    def parse_expression(self):
        token_type, lexeme = self.current_token
        if token_type == "IDENTIFIER":
            self.write_output("<Expression> -> <Term> <Expression Prime>")
            self.advance()
            self.parse_term()

    def parse_term(self):
        token_type, lexeme = self.current_token
        if token_type == "IDENTIFIER":
            self.write_output("<Term> -> <Factor> <Term Prime>")
            self.advance()
            self.parse_factor()

    def parse_factor(self):
        token_type, lexeme = self.current_token
        if token_type == "IDENTIFIER":
            self.write_output("<Factor> -> <Identifier>")
            self.advance()


def process_files(input_files, output_files):
    for input_file, output_file in zip(input_files, output_files):
        with open(output_file, 'w') as output:
            output.write(f"\nProcessing file: {input_file}\n")
            with open(input_file, 'r') as file:
                input_code = file.read()
                lexer = Lexer(input_code, output)
                parser = Parser(lexer, output)
                try:
                    parser.parse_function_declaration()
                except Exception as e:
                    output.write(f"\nParsing Error: {str(e)}\n")

# Example usage with multiple files
input_files = ['source_code_input.txt', 'source_code_input2.txt', 'source_code_input3.txt']
output_files = ['output_file1.txt', 'output_file2.txt', 'output_file3.txt']

process_files(input_files, output_files)