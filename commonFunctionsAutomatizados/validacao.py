from .captura import *
from time import sleep
from pyautogui import click, press, hotkey, write, doubleClick, rightClick, size
from pyperclip import copy, paste
import keyboard
from datetime import datetime
import xml.etree.ElementTree as ET
from os import mkdir, path, makedirs
from tkinter import messagebox, Toplevel, ttk, Tk, IntVar, LEFT
from shutil import copy as copyImage
from .lib import *


def nao_existe_registro(texto):
    hotkey("shift", "backspace")  # Limpa o campo
    copy("")  # Limpa área de transferência

    press("f12")  # Busca geral
    keyboard.write(texto)

    sleep(1)

    hotkey("ctrl", "c")
    check = paste()

    return check == ""


def valida_grid(registroAValidar, coordenadaAClicar, validacao, posicaoARemover=""):
    copy("")

    if (
        registroAValidar != ""
        and registroAValidar != " nota"
        and registroAValidar != "tudo"
    ):
        press("f12")
        sleep(0.5)
        keyboard.write(registroAValidar)  # Procura pelo registroAValidar
        sleep(0.6)

    if type(coordenadaAClicar) == list:  # Eh uma coordenadaAClicar
        if registroAValidar == "tudo":
            clicaDireito(coordenadaAClicar[0], coordenadaAClicar[1])
        else:
            clicaEsquerdo(coordenadaAClicar[0], coordenadaAClicar[1])

    elif coordenadaAClicar == "centroDireito":  # Copiar tuudo
        largura, altura = size()
        coordenadas_centro = (largura // 2, altura // 2)
        coords = coordenadas_centro
        clicaDireito(coords[0], coords[1])  # Clica no centro
    else:  # Eh uma string Clica Centro
        largura, altura = size()
        coordenadas_centro = (largura // 2, altura // 2)
        coords = coordenadas_centro
        clicaEsquerdo(coords[0], coords[1])  # Clica no centro
        hotkey("ctrl", "c")

    sleep(0.75)
    press("t")  # Copia tudo
    sleep(0.4)

    content = paste()
    sleep(0.4)

    try:
        content = content.split("\r")  # Divide entre labels e valores
        content.pop(0)  # Retira os labels

        aux = []
        for _ in content:
            aux += _.split("\t")

        if posicaoARemover != -1:
            for indx in posicaoARemover:
                aux.pop(indx)

    except IndexError:
        res = messagebox.askyesno(
            "IErro ao validar o GRID!",
            f"As informações parecem estar divergentes, por favor confira manualmente:\nEsperado:\n{validacao}\n\nCapturado:\n{aux}\n\nDeseseja CONTINUAR a execução do código?",
        )
        if res:
            clicaCentro()
            return False
        # messagebox.showerror('Erro na validação do grid', f'Ocorreu um erro em código, entre em contato com Eric!')
        return True

    # adicionar_log(f'Validacao = {(validacao)}')
    # adicionar_log(f'Capturado = {(aux)}')

    chk = aux == validacao

    if registroAValidar != "nota":
        if not chk:
            res = messagebox.askyesno(
                "Erro ao validar o GRID!",
                f"As informações parecem estar divergentes, por favor confira manualmente:\nEsperado:\n{validacao}\n\nCapturado:\n{aux}\n\nDeseseja CONTINUAR a execução do código?",
            )
            if res:
                chk = True  # Continua
                clicaCentro()

    return not chk


def substitui_imagem(modulo):

    try:
        (
            makedirs(
                rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\Imagens\{teste['teste']['versao']}\{maquina['nome']}\{modulo['pasta']}"
            )
            if not path.exists(
                rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\Imagens\{teste['teste']['versao']}\{maquina['nome']}\{modulo['pasta']}"
            )
            else True
        )
        copyImage(
            rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\captura.png",
            rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\Imagens\{teste['teste']['versao']}\{maquina['nome']}\{modulo['pasta']}\{modulo['imagem']}.png",
        )
        return False
    except Exception as err:
        print(f"Erro ao copiar a nova imagem: {err}")
        messagebox.showerror("Erro ao copiar a nova imagem", err)
        return True


def captura_imagem_naoexistente(inicio, fim):

    top, left = calcular_xy(inicio)
    bottom, right = calcular_xy(fim)

    width = right - left
    height = bottom - top
    captura = screenshot(region=(int(top), int(left), int(height), int(width)))

    # Verifica se a captura foi bem-sucedida
    if captura is None:
        print("Erro ao capturar a imagem.")
        return False

    captura.save(
        rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\captura.png"
    )
    cap = cv2.imread(
        rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\captura.png"
    )


def custom_dialog():
    # Cria um root temporário e esconde-o
    temp_root = Tk()
    temp_root.withdraw()  # Esconde a janela principal temporária

    result = IntVar(value=3)

    def salvar_continuar():
        result.set(0)
        dialog.destroy()

    def salvar_parar():
        result.set(1)
        dialog.destroy()

    def nao_salvar_continuar():
        result.set(2)
        dialog.destroy()

    def nao_salvar_parar():
        result.set(3)
        dialog.destroy()

    # Criando a janela de diálogo personalizada
    dialog = Toplevel(temp_root)
    dialog.title("As imagens não conferem")
    dialog.geometry("400x150")
    dialog.grab_set()  # Foca na janela de diálogo até que o usuário interaja

    # Rótulo com a mensagem
    label = ttk.Label(
        dialog,
        text="As imagens NÃO conferem!\nDeseja salvar a nova imagem e continuar a execução do teste?",
    )
    label.pack(pady=20)

    # Botões personalizados
    btn1 = ttk.Button(dialog, text="Salvar e\nContinuar", command=salvar_continuar)
    btn1.pack(side=LEFT, padx=10, pady=10)

    btn2 = ttk.Button(dialog, text="Salvar e\nParar", command=salvar_parar)
    btn2.pack(side=LEFT, padx=10, pady=10)

    btn3 = ttk.Button(
        dialog, text="Não Salvar e\nContinuar", command=nao_salvar_continuar
    )
    btn3.pack(side=LEFT, padx=10, pady=10)

    btn4 = ttk.Button(dialog, text="Não Salvar e\nParar", command=nao_salvar_parar)
    btn4.pack(side=LEFT, padx=10, pady=10)

    # Aguardando a ação do usuário
    dialog.wait_window()  # Pausa a execução até que a janela seja fechada

    temp_root.destroy()  # Destroi o root temporário após o uso
    return result.get()


def imagens_diferentes(modulo, coordenada_a_ignorar=(0, 0, 0, 0)):

    # Se nao existir a pasta, cria a pasta e salva a imagem
    if not path.exists(
        rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\Imagens\{teste['teste']['versao']}\{maquina['nome']}\{modulo['pasta']}"
    ):
        makedirs(
            rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\Imagens\{teste['teste']['versao']}\{maquina['nome']}\{modulo['pasta']}"
        )

    if not path.exists(
        rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\Imagens\{teste['teste']['versao']}\{maquina['nome']}\{modulo['pasta']}\{modulo['imagem']}.png"
    ):
        captura_imagem_naoexistente(modulo["inicio"], modulo["fim"])
        if substitui_imagem(modulo):
            return True
        return False

    check = captura_imagem(
        modulo["inicio"],
        modulo["fim"],
        modulo["pasta"],
        modulo["imagem"],
        coordenada_a_ignorar,
    )

    # Se existir a pasta mas nao a imagem salva a imagem
    if modulo["pasta"] == "campos":
        return not check  # Iguais
    else:
        if check:  # Iguais
            return False

    # São diferentes
    # adicionar_log(f'ERRO - Imagem {modulo['pasta']}\\{modulo['imagem']} não confere!')

    res = custom_dialog()
    sleep(1)

    if res == 0:  # Salva Continua
        substitui_imagem(modulo)
        clicaCentro()  # clica no centro da tela
        sleep(0.5)
        return False

    elif res == 1:  # Salva Para
        substitui_imagem(modulo)
        return True

    elif res == 2:  # Nao Salva Continua
        clicaCentro()  # clica no centro da tela
        sleep(0.5)
        return False

    elif res == 3:  # Nao Salva Para
        return True
    else:
        messagebox.showerror("Opcao inválida!", "Opção inválida! Abortando teste")
        return True


def adicionar_log_DESCONTINUADO(texto):
    data_hora_atual = datetime.now().strftime("%d/%m/%Y - %H:%M")

    log_formatado = f"[{data_hora_atual}] \n{texto}\n\n"

    mkdir("Logs/") if not path.exists("Logs/") else True
    with open("./Logs/log.txt", "a") as arquivo_log:
        arquivo_log.write(log_formatado)


def valida_visualizacao_xml(
    tag, valorTag
):  # <uTrib> {UN e CX } <cEAN> {SEM GTIN e EAN de cada produto}
    # Obter o XML da área de transferência
    xml_string = paste()

    # Verificar se o XML não está vazio
    if xml_string.strip() == "":
        print("Nenhum XML encontrado na área de transferência.")
        return True

    # Analisar o XML
    xml_string = xml_string[2:]
    xml_string = xml_string.replace("-", "")
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        print("Erro ao analisar o XML:", e)
        return True

    # Definir o namespace
    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

    # Encontrar o valor dentro da tag <uTrib>
    tag = root.find(f".//nfe:det/nfe:prod/nfe:{tag}", ns)

    if tag is not None:  # Encontrou
        if tag.text != valorTag:
            return True
    return False


def verifica_estoque_alterado(venda):
    maximizar_janela("Neo - #empresa1")
    sleep(4)
    entra_na_tela("sp001")  # Tela Produtos
    sleep(0.3)
    press("insert")  # Sai do filtro
    sleep(0.5)

    for prod in venda["produtos"]:
        hotkey("shift", "backspace")
        if valida_grid(prod["produto"], "centroDireito", prod["validacao"], [18]):
            # messagebox.showerror('Erro - Estoque Porduto - ' + prod['produto'], 'Esperado: ' + str(prod['validacao']))
            return True

    press("esc")

    return False
