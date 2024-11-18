from cadastra_empresa import cadastra_empresa
from compras import *
from financeiro import *
from parametros import parametros_gerais
from faturamento import *
from principal import *
from vendas import *
from servicos import *
from dados import *
from pyautogui import press
from time import sleep

def sair(arg=""):
    press("esc")
    sleep(0.2)


opcoes = [
    ("Cadastra Empresa", [], [empresa], cadastra_empresa),
    ("Parâmetros Gerais", ["m", "right", 'enter', 'r'], [parametrosGerais], parametros_gerais),
    ("Cadastra Usuário", ["p", "b", "u"], [usuario1], cadastra_usuario),
    ("Cadastra Funcionário", ["p", "n"], [funcionario1], cadastra_funcionario),
    ("Cadastra Município", ["p", "b", "e", "m"], [municipio1], cadastra_municipio),
    ("Cadastra Conta Movimento", ["f", "y", "n"], [[conta1, conta2]], cadastra_conta_movimento),
    ("Cadastra Classificação Cliente", ["p", "b", "l"], [[clienteClassificacao1, clienteClassificacao2]], cadastra_classificacao_cliente),
    ("Cadastra Marca", ["p", 'y', 'c'], [marca1], cadastra_marca),
    ("Cadastra Grupo", ["p", 'y', 'g'], [grupo1], cadastra_grupo),
    ("_sair", [], [], sair),
    ("Cadastra Subgrupo", ["p", 'y', 's'], [subgrupo1], cadastra_subgrupo),
    ("_sair", [], [], sair),
    ("Cadastra Unidade", ["p", 'y', 'u'], [[unidade1, unidade2]], cadastra_unidade),
    ("Cadastra Forma Pagamento", ['sv020'], [[formaPagamento2, formaPagamento3, formaPagamento4, formaPagamento5]], cadastra_forma_pagamento),
    ("Cadastra Tipo Condicional", ['sv018'], [tipoCondicional], cadastra_tipo_condicional),
    ("Cadastra Pessoa 1", ['p', 'a'], [pessoa1], cadastra_pessoa),
    ("Cadastra Pessoa 2", ['p', 'a'], [pessoa2], cadastra_pessoa),
    ("Cadastra Pessoa 3", ['p', 'a'], [pessoa3], cadastra_pessoa),
    ("Cadastra Pessoa 4", ['p', 'a'], [pessoa4], cadastra_pessoa),
    ("Cadastra Produto 1", ['p', 'p'], [produto1], cadastra_produto),
    ("Cadastra Produto 2", ['p', 'p'], [produto2], cadastra_produto),
    ("Cadastra Produto 3", ['p', 'p'], [produto3], cadastra_produto),
    ("Cadastra Serviço", ['p', 'v'], [servico1], cadastra_servico),
    ("Cadastra Equipamento", ['s', 'y', 'e'], [equipamento1], cadastra_equipamento),
    ("Cadastra Dav Estágio", ['sv073'], [davEstagio1], cadastra_dav_estagio),
    ("Cadastra Entrada Compra Manual 1", ['c', 'enter', 'enter'], [entradaCompraManual1], cadastra_entrada_compra_manual),
    ("Cadastra Entrada Compra Manual 2", ['c', 'enter', 'enter'], [entradaCompraManual2], cadastra_entrada_compra_manual),
    ("Cadastra Entrada Compra XML 1", ['c', 'right', 'enter'], [entradaCompraXML1], cadastra_entrada_compra_importacao_xml),
    ("Cadastra Entrada Compra XML 2", ['c', 'right', 'enter'], [entradaCompraXML2], cadastra_entrada_compra_importacao_xml),
    ("Validações Entrada Compra - Contas Pagar", ['f', 'right', 'enter'], [[entradaCompraManual1, entradaCompraManual2, entradaCompraXML1, entradaCompraXML2]], validacao_entrada_compra_contas_a_pagar),
    ("Validações Entrada Compra - Estoque", ['p', 'p'], [''], validacao_entrada_compra_produto),
    ("Cadastrar DAV 1", ['v', 'enter'], [dav1], cadastra_dav),
    ("Cadastrar DAV 2", ['v', 'enter'], [dav2], cadastra_dav),
    ("Validacões DAV - Contas Receber", ['f', 'enter'], [[dav1, dav2]], validacao_contas_receber),
    ("Validações DAV - Estoque", ['p', 'p'], [dav2], validacao_dav_estoque),
    ("Cadastra Orçamento", ['v', 'o', 'enter', 'enter'], [orcamento1], cadastra_orcamento),
    ("Cadastra Condicional", ['v', 'c', 'enter', 'enter'], [condicional1], cadastra_condicional),
    ("Cadastra Documento Fiscal", ['t', 'y', 'd'], [documentoFiscal1], cadastra_documento_fiscal),
    ("Cadastra Nota Fiscal", ['t', 'enter'], [notaFiscal1], cadastra_nota_fiscal),
    ("Lançamentos Avulsos - CR", ['f', 'enter'], [[contasReceber1, contasReceberMultiplasParcelas1]], cadastra_contas_receber_avulso),
    ("Lancamentos Avulsos - CP", ['f', 'right', 'enter'], [[contasPagar1, contasPagarMultiplasParcelas1]], cadastra_contas_pagar_avulso),
    ("Lançamentos Avulsos - MF", ['f', 'm'], [[lancamento1, lancamento2]], cadastra_lancamento_conta_corrente),
    ("Recebimento CR's", ['f', 'enter'] ,[recebimento1], recebe_contas_receber_paga_contas_pagar),
    ("Pagamento CP's", ['f', 'right', 'enter'], [pagamento1], recebe_contas_receber_paga_contas_pagar),
    # FIM
]


def smoke(index_inicio, insere_mensagem, step):
    global opcoes
    etapasSlice = opcoes[index_inicio:]

    step(index_inicio)

    # Ajusta o loop para começar no índice de início fornecido0
    for cont, (nomeTela, atalhos, dados, cadastro, *params) in enumerate(
        etapasSlice, start=index_inicio
    ):

        cancelaExecucao = False
        teste["forcaCancelaExecucao"] = False

        sleep(1)
        # Processamento de mensagens e entrada na tela
        if nomeTela and (nomeTela[0] != "_"):
            insere_mensagem(f"➤ {nomeTela}")
        
        if len(atalhos) > 0:
            entra_na_tela_neo(atalhos)

        # Executa cadastro se existir
        if cadastro:
            cancelaExecucao = cadastro(*dados, *params)

        # Verifica se a execução deve ser cancelada
        if cancelaExecucao or teste["forcaCancelaExecucao"]:
            insere_mensagem(f"✘ {nomeTela}", 2)
            insere_mensagem(f"\nExecução interrompida.\nErro em: {nomeTela}")
            return

        # Mensagem de sucesso
        if nomeTela and (nomeTela[0] != "_"):
            insere_mensagem(f"✔ {nomeTela}", 2)

        # Atualiza o passo
        step(cont)

    # Finalização bem-sucedida
    step(len(opcoes))
    insere_mensagem("✔ Teste Finalizado!")
    messagebox.showinfo("Finalizado com Sucesso!", "Teste Finalizado com Sucesso!")