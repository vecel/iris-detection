import tkinter as tk
from ttkthemes import ThemedStyle

from src.ui import Ui
from src.controller import Controller
from src.model import Model

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Iris Extractor')
        self.geometry('800x600')
        self.minsize(800, 600)
        
        self.style = ThemedStyle(self)
        self.style.theme_use('scidmint')
        
        self.model = Model()
        self.ui = Ui(self)
        self.controller = Controller(self.ui, self.model)

        self.ui.upload_button.config(command=self.controller.on_upload)