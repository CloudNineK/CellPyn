import cv2


class PynModule():
    def __init__(self):
        pass

    def apply(self):
        pass

    def cvToPixmap(self, img, col):
        pass


class Threshold(PynModule):

    def __init__(self):
        pass

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

    def apply(self):
        pass
