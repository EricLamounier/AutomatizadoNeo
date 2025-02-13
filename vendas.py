from _conf import *

def clica_devolver():
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        detalhamentoCondicional = main_window.child_window(
            title="Detalhamento da Condicional ", found_index=0
        ) 
        
        devolver = detalhamentoCondicional.child_window(
            title="Devolver", control_type="Pane"
        )
        devolver.click_input()

    except Exception as e:
        print(f"Erro: {e}")
        
def clica_gerar_dav():
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        detalhamentoCondicional = main_window.child_window(
            title="Detalhamento da Condicional ", found_index=0
        ) 
        
        gerarDAV = detalhamentoCondicional.child_window(
            title="Gerar DAV", control_type="Pane"
        )
        gerarDAV.click_input()

    except Exception as e:
        print(f"Erro: {e}")

def cadastra_tipo_condicional(tipoCondicional):
    sleep(0.5)
    novo(0.5)

    escreve(tipoCondicional['tipo'], 1) 
    sleep(0.3)
    press('insert') # Salva
    sleep(0.5)

    if valida_grid('', 'centroDireito', tipoCondicional['validacao']): return True
    press('esc')
    return False

def cadastra_dav_estagio(estagio):
    sleep(0.5)
    novo(0.5)

    escreve(estagio["estagio"], 1)

    escreve(estagio["tipoVenda"], 1)

    escreve(estagio["sequencia"], 1)

    escreve(estagio["tipo"], 1)

    escreve(estagio["edita"], 1)

    escreve(estagio["geraFinanceiro"], 1)

    escreve(estagio["cancelaDocumento"], 1)

    salva()
    if valida_grid("", "centroDireito", estagio["validacao"]):
        return True
    press('esc')
    return False

def validacao_contas_receber(davs):
    sleep(0.5)
    press('insert')
    sleep(0.5)
    for dav in davs:
        contasReceber = dav['contasReceber']
        cont = 1
        datasHoje = contasReceber["indicesData"]["hoje"]
        datasFuturas = contasReceber["indicesData"]["futuras"]

        for idx in datasHoje:
            contasReceber["validacao"][idx] = obter_data(0)

        for idx in datasFuturas:
            contasReceber["validacao"][idx] = obter_data(cont)
            cont += 1
        sleep(1)
        hotkey('shift', 'backspace')
        sleep(1)
        if valida_grid(contasReceber["parcelas"], "centroDireito", contasReceber["validacao"], contasReceber['indicesHora']):
            return True
    sleep(0.7)
    press('esc')

def cadastra_orcamento(orcamento):
    sleep(1)
    press('insert') # Sai do filtro
    sleep(0.5)

    novo(1)

    pula(3)
    escreve(orcamento['funcionario'], 1)
    escreve(orcamento['frete'], 3)
    escreve(orcamento['cliente'], 6)
    sleep(0.5)

    if len(orcamento['produtos']) > 0:
        for produto in orcamento['produtos']:
            escreve(produto['quantidade'], 1)
            escreve(produto['produto'], 1)
            escreve(produto['unitario'], 1)
            escreve(produto['desconto'], 2)

    if len(orcamento['servicos']) > 0:
        press('f1')
        sleep(0.7)
        for servico in orcamento['servicos']:
            escreve(servico['quantidade'], 1)
            escreve(servico['servico'], 1)
            escreve(servico['unitario'], 1)
            escreve(servico['desconto'], 2)

    if len(orcamento['produtosNaoCadastrados']) > 0:
        press('f1')
        sleep(0.7)
        for produtosNaoCadastrado in orcamento['produtosNaoCadastrados']:
            escreve(produtosNaoCadastrado['quantidade'], 1)
            escreve(produtosNaoCadastrado['produtoNaoCadastrado'], 1)
            escreve(produtosNaoCadastrado['unitario'], 1)
            escreve(produtosNaoCadastrado['desconto'], 2)

    sleep(0.7)
    if valida_grid('', 'centroDireito', orcamento['validacao1']): return True
    sleep(1)


    press('alt')
    sleep(1)
    press('f') # Forma de pagamento
    sleep(1)
    if len(orcamento['formasPagamento']):
        for formaPagamento in orcamento['formasPagamento']:
            escreve(formaPagamento['formaPagamento'], 1)
            escreve(formaPagamento['desconto'], 1)
            if formaPagamento['entrada'] != '-1': escreve(formaPagamento['entrada'], 1)
            if formaPagamento['formaCombinada'] == '1':
                press('space')
            sleep(0.2)
            press(['enter', 'enter'])
        sleep(0.7)
        if valida_grid('', 'centroDireito', formaPagamento['validacao']): return True

    sleep(1.5)
    modulo = {
        "pasta": "orcamento",
        "imagem": "orcamentoRodape",
        "inicio": "438x661",
        "fim": "1420x786",
    }
    if imagens_diferentes(modulo):
        return True
    
    press('insert')
    sleep(0.5)
    press('esc') # Tela consulta
    sleep(1)

    orcamento['validacao2'][1] = obter_data(0)
    if valida_grid('', 'centroDireito', orcamento['validacao2']): return True

    
    app = Application(backend="uia").connect(title="Neo - #empresateste")
    main_window = app.window(title="Neo - #empresateste")
    orcamentoTela = main_window.child_window(title="Orçamento ", found_index=0)
    executar = main_window.child_window(title="Executar")
    
    gerarDAV = orcamentoTela.child_window(found_index=8)
    gerarDAV.click_input()
    sleep(1)
    press('left')
    sleep((0.5))
    press('space')
    sleep(0.5)
    executar.click_input()
    
    sleep(1.5)

    dav = orcamento['dav']
    escreve(dav['cfop'], 1)
    escreve(dav['formaPagamento'], 1)
    escreve(dav['tipoVenda'], 1)
    if dav['finalizarOrcamento'] == '0': # Desmarcar
        press('space')
        sleep(0.5)
    press('enter')
    sleep(1)

    clicaDireito(900, 600)
    sleep(0.5)
    press('m') # Marcar todos
    sleep(1.5)

    if valida_grid('', 'centroDireito', orcamento['validacao3']): return True
    sleep(1)

    press('insert') # Exporta para o DAV
    sleep(5)

    if valida_grid('', 'centroDireito', orcamento['validacao4']): return True
    sleep(0.5)

    modulo = {
        "pasta": "orcamento",
        "imagem": 'orcamentoRodapeDAV',
        "inicio": "433x673",
        "fim": "1485x785",
    }
    if imagens_diferentes(modulo):
        return True
    
    press('esc') # Volta para o orcamento
    sleep(2)

    orcamento['validacao5'][2] = orcamento['validacao5'][3] = obter_data(0)
    if valida_grid('', 'centroDireito', orcamento['validacao5']): return True

    press('esc')
    return False
from dados import *
cadastra_orcamento(orcamento1)
def cadastra_condicional(condicional):
    sleep(1)
    press('insert') # Sai do filtro
    sleep(0.5)

    novo(1)
    pula(2)

    escreve(condicional['funcionario'], 1)
    escreve(condicional['formaPagamento'], 1)
    escreve(condicional['cliente'], 1)
    escreve(condicional['tipoCondicional'], 3)

    sleep(0.5)
    for produto in condicional['produtos']:
        hotkey('shift', 'tab')
        escreve(produto['quantidade'], 1)
        escreve(produto['produto'], 1)
    sleep(1)
    if valida_grid('tudo', [961, 552], condicional['validacaoProdutos']): return True

    sleep(1)
    modulo = {
        "pasta": "condicional",
        "imagem": "condicionalRodape",
        "inicio": "560x643",
        "fim": "1416x747",
    }
    if imagens_diferentes(modulo):
        return True

    salva(1)
    press('esc') # tela de consulta

    condicional['validacao1'][5] = condicional['validacao1'][10] = obter_data()
    if valida_grid('', 'centroDireito', condicional['validacao1'], [16]): return True
    sleep(1)

    press('f7') # Detalhamento Condicional
    sleep(1)
    if valida_grid('', 'centroDireito', condicional['validacaoDetalhamentoCondicional1']): return True
    sleep(0.5)

    modulo = {
        "pasta": "condicional",
        "imagem": "condicionalDetalhamentoCondicionalRodape1",
        "inicio": "535x611",
        "fim": "1365x741",
    }
    if imagens_diferentes(modulo):
        return True
    
    clica_devolver()
    sleep(1)

    for produto in condicional['produtosDevolver']:
        escreve(produto['quantidade'], 1)
        escreve(produto['produto'], 1)
        hotkey('shift', 'tab')

    sleep(1)
    if valida_grid('', 'centroDireito', condicional['validacaoDevolucaoCondicional2']): return True
    sleep(1)

    press('esc') # Volta
    sleep(1)

    if valida_grid('', 'centroDireito', condicional['validacaoDetalhamentoCondicional2']): return True
    sleep(0.5)

    modulo = {
        "pasta": "condicional",
        "imagem": "condicionalDetalhamentoCondicionalRodape2",
        "inicio": "535x611",
        "fim": "1365x741",
    }
    if imagens_diferentes(modulo):
        return True

    clica_gerar_dav()
    sleep(1)
    dav = condicional['dav']
    escreve(dav['cfop'], 2)
    sleep(0.5)

    if valida_grid('', 'centroDireito', condicional['validacaoExportarCondicionalDav']): return True
    sleep(0.5)

    press('insert') # Exportar
    sleep(5)

    if valida_grid('', 'centroDireito', dav['validacaoGridDav']): return True
    sleep(0.5)

    modulo = {
        "pasta": "condicional",
        "imagem": "imagemRodapeDav",
        "inicio": "433x673",
        "fim": "1485x785",
    }
    if imagens_diferentes(modulo):
        return True
    sleep(0.5)
    press('esc') # Volta para o detalhamento da condicional
    sleep(2.5)

    if valida_grid('', 'centroDireito', condicional['validacaoDetalhamentoCondicional3']): return True
    sleep(1)

    modulo = {
        "pasta": "condicional",
        "imagem": "condicionalDetalhamentoCondicionalRodape3",
        "inicio": "535x611",
        "fim": "1365x741",
    }
    if imagens_diferentes(modulo):
        return True

    sleep(0.5)
    press('esc') # Tela consulta condicional
    sleep(1.5)

    condicional['validacao2'][5] = condicional['validacao2'][10] = condicional['validacao2'][12] = obter_data()
    
    if valida_grid('', 'centroDireito', condicional['validacao2'], [16,16]): return True
    sleep(1)

    press('esc')
    return False


