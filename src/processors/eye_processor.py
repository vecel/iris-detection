import numpy as np
import cv2

class EyeProcessor:
    
    def __init__(self, image):
        self.image = image
        self.pupil_mask = np.zeros_like(image)
        self.iris_mask = np.zeros_like(image)
        self.iris_rect = None
        self.x = None
        self.y = None
        self.pupil_r = None
        self.iris_r = None

        self._bright = cv2.add(self.image, 100)
        
        self.process_pupil()
        self.process_iris()
        self.expand_to_rect()

    @property
    def pupil(self):
        return np.where(self.pupil_mask == 1, self.image, self._bright)

    @property
    def iris(self):
        return np.where(self.iris_mask == 1, self.image, self._bright)

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
        self.iris_r = max_r + self.pupil_r + 5
        self.iris_mask = np.zeros_like(self.image)
        cv2.circle(self.iris_mask, (self.x, self.y), self.iris_r, 1, thickness=-1)
        cv2.circle(self.iris_mask, (self.x, self.y), self.pupil_r, 0, thickness=-1)

    def expand_to_rect(self):
        width = int(2 * np.pi * self.iris_r)
        height = int(self.iris_r - self.pupil_r)
        self.iris_rect = np.ones((height, width)) * 128
        for y, x in np.argwhere(self.iris_mask == 1):
            r = np.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
            cos = (x - self.x) / r
            sin = (y - self.y) / r
            theta = np.arctan2(sin, cos)
            if theta < 0:
                theta += 2 * np.pi
            rect_y = int(r - self.pupil_r)
            rect_y = max(min(height - 1, rect_y), 0)
            rect_x = int(theta * self.iris_r)
            rect_x = max(min(width - 1, rect_x), 0)
            self.iris_rect[rect_y, rect_x] = self.image[y, x]
    
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
        