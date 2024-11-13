from _conf import *


def clica_privilegio():
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        usuario = main_window.child_window(
            title="Usuário", found_index=0
        )  # Ajuste o índice conforme necessário

        contaBancaria = usuario.child_window(title="Privilégio", control_type="Pane")
        contaBancaria.click_input()

    except Exception as e:
        print(f"Erro: {e}")


def clica_replicar_para_todas_as_guias():
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        clienteClassificacao = main_window.child_window(
            title="Incluir - Cliente Classificação"
        )

        replicarParaTodasAsGuias = clienteClassificacao.child_window(
            title="Replicar para todas as guias"
        )
        replicarParaTodasAsGuias.click_input()
    except Exception as e:
        print(f"Erro: {e}")


def cadastra_marca(marca):
    sleep(1)
    novo(0.5)
    escreve(marca["marca"], 1)
    salva()

    if valida_grid('', "centroDireito", marca["validacao"]):
        return True
    press('esc')
    return False


def cadastra_classificacao_cliente(classificacoes):
    for classificacao in classificacoes:
        sleep(1)
        novo()

        escreve(classificacao["nome"], 1)

        escreve(classificacao["cobrar"], 1)

        escreve(classificacao["mensagem"], 1)

        escreve(classificacao["bloqueiaVendaAPrazo"], 1)

        escreve(classificacao["bloqueiaAtraso"], 1)

        if classificacao["bloqueiaAtraso"] != "n":
            escreve(classificacao["mensagemBloqueiaAtrasoMensagem"], 1)

        escreve(classificacao["bloqueiaLimiteCredito"], 0)

        if classificacao["bloqueiaLimiteCredito"] != "n":
            press("enter")
            escreve(classificacao["mensagemBloqueiaCreditoMensagem"], 0)

        sleep(1)
        clicaCentro()
        sleep(1.5)
        clica_replicar_para_todas_as_guias()
        sleep(1)
        salva(1)

        if valida_grid(classificacao["nome"], "centroDireito", classificacao["validacao"]):
            return True

    press('esc')
    return False


def cadastra_pessoa(pessoa):
    sleep(1.5)
    novo(2)

    escreve(pessoa["tipoPessoa"], 1)

    escreve(pessoa["documento"], 1)

    escreve(pessoa["tipoIE"], 1)

    escreve(pessoa["IE"], 1)

    escreve(pessoa["nome"], 1)

    escreve(pessoa["nomeUsual"], 1)

    escreve(pessoa["cep"], 1)

    escreve(pessoa["logradouro"]["logradouro"], 1)

    escreve(pessoa["numero"], 1)

    escreve(pessoa["complemento"], 1)

    escreve(pessoa["bairro"], 1)

    escreve(pessoa["caixaPostal"], 1)

    escreve(pessoa["municipio"]["municipio"], 1)
    sleep(0.7)
    press("enter")

    escreve(pessoa["telefone"], 1)

    escreve(pessoa["celular"], 1)

    escreve(pessoa["email"], 1)

    for tp in pessoa["tipo"]:  # Se eh cliente e fornecedor
        if tp:
            press("space")
        press("enter")

    sleep(0.5)

    escreve(pessoa["observacao"], 0)

    if pessoa["crtFornecedor"]:
        press("enter")
        escreve(pessoa["crtFornecedor"], 0)
        hotkey("shift", "tab")

    if pessoa["cliente"]:
        sleep(0.7)
        press("alt")
        sleep(1)
        press("l")  # Aba cliente
        sleep(1)

        cliente = pessoa["cliente"]

        escreve(cliente["classificacao"], 1)

        sleep(0.5)

        escreve(cliente["limiteCredito"], 1)

        escreve(cliente["formaPagamentoPadrao"], 1)

    sleep(1)
    salva(1.5)
    if valida_grid(pessoa["nome"], "centroDireito", pessoa["validacao"], [20, 21]):
        return True
    
    press('esc')
    return False


def cadastra_usuario(usuario):
    sleep(1)

    novo(1)
    escreve(usuario["usuario"], 1)

    escreve(usuario["login"], 1)

    escreve(usuario["senha"], 1)

    escreve(usuario["senha"], 1)  # Confirmar senha

    escreve(usuario["RFID"], 1)

    escreve(usuario["menuPrincipal"], 1)

    escreve(usuario["tempoLogado"], 1)

    escreve(usuario["emailAtendimento"], 1)

    sleep(0.5)
    salva(1)

    clica_privilegio()
    sleep(1)
    escreve(usuario["privilegio"], 0)
    salva(1)

    if valida_grid("", "centroDireito", usuario["validacao"]):
        return True  # Erro

    press("esc")
    sleep(0.5)
    return False


def cadastra_funcionario(funcionario):
    sleep(1)

    novo()

    escreve(funcionario["pessoa"], 1)

    escreve(funcionario["usuario"], 1)

    escreve(funcionario["cargo"], 2)

    escreve(funcionario["liberaClienteSemCredito"], 1)

    escreve(funcionario["liberaCrAtraso"], 1)

    escreve(funcionario["liberaVendaAPrazo"], 1)

    escreve(funcionario["liberaEstoqueNegativo"], 1)

    escreve(funcionario["financeiro"], 1)

    escreve(funcionario["comercial"], 1)

    salva(1)

    if valida_grid("", "centroDireito", funcionario["validacao"]):
        return True

    press("esc")
    return False


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


def cadastra_unidade(unidades):
    for unidade in unidades:
        sleep(1)
        clicaCentro()
        novo(1)
        escreve(unidade["unidade"], 1)
        escreve(unidade["simbolo"], 1)
        sleep(1)

        if unidade["permiteDecimal"] == "s":
            press("up")
        else:
            press("down")
        sleep(0.5)

        press(["enter", "enter"])
        sleep(0.5)
    if valida_grid('', "centroDireito", unidades[0]["validacao"]):
        return True
    press('esc')
    return False


def cadastra_produto(produto):

    cadastro = produto["cadastro"]
    fiscal = produto["fiscal"]

    # filtro
    sleep(1)
    escreve(cadastro["produto"])
    sleep(0.7)
    press("insert")
    sleep(1)
    novo(1)

    escreve(cadastro["barras"], 1)

    escreve(cadastro["fabricante"], 1)

    escreve(cadastro["produto"], 1)

    escreve(cadastro["marca"], 1)

    escreve(cadastro["unidade"], 1)

    escreve(cadastro["grupo"], 1)

    escreve(cadastro["subgrupo"], 1)

    escreve(cadastro["controlaEstoque"], 3)  # Vai para o valor venda

    escreve(cadastro["venda"], 1)

    press("alt")
    sleep(1)
    press("f")  # Fiscal
    sleep(0.5)
    press("tab")  # CFOP
    sleep(0.5)

    escreve(fiscal["cfop"], 1)

    escreve(fiscal["cst"], 1)

    escreve(fiscal["origem"], 1)

    escreve(fiscal["icms"], 2)  # Vai para NCM
    if fiscal["cst"] == "900":
        press("enter")

    escreve(fiscal["ncm"], 1)

    sleep(0.5)
    salva()

    if valida_grid("", "centroDireito", produto["validacao"], [18]):
        return True
    press('esc')
    return False
