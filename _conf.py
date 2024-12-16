from commonFunctionsAutomatizados import *
from pywinauto import Application
from pywinauto.mouse import click as pyWinClick
app = None
main_window = None

def cadastra_logradouro(logradouro):
    escreve(logradouro["tipo"], 1)

    escreve(logradouro["logradouro"], 1)
    press("insert")
    sleep(0.5)


def cadastra_bairro(bairro):
    escreve(bairro, 1)
    press("insert")
    sleep(0.5)


def cadastra_municipio(municipio):
    sleep(1)
    novo()

    escreve(municipio["municipio"], 1)
    escreve(municipio["pais"], 1)
    salva()

    if valida_grid(municipio["municipio"], "centroDireito", municipio["validacao"]):
        return True

    press("esc")
    return False


def cadastra_forma_cobranca(formaCobranca):
    sleep(1)
    novo(1)

    escreve(formaCobranca["cobranca"], 1)
    escreve(formaCobranca["tipo"], 1)
    escreve(formaCobranca["vencimento"], 1)
    escreve(formaCobranca["cobrancapdvnfcedavrapido"], 1)
    salva()

    if valida_grid(
        '', "centroDireito", formaCobranca["validacao"]
    ):
        return True
    return False


def cadastra_forma_pagamento(formasPagamentos):
    for formaPagamento in formasPagamentos:
        sleep(1)
        novo(1)
        moveTo(10,10)
        sleep(0.5)

        escreve(formaPagamento["forma"], 1)  # Nome da forma de pagamento

        escreve(formaPagamento["tipo"], 1)  # Seleciona o tipo da forma de pagamento

        if formaPagamento["qntParcela"] != "-1":  # Se parcela for habilitada
            escreve(formaPagamento["qntParcela"], 1)

        if formaPagamento["entrada"] != "-1":  # Se entrada for habilitado
            escreve(formaPagamento["entrada"], 1)

        if formaPagamento["diasEntrada"] != "-1":  # Se dias entrada for habilitado
            escreve(formaPagamento["diasEntrada"], 1)

        if formaPagamento["tipoVencimento"] != "-1":  # Se tipo vencimento for habilitado
            escreve(formaPagamento["tipoVencimento"], 1)

        if formaPagamento["tipoJuros"] != "-1":  # Se tipo juros for habilitado
            press("enter")

        if formaPagamento["juros"] != "-1":  # Se juros for habilitado
            escreve(formaPagamento["juros"], 1)

        if formaPagamento["utiliza"] != "-1":  # Se utiliza for habilitado
            escreve(formaPagamento["utiliza"], 1)

        if formaPagamento["ajusteCentavos"] != "-1":  # Se ajuste centavos for habilitado
            escreve(formaPagamento["ajusteCentavos"], 1)

        escreve(formaPagamento["desconto"], 1)  # Adiciona desconto
        sleep(0.4)

        if formaPagamento["forma"] == "a prazo":
            press("enter")
            sleep(0.4)

        escreve(formaPagamento["meioPagamento"], 0)  # Seleciona o meio de pagamento

        sleep(0.5)
        press(["enter", "enter", "enter"])
        sleep(0.2)
        escreve(formaPagamento["finalizadora"], 0)
        salva(1)

    clicaCentro()
    if valida_grid(
        '', "centroDireito", formasPagamentos[0]["validacao"]
    ):
        return True
    press('esc')
    return False


def cadastra_grupo(grupo):
    sleep(1)
    novo(0.5)
    escreve(grupo["grupo"], 1)
    salva()

    if valida_grid(grupo["grupo"], "centroDireito", grupo["validacao"]):
        return True
    return False


def cadastra_subgrupo(subgrupo):
    sleep(1)
    novo(0.5)
    escreve(subgrupo["subgrupo"], 1)
    salva()

    if valida_grid(subgrupo["subgrupo"], "centroDireito", subgrupo["validacao"]):
        return True
    return False


def pula(quantidade, timeout=0.5):
    for _ in range(quantidade):
        press("enter")
    sleep(timeout)


def entra_na_tela_neo(atalhos, rastros): # TODO MELHORAR AQUI...
    if len(atalhos) > 0:
        if len(atalhos) == 1: # Nome da tela
            sleep(0.5)
            hotkey("ctrl", "f")  # Busca
            sleep(0.5)
            keyboard.write(atalhos[0])

            press('enter')
            sleep(1)
        else: # Atalhos
            press("alt")
            for atalho in atalhos:
                sleep(0.5)
                press(atalho)
            sleep(1)
            if rastros != '':
                copy('')
                hotkey('ctrl', 'f6')
                
                if paste() != rastros:
                    press(['esc', 'esc', 'esc', 'n', 'n'])
                    sleep(0.5)
                    hotkey('ctrl', 'f')
                    write(rastros.split('-')[0])
                    press('enter')
                    sleep(1)
            

def clica_menu_auxiliar(tela):
     
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        produto = main_window.child_window(title=tela, found_index=0)

        # Iterando sobre os descendentes até encontrar o elemento na posição 134
        for cont, child in enumerate(produto.descendants(), start=1):
            try:
                if cont == 134:
                    # Obtém as coordenadas do controle e clica
                    rect = child.rectangle()
                    pyWinClick(
                        coords=(
                            rect.left + (rect.right - rect.left) // 2 - 15,
                            rect.top + (rect.bottom - rect.top) // 2,
                        )
                    )
                    break
            except Exception as e:
                print(f"Erro interno no loop: {e}")

    except Exception as e:
        print(f"Erro: {e}")

def clica_estoque(tela, campoAClicar, timeout=1):
     
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        entradaCompra = main_window.child_window(title=tela)
        estoque_button = entradaCompra.child_window(
            title=campoAClicar, control_type="Pane"
        )
        estoque_button.click_input()
    except Exception as e:
        print(f"Erro: {e}")

def clicaCentroRel(offset_y=0):
    screen_width, screen_height = size()
    center_x = screen_width / 2
    center_y = screen_height / 2
    adjusted_y = center_y + offset_y
    click(center_x, adjusted_y)
    
    
def calcular_xy(x, y):
    resolucaoX, resolucaoY = size()
    x = (resolucaoX / 2) + (x - 800)  # 800 é metade da resolução padrão 1600
    y = (resolucaoY / 2) + (y - 450)  # 450 é metade da resolução padrão 900
    
    return x, y
    
