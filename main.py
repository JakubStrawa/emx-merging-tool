# created by Jakub Strawa, 2021
import gui
import codecs
from lexer import Lexer

if __name__ == "__main__":
    codecs.open("test.txt", encoding="utf-8", errors="strict").readlines()
    lexe = Lexer("test.txt")
    #gui.create_gui()
