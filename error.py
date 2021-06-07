
# custom Exception class for Lexer Errors

class LexerError(Exception):
    def __init__(self, line, position, token):
        self.line = line
        self.position = position - len(token)
        self.token = token

    def error_message(self):
        print(f'Invalid token: {self.token} found in line: {self.line} at position: {self.position}')


class SyntaxError(Exception):
    def __init__(self, token, msg=""):
        self.token = token
        self.message = msg
        self.default_error_message()

    def default_error_message(self):
        print(f'Unexpected token: {self.token.token_type} found in line: {self.token.line} at position: {self.token.position}')
        if self.message != "":
            self.custom_error_message()

    def custom_error_message(self):
        print(self.message)
