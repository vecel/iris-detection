import tkinter.filedialog as fd
import cv2
import numpy as np
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
        image_path = fd.askopenfilename(filetypes=[('Bitmap Files', '*.bmp')])
        # image_path = self._random_image_path() # temporary
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.ui.remove_image(cell=1)
        self.ui.remove_image(cell=2)
        self.ui.remove_image(cell=3)
        self.model.image = image
        self.display_image(self.model.image, text='Uploaded image')
        
    def on_extract(self):
        if self.model.image is None:
            self.ui.show_info('Image is not uploaded')
            return
        processor = EyeProcessor(self.model.image)
        self.display_image(processor.pupil, cell=1, text='Pupil')
        self.display_image(processor.iris, cell=2, text='Iris')
        self.display_image(processor.iris_rect, cell=3, text='Iris expanded to rectangle')

    def display_image(self, image, cell=0, text=None):
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.ui.display_image(image, cell=cell, text=text)

    def _random_image_path(self):
        person = random.randint(1, 46)
        side = 'left' if random.randint(0, 1) == 0 else 'right'
        eye = random.randint(1, 5)
        return f'./data/person_{person}_{side}{eye}.bmp'