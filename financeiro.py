from _conf import *
from pyautogui import moveTo

def clica_setinha_novo(tela, indice=31): # CR 19 CP 17
    try:
        # Conectar ao aplicativo
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")

        contaMovimento = main_window.child_window(
            title=tela, found_index=0
        )  # Ajuste o índice conforme necessário

        for cont, child in enumerate(contaMovimento.descendants()):
            if cont == indice:
                rect = child.rectangle()
                x = rect.left + (rect.right - rect.left) // 2
                y = rect.top + (rect.bottom - rect.top) // 2 + 35
                click(x, y)
                break                

    except Exception as e:
        print(f"Erro: {e}")

def clica_conta_bancaria():
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        contaMovimento = main_window.child_window(
            title="Conta Movimento", found_index=0
        )  # Ajuste o índice conforme necessário

        contaBancaria = contaMovimento.child_window(
            title="Conta Bancária", control_type="Pane"
        )
        contaBancaria.click_input()

    except Exception as e:
        print(f"Erro: {e}")

def cadastra_conta_movimento(contas):
     
    for conta in contas:
        sleep(1)
        novo(1.5)

        escreve(conta["planoDeContas"])

        escreve(conta["tipo"])

        escreve(conta["controleCheque"])

        salva(1.5)

        if valida_grid(conta["conta"], "centroDireito", conta["validacao"]): return True
        sleep(1)

        # Cadastra conta bancaria
        if conta["contaBancaria"]:  # Se houver conta bancaria
            clica_conta_bancaria()
            sleep(2)

            contaBancaria = conta["contaBancaria"]
            escreve(contaBancaria["codBanco"], 1)
            escreve(contaBancaria["municipio"], 1)
            escreve(contaBancaria["conta"], 1)
            escreve(contaBancaria["dvConta"], 1)
            escreve(contaBancaria["agencia"], 1)
            escreve(contaBancaria["dvAgencia"], 2)
            sleep(1.5)
            modulo = {
                "pasta": "financeiro",
                "imagem": "contaBancaria",
                "inicio": "635x306",
                "fim": "1300x762",
            }
            if imagens_diferentes(modulo, (326, 108, 441, 144)):
                return True
            sleep(0.5)

            press(["enter", "enter", "enter", "enter"])  # Salva e vai para a carteira

            sleep(2)

            carteira = conta["carteira"]

            escreve(carteira["numero"], 1)
            escreve(carteira["variacao"], 1)
            escreve(carteira["registro"], 1)
            escreve(carteira["aceite"], 1)
            escreve(carteira["especie"], 1)
            escreve(carteira["codigoCedente"], 1)
            escreve(carteira["digito"], 1)
            escreve(carteira["convenio"], 1)
            escreve(carteira["tipoMora"], 1)
            escreve(carteira["moraJuros"], 1)
            escreve(carteira["diasModaJuros"], 1)
            escreve(carteira["tipoMulta"], 1)
            escreve(carteira["diasProtestar"], 1)
            escreve(carteira["responsavel"], 1)
            escreve(carteira["enviaRemessa"], 1)
            escreve(carteira["localPagamento"], 1)
            escreve(carteira["numDocumento"], 1)
            escreve(carteira["instrucao1"], 1)
            escreve(carteira["instrucao2"], 1)
            escreve(carteira["relatorio"], 1)
            escreve(carteira["tipoBoletoCEF"], 1)
            escreve(carteira["ativo"], 1)
            escreve(carteira["homologada"], 1)
            escreve(carteira["tarifaPorBoleto"], 2)
            escreve(carteira["numInicialBoleto"], 1)
            escreve(carteira["numInicialRemessa"], 4)
            sleep(1)

            moveTo(10, 10)  # Move o mouse para tirar foco do campo

            sleep(1.5)

            modulo = {
                "pasta": "financeiro",
                "imagem": "carteira",
                "inicio": "635x306",
                "fim": "1300x762",
            }
            if imagens_diferentes(modulo):
                return True
            sleep(1)

            press("esc") # Sai conta bancaria
    sleep(1)
    press('esc') # sai conta movimento
    return False

### Contas Receber
def contas_receber_avulso(contasReceber):   
    novo(1.5)
    escreve(contasReceber['cliente'], 1)
    escreve(contasReceber['contaContabil'], 1)
    escreve(contasReceber['funcionario'], 4)
    escreve(contasReceber['valor'], 1)
    escreve(contasReceber['numeroDocumento'], 1)
    escreve(contasReceber['formaCobranca'], 1)
    salva(1.5)
    
    return False

def cadastra_contas_receber_avulso(contasReceber):
    sleep(1.5)
    press('insert')
    sleep(1)
    
    for CR in contasReceber:
        if CR['parcelas']: # Multi parcelas
            contas_receber_avulso_multiplas_parcelas(CR)
        else: # Normal
            contas_receber_avulso(CR)
    
    contasReceber = contasReceber[0]
    cont = 1
    datasHoje = contasReceber["indicesData"]["hoje"]
    datasFuturas = contasReceber["indicesData"]["futuras"]

    for idx in datasHoje:
        contasReceber["validacao"][idx] = obter_data(0)

    for idx in datasFuturas:
        contasReceber["validacao"][idx] = obter_data(cont)
        cont += 1
    if valida_grid('crm', 'centroDireito', contasReceber['validacao'], contasReceber['indicesHora']): return True
    press('esc')
    return False

def contas_receber_avulso_multiplas_parcelas(contasReceber):
       
    clica_setinha_novo('Contas a Receber ', 19)
    sleep(1.5)
    press('m')
    sleep(2)
    
    escreve(contasReceber['cliente'], 1)
    escreve(contasReceber['funcionario'], 3)
    escreve(contasReceber['numeroDocumento'], 1)
    escreve(contasReceber['formaCobranca'], 1)
    
    for parcela in contasReceber['parcelas']:
        pula(2)
        escreve(parcela['valor'], 2)
    
    sleep(1)
    press('alt')
    sleep(1)
    press('l') # lancamentos
    sleep(1.5)
    
    for contaContabil in contasReceber['contasContabeis']:
        escreve(contaContabil['conta'], 1)
        escreve(contaContabil['valor'], 2) 
    
    sleep(1.5)
    salva(1)
    
    press('esc')
    return False
 
### Contas Pagar
def contas_pagar_avulso(contasPagar):   
    novo(1.5)
    escreve(contasPagar['fornecedor'], 1)
    escreve(contasPagar['contaContabil'], 4)
    escreve(contasPagar['valor'], 1)
    escreve(contasPagar['numeroDocumento'], 1)
    escreve(contasPagar['documento'], 1)
    salva(1.5)
    
    return False

def contas_pagar_avulso_multiplas_parcelas(contasPagar):    
     
    clica_setinha_novo('Contas a Pagar', 17)
    sleep(1.5)
    press('m')
    sleep(2)
    
    escreve(contasPagar['fornecedor'], 3)
    escreve(contasPagar['numeroDocumento'], 1)
    escreve(contasPagar['documento'], 2)
    
    for parcela in contasPagar['parcelas']:
        pula(2)
        escreve(parcela['valor'], 2)
    
    sleep(1)
    press('alt')
    sleep(1)
    press('l') # lancamentos
    sleep(1.5)
    
    for contaContabil in contasPagar['contasContabeis']:
        escreve(contaContabil['conta'], 1)
        escreve(contaContabil['valor'], 2) 
    sleep(1.5)
    salva(1)

    return False
    
def cadastra_contas_pagar_avulso(contasPagar):
    sleep(1)
    press('insert')
    sleep(1)
    
    for CP in contasPagar:
        if CP['parcelas']: # Multi parcelas
            contas_pagar_avulso_multiplas_parcelas(CP)
        else: # Normal
            contas_pagar_avulso(CP)
            
    contasPagar = contasPagar[0]
    cont = 1
    datasHoje = contasPagar["indicesData"]["hoje"]
    datasFuturas = contasPagar["indicesData"]["futuras"]

    for idx in datasHoje:
        contasPagar["validacao"][idx] = obter_data(0)

    for idx in datasFuturas:
        contasPagar["validacao"][idx] = obter_data(cont)
        cont += 1

    if valida_grid('cpm', 'centroDireito', contasPagar['validacao']): return True
    press('esc')
    return False

### Movimento Financeiro
def lancamento_conta_corrente(lancamento):  
    novo(1.5)
    escreve(lancamento['operacao'], 1)
    escreve(lancamento['contaContabil'], 3)
    escreve(lancamento['valor'], 1)
    escreve(lancamento['numeroDocumento'], 4)

def cadastra_lancamento_conta_corrente(lancamentos): # TODO: PEGAR OS DADOS DA VALIDACAO
    sleep(2)
    escreve(lancamentos[0]['contaMovimento'])
    sleep(0.5)
    press('insert')
    sleep(1)
    
    for lancamento in lancamentos:
        lancamento_conta_corrente(lancamento)
        sleep(1.5)
    
    lancamentos = lancamentos[0]
    cont = 1
    datasHoje = lancamentos["indicesData"]["hoje"]
    datasFuturas = lancamentos["indicesData"]["futuras"]

    for idx in datasHoje:
        lancamentos["validacao"][idx] = obter_data(0)

    for idx in datasFuturas:
        lancamentos["validacao"][idx] = obter_data(cont)
        cont += 1

    if valida_grid('', 'centroDireito', lancamentos['validacao'], lancamentos['indicesHora']): return True
    press('esc')
    return False

### Recebimentos
def recebe_contas_receber_paga_contas_pagar(conta):
    sleep(1)
    press('insert')
    sleep(0.5)

    press('f7') # Receber
    sleep(3)
    
    pula(8) # Filtrar

    clicaCentro()
    clicaCentro()
    sleep(0.5)

    press('f7') # Seleciona todos
    sleep(2)

    modulo = {
        "pasta": 'financeiro',
        "imagem": conta['imagem'],
        "inicio": "1294x310",
        "fim": "1478x820",
    }
    if imagens_diferentes(modulo):
        return True
    
    salva(1)
    escreve('1')
    sleep(0.6)
    salva(2)

    relatorio = conta['relatorio']

    #Valida recibo
    press('enter') # Recibo
    sleep(2)
    for pesquisa in relatorio['valorPesquisado']:
        hotkey('ctrl', 'f') # Pesquisa no relatorio
        sleep(0.5)
        write(pesquisa)
        sleep(1)
        press('enter') # Localizar primeiro
        sleep(1)

        copy('')
        clicaCentroRel(-45)
        hotkey('ctrl', 'c')
        if paste() != '': return True # Apareceu uma mensagem de texto nao encontrado
        sleep(1.5)

    press('esc') # Sai relatorio
    sleep(1)

    press('esc') # Sai CR/CP
    sleep(1)
    press('esc') # Sai consulta
    return False
