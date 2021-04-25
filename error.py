

class LexerError(Exception):
    def __init__(self, line, token):
        self.line = line
        self.token = token
        self.error_message()

    def error_message(self):
        print(f'Unexpected token {self.token} found in line {self.line}')