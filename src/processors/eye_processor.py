import numpy as np
import cv2

class EyeProcessor:
    
    def __init__(self, image):
        self.image = image

    def process(self):
        self.binarize(threshold=40)
        self.open()
        self.close()
        self.eye_pupil()
        return (1 - self.image) * 255
    
    def binarize(self, threshold):
        self.image = (self.image < threshold).astype(np.uint8)

    def open(self):
        kernel = np.ones((5, 5), np.uint8)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)

    def close(self):
        kernel = np.ones((9, 9), np.uint8)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)

    def eye_pupil(self):
        def find_middle(projection):
            nonzero = np.nonzero(projection)[0]
            return nonzero[len(nonzero) // 2]
        x = find_middle(np.sum(self.image, axis=0))
        y = find_middle(np.sum(self.image, axis=1))
        r = len(np.nonzero(np.sum(self.image, axis=0))[0]) // 2
        return x, y, r
        