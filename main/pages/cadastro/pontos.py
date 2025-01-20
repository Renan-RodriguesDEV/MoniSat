import os
from main.uteis import load_page, wait_load_elements
from main.SuperClassMoni import CustomFormatter, ch, logger

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

path_cards = os.path.join(os.getcwd(), "cards")


def fill_pontos(
    page_monisat,
    ponto="",
    cidade="",
    cnpj="",
    tipo="",
    raio="",
    cliente_points=False,
    mapa=True,
    cadastrar=False,
):
    data_cadastro = {
        "ponto": ponto,
        "cidade": cidade,
        "cnpj": cnpj,
        "tipo": tipo,
        "raio": raio,
    }
    selectors = {
        "ponto": "#tablePonto > thead > tr > th:nth-child(2) > center > input",
        "cidade": "#tablePonto > thead > tr > th:nth-child(3) > center > input",
        "cnpj": "#tablePonto > thead > tr > th:nth-child(4) > center > input",
        "tipo": "#tablePonto > thead > tr > th:nth-child(5) > center > input",
        "raio": "#tablePonto > thead > tr > th:nth-child(6) > center > input",
    }
    btn_pontos = "#conteudoPagina > div > div > div > div > div > div.float-right > a:nth-child(1) > button"
    maximize_minimize = "#mapPonto > div.leaflet-control-container > div.leaflet-top.leaflet-left > div.leaflet-control-fullscreen.leaflet-bar.leaflet-control > a"
    mapa_selector = "#mapPonto"

    if cliente_points:
        page_monisat.click(btn_pontos)

    # Selecionar a opção "Todos"
    select_selector = 'select[name="tablePonto_length"]'
    page_monisat.hover(select_selector)  # Passar o mouse
    page_monisat.click(select_selector)
    page_monisat.select_option(select_selector, value="-1")
    logger.info("Selecionada a opção 'Todos' no campo select.")

    if mapa:
        page_monisat.click(maximize_minimize)
        page_monisat.wait_for_load_state("networkidle", timeout=30000)
        page_monisat.wait_for_selector(mapa_selector)
        mapa_element = page_monisat.query_selector(mapa_selector)
        mapa_element.screenshot(path=os.path.join(path_cards, "MAPA_PONTOS.png"))
        page_monisat.click(maximize_minimize)

    for key, value in data_cadastro.items():
        page_monisat.fill(selectors[key], value)
    # carrega a tabela por completa
    load_page(page_monisat)
    wait_load_elements(page_monisat, "#tablePonto_processing")
    page_monisat.wait_for_load_state("networkidle", timeout=30000)
    card = page_monisat.query_selector("#tablePonto")
    card.screenshot(path=os.path.join(path_cards, "TABLE_PONTOS.png"))
    if cadastrar:
        logger.info("Cadastrando pontos...")
