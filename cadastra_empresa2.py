from _conf import *
# def cadastra_logradouro(logradouro):
#     escreve(logradouro['tipo'], 1)
#     escreve(logradouro['logradouro'], 1)
#     press('insert')
#     sleep(0.5)
# def cadastra_bairro(bairro):
#     escreve(bairro, 1)
#     press('insert')
#     sleep(0.5)
    
# def cadastra_municipio(municipio): JA CADASTRADO NO CONF
#     escreve(municipio['municipio'], 1)
#     escreve(municipio['pais'], 1)
#     press('insert')
#     sleep(0.5)
def valida_cadastro_inicial():
    copy('')
    sleep(0.5)
    hotkey('ctrl', 'c')
    sleep(0.5)
    return paste()
def cadastra_pessoa_municipio_logradouro(pessoa):
    sleep(2)
    escreve(pessoa['tipoPessoa'], 1)
    escreve(pessoa['documento'], 1)
    escreve(pessoa['tipoIE'], 1)
    escreve(pessoa['IE'], 1)
    escreve(pessoa['nome'], 1)
    escreve(pessoa['nomeUsual'], 1)
    escreve(pessoa['cep'], 1)
    entrar_combo() # Entra no logradouro
    novo() # Novo logradouro
    cadastra_logradouro(pessoa['logradouro'])
    sleep(0.5)
    if valida_cadastro_inicial() == '': return True # Nao foi criado
    seleciona() # Seleciona o logradouro criado
    sleep(0.5)
    escreve(pessoa['numero'], 1)
    escreve(pessoa['complemento'], 1)
    entrar_combo() # Entra no bairro
    novo() # Novo bairro
    cadastra_bairro(pessoa['bairro'])
    if valida_cadastro_inicial() == '': return True # Nao foi criado
    seleciona() # Seleciona o logradouro criado
    sleep(0.5)
    escreve(pessoa['caixaPostal'], 1)
    sleep(0.7)
    escreve(pessoa['municipio']['municipio'], 1)
    sleep(0.5)
    escreve(pessoa['telefone'], 1)
    escreve(pessoa['celular'], 1)
    escreve(pessoa['email'], 1)
    for tp in pessoa['tipo']: # Se eh cliente e fornecedor
        if tp:
            press('space')
        press('enter')
    sleep(0.5)
    escreve(pessoa['observacao'], 1)
    press('insert')
    # TODO Valida se a pessoa fdoi gerada correramente
    
    return False # Nao ocorreu nenhum erro
def cadastra_pessoa_empresa(pessoa):
    sleep(2)
    escreve(pessoa['tipoPessoa'])
    escreve(pessoa['documento'])
    escreve(pessoa['tipoIE'])
    escreve(pessoa['IE'])
    escreve(pessoa['nome'])
    escreve(pessoa['nomeUsual'])
    escreve(pessoa['cep'])
    escreve(pessoa['logradouro']['logradouro'])
    sleep(0.5)
    escreve(pessoa['numero'])
    escreve(pessoa['complemento'])
    escreve(pessoa['bairro'])
    sleep(0.5) # Vai para caixa postal
    escreve(pessoa['caixaPostal'])
    sleep(0.5)
    escreve(pessoa['municipio']['municipio'])
    sleep(0.5)
    escreve(pessoa['telefone'])
    escreve(pessoa['celular'])
    escreve(pessoa['email'])
    for tp in pessoa['tipo']: # Se eh cliente e fornecedor
        if tp:
            press('space')
        press('enter')
    sleep(0.5)
    escreve(pessoa['observacao'])
    press('insert')
    # TODO Valida se a pessoa fdoi gerada correramente
    
    return False # Nao ocorreu nenhum erro
def cadastra_empresa(empresa): # TODO ADICIONAR O CERTIFICADO DIGIAL A PARTIR DA TELA PRINCIPAL DO TESTE
    
    sleep(0.5)
    escreve(empresa['certificado'])
    
    return False
    escreve(empresa['cnae'])
    escreve(empresa['desmembramentoCNAE'])
    escreve(empresa['servicoPrestado'])
    escreve(empresa['codTribMun'])
    escreve(empresa['inscricaoMunicipal'])
    sleep(1)
    press('insert') # Salva
    sleep(1)
    # Valida se foi criado a empresa
    if valida_cadastro_inicial() == '': return True # Nao foi criado
    press('f5')
    sleep(6) # Entra no sistema
    return False # Criou
    
empresa = {
    'certificado': '626C48514C286B9B',
}

cadastra_empresa(empresa)