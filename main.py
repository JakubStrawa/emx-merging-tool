# created by Jakub Strawa, 2021
import gui
import codecs
from lexer import Lexer

if __name__ == "__main__":
    filepath = "JavaBlankModel.emx"
    codecs.open(filepath, encoding="utf-8", errors="strict").readlines()
    lexer = Lexer(filepath)
    print(lexer.tokens_found)
    #gui.create_gui()
