from commonFunctionsAutomatizados import *
from pywinauto import Application
from pywinauto.mouse import click as pyWinClick
app = None
main_window = None

def cadastra_logradouro(logradouro):
    escreve(logradouro["tipo"], 1)

    escreve(logradouro["logradouro"], 1)
    press("insert")
    sleep(0.5)


def cadastra_bairro(bairro):
    escreve(bairro, 1)
    press("insert")
    sleep(0.5)


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

def clica_menu_auxiliar(tela):
     
    try:
        app = Application(backend="uia").connect(title="Neo - #empresateste")
        main_window = app.window(title="Neo - #empresateste")
        produto = main_window.child_window(title=tela, found_index=0)

        # Iterando sobre os descendentes até encontrar o elemento na posição 134
        for cont, child in enumerate(produto.descendants(), start=1):
            try:
                if cont == 134:
                    # Obtém as coordenadas do controle e clica
                    rect = child.rectangle()
                    pyWinClick(
                        coords=(
                            rect.left + (rect.right - rect.left) // 2 - 15,
                            rect.top + (rect.bottom - rect.top) // 2,
                        )
                    )
                    break
            except Exception as e:
                print(f"Erro interno no loop: {e}")

    except Exception as e:
        print(f"Erro: {e}")
    

    
