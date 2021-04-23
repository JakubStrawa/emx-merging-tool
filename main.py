# created by Jakub Strawa, 2021
import gui

if __name__ == "__main__":
    try:
        file = open("JavaBlankModel.emx", "r")
    finally:
        file.close()
    gui.create_gui()
