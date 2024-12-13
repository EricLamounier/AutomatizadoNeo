from _conf import *

def clica_situacao_filtro(tela, campoAClicar, timeout=1):
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        # Obter a janela do filtro
        telaAtual = main_window.window(title=tela)

        # Acessar diretamente o grupo "Situação"
        situacao_group = telaAtual.child_window(title="Situação")

        # Tentar encontrar e clicar no controle "campoAClicar" dentro do grupo "Situação"
        situacao_child = situacao_group.child_window(title=campoAClicar)

        # Clicar diretamente no controle sem verificações extras
        situacao_child.click_input()
    except Exception as e:
        print(f"Erro ao tentar clicar no botão: {e}")

def clica_variacao():
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        telaProduto = main_window.child_window(
            title="Alterar - Entrada Compra ", found_index=0
        )
        variacao_pane = telaProduto.child_window(title="Variação", control_type="Pane")
        variacao_pane.click_input()
    
    except Exception as e:
        print(f"Erro: {e}")

def clica_atualizar_ncm_do_produto_com_ncm_do_xml(tela, campoAClicar, timeout=1):
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        telaAtual = main_window.window(title=tela)

        ncm = telaAtual.child_window(title=campoAClicar)
        ncm.click_input()

    except Exception as e:
        print(f"Erro: {e}")

def clica_frete():
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        entradaCompra = main_window.child_window(title="Incluir - Entrada Compra ")
        cont = 0
        for child in entradaCompra.descendants():
            if child.element_info.control_type == "Pane":
                cont += 1
                if cont == 14:
                    child.click_input()
                    break
    except Exception as e:
        print(f"Erro: {e}")

def cadastra_entrada_compra_manual(compra):
     
    principal = compra["principal"]
    itens = compra["itens"]
    financeiro = compra["financeiro"]
    sleep(0.5)

    press("insert")  # Sai do filtro
    sleep(0.8)
    novo(3)

    escreve(principal["chaveNFe"])

    escreve(principal["numero"])

    escreve(principal["serie"])

    escreve(principal["tipoDocumento"], 5)

    escreve(principal["cfop"])

    escreve(principal["fornecedor"])

    escreve(principal["crt"])

    escreve(principal["funcionario"])

    escreve(principal["formaPagamento"])

    escreve(principal["frete"])
    sleep(0.8)
    press("enter")  # Salva principal
    sleep(1.5)

    # Itens
    for produto in itens["produtos"]:
        escreve(produto["produtoID"])
        escreve(produto["cfop"])
        escreve(produto["cst"], 2)
        escreve(produto["quantidade"])
        escreve(produto["unitario"], 1)
        escreve(produto["desconto"], 2)

        if produto["cst"] != "103":  # Campos habilitados
            escreve(produto["redBCIMCS"], 1)
            escreve(produto["ICMS"], 6)
        else:
            escreve(produto["ICMS"], 2)

        press("enter")  # Incluir
        sleep(0.7)

    sleep(1)
    if valida_grid("", "centroDireito", itens["validacao"]):
        return True
    sleep(0.5)

    clica_frete()

    sleep(1)
    escreve(compra["frete"], 3)  # Inclui

    # Seguro
    escreve(compra["seguro"], 3)  # Inclui

    # Outras
    escreve(compra["outras"], 3)  # Inclui
    sleep(0.5)
    press("esc")
    
    moveTo(10, 10) # Move o mouse para fora do botao frete
    sleep(2)

    modulo = {
        "pasta": "compras",
        "imagem": compra["imagem"],
        "inicio": "450x700",
        "fim": "1498x820",
    }
    if imagens_diferentes(modulo):
        return True
    sleep(0.5)

    clica_estoque("Incluir - Entrada Compra ", "Estoque")
    sleep(1)
    press("enter")  # Financeiro
    sleep(1.5)

    press(["enter", "enter", "enter", "enter", "enter"])  # Gera parcelas
    sleep(1)

    financeiro["validacao"][1] = obter_data(1)
    try:  # GAMBIARRA PARA A ENTRADA COMPRA 2
        financeiro["validacao"][7] = obter_data(2)
    except IndexError:
        pass
    if valida_grid("tudo", [957, 617], financeiro["validacao"]):
        return True
    sleep(0.5)

    press("insert")
    sleep(1)
    press("esc")  # Tela de consulta
    sleep(1)

    compra["validacao"][2] = compra["validacao"][3] = obter_data(0)
    if valida_grid(compra["validacao"][0], "centroDireito", compra["validacao"]):
        return True
    press('esc')
    return False

def cadastra_entrada_compra_importacao_xml(compra=""):
     
    validacoes = compra["validacoes"]
    produtos = compra["itens"]["produtos"]
    sleep(1)
    novo(1)
    hotkey("alt", "l")
    sleep(1.5)
    CAMINHO_XML_LOCAL = compra["xml"]
    write(CAMINHO_XML_LOCAL)
    sleep(1.5)
    press("enter")
    sleep(1)
    press("s")  # Sim
    sleep(5)

    rang = 3
    if compra["cfopPrevio"]:
        rang = 4
    sleep(0.7)

    for _ in range(rang):
        hotkey("shift", "tab")  # Emissao
    sleep(0.5)
    press("h")  # Data de hoje
    sleep(0.8)

    press(["enter", "enter"])  # CFOP
    escreve(compra["cfop"], 1)

    escreve(compra["fornecedor"], 1)

    escreve(compra["funcionario"], 1)

    escreve(compra["formaPagamento"], 2)
    sleep(2.5)

    validacao1 = validacoes["validacaoAposImportar"]
    if valida_grid("", "centroDireito", validacao1):
        return True

    # Produtos
    sleep(0.5)
    press(["left", "left", "left", "left", "left"])  # Precaucao
    sleep(0.5)

    for produto in compra["itens"]["produtos"]:

        if produto["vinculaOuExclui"]:  # Vincula
            press(["right", "right"])  # Codigo primeiro produto
            sleep(0.8)
            escreve(produto["produtoID"], 1)
            hotkey(["shift", "tab"])
            sleep(0.5)

            if isinstance(produto["edita"], dict):  # Se for um dicionario
                edita = produto["edita"]
                press("f3")  # Edita
                sleep(1)

                escreve(edita["cfop"], 1)

                escreve(edita["cst"], 1)

                escreve(edita["quantidade"], 1)

                escreve(edita["unitario"], 1)

                escreve(edita["desconto"], 1)
                
                click(calcular_xy(793,387))
                
                if produto["marcaNCM"]:
                    clica_atualizar_ncm_do_produto_com_ncm_do_xml(
                        "Alterar - Item do XML",
                        "Atualizar NCM do Produto com NCM do XML",
                    )
                    sleep(0.3)

            salva(1)
            press("down")  # Proximo
            sleep(1)
        else:  # Exclui
            press("f4")
            sleep(0.5)
            press("s")
            sleep(0.8)

    validacao2 = validacoes["validacaoAposEditarProdutosNaImportacao"]
    if valida_grid("", "centroDireito", validacao2):
        return True

    sleep(0.5)
    modulo = {
        "pasta": "compras",
        "imagem": compra["imagemRodapeXMLTotalXML"],
        "inicio": "449x733",
        "fim": "1471x817",
    }
    if imagens_diferentes(modulo):
        return True
    sleep(0.5)

    press("alt")
    sleep(1)
    press("s")
    sleep(1.5)

    modulo = {
        "pasta": "compras",
        "imagem": compra["imagemRodapeXMLTotalItens"],
        "inicio": "449x733",
        "fim": "1471x817",
    }
    if imagens_diferentes(modulo):
        return True
    sleep(0.5)

    press("insert")  # Exportar
    sleep(1)
    press("s")  # Total difere SIM

    sleep(5)  # Entrada compra

    validacao3 = validacoes["validacaoProdutosDentroDaEntradaCompra"]
    if valida_grid("", "centroDireito", validacao3):
        return True

    sleep(1)
    modulo = {
        "pasta": "compras",
        "imagem": compra["imagemRodapeEntradaCompra"],
        "inicio": "450x700",
        "fim": "1498x820",
    }
    if imagens_diferentes(modulo):
        return True
    sleep(1.5)

    clicaEsquerdo(890, 309)
    clicaEsquerdo(890, 309)

    press("alt")
    sleep(0.3)
    press("i")  # Aba Itens
    sleep(0.5)

    # Caso tenha produto com estoque
    for produto in produtos:
        if isinstance(produto["grade"], dict):
            clicaCentro()
            hotkey("shift", "backspace")
            press("f12")
            sleep(0.3)
            keyboard.write(produto["nome"])
            sleep(1)
            press("f3")  # Edita o produto com grade
            sleep(0.5)
            clica_variacao()            
            sleep(0.5)

            for variacao in produto["grade"]["variacoes"]:
                escreve(variacao["quantidade"], 1)
                escreve(variacao["barras"], 4)
                sleep(0.5)
            sleep(0.5)

            if valida_grid("", "centroDireito", produto["grade"]["validacao"]):
                return True
            press("insert")  # Sai
            sleep(0.5)
            press("enter")  # Incluir
            sleep(0.7)

    clica_estoque("Alterar - Entrada Compra ", "Estoque")
    sleep(1)
    press("enter")  # Financeiro
    sleep(0.5)
    press("s")  # Total da nota difere
    sleep(2)

    press(["enter", "enter", "enter", "enter", "enter"])  # Gera parcelas
    sleep(1)

    validacao4 = validacoes["validacaoFinanceiro"]
    validacao4[1] = obter_data(1)
    if valida_grid("tudo", [957, 617], validacao4):
        return True
    sleep(0.5)

    press("insert")
    sleep(1)
    press("esc")
    sleep(0.5)
    press("esc")  # Tela de consulta XML
    sleep(1)
    press('esc')
    return False

def valida_entrada_compra_importacao_xml(compra):
    sleep(1)
    press("insert")  # Sai do filtro
    sleep(0.5)

    validacao = compra["validacao"]
    dataAtual = obter_data(0)

    validacao[2] = validacao[3] = dataAtual
    if valida_grid(compra["numero"], "centroDireito", validacao):
        return True
    return False

def valida_custo_estoque_ncm_produto_entrada_compra(produto):
    sleep(3)
    # Aba Cadastro
    modulo = {
        "pasta": "compras",
        "imagem": produto["imagemCadastro"],
        "inicio": "504x362",
        "fim": "1498x820",
    }

    if imagens_diferentes(modulo):
        return True
    
    press('alt')
    sleep(1)
    press('f')
    sleep(2.5)
    
    # Aba Fiscal
    modulo["imagem"] = produto["imagemFiscal"]
    
    if imagens_diferentes(modulo):
        return True
    
    press('esc')
    press('enter')
    sleep(1.5)
    return False

def valida_contas_pagar(contasPagar):

    cont = 1
    datasHoje = contasPagar["indicesData"]["hoje"]
    datasFuturas = contasPagar["indicesData"]["futuras"]

    for idx in datasHoje:
        contasPagar["validacao"][idx] = obter_data(0)

    for idx in datasFuturas:
        contasPagar["validacao"][idx] = obter_data(cont)
        cont += 1

    if valida_grid(contasPagar["valor"], "centroDireito", contasPagar["validacao"]):
        return True

    return False

def validacao_entrada_compra_contas_a_pagar(compras):
    sleep(1.5)
    press('insert') # Sai do filtro
    sleep(1.5)

    for compra in compras:
        if valida_contas_pagar(compra['contasPagar']): return True
        hotkey('shift', 'backspace')
    press('esc')
    return False

def validacao_entrada_compra_produto(compras=''):
     
    sleep(1.5)
    press('insert') # Sai do filtro
    sleep(1.5)

    produtos = [
        {
            'nome': '#produto1',
            'imagemCadastro': 'validacaoEstoqueCadastroProduto1',
            'imagemFiscal': 'validacaoEstoqueFiscalProduto1'
        },
        {
            'nome': '#produto2',
            'imagemCadastro': 'validacaoEstoqueCadastroProduto2',
            'imagemFiscal': 'validacaoEstoqueFiscalProduto2'
        },
        {
            'nome': '#produto3',
            'imagemCadastro': 'validacaoEstoqueCadastroProduto3',
            'imagemFiscal': 'validacaoEstoqueFiscalProduto3'
        }
    ]

    for produto in produtos:
        hotkey('shift', 'backspace')
        keyboard.write(produto['nome'])
        sleep(0.6)
        press('f3')
        if valida_custo_estoque_ncm_produto_entrada_compra(produto): return True
    press('esc')
    return False