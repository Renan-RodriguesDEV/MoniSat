import os

import pandas as pd
from main.uteis import load_page, wait_load_elements
from main.SuperClassMoni import CustomFormatter, ch, logger

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

path_cards = os.path.join(os.getcwd(), "cards")
path_data = os.path.join(os.getcwd(), "data")


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

    get_data_of_reboques(page_monisat)


def get_data_of_reboques(page):
    print(">> Iterando sobre dados de reboques...")
    lines_of_table = page.query_selector_all('//*[@id="tablesemreb"]/tbody/tr')
    campos = [
        "placa_reboque",
        "chassi",
        "renavam",
        "sub_categoria",
        "marca",
        "consulta",
        "validade",
        "status",
        "referencia",
        "acao",
    ]
    data = []
    for row_index, row in enumerate(lines_of_table, start=1):
        row_data = {}
        for col_index, campo in enumerate(campos, start=1):
            try:
                content = page.query_selector(
                    f'//*[@id="tablesemreb"]/tbody/tr[{row_index}]/td[{col_index}]/center'
                )
                if content:
                    content_text = content.text_content().strip()
                    print(f"{campo} | {content_text}")
                    row_data[campo] = content_text
                else:
                    print(f"{campo} | ")
                    row_data[campo] = ""
            except Exception as e:
                print(f"[ERROR] {str(e)} [ERROR]")
                continue
        data.append(row_data)
        print("=" * 100)

    if data:
        df = pd.DataFrame(data)
        df.drop("acao", axis=1, inplace=True, errors="ignore")
        df.to_csv(f"{path_data}/reboques.csv", index=False)
        print("[INFO]>> Dados salvos em reboques.csv [INFO]")
    else:
        print("[INFO]>> Não foi possivel salvar reboques.csv [INFO]")
