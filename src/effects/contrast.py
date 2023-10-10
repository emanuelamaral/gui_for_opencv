import cv2
import numpy as np


class Contrast:
    def __init__(self, img, named_filter):
        self.imagem_alterada = np.copy(img)
        self.imagem_original = np.copy(img)
        self.named_filter = named_filter
        self.final_value = 0

        self.contrast_value = 100  # Valor inicial

    def apply_contrast(self):
        self.imagem_alterada = cv2.convertScaleAbs(self.imagem_original, alpha=self.contrast_value / 100.0, beta=0)
        self.final_value = 0
        cv2.imshow(self.named_filter, self.imagem_alterada)

    def contrast_callback(self, value):
        self.contrast_value = value
        self.apply_contrast()

    def run_contrast(self, img=None):
        cv2.namedWindow(self.named_filter, cv2.WINDOW_NORMAL)

        def on_trackbar_change(value):
            self.contrast_callback(value)

        cv2.createTrackbar("Contraste", self.named_filter, self.contrast_value, 200, on_trackbar_change)

        while True:
            cv2.imshow(self.named_filter, self.imagem_alterada)
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == 27:  # Tecla 'Esc' para sair
                break
            if tecla == ord('s'):
                cv2.destroyWindow(self.named_filter)
                return self.imagem_alterada.copy(), self.final_value

        cv2.destroyAllWindows()