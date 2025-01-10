from _conf import *

def clica_desconto_nota_fiscal():
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        notaFiscal = main_window.child_window(
            title="Incluir - Nota Fiscal - (Ambiente de Homologação)", found_index=0
        )  # Ajuste o índice conforme necessário

        for cont, child in enumerate(notaFiscal.descendants()):
            if child.element_info.control_type == 'Pane' and cont == 14:
                child.click_input()
                break

    except Exception as e:
        print(f"Erro: {e}")

def clica_incluir_nota_fiscal():
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        contaMovimento = main_window.child_window(title="Incluir - Nota Fiscal - (Ambiente de Homologação)", found_index=0)  # Ajuste o índice conforme necessário

        for cont, child in enumerate(contaMovimento.descendants()):
            if child.element_info.control_type == 'Pane' and child.window_text() == 'Incluir':
                child.click_input()
                break
    except Exception as e:
        print(f"Erro: {e}")

def cadastra_documento_fiscal(documento):
    sleep(1)
    novo(1)
    moveTo(10,10)
    escreve(documento["serie"], 1)
    escreve(documento["expiracao"], 1)
    escreve(documento["numInicial"], 1)
    escreve(documento["especie"], 1)
    sleep(1)
    #escreve(documento["relatorio"], 1) TA DANDO UM ERRO MUITO LOUCO QUE NAO SEI PORQUE ACONTECE #GAMBIARRA
    press("down")
    sleep(1)
    salva(0.8)

    if valida_grid("", "centroDireito", documento["validacao"]):
        return True
    sleep(0.5)
    press('esc')
    return False

def cadastra_nota_fiscal(notaFiscal):
     
    sleep(1.5)
    press('insert')
    sleep(1.5)
    novo(8)

    escreve(notaFiscal['documentoFiscal'], 1)
    escreve(notaFiscal['numeroFiscal'], 5)
    escreve(notaFiscal['cfop'], 1)
    escreve(notaFiscal['pessoa'], 1)
    escreve(notaFiscal['funcionario'], 1)
    escreve(notaFiscal['formaPagamento'], 1)
    escreve(notaFiscal['finalidade'], 1)
    escreve(notaFiscal['situacaoDocumento'], 1)
    escreve(notaFiscal['tipoAtendimento'], 1)
    escreve(notaFiscal['consumidorFinal'], 1)
    escreve(notaFiscal['intermediador'], 2) # Salva

    sleep(2)
    press('n') # Primeira nota do mes
    sleep(2) # Aba produtos

    for produto in notaFiscal['produtos']:
        escreve(produto['produto'], 3)
        #escreve(produto['cfop'], 1)
        #escreve(produto['csp'], 1)
        escreve(produto['quantidade'], 1)
        escreve(produto['unitario'], 1)
        clica_incluir_nota_fiscal()
        sleep(1.5)
    sleep(1)
    if valida_grid('', 'centroDireito', notaFiscal['validacaoProdutos']): return True

    clica_desconto_nota_fiscal()
    sleep(0.5)
    escreve(notaFiscal['desconto'])
    salva(2.5)

    if valida_grid('', 'centroDireito', notaFiscal['validacaoProdutosDesconto']): return True
    sleep(1)
    modulo = {
        "pasta": "notafiscal",
        "imagem": "imagemRodapeNotaFiscal",
        "inicio": "433x673",
        "fim": "1485x785",
    }
    if imagens_diferentes(modulo):
        return True

    salva(1)

    press('esc')
    sleep(1)

    notaFiscal['validacao'][2] = obter_data(0)
    if valida_grid('', 'centroDireito', notaFiscal['validacao']): return True

    press('esc')
    return False