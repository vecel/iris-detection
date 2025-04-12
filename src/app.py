import tkinter as tk
from ttkthemes import ThemedStyle

from src.ui import Ui
from src.controller import Controller
from src.model import Model

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Iris Extractor')
        self.geometry('1024x768')
        self.minsize(1024, 768)
        
        self.style = ThemedStyle(self)
        self.style.theme_use('scidmint')

        self.primary_color = '#434343'
        self.secondary_color = '#A3A3A3'
        self.tertiary_color = '#707070'
        
        self.model = Model()
        self.ui = Ui(self)
        self.controller = Controller(self.ui, self.model)

        self.ui.upload_button.config(command=self.controller.on_upload)
        self.ui.extract_button.config(command=self.controller.on_extract)