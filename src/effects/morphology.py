import cv2
import numpy as np


class Morphology:
    def __init__(self, img, named_morphology, type_morphology):
        self.altered_img = np.copy(img)
        self.original_img = np.copy(img)
        self.named_morphology = named_morphology
        self.type_morphology = type_morphology
        self.value_erosion = 0
        self.value_dilation = 0

    def apply_erosion(self, value):
        kernel = np.ones((value, value), np.uint8)
        self.altered_img = cv2.erode(self.original_img, kernel, iterations=1)
        cv2.imshow(self.named_morphology, self.altered_img)

    def apply_dilatation(self, value):
        kernel = np.ones((value, value), np.uint8)
        self.altered_img = cv2.dilate(self.original_img, kernel, iterations=1)
        cv2.imshow(self.named_morphology, self.altered_img)

    def run_morphology(self):
        cv2.namedWindow(self.named_morphology, cv2.WINDOW_AUTOSIZE)

        if self.type_morphology == "erosion":
            def on_trackbar_change(value):
                self.apply_erosion(value)

            cv2.createTrackbar('Element Size', self.named_morphology, self.value_erosion, 50, on_trackbar_change)

        if self.type_morphology == "dilatation":
            def on_trackbar_change(value):
                self.apply_dilatation(value)

            cv2.createTrackbar('Element Size', self.named_morphology, self.value_dilation, 50, on_trackbar_change)

        while True:
            cv2.imshow(self.named_morphology, self.altered_img)
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == 27:
                break
            if tecla == ord('s'):
                cv2.destroyWindow(self.named_morphology)
                return self.altered_img

        cv2.destroyAllWindows()
