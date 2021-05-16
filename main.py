# created by Jakub Strawa, 2021
import gui
import codecs
from lexer import Lexer
from parser import Parser

if __name__ == "__main__":
    # filepath to lexer source
    filepath = "input_files/JavaBlankModel.emx"
    # check if source is utf-8 compatible
    codecs.open(filepath, encoding="utf-8", errors="strict").readlines()
    # create lexer and tokenize source
    lexer = Lexer(filepath)
    parser = Parser(lexer.tokens_found)
    print("Token parsing complete")
    #gui.create_gui()
