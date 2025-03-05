import tkinter as tk
from tkinter import messagebox, scrolledtext, DISABLED, NORMAL, END
import socket
import sys
import threading
from os import mkdir
from os.path import join, dirname, exists
from subprocess import run, CalledProcessError
from keyboard import add_hotkey
from pyautogui import click, size, hotkey
from traceback import format_exception
from time import sleep
from commonFunctionsAutomatizados import *
from _opcoes import opcoes, smoke
from commonFunctionsAutomatizados._dados import teste as test
import commonFunctionsAutomatizados.timeelapsed as te
import ctypes
import re

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

current_line = 1
theme = 0

def reset_timer():
    global running, time_elapsed
    running = False
    time_elapsed = 0
    label_time_elapsed.config(text="00:00:00")


def configuracao_inicial():
    """Inicia o teste selecionado e configura a interface de usuário adequadamente."""
    test["teste"] = {
        "nome": "Neo",
        "index": 0,
        "versao": "2.55",
        "nomeExe": "AutomatizadoNeo",
    }

    """Obtém o endereço IP e nome da máquina e preenche os campos correspondentes."""
    try:
        host_name = socket.gethostname()
        endereco_ip = socket.gethostbyname(host_name)
        maquina["ip"] = endereco_ip
        maquina["nome"] = host_name

        entry_ip.insert(0, endereco_ip)
        entry_nome.insert(0, host_name)
        # entry_ip["state"] = DISABLED
        # entry_nome["state"] = DISABLED
    except socket.error as e:
        messagebox.showerror(
            "Erro IP",
            f"Erro ao obter o endereço IP/Nome da máquina: {e}\nPor favor, insira manualmente.",
        )

    print(f'Olá, {maquina["nome"]}!')


def limpa():
    """Limpa o conteúdo do widget de texto de saída."""
    global current_line
    text_output.config(state=NORMAL)
    text_output.delete("1.0", END)
    text_output.config(state=DISABLED)
    current_line = 1


def cria_pasta():
    base_dir = rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Automatizados\{test["teste"]["nomeExe"]}\Imagens"
    if not exists(base_dir):  # Se nao existir a pasta Imagens, cria
        mkdir(base_dir)

    dir_imagens_versao = join(base_dir, test["teste"]["versao"])
    if not exists(dir_imagens_versao):  # Se nao existir a pasta Imagem/Versao, cria
        mkdir(dir_imagens_versao)

    dir_imagens_maquina = join(dir_imagens_versao, maquina["nome"])
    if not exists(
        dir_imagens_maquina
    ):  # Se nao existir a pasta Imagem/Versao/Maquina, cria
        # Caso existir uma versao anterior com imagem, copia para a versao atual
        if (
            copia_pasta_imagem_versao_anterior(
                teste=test["teste"]["nomeExe"],
                versaoAtual=test["teste"]["versao"],
                maquina=maquina["nome"],
            )
            == False
        ):  # Nao foi possivel copiar
            mkdir(dir_imagens_maquina)


def encontrar_indice(nome):
    for index, item in enumerate(opcoes):
        if item[0] == nome:
            return index
    return None


def iniciar():

    te.start_timer()  
    global app
    global main_window

    test["etapa"] = {
        "nome": comboBox_inicio.get(),
        "index": encontrar_indice(comboBox_inicio.get()),
    }

    """if int(test["etapa"]['index']) == 0:
        caminho_banco = entry_banco.get()
        caminho_banco = caminho_banco.replace('\"', '').strip()

        response, msg = rodar_comando_banco(caminho_banco)
        if not response:
            print(f'Comando executado com erro! - {msg}')
        else:
            print('Comando executado com sucesso!')"""

    cria_pasta()

    click_center()
    limpa()

    # Iniciar o teste em uma nova thread
    threading.Thread(target=lambda: smoke(teste["etapa"]["index"], insere_mensagem, step)).start()


def parar():
    """Interrompe o teste em andamento."""
    hotkey("ctrl", "shift", "esc")
    test["forcaCancelaExecucao"] = True
    te.stop_timer()
    messagebox.showinfo(
        "Parando Teste",
        "Aguarde a finalização dessa etapa ou bloqueie seu computador para parar imediatamente...",
    )


def forcarFechar():
    """Força o fechamento dos processos relacionados ao teste."""
    for processo in ["python.exe", "AutomatizadoNeo.exe"]:
        try:
            run(
                ["taskkill", "/IM", processo, "/F"],
                capture_output=True,
                text=True,
                check=True,
            )
        except CalledProcessError:
            pass


def atalhos():
    """Configura os atalhos de teclado para o aplicativo."""
    add_hotkey("delete", forcarFechar)
    add_hotkey("alt", parar)


def redirect_output_to_widget(text_widget):
    """Redireciona a saída padrão para o widget de texto."""

    # Checa se o widget de texto é None
    if text_widget is None:
        print("O widget de texto é None. A saída não será redirecionada.")
        return

    class WidgetLogger:
        def __init__(self, widget):
            self.widget = widget

        def write(self, text):
            self.widget.config(state=NORMAL)
            self.widget.insert(END, text)
            self.widget.config(state=DISABLED)
            self.widget.see(END)

        def flush(self):
            pass

    sys.stdout = WidgetLogger(text_widget)
    sys.stderr = WidgetLogger(text_widget)

    # Define o tratamento de exceções
    sys.excepthook = lambda exc_type, exc_value, exc_traceback: handle_exception(
        text_widget, exc_type, exc_value, exc_traceback
    )


def handle_exception(text_widget, exc_type, exc_value, exc_traceback):
    """Trata exceções não capturadas e exibe no widget de texto."""
    text_widget.config(state=NORMAL)
    traceback_text = "".join(format_exception(exc_type, exc_value, exc_traceback))
    text_widget.insert(END, traceback_text)
    text_widget.config(state=DISABLED)
    text_widget.see(END)


def insere_mensagem(msg, check=1):
    global current_line
    text_output.config(state=NORMAL)
    text_output.see(END)

    if msg[0] == "➤":
        # Insira a mensagem e colora de #EFB237 (amarelo)
        text_output.insert(END, f"{msg}")
        text_output.config(state=DISABLED)
        change_color(msg)
        te.root.update()
        return

    # Limpa a linha anterior
    start_index = text_output.index(f"{current_line}.0")
    end_index = text_output.index(f"{current_line}.end")
    text_output.delete(start_index, end_index)

    # Insere a mensagem e colora de verde se for ✔, de vermelho se for ✘
    text_output.insert(END, f"{msg}\n")
    text_output.config(state=DISABLED)
    change_color(msg)
    te.root.update()
    current_line += 1


def change_color(msg):
    global current_line
    chk = msg[0]

    start_index = text_output.index(f"{current_line}.0")
    end_index = text_output.index(f"{current_line}.end")
    tag_name = f"line_{current_line}_tag"
    text_output.tag_configure(
        tag_name,
        foreground="green" if chk == "✔" else "red" if chk == "✘" else "#c98e16",
    )
    text_output.tag_add(tag_name, start_index, end_index)


def step(val):
    """Atualiza a barra de progresso e o rótulo de porcentagem."""
    num = len(opcoes)
    porcent = round((val * 100) / num, 2)
    progress["value"] = porcent
    porcentagem["text"] = f"{porcent}%"


def click_center():
    """Simula um clique no centro da tela."""
    largura, altura = size()
    click(largura // 2, altura // 2)


def criar_interface():
    """Configura a interface gráfica principal da aplicação."""
    global  entry_ip, entry_nome, entry_banco, comboBox_inicio, text_output, progress, porcentagem, test, label_time_elapsed, style, varTheme

    WINDOW_TITLE = f"AutomatizadoNeo - {test["teste"]["versao"]}"
    ICON_PATH = join(
        dirname(__file__), "commonFunctionsAutomatizados", "_assets", "logo.ico"
    )

    # Criação da janela principal
    #te.root = tk.Tk()
    te.root = ttk.Window()
    te.root.title(WINDOW_TITLE)
    te.root.iconbitmap(ICON_PATH)
    te.root.geometry("500x470")
    te.root.resizable(False, False)
    style = ttk.Style()
    style.theme_use("cerculean")  # Tema inicial

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("testeautomatizadoneo")
    ctypes.windll.user32.LoadIconW(0, ICON_PATH)

    # Frame para ID Máquina e Nome Máquina
    configuracao = ttk.LabelFrame(te.root, text="Configuração")
    configuracao.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    label_ip = ttk.Label(configuracao, text="IP Máquina")
    label_ip.grid(row=0, column=0, padx=config["labelPadX"], sticky="w")
    entry_ip = ttk.Entry(configuracao)
    entry_ip.grid(row=1, column=0, padx=config["inputPadX"], pady=config["inputPadY"], sticky="ew")

    label_nome = ttk.Label(configuracao, text="Nome Máquina")
    label_nome.grid(row=0, column=1, padx=config["labelPadX"], sticky="w")
    entry_nome = ttk.Entry(configuracao)
    entry_nome.grid(row=1, column=1, padx=config["inputPadX"], pady=config["inputPadY"], sticky="ew")

   
    # Frame para Teste e Início
    teste = ttk.LabelFrame(te.root, text="Testes")
    teste.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    label_inicio = ttk.Label(teste, text="Início")
    label_inicio.grid(row=2, column=0, padx=config["labelPadX"], sticky="w")

    # Time Elapsed
    """label_time_elapsed = tk.Label(teste, text="00:00:00")
    label_time_elapsed.grid(row=2, column=1, padx=10, sticky="e")"""
    te.label_timer = tk.Label(teste, text="00:00:00", fg='#0480d8')
    te.label_timer.grid(row=2, column=1, padx=10, sticky="e")

    opcoesFormatadas = [x[0] for x in opcoes if x[0][0] != "_"]
    comboBox_inicio = ttk.Combobox(teste, values=opcoesFormatadas, state="readonly", style="Custom.TCombobox")
    comboBox_inicio.set(opcoesFormatadas[0])  # Valor padrao
    comboBox_inicio.grid(
        row=3,
        column=0,
        padx=config["inputPadX"],
        pady=config["inputPadY"],
        columnspan=2,
        sticky="nsew",
    )

    style.configure(
        "Custom.TCombobox",  # Nome do estilo personalizado
        fieldbackground="white",  # Cor de fundo do Combobox
    )


    # Personaliza a cor de fundo e texto selecionado
    style.map(
        "Custom.TCombobox",
        selectbackground=[("readonly", "transparent")],  # Cor de fundo do texto selecionado
        selectforeground=[("readonly", "#373A3C")],  # Cor do texto selecionado
    )


    # Frame para botões
    frame_botoes = ttk.Frame(teste)
    frame_botoes.grid(row=4, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

    btn_iniciar = ttk.Button(frame_botoes, text="Iniciar", width=13, command=iniciar)
    btn_iniciar.grid(row=0, column=0, padx=5, sticky="ew")

    btn_parar = ttk.Button(frame_botoes, text="Parar (Alt)", width=13, command=parar)
    btn_parar.grid(row=0, column=1, padx=5, sticky="ew")

    btn_forcar = ttk.Button(
        frame_botoes, text="Fechar (DEL)", width=13, command=forcarFechar
    )
    btn_forcar.grid(row=0, column=2, padx=5, sticky="ew")

    btn_limpar = ttk.Button(frame_botoes, text="Limpar", width=13, command=limpa)
    btn_limpar.grid(row=0, column=3, padx=5, sticky="ew")

    text_output = scrolledtext.ScrolledText(te.root, height=9)
    text_output.configure(font=("Mono", 10))
    text_output["state"] = DISABLED
    text_output.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    insere_mensagem('✔ ATENÇÃO!')
    insere_mensagem('✔ Certifíque-se de ter o CERTIFICADO REALTEC instalado na sua máquina!')
    insere_mensagem('✔ Tenha apenas uma instância do Neo aberta!')
    insere_mensagem(rf'✔ Qualquer dúvida acessar: \\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\FAQ.docx')

    # Barra de progresso
    progress = ttk.Progressbar(
        te.root, orient="horizontal", length=100, mode="determinate"
    )
    progress.grid(row=3, column=0, padx=10, sticky="ew")

    porcentagem = ttk.Label(te.root, text="0%", background=te.root.cget("bg"))
    porcentagem.grid(column=0, row=3, columnspan=1)

    # Rodapé
    frame_rodape = ttk.Frame(te.root)
    frame_rodape.grid(row=4, padx=10, pady=10, columnspan=2)

    # Footer
    label_footer = tk.Label(frame_rodape, text=f"Realtec © {datetime.now().year}", fg="gray")
    label_footer.grid(row=0, column=0, padx=10, sticky="s")

    # Configura o grid do LabelFrame para dividir as colunas igualmente
    configuracao.grid_columnconfigure(0, weight=1)
    configuracao.grid_columnconfigure(1, weight=1)
    configuracao.grid_rowconfigure(1, weight=1)

    teste.grid_columnconfigure(0, weight=1)
    teste.grid_columnconfigure(1, weight=1)
    teste.grid_rowconfigure(1, weight=1)

    frame_botoes.grid_columnconfigure(0, weight=1)
    frame_botoes.grid_columnconfigure(1, weight=1)
    frame_botoes.grid_columnconfigure(2, weight=1)
    frame_botoes.grid_rowconfigure(0, weight=1)

    te.root.grid_columnconfigure(0, weight=1)
    te.root.grid_columnconfigure(0, weight=1)
    # redirect_output_to_widget(text_output) #TODO Verificar real necessidade

    configuracao_inicial()
    atalhos()

    te.root.mainloop()


if __name__ == "__main__":
    criar_interface()
