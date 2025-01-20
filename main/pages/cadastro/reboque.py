import os
from main.uteis import load_page, wait_load_elements
from main.SuperClassMoni import CustomFormatter, ch, logger

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

path_cards = os.path.join(os.getcwd(), "cards")


def fill_reboque(
    page_monisat,
    placa_reboque="",
    chassi="",
    renavam="",
    subcategoria="",
    marca="",
    consulta="",
    validade="",
    status="",
    referencia="",
    cadastrar=False,
):
    data_cadastro = {
        "placa_reboque": placa_reboque,
        "chassi": chassi,
        "renavam": renavam,
        "subcategoria": subcategoria,
        "marca": marca,
        "consulta": consulta,
        "validade": validade,
        "status": status,
        "referencia": referencia,
    }
    selectors = {
        "placa_reboque": "#tablesemreb_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th.sorting_asc > center > input",
        "chassi": "#tablesemreb_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(2) > center > input",
        "renavam": "#tablesemreb_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(3) > center > input",
        "subcategoria": "#tablesemreb_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(4) > center > input",
        "marca": "#tablesemreb_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(5) > center > input",
        "consulta": "#tablesemreb_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(6) > center > input",
        "validade": "#tablesemreb_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(7) > center > input",
        "status": "#tablesemreb_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(8) > center > input",
        "referencia": "#tablesemreb_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(9) > center > input",
    }
    # Selecionar a opção "Todos"
    select_selector = 'select[name="tablesemreb_length"]'
    page_monisat.hover(select_selector)  # Passar o mouse
    page_monisat.click(select_selector)
    page_monisat.select_option(select_selector, value="-1")
    logger.info("Selecionada a opção 'Todos' no campo select.")

    # Preencher os campos
    for key, value in data_cadastro.items():
        if value:
            page_monisat.fill(selectors[key], value)

    # carrega a tabela por completa
    load_page(page_monisat)
    wait_load_elements(page_monisat, "#tablesemreb_processing")
    page_monisat.wait_for_load_state("networkidle", timeout=30000)
    card = page_monisat.query_selector(".dataTables_scroll")
    card.screenshot(path=os.path.join(path_cards, "TABLE_REBOQUES.png"))
    if cadastrar:
        save_selector = "#cadastrarveiculobtn"
        page_monisat.click(
            "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
        )
        page_monisat.click(save_selector)
