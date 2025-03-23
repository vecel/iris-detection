import tkinter as tk
from tkinter import ttk

class Ui:
    def __init__(self, root: tk.Tk):
        self.root = root

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.tools_frame = tk.Frame(root, bg='blue', width=250, height=600)
        self.image_frame = tk.Frame(root, bg='red', width=550, height=400)
        self.iris_frame = tk.Frame(root, bg='yellow', width=550, height=200)

        self.tools_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.image_frame.grid(row=0, column=1, sticky='nsew')
        self.iris_frame.grid(row=1, column=1, sticky='nsew')

        self.upload_button = ttk.Button(self.tools_frame, text='Upload')

        self.upload_button.pack()