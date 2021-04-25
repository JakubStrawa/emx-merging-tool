import unittest
import tokens.token as token


class TestToken(unittest.TestCase):
    def test_create_new_token(self):
        new_token = token.create_new_token(token.TokenType.T_UML_MODEL, "uml:Model")
        self.assertEqual(token.TokenType.T_UML_MODEL, new_token.token_type)
        self.assertEqual(type(new_token), token.Token)
        new_token = token.create_new_token(token.TokenType.T_UML_MODEL, "111")
        self.assertEqual(token.TokenType.T_UML_MODEL, new_token.token_type)
        self.assertEqual(type(new_token), token.Token)
        new_token = token.create_new_token(token.TokenType.T_STRING_VALUE, '"abcd"')
        self.assertEqual(token.TokenType.T_STRING_VALUE, new_token.token_type)
        self.assertEqual(new_token.value, '"abcd"')
        self.assertEqual(type(new_token), token.ValueToken)

    def test_token_to_string(self):
        self.assertEqual(token.TokenType.T_LEFT_BRACKET.to_string(), "<")
        self.assertEqual(token.TokenType.T_RIGHT_BRACKET.to_string(), ">")
        self.assertNotEqual(token.TokenType.T_RIGHT_BRACKET.to_string(), ">=")