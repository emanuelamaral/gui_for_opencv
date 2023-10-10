import cv2
import numpy as np


class Threshold:
    def __init__(self, img, named_threshold, type_threshold):
        self.altered_img = np.copy(img)
        self.original_img = np.copy(img)
        self.named_threshold = named_threshold
        self.type_threshold = type_threshold

        self.threshold = 128

    def binarize_rgb(self, value):
        _, binary_image = cv2.threshold(self.original_img, value, 255, cv2.THRESH_BINARY)
        self.altered_img = binary_image

        cv2.imshow(self.named_threshold, self.altered_img)

    def binarize_gray(self, value):
        gray_image = cv2.cvtColor(self.original_img, cv2.COLOR_RGB2GRAY)
        _, binary_image = cv2.threshold(gray_image, value, 255, cv2.THRESH_BINARY)
        self.altered_img = binary_image

        cv2.imshow(self.named_threshold, self.altered_img)

    def run_threshold(self):
        cv2.namedWindow(self.named_threshold, cv2.WINDOW_NORMAL)

        if self.type_threshold == 'binarize_rgb':
            def on_trackbar_change(value):
                self.binarize_rgb(value)

            cv2.createTrackbar("Threshold", self.named_threshold, self.threshold, 255, on_trackbar_change)

        elif self.type_threshold == 'binarize_gray':
            def on_trackbar_change(value):
                self.binarize_gray(value)

            cv2.createTrackbar("Threshold", self.named_threshold, self.threshold, 255, on_trackbar_change)

        while True:
            cv2.imshow(self.named_threshold, self.altered_img)
            tecla = cv2.waitKey(1) & 0xFF

            if tecla == 27:
                break

            if tecla == ord('s'):
                cv2.destroyWindow(self.named_threshold)
                return self.altered_img

        cv2.destroyAllWindows()
