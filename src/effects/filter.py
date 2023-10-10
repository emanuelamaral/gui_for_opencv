import cv2
import numpy as np


class Filter:
    def __init__(self, img, named_filter, type_filter):
        self.imagem_alterada = np.copy(img)
        self.imagem_original = np.copy(img)
        self.named_filter = named_filter
        self.type_filter = type_filter
        self.final_value = 0
        self.kernel_size_atual = 1
        self.sigma_atual = 0
        self.diameter = 0

    def aplicar_filtro_median(self):
        imagem_median = cv2.medianBlur(self.imagem_original, self.kernel_size_atual)
        self.imagem_alterada = imagem_median
        self.final_value = self.kernel_size_atual
        cv2.imshow(self.named_filter, self.imagem_alterada)

    def aplicar_filtro_gaussian(self):
        imagem_gaussian = cv2.GaussianBlur(self.imagem_original, (5, 5), self.sigma_atual)
        self.imagem_alterada = imagem_gaussian
        self.final_value = self.sigma_atual
        cv2.imshow(self.named_filter, self.imagem_alterada)

    def aplicar_filtro_bilateral(self):
        imagem_bilateral = cv2.bilateralFilter(self.imagem_original, self.diameter, self.diameter * 2, self.diameter / 2)
        self.imagem_alterada = imagem_bilateral
        self.final_value = self.diameter
        cv2.imshow(self.named_filter, self.imagem_alterada)

    def median_blur(self, valor):
        self.kernel_size_atual = valor if valor % 2 == 1 else valor + 1
        self.aplicar_filtro_median()

    def gaussian_blur(self, valor):
        self.sigma_atual = valor
        self.aplicar_filtro_gaussian()

    def bilateral_filter(self, valor):
        self.diameter = valor
        self.aplicar_filtro_bilateral()

    def run_filter(self, img=None):
        cv2.namedWindow(self.named_filter, cv2.WINDOW_NORMAL)

        if img is not None:
            self.aplicar_filtro_median()
            cv2.destroyWindow(self.named_filter)
            return self.imagem_alterada

        else:
            if self.type_filter == "median":
                def on_trackbar_change(valor):
                    self.median_blur(valor)

                cv2.createTrackbar("Kernel Size", self.named_filter, self.kernel_size_atual, 50, on_trackbar_change)

            if self.type_filter == "gaussian":
                def on_trackbar_change(valor):
                    self.gaussian_blur(valor)

                cv2.createTrackbar("Sigma", self.named_filter, self.sigma_atual, 50, on_trackbar_change)

            if self.type_filter == "bilateral":
                def on_trackbar_bilateral(diameter):
                    self.bilateral_filter(diameter)

                cv2.createTrackbar("Diameter", self.named_filter, self.diameter, 50, on_trackbar_bilateral)

            while True:
                cv2.imshow(self.named_filter, self.imagem_alterada)
                tecla = cv2.waitKey(1) & 0xFF
                if tecla == 27:  # Tecla 'Esc' para sair
                    break
                if tecla == ord('s'):
                    cv2.destroyWindow(self.named_filter)
                    return self.imagem_alterada, self.final_value

        cv2.destroyAllWindows()
