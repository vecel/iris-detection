import tkinter.filedialog as fd
import cv2
from PIL import Image, ImageTk

from src.ui import Ui
from src.model import Model

class Controller:
    def __init__(self, ui: Ui, model: Model):
        self.ui = ui
        self.model = model

    def on_upload(self):
        # image_path = fd.askopenfilename(filetypes=[('Bitmap Files', '*.bmp')])
        image_path = './data/MMU-Iris-Database/1/left/aeval1.bmp' # temporary
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.model.image = image
        self.display_image()

    def display_image(self):
        image = Image.fromarray(self.model.image)
        image = ImageTk.PhotoImage(image)
        self.ui.display_image(image)

    def toggle_processing(self):
        self.model.processing = not self.model.processing
        if self.model.processing:
            self.ui.show_processing_label()
        else:
            self.ui.hide_processing_label()