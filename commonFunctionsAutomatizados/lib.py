from pyautogui import (
    click,
    press,
    hotkey,
    write,
    doubleClick,
    rightClick,
    size,
    moveTo,
    size,
    FAILSAFE,
)
import keyboard
from pygetwindow import getWindowsWithTitle
from time import sleep
from os import path
from shutil import copytree
from pyperclip import copy, paste, waitForPaste
from tkinter import messagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ._dados import *

FAILSAFE = False


def novo(timeout=1):
    press("f2")
    sleep(timeout)


def salva(timeout=1):
    press("insert")
    sleep(timeout)


def editar(timeout=1):
    press("f3")
    sleep(timeout)


def excluir(timeout=1):
    press("f4")
    sleep(timeout)


def cancelar(timeout=1):
    press("f4")
    sleep(timeout)


def seleciona(timeout=1):
    press("f5")
    sleep(timeout)


def entrar_combo(time=1):
    write("0")
    press("enter")
    sleep(time)


def escreve(texto, quantidadeEnter=1):
    keyboard.write(texto)
    for enter in range(quantidadeEnter):
        press("enter")


def obter_data_OLD(qtdMes_a_mais=0):
    data_atual = datetime.now()
    nova_data = data_atual + relativedelta(months=+qtdMes_a_mais)
    nova_data_formatada = nova_data.strftime("%d/%m/%Y")
    return nova_data_formatada

from datetime import datetime
from dateutil.relativedelta import relativedelta

def obter_data(qtdMes_a_mais=0):
    data_atual = datetime.now()
    
    for _ in range(qtdMes_a_mais):
        data_atual = data_atual + relativedelta(months=+1)
    
    nova_data_formatada = data_atual.strftime("%d/%m/%Y")
    return nova_data_formatada

def obter_hora_atual():
    return datetime.now().strftime("%H:%M")

def calcular_xy(coordenada):
    screen_width, screen_height = size()
    x, y = map(int, coordenada.split("x"))
    x = (screen_width / 2) + (x - 960)
    y = (screen_height / 2) + (y - 540)
    return x, y


def clicaCentro():
    screen_width, screen_height = size()
    center_x = screen_width / 2
    center_y = screen_height / 2
    click(center_x, center_y)


def clicaEsquerdo(x, y):
    x, y = calcular_xy("x".join([str(x), str(y)]))
    click(x, y)


def clicaDireito(x, y):
    x, y = calcular_xy("x".join([str(x), str(y)]))
    sleep(0.7)
    rightClick(x, y)


def clicaEsquerdoDuplo(x, y):
    x, y = calcular_xy("x".join([str(x), str(y)]))
    doubleClick(x, y)


def maximizar_janela(title):
    try:
        window = getWindowsWithTitle(title)[0]
        sleep(0.5)
        window.activate()
        window.maximize()
        sleep(0.5)
    except IndexError:
        messagebox.showerror(
            "Janela não encontrada!", f"Certifique-se de estar com {title} aberto."
        )


def minimizar_janela(title=""):
    try:
        window = getWindowsWithTitle(title)[0]
        sleep(0.5)
        window.activate()
        window.minimize()
        sleep(0.5)
    except IndexError:
        messagebox.showerror(
            "Janela não encontrada!", f"Certifique-se de estar com {title} abertos"
        )


def copia_e_cola(texto):
    copy(texto)
    sleep(1)
    hotkey("ctrl", "c")
    sleep(0.5)
    return not paste() == ""


def entra_na_tela(tela):
    sleep(0.5)
    hotkey("ctrl", "f")  # Busca
    sleep(0.5)
    keyboard.write(tela)
    press("enter")
    sleep(1)


def copia_pasta_imagem_versao_anterior(teste, versaoAtual, maquina):
    versaoAnterior = f"{(float(versaoAtual) - 0.01):.2f}"

    caminhoImagensVersaoAnterior = rf"\\10.1.10.50\Users\ebotelho\Desktop\Automatizados\{teste}\Imagens\{versaoAnterior}\{maquina}"
    caminhoImagensVersaoAtual = rf"\\10.1.10.50\Users\ebotelho\Desktop\Automatizados\{teste}\Imagens\{versaoAtual}\{maquina}"

    if path.isdir(
        caminhoImagensVersaoAnterior
    ):  # Se tiver versao anterior e imagem salva, copia para a versao atual
        copytree(caminhoImagensVersaoAnterior, caminhoImagensVersaoAtual)
        return True

    return False
