import cv2
import numpy as np
from Controllers import Slider


class PynModule():
    def __init__(self, img):
        self.img = img

    def apply(self):
        pass

    def cvToPixmap(self, img, col):
        pass


class Threshold(PynModule):

    def __init__(self):
        super().__init__(self)
        self.controllers = {'Blur': Slider()}

    def app(self, image, blurAmount, thresh='Adaptive'):
        """ Apply selected thresholding algorithm to image"""

        # Greyscale image for thresholding
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Blur image to adjust threshold accuracy
        blur = cv2.medianBlur(gray, blurAmount)

        # Adaptive Threshold
        out = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 61, 2)

        return out


class Filter(PynModule):
    def __init__(self):
        pass

    def app(self, image, lower, upper):
        """ Apply color filter to the image"""

        lower = np.array([0, 70, 0])
        upper = np.array([90, 255, 90])
        mask = cv2.inRange(image, lower, upper)
        out = cv2.bitwise_and(image, image, mask=mask)

        return out
