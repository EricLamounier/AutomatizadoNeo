from _conf import *
from pyautogui import scroll

def certificado_realtec():
    try:
        app = Application(backend="uia").connect(title="Segurança do Windows", found_index=0)
        main_window = app.window(title="Segurança do Windows")

        maisOpcoes = main_window.child_window(control_type="Hyperlink", title="Mais opções")
        botaoOk = main_window.child_window(control_type="Button", title="OK")
        
        maisOpcoes.click_input()
        sleep(1)

        isOn = False
        while not isOn:
            for child in main_window.descendants():
                if child.element_info.control_type == 'Text' and 'REALTEC SISTEMAS' in child.window_text():
                    if child.is_visible():
                        sleep(0.7)
                        child.click_input(double=True)
                        sleep(0.7)
                        botaoOk.click_input()
                        isOn = True  # Encerra o loop
                        return False
                        #break
            if not isOn:
                scroll(-105)

        print("Processo concluído com sucesso.")
    except Exception as e:
        print(f"Erro: {e}")
        return True


def seleciona_certificado():
    app = Application(backend="uia").connect(title="Empresa ", found_index=0)
    main_window = app.window(title="Incluir - Empresa", found_index=0)
    
    botaoCertificado = main_window.child_window(found_index=26)
    
    rect = botaoCertificado.rectangle()
    clicaEsquerdo(rect.left + (rect.right - rect.left) // 2 + 125,rect.top + (rect.bottom - rect.top) // 2)
    
    sleep(2)
    
    return certificado_realtec()

def valida_cadastro_inicial():
    copy("")
    sleep(0.5)
    hotkey("ctrl", "c")
    sleep(0.5)
    return paste()


def cadastra_pessoa_municipio_logradouro(pessoa):
    sleep(1.5)
    escreve(pessoa["tipoPessoa"], 1)
    sleep(0.2)

    escreve(pessoa["documento"], 1)
    sleep(0.2)

    escreve(pessoa["tipoIE"], 1)

    escreve(pessoa["IE"], 1)

    escreve(pessoa["nome"], 1)

    escreve(pessoa["nomeUsual"], 1)

    escreve(pessoa["cep"], 1)

    entrar_combo()  # Entra no logradouro
    sleep(1)
    novo(1)  # Novo logradouro
    cadastra_logradouro(pessoa["logradouro"])
    sleep(0.5)
    if valida_cadastro_inicial() == "":
        return True  # Nao foi criado
    seleciona(2)  # Seleciona o logradouro criado

    escreve(pessoa["numero"], 1)

    escreve(pessoa["complemento"], 1)

    entrar_combo()  # Entra no bairro
    novo()  # Novo bairro
    cadastra_bairro(pessoa["bairro"])
    if valida_cadastro_inicial() == "":
        return True  # Nao foi criado
    seleciona(1.5)  # Seleciona o logradouro criado

    escreve(pessoa["caixaPostal"], 1)

    escreve(pessoa["municipio"]["municipio"], 1)
    sleep(0.7)
    #press('space')
    sleep(0.5)
    press('enter')

    escreve(pessoa["telefone"], 1)

    escreve(pessoa["celular"], 1)

    escreve(pessoa["email"], 1)

    for tp in pessoa["tipo"]:  # Se eh cliente e fornecedor
        if tp:
            press("space")
        press("enter")
    sleep(0.5)

    escreve(pessoa["observacao"], 1)
    press("insert")

    return False  # Nao ocorreu nenhum erro


def cadastra_pessoa_empresa(pessoa):
    sleep(1)
    escreve(pessoa["tipoPessoa"])

    escreve(pessoa["documento"])

    escreve(pessoa["tipoIE"])

    escreve(pessoa["IE"])

    escreve(pessoa["nome"])

    escreve(pessoa["nomeUsual"])

    escreve(pessoa["cep"])

    escreve(pessoa["logradouro"]["logradouro"])
    sleep(0.5)

    escreve(pessoa["numero"])

    escreve(pessoa["complemento"])

    escreve(pessoa["bairro"])
    sleep(0.5)  # Vai para caixa postal

    escreve(pessoa["caixaPostal"])
    sleep(0.5)

    escreve(pessoa["municipio"]["municipio"],1)

    sleep(0.7)
    if "mesmoEnderecoCobranca" in pessoa: press('space')
    sleep(0.5)
    press("enter")

    sleep(0.5)

    escreve(pessoa["telefone"])

    escreve(pessoa["celular"])

    escreve(pessoa["email"])

    for tp in pessoa["tipo"]:  # Se eh cliente e fornecedor
        if tp:
            press("space")
        press("enter")
    sleep(0.5)

    escreve(pessoa["observacao"])
    salva(0.5)

    return False  # Nao ocorreu nenhum erro


def cadastra_empresa(empresa): 

    sleep(1)
    novo()  # Novo

    entrar_combo()  # Entra no cadastro de pessoa

    novo()  # Nova pessoa
    if cadastra_pessoa_municipio_logradouro(empresa["pessoa"]):
        return True  # Erro
    sleep(1.5)
    if valida_cadastro_inicial() == "":
        return True  # Nao foi criado

    seleciona(0.5)  # Seleciona a pessoa criada (empresa)

    escreve(empresa["perfilInformante"], 1)

    escreve(empresa["crt"], 1)

    escreve(empresa["tipoAtividade"], 1)

    escreve(empresa["enquadramentoFederal"], 1)

    entrar_combo()  # Entra no cadastro de pessoa = Reponsavel Legal
    novo(1)
    if cadastra_pessoa_empresa(empresa["responsavelLegal"]):
        return True
    sleep(1)
    seleciona(0.5)

    if seleciona_certificado(): return True
    sleep(1)
    press('enter')

    # escreve(empresa["cnae"])

    # escreve(empresa["desmembramentoCNAE"])

    # escreve(empresa["servicoPrestado"])

    # escreve(empresa["codTribMun"])

    # escreve(empresa["inscricaoMunicipal"], 1)

    press("insert")  # Salva

    sleep(1.5)

    # Valida se foi criado a empresa
    if valida_cadastro_inicial() == "":
        return True  # Nao foi criado

    clicaCentro()
    press("f5")
    clicaCentro()
    clicaCentro()
    clicaCentro()
    clicaCentro()
    clicaCentro()
    sleep(0.5)
    sleep(10)  # Entra no sistema
    return False  # Criou
