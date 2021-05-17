import unittest
from tokens.token import create_new_token, TokenType
from parser import Parser
from error import SyntaxError

class TestParser(unittest.TestCase):
    def test_compare_tokens(self):
        token = create_new_token(TokenType.T_EQUALS, 1)
        self.assertEqual(token.token_type, TokenType.T_EQUALS)
        with self.assertRaises(SyntaxError):
            Parser.compare_tokens(self, token, TokenType.T_TYPE)

    def test_parse_model_end(self):
        tokens = []
        for i in range(5):
            token = create_new_token(TokenType.T_EQUALS, 1)
            tokens.append(token)
        with self.assertRaises(SyntaxError):
            parser = Parser(tokens)
            parser.parse_model_end()

    def test_parse_applied_profile(self):
        tokens = []
        for i in range(5):
            token = create_new_token(TokenType.T_EQUALS, 1)
            tokens.append(token)
        with self.assertRaises(SyntaxError):
            parser = Parser(tokens)
            parser.parse_applied_profile()