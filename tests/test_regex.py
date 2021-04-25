import unittest
import tokens.token_regex as token_regex
import tokens.token as token

class TestRegex(unittest.TestCase):
    def test_compile_regex_rules(self):
        compiled_regex = token_regex.compile_regex_rules()
        self.assertEqual(59, len(compiled_regex.keys()))

    def test_regex(self):
        compiled_regex = token_regex.compile_regex_rules()
        for r in compiled_regex:
            if r.match('<'):
                self.assertEqual(compiled_regex[r], token.TokenType.T_LEFT_BRACKET)
            if r.match('"abcdefg"'):
                self.assertEqual(compiled_regex[r], token.TokenType.T_STRING_VALUE)
            if r.match('uml:Model'):
                self.assertEqual(compiled_regex[r], token.TokenType.T_UML_MODEL)
            if r.match('"asbasub hjdahs"'):
                self.assertEqual(compiled_regex[r], token.TokenType.T_DOUBLE_STRING_VALUE)