import tkinter as tk
from tkinter import ttk

class Ui:
    def __init__(self, root: tk.Tk):
        self.root = root

        self.root.columnconfigure(0, weight=1, minsize=200)
        self.root.columnconfigure(1, weight=1, minsize=824)
        self.root.rowconfigure(0, weight=1, minsize=666)
        self.root.rowconfigure(1, weight=1, minsize=102)

        self.tools_frame = tk.Frame(root, bg='blue', width=200, height=768)
        self.image_frame = tk.Frame(root, bg='red', width=824, height=666)
        self.iris_frame = tk.Frame(root, bg='yellow', width=824, height=102)

        self.image_frame.rowconfigure(0, weight=1, minsize=333)
        self.image_frame.rowconfigure(1, weight=1, minsize=333)
        self.image_frame.columnconfigure(0, weight=1, minsize=412)
        self.image_frame.columnconfigure(1, weight=1, minsize=412)

        # self.tools_label = ttk.Label(self.tools_frame, width=180 ,text='Upload eye image in .bmp format and extract iris')
        self.upload_button = ttk.Button(self.tools_frame, text='Upload')
        self.extract_button = ttk.Button(self.tools_frame, text='Extract')
        self.info_label = ttk.Label(self.tools_frame)
        
        self.image_views = [ttk.Label(self.image_frame) for i in range(4)]

        self.tools_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.image_frame.grid(row=0, column=1, sticky='nsew')
        self.iris_frame.grid(row=1, column=1, sticky='nsew')

        self.upload_button.pack(pady=15)
        self.extract_button.pack()

    def display_image(self, image, cell):
        self.image_views[cell].configure(image=image)
        self.image_views[cell].image = image
        row = 0 if cell < 2 else 1
        column = 0 if cell % 2 == 0 else 1
        self.image_views[cell].grid(row=row, column=column)

    def remove_image(self, cell):
        self.image_views[cell].grid_forget()
    
    def show_info(self, info):
        self.info_label.configure(text=info)
        self.info_label.pack(side=tk.BOTTOM)

    def hide_info(self):
        self.info_label.pack_forget()