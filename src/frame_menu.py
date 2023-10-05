import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
from filter import Filter
from border import Border
from threshold import Threshold
from morphology import Morphology


class ManipulacaoImagemApp:
    def __init__(self, master):
        self.master = master
        self.caminho_da_imagem = None

        self.imagem_cv2 = None
        self.label_imagem_alterada = None
        self.label_imagem_original = None
        self.imagem_alterada = None

        self.conversion_effect_applied = False
        self.filter_effect_applied = False
        self.border_effect_applied = False
        self.threshold_effect_applied = False
        self.morphology_effect_applied = False
        self.conversion_effect = None
        self.filter_effect = None
        self.border_effect = None
        self.morph_effect = None
        self.threshold_effect = None

        self.resulted_image = None
        self.applied_effects = []

        master.title("Manipulação de Imagem")
        master.geometry("800x600")

        # Criar ListView à esquerda usando um Treeview
        self.list_view_effects = ttk.Treeview(master)
        self.list_view_effects.column("#0", width=250, minwidth=210)

        # ListView Para conversões de cores
        self.list_view_effects.insert("", "end", text="Converter de RGB --> GRAY", tags=("cvt_rgb_2_gray",))
        self.list_view_effects.insert("", "end", text="Converter de RGB --> XYZ", tags=("cvt_rgb_2_xyz",))
        self.list_view_effects.insert("", "end", text="Converter de RGB --> YCrCb", tags=("cvt_rgb_2_ycrcb",))
        self.list_view_effects.insert("", "end", text="Converter de RGB --> HSV", tags=("cvt_rgb_2_hsv",))
        self.list_view_effects.insert("", "end", text="Converter de RGB --> HLS", tags=("cvt_rgb_2_hls",))
        self.list_view_effects.insert("", "end", text="Converter de RGB --> CIE L*a*b*", tags=("cvt_rgb_2_cielab",))
        self.list_view_effects.insert("", "end", text="Converter de RGB --> CIE L*u*v*", tags=("cvt_rgb_2_cieluv",))

        # Atribuição de funções para as opções do ListView de conversão de cores.
        self.list_view_effects.tag_bind("cvt_rgb_2_gray", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_gray())
        self.list_view_effects.tag_bind("cvt_rgb_2_xyz", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_xyz())
        self.list_view_effects.tag_bind("cvt_rgb_2_ycrcb", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_ycrcb())
        self.list_view_effects.tag_bind("cvt_rgb_2_hsv", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_hsv())
        self.list_view_effects.tag_bind("cvt_rgb_2_hls", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_hls())
        self.list_view_effects.tag_bind("cvt_rgb_2_cielab", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_cielab())
        self.list_view_effects.tag_bind("cvt_rgb_2_cieluv", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_cieluv())

        # ListView para Filtros
        self.list_view_effects.insert("", "end", text="Filtro Median Blur", tags=("blur_median_filter", ))
        self.list_view_effects.insert("", "end", text="Filtro Gaussian Blur", tags=("blur_gaussian_filter", ))

        # Atribuição de funções para as opções do ListView filtros.
        self.list_view_effects.tag_bind("blur_median_filter", "<ButtonRelease-1>", lambda event: self.blur_median_filter())
        self.list_view_effects.tag_bind("blur_gaussian_filter", "<ButtonRelease-1>", lambda event: self.blur_gaussian_filter())

        # ListView para detector de bordas
        self.list_view_effects.insert("", "end", text="Detector de borda Canny", tags=("canny_border_detector", ))

        # Atribuição de funções para as opções do ListView de detecção de bordas
        self.list_view_effects.tag_bind("canny_border_detector", "<ButtonRelease-1>", lambda event: self.canny_border_detector())

        # ListView para threshold
        self.list_view_effects.insert("", "end", text="Threshold RGB", tags=("threshold_rgb", ))

        # Atribuição de funções para as opções de threshold
        self.list_view_effects.tag_bind("threshold_rgb", "<ButtonRelease-1>", lambda event: self.threshold_rgb())

        # ListView para Morfologias Matemáticas
        self.list_view_effects.insert("", "end", text="Erosão", tags=("morph_erosion", ))
        self.list_view_effects.insert("", "end", text="Dilatação", tags=("morph_dilatation"))

        # Atribuição de funções para as opções de morfologia matemática
        self.list_view_effects.tag_bind("morph_erosion", "<ButtonRelease-1>", lambda evet: self.morph_erosion())
        self.list_view_effects.tag_bind("morph_dilatation", "<ButtonRelease-1>", lambda evet: self.morph_dilatation())

        self.list_view_effects.pack(side="left", fill="y")

        # Cria um ListView abaixo para mostrar os filtros aplicados
        self.list_view_efeitos_aplicados = ttk.Treeview(master)
        self.list_view_efeitos_aplicados.pack(side="bottom", fill="x")

        # Criar um frame para a imagem no meio
        self.frame_imagem = tk.Frame(master)
        self.frame_imagem.pack(expand=True, fill="both")

        # Criar um frame para os botões
        self.frame_buttons = tk.Frame(master)
        self.frame_buttons.pack(side="top", pady=10)

        self.botao_carregar_imagem = tk.Button(self.frame_buttons, text="Carregar Imagem", command=self.abrir_arquivo)
        self.botao_carregar_imagem.pack(side="left", padx=10)

        self.botao_apagar_efeito = tk.Button(self.frame_buttons, text="Apagar", command=self.selecionar_filtro_para_remover)
        self.botao_apagar_efeito.pack(side="left", padx=10)

    def morph_dilatation(self):
        if not self.morphology_effect_applied and self.caminho_da_imagem:
            morphology = Morphology(self.imagem_alterada, "Dilatacao", "dilatation")
            dilatation_image = morphology.run_morphology()
            if dilatation_image is not None:
                effect_name = "Dilatação"
                self.add_effect_to_list_view_applied_effects(effect_name, "morph")
                self.morphology_effect_applied = True
                self.show_image_effect(dilatation_image)
                self.applied_effects.append(("morph", morphology))
        elif self.morphology_effect_applied:
            messagebox.showinfo("Aviso", "A morfologia já foi aplicada.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def morph_erosion(self):
        if not self.morphology_effect_applied and self.caminho_da_imagem:
            morphology = Morphology(self.imagem_alterada, "Erosao", "erosion")
            erosion_image = morphology.run_morphology()
            if erosion_image is not None:
                effect_name = "Erosão"
                self.add_effect_to_list_view_applied_effects(effect_name, "morph")
                self.morphology_effect_applied = True
                self.show_image_effect(erosion_image)
                self.applied_effects.append(("morph", morphology))
        elif self.morphology_effect_applied:
            messagebox.showinfo("Aviso", "A morfologia já foi aplicada.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def threshold_rgb(self):
        if not self.threshold_effect_applied and self.caminho_da_imagem:
            threshold_rgb = Threshold(self.imagem_alterada, "Threshold RGB", "binarize")
            binarized_image = threshold_rgb.run_threshold()
            if binarized_image is not None:
                effect_name = "Threshold"
                self.add_effect_to_list_view_applied_effects(effect_name, "threshold")
                self.threshold_effect_applied = True
                self.show_image_effect(binarized_image)
                self.applied_effects.append(("threshold", threshold_rgb))
        elif self.threshold_effect_applied:
            messagebox.showinfo("Aviso", "O Threshold já foi aplicado.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def canny_border_detector(self):
        if not self.border_effect_applied and self.caminho_da_imagem:
            canny_border = Border(self.imagem_alterada, "Canny Border", "canny")
            image_canny = canny_border.run_filter()
            if image_canny is not None:
                effect_name = "Detector de borda Canny"
                self.add_effect_to_list_view_applied_effects(effect_name, "border")
                self.border_effect_applied = True
                self.show_image_effect(image_canny)
                self.applied_effects.append(("borda", canny_border))
        elif self.border_effect_applied:
            messagebox.showinfo("Aviso", "O detector de bordas já foi aplicado.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def blur_gaussian_filter(self):
        if not self.filter_effect_applied and self.caminho_da_imagem:
            gaussian_filter = Filter(self.imagem_alterada, "Filter Gaussian", "gaussian")
            imagem_gaussian = gaussian_filter.run_filter()
            if imagem_gaussian is not None:
                effect_name = "Filtro Gaussian Blur"
                self.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.filter_effect_applied = True
                self.show_image_effect(imagem_gaussian)
                self.applied_effects.append(("filtro", gaussian_filter))
        elif self.filter_effect_applied:
            messagebox.showinfo("Aviso", "O filtro já foi aplicado.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def blur_median_filter(self):
        if not self.filter_effect_applied and self.caminho_da_imagem:
            median_filter = Filter(self.imagem_alterada, "Filter Median", "median")
            imagem_median = median_filter.run_filter()
            if imagem_median is not None:
                effect_name = "Filtro Median Blur"
                self.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.filter_effect_applied = True
                self.show_image_effect(imagem_median)
                self.applied_effects.append(("filtro", median_filter))
        elif self.filter_effect_applied:
            messagebox.showinfo("Aviso", "O filtro já foi aplicado.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def cvt_rgb_2_cieluv(self):
        if not self.conversion_effect_applied and self.caminho_da_imagem:
            imagem_cieluv = cv2.cvtColor(self.imagem_cv2, cv2.COLOR_RGB2LUV)
            effect_name = "RGB --> CIE L*u*v*"
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.conversion_effect = imagem_cieluv.copy()
            self.show_image_effect(imagem_cieluv)
            self.applied_effects.append(("conversion", imagem_cieluv))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Aviso", "A conversão já foi aplicada.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def cvt_rgb_2_cielab(self):
        if not self.conversion_effect_applied and self.caminho_da_imagem:
            imagem_cielab = cv2.cvtColor(self.imagem_cv2, cv2.COLOR_RGB2LAB)
            effect_name = "RGB --> CIE L*a*b*"
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.conversion_effect = imagem_cielab.copy()
            self.show_image_effect(imagem_cielab)
            self.applied_effects.append(("conversion", imagem_cielab))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Aviso", "A conversão já foi aplicada.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def cvt_rgb_2_hls(self):
        if not self.conversion_effect_applied and self.caminho_da_imagem:
            imagem_hls = cv2.cvtColor(self.imagem_cv2, cv2.COLOR_RGB2HLS)
            effect_name = "RGB --> HLS"
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.conversion_effect = imagem_hls.copy()
            self.show_image_effect(imagem_hls)
            self.applied_effects.append(("conversion", imagem_hls))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Aviso", "A conversão já foi aplicada.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def cvt_rgb_2_hsv(self):
        if not self.conversion_effect_applied and self.caminho_da_imagem:
            imagem_hsv = cv2.cvtColor(self.imagem_cv2, cv2.COLOR_RGB2HSV)
            effect_name = "RGB --> HSV"
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.conversion_effect = imagem_hsv.copy()
            self.show_image_effect(imagem_hsv)
            self.applied_effects.append(("conversion", imagem_hsv))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Aviso", "A conversão já foi aplicada.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def cvt_rgb_2_ycrcb(self):
        if not self.conversion_effect_applied and self.caminho_da_imagem:
            imagem_ycrcb = cv2.cvtColor(self.imagem_cv2, cv2.COLOR_RGB2YCrCb)
            effect_name = "RGB --> YCrCb"
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.conversion_effect = imagem_ycrcb.copy()
            self.show_image_effect(imagem_ycrcb)
            self.applied_effects.append(("conversion", imagem_ycrcb))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Aviso", "A conversão já foi aplicada.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def cvt_rgb_2_xyz(self):
        if not self.conversion_effect_applied and self.caminho_da_imagem:
            imagem_xyz = cv2.cvtColor(self.imagem_cv2, cv2.COLOR_RGB2XYZ)
            effect_name = "RGB --> XYZ"
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.conversion_effect = imagem_xyz.copy()
            self.show_image_effect(imagem_xyz)
            self.applied_effects.append(("conversion", imagem_xyz))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Aviso", "A conversão já foi aplicada.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def cvt_rgb_2_gray(self):
        if not self.conversion_effect_applied and self.caminho_da_imagem:
            imagem_gray = cv2.cvtColor(self.imagem_cv2, cv2.COLOR_BGR2GRAY)
            effect_name = "RGB --> GRAY"
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.conversion_effect = imagem_gray.copy()
            self.show_image_effect(imagem_gray)
            self.applied_effects.append(("conversion", imagem_gray))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Aviso", "A conversão já foi aplicada.")
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem antes de converter para escala de cinza.")

    def add_effect_to_list_view_applied_effects(self, effect_name, tag):

        if tag == "conversion":
            self.list_view_efeitos_aplicados.insert("", "end", text=effect_name, tags=("conversion", ))
        elif tag == "morph":
            self.list_view_efeitos_aplicados.insert("", "end", text=effect_name, tags=("morph",))
        elif tag == "filter":
            self.list_view_efeitos_aplicados.insert("", "end", text=effect_name, tags=("filter",))
        elif tag == "border":
            self.list_view_efeitos_aplicados.insert("", "end", text=effect_name, tags=("border",))
        elif tag == "threshold":
            self.list_view_efeitos_aplicados.insert("", "end", text=effect_name, tags=("threshold",))

    def limpar_efeitos_aplicados(self):
        # Limpa todos os itens no self.list_view_efeitos_aplicados
        for item in self.list_view_efeitos_aplicados.get_children():
            self.list_view_efeitos_aplicados.delete(item)
        self.morphology_effect_applied = False
        self.threshold_effect_applied = False
        self.border_effect_applied = False
        self.conversion_effect_applied = False
        self.filter_effect_applied = False

    def remover_filtro(self, tag_item):
        # Remove o filtro específico da lista de efeitos aplicados
        self.applied_effects = [op for op in self.applied_effects if op[0] != tag_item]

        # Reconstrói a imagem sem o filtro específico
        imagem_sem_filtro = self.imagem_cv2.copy()

        # Aplica os filtros restantes na ordem correta
        for effect_type, effect in self.applied_effects:
            if effect_type == "conversion":
                imagem_sem_filtro = effect.copy()
                self.conversion_effect_applied = False
            elif effect_type == "morph":
                imagem_sem_filtro = effect.run_morphology(imagem_sem_filtro)
                self.morphology_effect_applied = False
            elif effect_type == "filter":
                imagem_sem_filtro = effect.run_filter(imagem_sem_filtro)
                self.filter_effect_applied = False
            elif effect_type == "border":
                imagem_sem_filtro = effect.run_filter(imagem_sem_filtro)
                self.border_effect_applied = False
            elif effect_type == "threshold":
                imagem_sem_filtro = effect.run_threshold(imagem_sem_filtro)
                self.threshold_effect_applied = False

        # Atualiza a imagem alterada
        if self.label_imagem_alterada:
            self.label_imagem_alterada.destroy()
            self.resize_altered_image(imagem_sem_filtro)

        # Remove o efeito do self.list_view_efeitos_aplicados
        for item in self.list_view_efeitos_aplicados.get_children():
            item_tags = self.list_view_efeitos_aplicados.item(item)["tags"]
            if tag_item in item_tags:
                self.list_view_efeitos_aplicados.delete(item)

    def selecionar_filtro_para_remover(self):
        selected_item = self.list_view_efeitos_aplicados.selection()
        if selected_item:
            effect_text = self.list_view_efeitos_aplicados.item(selected_item)
            tag_item = str(effect_text.__getitem__("tags")[0])

            self.remover_filtro(tag_item)
        else:
            messagebox.showinfo("Aviso", "Selecione um efeito para apagar.")

    def load_image(self):
        self.imagem_cv2 = cv2.imread(self.caminho_da_imagem)
        self.imagem_cv2 = cv2.cvtColor(self.imagem_cv2, cv2.COLOR_BGR2RGB)

        self.limpar_efeitos_aplicados()
        self.show_original_image(self.imagem_cv2)
        self.resulted_image = None
        self.show_image_effect(self.imagem_cv2)

    def show_image_effect(self, img):

        if self.label_imagem_alterada:
            self.label_imagem_alterada.destroy()

        self.resize_altered_image(img)

    # Redimensiona a imagem resultante
    def resize_altered_image(self, img):
        largura_imagem = 600
        altura_imagem = 350

        imagem_redimensionada = cv2.resize(img, (largura_imagem, altura_imagem))

        self.imagem_alterada = imagem_redimensionada

        imagem_pil = Image.fromarray(imagem_redimensionada)
        imagem_tk = ImageTk.PhotoImage(image=imagem_pil)

        self.label_imagem_alterada = tk.Label(self.frame_imagem, image=imagem_tk)
        self.label_imagem_alterada.image = imagem_tk
        self.label_imagem_alterada.pack(expand=True, fill="both")

        self.frame_imagem.update_idletasks()


    def show_original_image(self, img):

        if self.label_imagem_original and self.label_imagem_alterada:
            self.label_imagem_original.destroy()
            self.label_imagem_alterada.destroy()

        largura_imagem = 600
        altura_imagem = 350
        imagem_redimensionada = cv2.resize(img, (largura_imagem, altura_imagem))

        imagem_pil = Image.fromarray(imagem_redimensionada)
        imagem_tk = ImageTk.PhotoImage(image=imagem_pil)

        self.label_imagem_original = tk.Label(self.frame_imagem, image=imagem_tk)
        self.label_imagem_original.image = imagem_tk
        self.label_imagem_original.pack(expand=True, fill="both")

        self.frame_imagem.update_idletasks()

    def abrir_arquivo(self):
        self.caminho_da_imagem = filedialog.askopenfilename()

        if self.caminho_da_imagem:
            print('Arquivo Selecionado', self.caminho_da_imagem)
            self.load_image()
        else:
            print('Nenhum arquivo selecionado')

    def run(self):
        self.master.mainloop()


# Inicializar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ManipulacaoImagemApp(root)
    app.run()
