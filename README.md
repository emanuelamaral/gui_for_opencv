# Projeto de Processamento de Imagens com OpenCV e Interface Gráfica

Este projeto em Python utiliza OpenCV para processamento de imagens e oferece uma interface gráfica para visualizar e aplicar diversos filtros em uma imagem. A interface exibe duas imagens: a original à esquerda e a imagem modificada à direita.

## Sobre o trabalho

- Disciplina: OP63I-CC8 - Processamento de Imagens e Reconhecimento de Padrões
- Turma: 2023/2 - 8° Período
- Professor: Pedro Luiz de Paula Filho

## Pré-requisitos e Instalação no Linux

### Python (versão recomendada: 3.11 ou superior)

A maioria das distribuições Linux já vem com o Python instalado. Para verificar se o Python está instalado, abra o terminal e digite:

`python3 --version`

Se não estiver instalado, você pode instalá-lo usando o gerenciador de pacotes da sua distribuição. Por exemplo, no Ubuntu/Debian:

`
sudo apt-get update
sudo apt-get install python3
`

No Arch Linux:

`
sudo pacman -Sy python
`


### PyCharm (ou qualquer outra IDE de sua escolha)

Você pode baixar o PyCharm diretamente do site oficial da JetBrains (https://www.jetbrains.com/pycharm/download/) ou, se preferir, pode usar o gerenciador de pacotes da sua distribuição para instalar a versão Community


#### Ubuntu/Debian:

`
sudo snap install pycharm-community --classic
`

#### Arch Linux:

`
sudo pacman -Sy pycharm-community
`

## Pré-requisitos e Instalação no Windows

### Python (versão recomendada: 3.11 ou superior)

1. Baixe o instalador Python para Windows no site oficial (https://www.python.org/downloads/windows/).

2. Execute o instalador e marque a opção "Adicionar o Python X.Y ao PATH" durante a instalação, onde X.Y é a versão do Python (por exemplo, 3.11).

### PyCharm (ou qualquer outra IDE de sua escolha)

1. Baixe o instalador do PyCharm Community ou Professional do site oficial da JetBrains (https://www.jetbrains.com/pycharm/download/).


## Requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

- OpenCV
- Matplotlib
- Pillow
- Numpy
- OS

Você pode instalá-las usando pip:

```bash
pip install opencv-python matplotlib pillow numpy
```

## Utilização

1. Execute o script `frame_menu.py`.
2. Pressione o botão "Carregar Imagem" para selecionar uma imagem para processamento.
3. Para aplicar os filtros (exceto conversões), pressione a tecla "S".
4. Use os botões "Apagar", "Salvar Imagem" e "Gerar Histograma" para executar as respectivas ações.

### Botões

- **Carregar Imagem:** Permite selecionar uma imagem para ser carregada na aplicação.
- **Apagar:** Limpa as imagens exibidas.
- **Salvar Imagem:** Salva a imagem modificada em um arquivo.
- **Gerar Histograma:** Gera e exibe o histograma da imagem modificada.

### Atalhos

- **S:** Aplica os efeito selecionados na imagem.
- **ESC:** Sai da tela de aplicação de efeito

### Imagens
![Screenshot_20231010_142931](https://github.com/emanuelamaral/gui_for_opencv/assets/105809178/c1e7c592-9c28-4c3e-a7ee-af4b6aef0ec3)
![Screenshot_20231010_143304](https://github.com/emanuelamaral/gui_for_opencv/assets/105809178/fd93e9bb-b5fe-4f79-9c77-2f6cfaa7cffa)

