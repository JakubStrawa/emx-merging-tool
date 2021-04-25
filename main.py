# created by Jakub Strawa, 2021
import gui
import codecs
from lexer import Lexer

if __name__ == "__main__":
    codecs.open("JavaBlankModel.emx", encoding="utf-8", errors="strict").readlines()
    lexer = Lexer("JavaBlankModel.emx")
    #gui.create_gui()
