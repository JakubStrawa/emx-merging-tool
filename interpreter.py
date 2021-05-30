from lexer import Lexer
from parser import Parser


class Interpreter:
    def __init__(self, file1, file2, resolve_mode, merge_destination):
        self.file1_path = file1
        self.file2_path = file2
        self.resolve_conflicts_mode = resolve_mode
        self.merge_destination = merge_destination
        self.merged_tree = None
        self.tokenize_input_files()

    def tokenize_input_files(self):
        lexer1 = Lexer(self.file1_path)
        lexer2 = Lexer(self.file2_path)
        print("File tokenizing complete")
        self.parse_input_files(lexer1.tokens_found, lexer2.tokens_found)

    def parse_input_files(self, token_list1, token_list2):
        tree1 = Parser(token_list1)
        tree2 = Parser(token_list2)
        print("Parsing complete")
        self.combine_input_files(tree1, tree2)

    def combine_input_files(self, tree1, tree2):
        pass
