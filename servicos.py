from _conf import *
def cadastra_informacao_equipamento(dado):
    sleep(0.4)
    novo(0.4)
    escreve(dado["dado"], 1)
    salva()

    if valida_grid("", "centroDireito", dado["validacao"]):
        return True
    return False


def cadastra_tipo_equipamento(tipo):
    novo(0.5)

    escreve(tipo["tipo"])

    escreve(tipo["genero"])

    escreve(tipo["habilitarIndicador"])

    escreve(tipo["equipamentoVinculado"])

    if tipo["equipamentoVinculado"] == "n":
        escreve(tipo["tipoMascara"])
        escreve(tipo["mascara"])

    salva(1)
    if valida_grid("", "centroDireito", tipo["validacao"]):
        return True
    return False


def cadastra_servico(servico):
    sleep(1)
    novo(1)
    cadastro = servico["cadastro"]
    fiscal = servico["fiscal"]

    escreve(cadastro["servico"], 1)
    escreve(cadastro["unidade"], 1)
    escreve(cadastro["valor"], 1)
    escreve(cadastro["codGTIN"], 1)

    escreve("0", 1)
    sleep(1)
    # Cadastra grupo serviço
    if cadastra_grupo(cadastro["grupo"]):
        return True
    seleciona()

    escreve("0", 1)
    sleep(1)
    # Cadastra subgrupo serviço
    if cadastra_subgrupo(cadastro["subgrupo"]):
        return True
    seleciona()
    sleep(1)

    escreve(fiscal["NBS"])
    escreve(fiscal["ISS"])

    salva(1.5)

    if valida_grid("", "centroDireito", servico["validacao"]):
        return True
    press('esc')
    return False


def cadastra_equipamento(equipamento):

    veiculo = equipamento["veiculo"]

    sleep(1)
    novo()

    escreve(equipamento["descricao"], 1)

    entrar_combo(1)

    if cadastra_tipo_equipamento(equipamento["tipo"]):
        return True
    seleciona()

    if equipamento["tipo"]["habilitarIndicador"] == "s":
        escreve(equipamento["identificacao"], 1)

    escreve(equipamento["cliente"], 1)

    # Guia Veiculo
    escreve(veiculo["veiculo"], 1)

    escreve(veiculo["renavam"], 1)

    escreve(veiculo["placa"], 1)

    escreve(veiculo["chassi"], 1)

    escreve(veiculo["anoFabricacao"], 1)

    escreve(veiculo["anoModelo"], 1)

    escreve(veiculo["tipoCombustivel"], 1)

    escreve(veiculo["especie"], 1)

    escreve(veiculo["tipoVeiculo"], 1)

    entrar_combo(1)
    if cadastra_informacao_equipamento(veiculo["marca"]):
        return True  # Cadastra marca
    seleciona()

    entrar_combo(1)
    if cadastra_informacao_equipamento(veiculo["modelo"]):
        return True  # Cadastra modelo
    seleciona()

    escreve(veiculo["cor"], 1)
    salva()

    if valida_grid("", "centroDireito", equipamento["validacao"]):
        return True
    press('esc')
    return False
