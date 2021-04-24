from tokens.token import TokenType, create_new_token
from tokens.token_regex import compile_regex_rules
from file_reader import FileReader


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
            except EOFError as e:
                print("LEXER ERROR!!!!")
                print(e)
        else:
            token_builder = char
            char = self.source_file.get_char()
            while not char.isspace() and not self.is_char_simple_token(char):
                token_builder += char
                char = self.source_file.get_char()
            self.source_file.position -= 1
            #if char.isspace() and self.check_for_double_string_token(token_builder):
             #   self.source_file.position += 1
              #  token_builder += char
               # char = self.source_file.get_char()
                #while not char.isspace() and not self.is_char_simple_token(char):
                 #   token_builder += char
                  #  char = self.source_file.get_char()
            try:
                for r in self.regex_table:
                    if r.match(token_builder):
                        return create_new_token(self.regex_table[r], token_builder)
            except EOFError as e:
                print("LEXER ERROR!!!!")
                print(e)


    def lexer_loop(self):
        token = self.get_token()
        print(token.token_type)
        while token.token_type != TokenType.T_EOF:
            token = self.get_token()
            print(token.token_type)
            if token.token_type == TokenType.T_STRING_VALUE:
                print(token.value)
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

    def check_for_double_string_token(self, token_builder):
        tmp = token_builder + self.source_file.peek()
        for r in self.regex_table:
            if r.match(tmp) and self.regex_table[r] == TokenType.T_DOUBLE_STRING_VALUE:
                return True
        return False
