# created by Jakub Strawa, 2021
import tkinter as tk


def button_callback():
    print("Button pressed")


def setup_widgets(gui):
    check_val = tk.IntVar()
    greet = tk.Label(text="Witaj tkinter")
    button1 = tk.Button(gui, text="Choose file", command = button_callback)
    button2 = tk.Button(gui, text="Choose file", command = button_callback)
    c1 = tk.Checkbutton(gui, text = "Don't resolve conflicts", variable = check_val, onvalue = 1, offvalue = 0, height=5, width = 20)
    greet.pack()
    button1.pack()
    button2.pack()
    c1.pack()
    closeButton = tk.Button(gui, text="Close")
    closeButton.pack(side=tk.RIGHT, padx=5, pady=5)
    runButton = tk.Button(gui, text="Run")
    runButton.pack(side=tk.RIGHT, padx=30, pady=5)

def create_gui():
    gui = tk.Tk()
    gui.title("EMX Merger")
    setup_widgets(gui)
    gui.mainloop()


if __name__ == "__main__":
    print("Witajcie")
    try:
        file = open("JavaBlankModel.emx", "r")
    finally:
        file.close()
    create_gui()