from _conf import *


def clique_parametros_gerais(campoAClicar, timeout=1):
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        parameters_window = main_window.child_window(
            title="Parâmetros Gerais", control_type="Window"
        )
        tree_view = parameters_window.child_window(control_type="Tree")

        principal_item = tree_view.child_window(
            title=campoAClicar, control_type="TreeItem"
        )
        principal_item.click_input(double=True)
        sleep(1.5)
    except Exception as e:
        print(f"Erro ao tentar clicar no botão: {e}")


def clique_combo(indexCampoAClicar, tela, timeout=1):
    cont = 1
    # 2.54 11
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        parametrosGerais = main_window.child_window(title=tela, found_index=0)

        for child in parametrosGerais.descendants():
            if child.element_info.control_type == "Edit":
                if cont == indexCampoAClicar:
                    child.click_input(double=True)
                    break
                cont += 1

    except Exception as e:
        print(f"Erro: {e}")


def parametros_gerais(parametros):

    sleep(6)  # Aguarda abrir
    clique_parametros_gerais("Principal")

    press(
        [
            "enter",
            "enter",
            "enter",
            "enter",
        ]
    )  # Campo Modo Preco Venda
    escreve("ambos", 1)

    escreve("sim", 1)

    escreve("medio", 1)

    escreve("todos", 1)

    sleep(3)
    modulo = {
        "pasta": "parametros",
        "imagem": "geralPrincipal",
        "inicio": "724x265",
        "fim": "1334x480",
    }
    if imagens_diferentes(modulo):
        return True

    clique_parametros_gerais("Compras")

    press("enter")  # Habilita CRT
    escreve("sim", 1)

    escreve("avisa", 1)

    escreve("avisa", 1)

    sleep(3)
    modulo = {
        "pasta": "parametros",
        "imagem": "geralCompras",
        "inicio": "724x265",
        "fim": "1334x382",
    }
    if imagens_diferentes(modulo):
        return True

    clique_parametros_gerais("Vendas")
    press(
        [
            "enter",
            "enter",
            "enter",
            "enter",
        ]
    )  # Boleto DAV
    escreve("sim", 2)

    escreve("nao", 1)

    sleep(1)
    clique_combo(15, "Parâmetros Gerais")  # Forma Cobrança
    sleep(0.5)
    entrar_combo()

    if cadastra_forma_cobranca(parametros["formaCobranca"]):
        return True
    sleep(1)
    seleciona(1)

    entrar_combo()
    if cadastra_forma_pagamento([parametros["formaPagamento"]]):
        return True
    sleep(1)
    escreve('1', 1)

    sleep(3)
    modulo = {
        "pasta": "parametros",
        "imagem": "geralVendas",
        "inicio": "724x265",
        "fim": "1334x685",
    }
    if imagens_diferentes(modulo):
        return True

    clique_parametros_gerais("Financeiro")

    press("enter")  # Tipo de Jutos
    escreve("comp", 1)

    escreve("3", 1)

    escreve("5", 1)

    escreve("10", 2)

    escreve("sim", 1)
    sleep(1)
    
    clique_combo(12, "Parâmetros Gerais")  # Cliente Padrão
    escreve("155", 1)  # Cartao a Receber

    sleep(3)
    modulo = {
        "pasta": "parametros",
        "imagem": "geralFinanceiro",
        "inicio": "724x265",
        "fim": "1334x448",
    }
    if imagens_diferentes(modulo):
        return True

    clique_parametros_gerais("Faturamento")

    press("enter")  # NFe
    escreve("homologacao", 1)

    escreve("homologacao", 1)

    escreve("homologacao", 1)

    escreve("homologacao", 1)

    sleep(3)
    modulo = {
        "pasta": "parametros",
        "imagem": "geralFaturamento",
        "inicio": "724x265",
        "fim": "1334x368",
    }
    if imagens_diferentes(modulo):
        return True

    clique_parametros_gerais("Geral")

    press("enter")  # Geral
    escreve("codigo interno", 2)

    escreve("todos", 3)

    escreve("logado")
    press("enter")

    sleep(3)
    modulo = {
        "pasta": "parametros",
        "imagem": "geralGeral",
        "inicio": "724x265",
        "fim": "1334x479",
    }
    if imagens_diferentes(modulo):
        return True

    press("insert")  # Salva
    sleep(0.5)

    copy(
        ""
    )  # Copie e cole para verificar o aparecimento da tela de Usuários do Banco de Dados
    sleep(0.5)
    hotkey("ctrl", "f6")
    sleep(0.5)
    rastro = paste()

    if rastro != "":  # Se a tela de Usuários do Banco de Dados aparecer, volte
        press("esc")
        sleep(0.5)
        press("left")
        sleep(0.5)
        press("enter")

    sleep(1)
    return False