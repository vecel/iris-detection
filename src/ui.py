import tkinter as tk
from tkinter import ttk

class Ui:
    def __init__(self, root: tk.Tk):
        self.root = root

        self.root.columnconfigure(0, weight=1, minsize=250)
        self.root.columnconfigure(1, weight=1, minsize=550)
        self.root.rowconfigure(0, weight=1, minsize=400)
        self.root.rowconfigure(1, weight=1, minsize=200)

        self.tools_frame = tk.Frame(root, bg='blue', width=250, height=600)
        self.image_frame = tk.Frame(root, bg='red', width=550, height=400)
        self.iris_frame = tk.Frame(root, bg='yellow', width=550, height=200)
        self.upload_button = ttk.Button(self.tools_frame, text='Upload')
        self.processing_label = ttk.Label(self.tools_frame, text='Processing...')
        self.image_view = ttk.Label(self.image_frame)

        self.tools_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.image_frame.grid(row=0, column=1, sticky='nsew')
        self.iris_frame.grid(row=1, column=1, sticky='nsew')

        self.upload_button.pack()
    
    def display_image(self, image):
        self.image_view.configure(image=image)
        self.image_view.image = image
        self.image_view.pack(expand=True)

    def show_processing_label(self):
        self.processing_label.pack(side=tk.BOTTOM, anchor=tk.W, padx=10)

    def hide_processing_label(self):
        self.processing_label.pack_forget()