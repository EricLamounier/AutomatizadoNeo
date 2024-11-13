from .lib import *


def sair(arg=""):
    press("esc")
    sleep(0.2)


def smoke(index_inicio, insere_mensagem, step):
    global opcoes

    etapasSlice = opcoes[index_inicio:]

    step(index_inicio + 0.23)

    # Ajusta o loop para começar no índice de início fornecidoo
    for cont, (nomeTela, tela, dados, cadastro, *params) in enumerate(
        etapasSlice, start=index_inicio
    ):
        cancelaExecucao = False

        # Processamento de mensagens e entrada na tela
        if nomeTela:
            insere_mensagem(f"➤ {nomeTela}")
        if tela:
            entra_na_tela(tela)

        # Executa cadastro se existir
        if cadastro:
            cancelaExecucao = cadastro(*dados, *params)

        # Verifica se a execução deve ser cancelada
        if cancelaExecucao or teste["forcaCancelaExecucao"]:
            insere_mensagem(f"✘ {nomeTela}", 2)
            insere_mensagem(
                f"\nExecução interrompida.\nErro em: {tela.upper()} - {nomeTela}"
            )
            return

        # Mensagem de sucesso
        if nomeTela:
            insere_mensagem(f"✔ {nomeTela}", 2)

        # Atualiza o passo
        step(cont)

    # Finalização bem-sucedida
    step(len(opcoes))
    insere_mensagem("✔ Teste Finalizado!")
    messagebox.showinfo("Finalizado com Sucesso!", "Teste Finalizado com Sucesso!")
