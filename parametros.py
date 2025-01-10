from _conf import *

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
        "fim": "1334x620",
    }
    if imagens_diferentes(modulo):
        return True

    clique_parametros_gerais("Faturamento")

    press("enter")  # NFe
    escreve("homol", 1)

    escreve("homol", 1)

    escreve("homol", 1)

    escreve("homol", 1)

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