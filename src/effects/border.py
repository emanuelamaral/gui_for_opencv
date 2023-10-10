import cv2
import numpy as np


class Border:
    def __init__(self, img, named_border, type_border):
        self.altered_image = np.copy(img)
        self.original_image = np.copy(img)
        self.named_border = named_border
        self.type_border = type_border
        self.final_value = 0

        self.upper_threshold_canny = 50
        self.bottom_threshold_canny = 150

    def canny_border_upper(self, valor):
        self.upper_threshold_canny = valor
        self.update_canny_border()

    def canny_border_bottom(self, valor):
        self.bottom_threshold_canny = valor
        self.update_canny_border()

    def update_canny_border(self):
        edges = cv2.Canny(self.original_image, self.bottom_threshold_canny, self.upper_threshold_canny, apertureSize=3, L2gradient=False)
        self.altered_image = edges
        self.final_value = f"{self.bottom_threshold_canny}, {self.upper_threshold_canny}"
        cv2.imshow(self.named_border, self.altered_image)

    def laplace_border(self, laplace_threshold):
        # Aplica o operador Laplace para detectar as bordas
        laplacian_edges = cv2.Laplacian(self.original_image, cv2.CV_64F)
        # Aplica um limite (threshold) ao resultado do operador Laplace
        self.altered_image = cv2.convertScaleAbs(laplacian_edges)
        _, self.altered_image = cv2.threshold(self.altered_image, laplace_threshold, 255, cv2.THRESH_BINARY)
        self.final_value = laplace_threshold

        cv2.imshow(self.named_border, self.altered_image)

    def run_border(self):
        cv2.namedWindow(self.named_border, cv2.WINDOW_NORMAL)

        if self.type_border == "canny":
            def on_upper_threshold_change(valor):
                self.canny_border_upper(valor)

            def on_bottom_threshold_change(valor):
                self.canny_border_bottom(valor)

            cv2.createTrackbar("Limiar Superior Canny", self.named_border, self.upper_threshold_canny, 255, on_upper_threshold_change)
            cv2.createTrackbar("Limiar Inferior Canny", self.named_border, self.bottom_threshold_canny, 255, on_bottom_threshold_change)

        elif self.type_border == "laplace":
            def on_laplace_threshold_change(valor):
                self.laplace_border(valor)

            cv2.createTrackbar("Limiar Laplace", self.named_border, 0, 255, on_laplace_threshold_change)

        while True:
            cv2.imshow(self.named_border, self.altered_image)
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == 27:
                break
            if tecla == ord('s'):
                cv2.destroyWindow(self.named_border)
                return self.altered_image, self.final_value

        cv2.destroyAllWindows()

