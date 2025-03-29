import numpy as np
import cv2

class EyeProcessor:
    
    def __init__(self, image):
        self.image = image
        self.pupil_mask = np.zeros_like(image)
        self.iris_mask = np.zeros_like(image)
        self.x = None
        self.y = None
        self.pupil_r = None
        self.iris_r = None
        
        self.process_pupil()
        self.process_iris()

    def get_pupil_mask(self):
        return (1 - self.pupil_mask) * 255
    
    def get_iris_mask(self):
        return (1 - self.iris_mask) * 255

    def process_pupil(self):
        self.pupil_mask = self._binarize(self.image, threshold=40)
        self.pupil_mask = self._open(self.pupil_mask, kernel=np.ones((5, 5), np.uint8))
        self.pupil_mask = self._close(self.pupil_mask)
        self.pupil_mask = self._remove_noise(self.pupil_mask)
        self.pupil_mask = self._pupil(self.pupil_mask)

    def process_iris(self):
        mask = np.zeros_like(self.image)
        cv2.circle(mask, (self.x, self.y), 3 * self.pupil_r, 1, thickness=-1)
        cv2.circle(mask, (self.x, self.y), self.pupil_r - 1, 0, thickness=-1)
        self.iris_mask = self._binarize(np.where(mask == 1, self.image, 255), threshold=110)
        means = np.zeros(2 * self.pupil_r + 1)

        for r in range(self.pupil_r - 1, 3 * self.pupil_r):
            mask = np.zeros_like(self.image)
            cv2.circle(mask, (self.x, self.y), r, 1, thickness=-1)
            means[r - self.pupil_r + 1] = np.mean(self.iris_mask[mask == 1])
        max_r = np.argmax(means)
        self.iris_r = max_r + self.pupil_r
        self.iris_mask = np.zeros_like(self.image)
        cv2.circle(self.iris_mask, (self.x, self.y), self.iris_r, 1, thickness=-1)
        cv2.circle(self.iris_mask, (self.x, self.y), self.pupil_r, 0, thickness=-1)
    
    def _binarize(self, image, threshold):
        return (image < threshold).astype(np.uint8)

    def _open(self, image, kernel):
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    def _close(self, image):
        kernel = np.ones((9, 9), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

    def _remove_noise(self, image):
        _, labels, stats, _ = cv2.connectedComponentsWithStats(image)
        areas = [stat[cv2.CC_STAT_AREA] for stat in stats]
        pupil_index = np.argsort(areas)[-2]
        return (labels == pupil_index).astype(np.uint8)

    def _pupil(self, image):
        def find_middle(projection):
            nonzero = np.nonzero(projection)[0]
            return nonzero[len(nonzero) // 2]
        self.x = find_middle(np.sum(image, axis=0))
        self.y = find_middle(np.sum(image, axis=1))
        self.pupil_r = len(np.nonzero(np.sum(image, axis=0))[0]) // 2
        mask = np.zeros_like(image)
        cv2.circle(mask, (self.x, self.y), self.pupil_r, 1, thickness=-1)
        return mask
        