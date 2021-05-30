import tkinter as tk
from tkinter import filedialog
from interpreter import Interpreter


# gui app class
class App:
    def __init__(self):
        self.gui = tk.Tk()
        self.gui.title("EMX Merger")
        self.setup_grid_layout()
        self.file1_path_label = tk.Label(text="Choose file 1")
        self.file2_path_label = tk.Label(text="Choose file 2")
        self.file1_path = ""
        self.file2_path = ""
        self.log_textfield = tk.Text(self.gui, height=10, bg="white smoke")
        self.merge_destination = tk.IntVar()
        self.resolve_conflicts_mode = tk.IntVar()
        self.setup_widgets()

    def run(self):
        self.gui.mainloop()

    def run_button_callback(self):
        self.log_textfield.delete('1.0', tk.END)
        try:
            interpreter = Interpreter(self.file1_path, self.file2_path, self.resolve_conflicts_mode.get(), self.merge_destination.get())
        except FileNotFoundError:
            self.log_textfield.insert("0.0", "You have to choose both files!")

    def choose_file1_callback(self):
        self.gui.filename = tk.filedialog.askopenfilename(initialdir="./input_files", title="File select")
        self.file1_path_label.config(text=self.gui.filename)
        self.file1_path = self.gui.filename
        # shorten filepath if too long
        if len(self.gui.filename) > 35:
            short_path = "..." + self.gui.filename[-35:]
            self.file1_path_label.config(text=short_path)

    def choose_file2_callback(self):
        self.gui.filename = tk.filedialog.askopenfilename(initialdir="./input_files", title="File select")
        self.file2_path_label.config(text=self.gui.filename)
        self.file2_path = self.gui.filename
        # shorten filepath if too long
        if len(self.gui.filename) > 35:
            short_path = "..." + self.gui.filename[-35:]
            self.file2_path_label.config(text=short_path)

    def setup_grid_layout(self):
        self.gui.columnconfigure(0, weight=1)
        self.gui.columnconfigure(1, weight=1)
        self.gui.rowconfigure(0, weight=2)
        self.gui.rowconfigure(1, weight=1)
        self.gui.rowconfigure(2, weight=1)
        self.gui.rowconfigure(3, weight=1)
        self.gui.rowconfigure(4, weight=1)
        self.gui.rowconfigure(5, weight=1)
        self.gui.rowconfigure(6, weight=1)
        self.gui.rowconfigure(7, weight=10)
        self.gui.rowconfigure(8, weight=3)

    def setup_widgets(self):
        greet = tk.Label(text="Welcome to EMX merging tool!\nPlease choose files to merge.")
        file1_label = tk.Label(text="File 1")
        file2_label = tk.Label(text="File 2")
        button1 = tk.Button(self.gui, text="Choose file", command=self.choose_file1_callback)
        button2 = tk.Button(self.gui, text="Choose file", command=self.choose_file2_callback)
        new_file_checkbox = tk.Checkbutton(self.gui, text="Merge into new file",
                            variable=self.merge_destination, onvalue=1, offvalue=0, height=2, width=20)
        merge_int_file1_checkbox = tk.Checkbutton(self.gui, text="Merge into file 1",
                            variable=self.merge_destination, onvalue=0, offvalue=1, height=2, width=20)
        dont_resolve_conflicts_checkbox = tk.Checkbutton(self.gui, text="Don't resolve conflicts",
                            variable=self.resolve_conflicts_mode, onvalue=1, offvalue=0, height=2, width=20)
        close_button = tk.Button(self.gui, text="Close", command=self.gui.destroy)
        run_button = tk.Button(self.gui, text="Run", command=self.run_button_callback)
        greet.grid(row=0, column=0, columnspan=2)
        file1_label.grid(row=1, column=0)
        file2_label.grid(row=1, column=1)
        self.file1_path_label.grid(row=2, column=0)
        self.file2_path_label.grid(row=2, column=1)
        button1.grid(row=3, column=0)
        button2.grid(row=3, column=1)
        new_file_checkbox.grid(row=4, column=0, columnspan=2)
        merge_int_file1_checkbox.grid(row=5,  column=0, columnspan=2)
        dont_resolve_conflicts_checkbox.grid(row=6, column=0, columnspan=2)
        self.log_textfield.grid(row=7, column=0, columnspan=2, sticky="NSEW")
        close_button.grid(row=8, column=1)
        run_button.grid(row=8, column=0)


def create_gui():
    app = App()
    app.run()
