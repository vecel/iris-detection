import tkinter.filedialog as fd
import cv2
from PIL import Image, ImageTk

from src.ui import Ui
from src.model import Model
from src.processors.eye_processor import EyeProcessor

import random # temporary

class Controller:
    def __init__(self, ui: Ui, model: Model):
        self.ui = ui
        self.model = model

    def on_upload(self):
        # image_path = fd.askopenfilename(filetypes=[('Bitmap Files', '*.bmp')])
        image_path = self._random_image_path() # temporary
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.model.image = image
        self.display_image()

    def on_extract(self):
        if self.model.image is None:
            self.ui.show_info('Image is not uploaded')
            return
        processor = EyeProcessor(self.model.image)
        self.model.image = processor.process()
        self.display_image()

    def display_image(self):
        image = Image.fromarray(self.model.image)
        image = ImageTk.PhotoImage(image)
        self.ui.display_image(image)

    def _random_image_path(self):
        person = random.randint(1, 46)
        side = 'left' if random.randint(0, 1) == 0 else 'right'
        eye = random.randint(1, 5)
        return f'./data/person_{person}_{side}{eye}.bmp'