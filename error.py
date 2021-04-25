
# custom Exception class for Lexer Errors

class LexerError(Exception):
    def __init__(self, line, position, token):
        self.line = line
        self.position = position - len(token)
        self.token = token

    def error_message(self):
        print(f'Invalid token: {self.token} found in line: {self.line} at position: {self.position}')