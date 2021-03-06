import unittest
from lexer import Lexer
from error import LexerError

# lexer testing class


class TestLexer(unittest.TestCase):
    def test_get_token(self):
        new_lexer = Lexer("test1.txt")
        tokens1 = ['T_LEFT_BRACKET', 'T_PACKAGED_ELEMENT', 'T_XMI_TYPE', 'T_EQUALS', 'T_STRING_VALUE', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_NAME', 'T_EQUALS', 'T_STRING_VALUE', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_OWNED_ATTRIBUTE', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_NAME', 'T_EQUALS', 'T_STRING_VALUE', 'T_VISIBILITY', 'T_EQUALS', 'T_STRING_VALUE', 'T_SLASH', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_OWNED_OPERATION', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_NAME', 'T_EQUALS', 'T_STRING_VALUE', 'T_SLASH', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_SLASH', 'T_PACKAGED_ELEMENT', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_PACKAGED_ELEMENT', 'T_XMI_TYPE', 'T_EQUALS', 'T_STRING_VALUE', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_NAME', 'T_EQUALS', 'T_STRING_VALUE', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_OWNED_ATTRIBUTE', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_NAME', 'T_EQUALS', 'T_STRING_VALUE', 'T_VISIBILITY', 'T_EQUALS', 'T_STRING_VALUE', 'T_TYPE', 'T_EQUALS', 'T_STRING_VALUE', 'T_SLASH', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_OWNED_OPERATION', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_NAME', 'T_EQUALS', 'T_STRING_VALUE', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_OWNED_PARAMETER', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_NAME', 'T_EQUALS', 'T_STRING_VALUE', 'T_TYPE', 'T_EQUALS', 'T_STRING_VALUE', 'T_SLASH', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_SLASH', 'T_OWNED_OPERATION', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_SLASH', 'T_PACKAGED_ELEMENT', 'T_RIGHT_BRACKET', 'T_EOF']
        for i in range(len(tokens1)):
            self.assertEqual(tokens1[i], new_lexer.tokens_found[i].token_type.name)
        new_lexer = Lexer("test2.txt")
        tokens2 = ['T_LEFT_BRACKET', 'T_PACKAGED_ELEMENT', 'T_XMI_TYPE', 'T_EQUALS', 'T_STRING_VALUE', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_MEMBER_END', 'T_EQUALS', 'T_DOUBLE_STRING_VALUE', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_OWNED_END', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_NAME', 'T_EQUALS', 'T_STRING_VALUE', 'T_VISIBILITY', 'T_EQUALS', 'T_STRING_VALUE', 'T_TYPE', 'T_EQUALS', 'T_STRING_VALUE', 'T_ASSOCIATION', 'T_EQUALS', 'T_STRING_VALUE', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_UPPER_VALUE', 'T_XMI_TYPE', 'T_EQUALS', 'T_STRING_VALUE', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_VALUE', 'T_EQUALS', 'T_STRING_VALUE', 'T_SLASH', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_LOWER_VALUE', 'T_XMI_TYPE', 'T_EQUALS', 'T_STRING_VALUE', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_VALUE', 'T_EQUALS', 'T_STRING_VALUE', 'T_SLASH', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_SLASH', 'T_OWNED_END', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_SLASH', 'T_PACKAGED_ELEMENT', 'T_RIGHT_BRACKET', 'T_LEFT_BRACKET', 'T_PROFILE_APPLICATION', 'T_XMI_ID', 'T_EQUALS', 'T_STRING_VALUE', 'T_RIGHT_BRACKET', 'T_EOF']
        self.assertNotEqual(tokens1, new_lexer.tokens_found)
        for i in range(len(tokens2)):
            self.assertEqual(tokens2[i], new_lexer.tokens_found[i].token_type.name)
