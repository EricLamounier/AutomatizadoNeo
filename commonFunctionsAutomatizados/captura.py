import cv2
import numpy as np
from pyautogui import screenshot, size
from ._dados import maquina, teste, ipCaminhoImagensNeo
from .lib import calcular_xy


def merge_overlapping_rectangles(rectangles, padding):
    merged_rectangles = []
    for rect in rectangles:
        merged = False
        for i, existing_rect in enumerate(merged_rectangles):
            if intersect(rect, existing_rect, padding):
                merged_rectangles[i] = merge(rect, existing_rect)
                merged = True
                break
        if not merged:
            merged_rectangles.append(rect)
    return merged_rectangles


def intersect(rect1, rect2, padding):
    rect1_expanded = expand_rectangle(rect1, padding)
    rect2_expanded = expand_rectangle(rect2, padding)

    return not any(
        rect1_expanded[i] + rect1_expanded[i + 2] < rect2_expanded[i]
        or rect2_expanded[i] + rect2_expanded[i + 2] < rect1_expanded[i]
        for i in range(2)
    )


def expand_rectangle(rect, padding):
    x, y, w, h = rect
    return x - padding, y - padding, w + 2 * padding, h + 2 * padding


def merge(rect1, rect2):
    x = min(rect1[0], rect2[0])
    y = min(rect1[1], rect2[1])
    w = max(rect1[0] + rect1[2], rect2[0] + rect2[2]) - x
    h = max(rect1[1] + rect1[3], rect2[1] + rect2[3]) - y
    return x, y, w, h


def show_errors_OLD_FUNCIONANDO_BACKUP(
    previa, captura, modulo, coordenadas_a_ignorar=(0, 0, 0, 0)
):
    h, w, _ = previa.shape

    nova_largura = w * 2 + 10
    nova_imagem = np.zeros((h + 30, nova_largura, 3), dtype=np.uint8)

    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(
        nova_imagem,
        "Esperado",
        (10, h + 25),
        fonte,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        nova_imagem,
        "Capturado",
        (w + 20, h + 25),
        fonte,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    mascara_ignorar = np.zeros((h, w), dtype=np.uint8)
    mascara_ignorar[
        coordenadas_a_ignorar[1] : coordenadas_a_ignorar[3],
        coordenadas_a_ignorar[0] : coordenadas_a_ignorar[2],
    ] = 255

    nova_previa = cv2.bitwise_and(previa, previa, mask=~mascara_ignorar)
    nova_captura = cv2.bitwise_and(captura, captura, mask=~mascara_ignorar)
    diff_media = np.mean(np.abs(nova_captura - nova_previa))
    tolerancia_erro = 0  #

    # print(f'{modulo} - {round(diff_media, 4)} de erro | max = {tolerancia_erro}\n')
    if modulo == "assinatura":
        if diff_media < tolerancia_erro:  # Menor que a tolerancia
            return True

    if (
        diff_media > tolerancia_erro and modulo.lower() != "campos"
    ):  # Se for DIFERENTE e o modulo das imgs nao ser campos
        highlight_differences(previa, captura, nova_captura)
        nova_imagem[:h, :w, :] = nova_previa
        nova_imagem[:h, w + 10 : w * 2 + 10, :] = nova_captura

        cv2.namedWindow("Imagens diferentes!", cv2.WINDOW_NORMAL)
        cv2.resizeWindow(
            "Imagens diferentes!", nova_imagem.shape[1], nova_imagem.shape[0]
        )

        cv2.setWindowProperty("Imagens diferentes!", cv2.WND_PROP_TOPMOST, 1)

        cv2.imshow("Imagens diferentes!", nova_imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if diff_media > tolerancia_erro:
        return False  # Diferente
    return True  # Iguais


def show_errors(previa, captura, modulo, coordenadas_a_ignorar=(0, 0, 0, 0)):
    h, w, _ = previa.shape

    # Criação da imagem de comparação
    nova_largura = w * 2 + 10
    nova_imagem = np.zeros((h + 30, nova_largura, 3), dtype=np.uint8)

    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(
        nova_imagem,
        "Esperado",
        (10, h + 25),
        fonte,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        nova_imagem,
        "Capturado",
        (w + 20, h + 25),
        fonte,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    mascara_ignorar = np.zeros((h, w), dtype=np.uint8)
    mascara_ignorar[
        coordenadas_a_ignorar[1] : coordenadas_a_ignorar[3],
        coordenadas_a_ignorar[0] : coordenadas_a_ignorar[2],
    ] = 255

    # Verifica se as imagens têm o mesmo tamanho; se não, exibe uma mensagem de erro e redimensiona a captura
    if previa.shape != captura.shape:
        # print("As imagens não têm o mesmo tamanho. Redimensionando a imagem capturada...")
        captura = cv2.resize(
            captura, (previa.shape[1], previa.shape[0])
        )  # Redimensiona para o tamanho da 'previa'

    nova_previa = cv2.bitwise_and(previa, previa, mask=~mascara_ignorar)
    nova_captura = cv2.bitwise_and(captura, captura, mask=~mascara_ignorar)
    diff_media = np.mean(np.abs(nova_captura - nova_previa))
    tolerancia_erro = 0  # Ajuste o valor da tolerância conforme necessário

    # print(f'{modulo} - {round(diff_media, 4)} de erro | max = {tolerancia_erro}\n')
    if modulo == "assinatura":
        if diff_media < tolerancia_erro:  # Menor que a tolerância
            return True

    if (
        diff_media > tolerancia_erro and modulo.lower() != "campos"
    ):  # Se for DIFERENTE e o modulo das imgs não for 'campos'
        highlight_differences(previa, captura, nova_captura)
        nova_imagem[:h, :w, :] = nova_previa
        nova_imagem[:h, w + 10 : w * 2 + 10, :] = nova_captura

        cv2.namedWindow("Imagens diferentes!", cv2.WINDOW_NORMAL)
        cv2.resizeWindow(
            "Imagens diferentes!", nova_imagem.shape[1], nova_imagem.shape[0]
        )

        cv2.setWindowProperty("Imagens diferentes!", cv2.WND_PROP_TOPMOST, 1)

        cv2.imshow("Imagens diferentes!", nova_imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if diff_media > tolerancia_erro:
        return False  # Diferente
    return True  # Iguais


def highlight_differences(previa, capturada, resultado):
    if previa is None or capturada is None or previa.shape != capturada.shape:
        print("Erro ao carregar ou comparar as imagens.")
        return

    transparency = 1
    padding = 3

    diff = cv2.absdiff(previa, capturada)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangles = [cv2.boundingRect(contour) for contour in contours]
    merged_rectangles = merge_overlapping_rectangles(rectangles, padding)

    for rect in merged_rectangles:
        x, y, w, h = [max(0, val) for val in rect]
        w = min(capturada.shape[1] - x, w)
        h = min(capturada.shape[0] - y, h)

        # Adiciona um buffer ao redor do retângulo
        x -= padding
        y -= padding
        w += 2 * padding
        h += 2 * padding

        resultado[y : y + h, x : x + w, 2] = (
            resultado[y : y + h, x : x + w, 2] * (1 - transparency) + 255 * transparency
        )


def calculate_xy(coordenada):
    screen_width, screen_height = size()
    x, y = map(int, coordenada.split("x"))
    x = (screen_width / 2) + (x - 960)
    y = (screen_height / 2) + (y - 540)
    return x, y


def captura_imagem(inicio, fim, modulo, imagem, coordenadas_a_ignorar):

    top, left = calcular_xy(inicio)
    bottom, right = calcular_xy(fim)

    width = right - left
    height = bottom - top

    captura = screenshot(region=(int(top), int(left), int(height), int(width)))

    # Verifica se a captura foi bem-sucedida
    if captura is None:
        print("Erro ao capturar a imagem.")
        return False

    captura.save(
        rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\captura.png"
    )
    cap = cv2.imread(
        rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\captura.png"
    )

    imagem_previa = cv2.imread(
        rf"\\{ipCaminhoImagensNeo}\Users\ebotelho\Desktop\Automatizados\{teste['teste']['nomeExe']}\Imagens\{teste['teste']['versao']}\{maquina['nome']}\{modulo}\{imagem}.png"
    )

    return show_errors(imagem_previa, cap, modulo, coordenadas_a_ignorar)
