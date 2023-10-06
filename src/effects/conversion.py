import cv2
import numpy as np


class Conversion:
    def __init__(self, img, named_conversion, type_conversion):
        self.altered_img = np.copy(img)
        self.original_img = np.copy(img)
        self.named_conversion = named_conversion
        self.type_conversion = type_conversion

    def run_conversion(self):

        return self.verify_type()

    def verify_type(self):
        if self.type_conversion == "RGB --> GRAY":
            return cv2.cvtColor(self.original_img, cv2.COLOR_RGB2GRAY)

        if self.type_conversion == "RGB --> XYZ":
            return cv2.cvtColor(self.original_img, cv2.COLOR_RGB2XYZ)

        if self.type_conversion == "RGB --> YCrCb":
            return cv2.cvtColor(self.original_img, cv2.COLOR_RGB2YCrCb)

        if self.type_conversion == "RGB --> HSV":
            return cv2.cvtColor(self.original_img, cv2.COLOR_RGB2HSV)

        if self.type_conversion == "RGB --> HLS":
            return cv2.cvtColor(self.original_img, cv2.COLOR_RGB2HLS)

        if self.type_conversion == "RGB --> CIE L*a*b*":
            return cv2.cvtColor(self.original_img, cv2.COLOR_RGB2LAB)

        if self.type_conversion == "RGB --> CIE L*u*v*":
            return cv2.cvtColor(self.original_img, cv2.COLOR_RGB2LUV)
