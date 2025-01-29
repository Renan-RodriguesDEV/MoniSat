import os

import pandas as pd
from main.uteis import load_page, wait_load_elements
from main.SuperClassMoni import CustomFormatter, ch, logger

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

path_cards = os.path.join(os.getcwd(), "cards")
path_data = os.path.join(os.getcwd(), "data")


def fill_retrograma(
    page_monisat,
    id_="",
    retrograma="",
    distancia="",
    criado_por="",
    data_hora="",
    rotas_alternativas=False,
    cadastrar=False,
):
    data_cadastro = {
        "id": id_,
        "retrograma": retrograma,
        "distancia": distancia,
        "criado_por": criado_por,
        "data_hora": data_hora,
    }
    selectors = {
        "id": "#tableRotograma_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(2) > center > input",
        "retrograma": "#tableRotograma_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(3) > center > input",
        "distancia": "#tableRotograma_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(4) > center > input",
        "criado_por": "#tableRotograma_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(5) > center > input",
        "data_hora": "#tableRotograma_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(6) > center > input",
    }
    if rotas_alternativas:
        page_monisat.click(
            "#conteudoPagina > div > div > div > div > div > div.float-right > button:nth-child(2)"
        )

    # Selecionar a opção "Todos"
    select_selector = 'select[name="tableRotograma_length"]'
    page_monisat.hover(select_selector)  # Passar o mouse
    page_monisat.click(select_selector)
    page_monisat.select_option(select_selector, value="-1")
    logger.info("Selecionada a opção 'Todos' no campo select.")

    for key, value in data_cadastro.items():
        page_monisat.fill(selectors[key], value)

    # carrega a tabela por completa
    load_page(page_monisat)
    wait_load_elements(page_monisat, "#tableRotograma_processing")
    page_monisat.wait_for_load_state("networkidle", timeout=30000)
    card = page_monisat.query_selector(".dataTables_scroll")
    card.screenshot(path=os.path.join(path_cards, "TABLE_RETROGRAMA.png"))
    if cadastrar:
        logger.info("Cadastrando retrogrma...")
    get_data_of_retrogramas(page_monisat)


def get_data_of_retrogramas(page):
    print(">> Iterando sobre dados de retrogramas...")
    lines_of_table = page.query_selector_all('//*[@id="tableRotograma"]/tbody/tr')
    campos = ["#", "id", "retrograma", "distancia", "criado_por", "data_hora", "acao"]
    data = []
    for row_index, row in enumerate(lines_of_table, start=1):
        row_data = {}
        for col_index, campo in enumerate(campos, start=1):
            try:
                content = page.query_selector(
                    f'//*[@id="tableRotograma"]/tbody/tr[{row_index}]/td[{col_index}]/center'
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
        pd.DataFrame(data).to_csv(f"{path_data}/retrogramas.csv", index=False)
        print("[INFO]>> Dados salvos em retrogramas.csv [INFO]")
    else:
        print("[INFO]>> Não foi possivel salvar retrogramas.csv [INFO]")
