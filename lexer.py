from error import LexerError
from file_reader import FileReader
from tokens.token import TokenType, create_new_token
from tokens.token_regex import compile_regex_rules


class Lexer:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.source_file = FileReader(self.filepath)
        self.regex_table = compile_regex_rules()
        self.isEAnnotationFound = False
        self.tokens_found = self.lexer_loop()

    # get next token from source file
    def get_token(self):
        char = self.source_file.get_char()
        while char.isspace():
            char = self.source_file.get_char()
        if self.is_char_simple_token(char):
            for r in self.regex_table:
                if r.match(char):
                    return create_new_token(self.regex_table[r], char)
            raise LexerError(self.source_file.line, self.source_file.position, char)
        else:
            token_builder = char
            char = self.source_file.get_char()
            while (not char.isspace() or token_builder.count('"') == 1) and not self.is_char_simple_token(char):
                token_builder += char
                char = self.source_file.get_char()
            self.source_file.position -= 1
            self.source_file.absolute_position -= 1
            for r in self.regex_table:
                if r.match(token_builder):
                    return create_new_token(self.regex_table[r], token_builder)
            raise LexerError(self.source_file.line, self.source_file.position, token_builder)

    # tokenize everything inside graphics description
    def tokenize_graphics(self):
        graphics_tokens = []
        token = self.get_token()
        graphics_tokens.append(token)
        # tokenize entire eAnnotations line
        while token.token_type != TokenType.T_RIGHT_BRACKET:
            token = self.get_token()
            graphics_tokens.append(token)
        # skip all tokens until second eAnnotation token
        while token.token_type != TokenType.T_EANNOTATIONS:
            token = self.get_graphics_token()
            graphics_tokens.append(token)
        return graphics_tokens

    # get_token method without raising errors, but returning value tokens if not expected token found
    def get_graphics_token(self):
        char = self.source_file.get_char()
        while char.isspace():
            char = self.source_file.get_char()
        if self.is_char_simple_token(char):
            for r in self.regex_table:
                if r.match(char):
                    return create_new_token(self.regex_table[r], char)
            raise LexerError(self.source_file.line, self.source_file.position, char)
        else:
            token_builder = char
            char = self.source_file.get_char()
            while (not char.isspace() or token_builder.count('"') == 1) and not self.is_char_simple_token(char):
                token_builder += char
                char = self.source_file.get_char()
            self.source_file.position -= 1
            self.source_file.absolute_position -= 1
            for r in self.regex_table:
                if r.match(token_builder):
                    return create_new_token(self.regex_table[r], token_builder)
            return create_new_token(TokenType.T_STRING_VALUE, token_builder)

    # main lexer loop building token array
    def lexer_loop(self):
        token_array = []
        while True:
            try:
                token = self.get_token()
                token_array.append(token)
                # tokenize graphics description
                if token.token_type == TokenType.T_EANNOTATIONS and self.isEAnnotationFound is False:
                    self.isEAnnotationFound = True
                    graphics = self.tokenize_graphics()
                    token_array.extend(graphics)
                if token.token_type == TokenType.T_EOF:
                    break
            except LexerError as e:
                e.error_message()
                self.lexer_critical_error()
        print("EOF token found")
        self.source_file.close_file()
        return token_array

    # checks if char is one char token
    def is_char_simple_token(self, char):
        if char == '<' or char == '>' or char == '=' or char == '':
            return True
        elif char == '/':
            c = self.source_file.get_char()
            self.source_file.position -= 1
            self.source_file.absolute_position -= 1
            if c == '>':
                return True
            else:
                self.source_file.position -= 2
                self.source_file.absolute_position -= 2
                c = self.source_file.get_char()
                self.source_file.position += 1
                self.source_file.absolute_position += 1
                if c == '<':
                    return True
                else:
                    return False
        else:
            return False

    # critical lexer error when invalid token is met
    def lexer_critical_error(self):
        self.source_file.close_file()
        print("Critical error found, exiting lexer...")
        exit(5)