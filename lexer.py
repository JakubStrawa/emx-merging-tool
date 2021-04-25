from tokens.token import TokenType, create_new_token
from tokens.token_regex import compile_regex_rules
from file_reader import FileReader
from error import LexerError

class Lexer:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.source_file = FileReader(self.filepath)
        self.regex_table = compile_regex_rules()
        self.lexer_loop()

    def get_token(self):
        char = self.source_file.get_char()
        while char.isspace():
            char = self.source_file.get_char()
        if self.is_char_simple_token(char):
            try:
                for r in self.regex_table:
                    if r.match(char):
                        return create_new_token(self.regex_table[r], char)
            except LexerError:
                raise LexerError(self.source_file.line, char)
            #except LexerError(self.source_file.line, char) as e:
             #   print(e.error_message())
        else:
            token_builder = char
            char = self.source_file.get_char()
            while (not char.isspace() or token_builder.count('"') == 1) and not self.is_char_simple_token(char):
                token_builder += char
                char = self.source_file.get_char()
            self.source_file.position -= 1
            try:
                for r in self.regex_table:
                    if r.match(token_builder):
                        return create_new_token(self.regex_table[r], token_builder)
            except LexerError:
                raise LexerError(self.source_file.line, token_builder)


    def lexer_loop(self):
        token = self.get_token()
        print(token.token_type)
        while token.token_type != TokenType.T_EOF:
            token = self.get_token()
            #print(token.token_type)
            #if token.token_type == TokenType.T_STRING_VALUE or token.token_type == TokenType.T_DOUBLE_STRING_VALUE:
                #print(token.value)
        print("EOF token found")

    def is_char_simple_token(self, char):
        if char == '<' or char == '>' or char == '=' or char == '':
            return True
        elif char == '/':
            c = self.source_file.get_char()
            self.source_file.position -= 1
            if c == '>':
                return True
            else:
                self.source_file.position -= 2
                c = self.source_file.get_char()
                self.source_file.position += 1
                if c == '<':
                    return True
                else:
                    return False
        else:
            return False
