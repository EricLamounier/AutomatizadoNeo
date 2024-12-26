from _conf import *

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

    escreve(fiscal["icms"], 1)

    if fiscal["nfce"] != "":
        escreve(fiscal["nfce"], 2)
    else:
        press("enter")

    if fiscal["cst"] == "900":
        press("enter")

    escreve(fiscal["ncm"], 1)

    sleep(0.5)
    salva()

    if valida_grid("", "centroDireito", produto["validacao"], [18]):
        return True
    press('esc')
    return False
