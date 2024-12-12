import time
from playwright.sync_api import sync_playwright


def load_page(page, scroll_pause_time=2.5):
    # Função para rolar a página até o final e esperar carregar novos itens
    previous_height = page.evaluate("document.body.scrollHeight")

    while True:
        # Rola até o final da página
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(scroll_pause_time)  # Pausa para esperar o carregamento

        # Atualiza a altura da página após a rolagem
        new_height = page.evaluate("document.body.scrollHeight")

        # Verifica se chegou ao final da página
        if new_height == previous_height:
            break  # Se a altura não mudou, encerra a rolagem

        previous_height = new_height  # Atualiza a altura para a próxima iteração


def wait_load_elements(page, selector, timeout=40000):
    page.wait_for_function(
        f"() => getComputedStyle(document.querySelector('{selector}')).display === 'none'",
        timeout=timeout,
    )
