import os

import pandas as pd
from main.uteis import load_page, wait_load_elements
from main.SuperClassMoni import CustomFormatter, ch, logger

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

path_cards = os.path.join(os.getcwd(), "cards")
path_data = os.path.join(os.getcwd(), "data")


def fill_car(
    page_monisat,
    placa="",
    situacao="",
    tipo="",
    categoria="",
    rastreador="",
    n_antena="",
    semi_reboque="",
    motorista="",
    operacao="",
    consulta="",
    validade="",
    status="",
    referencia="",
    cadastrar=False,
):

    data_catastro = {
        "placa": placa,
        "situacao": situacao,
        "tipo": tipo,
        "categoria": categoria,
        "rastreador": rastreador,
        "n_antena": n_antena,
        "semi_reboque": semi_reboque,
        "motorista": motorista,
        "operacao": operacao,
        "consulta": consulta,
        "validade": validade,
        "status": status,
        "referencia": referencia,
    }
    selectors = {
        "placa": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th.sorting_asc > center > input",
        "situacao": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(3) > center > input",
        "tipo": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(4) > center > input",
        "categoria": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(5) > center > input",
        "rastreador": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(6) > center > input",
        "n_antena": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(7) > center > input",
        "semi_reboque": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(8) > center > input",
        "motorista": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(9) > center > input",
        "operacao": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(10) > center > input",
        "consulta": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(11) > center > input",
        "validade": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(12) > center > input",
        "status": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(13) > center > input",
        "referencia": "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(14) > center > input",
    }

    # Selecionar a opção "Todos"
    select_selector = 'select[name="tableveic_length"]'
    page_monisat.hover(select_selector)  # Passar o mouse
    page_monisat.click(select_selector)
    page_monisat.select_option(select_selector, value="-1")
    logger.info("Selecionada a opção 'Todos' no campo select.")

    logger.info("Preenchendo veículo...")
    for key, value in data_catastro.items():
        page_monisat.fill(selectors[key], value)

    # carrega a tabela por completa
    load_page(page_monisat)
    wait_load_elements(page_monisat, "#tableveic_processing")
    page_monisat.wait_for_load_state("networkidle", timeout=30000)
    card = page_monisat.query_selector(".dataTables_scroll")
    card.screenshot(path=os.path.join(path_cards, "TABLE_CARS.png"))
    if cadastrar:
        cad_veiculo(page_monisat, placa)

    get_data_of_cars(page_monisat)


def cad_veiculo(page, placa):
    try:
        selecao_element = page.query_selector(
            "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
        )
        selecao_element.click()
        placa_element = page.query_selector("#veic-placa")
        procurar_element = page.query_selector(
            "#cadastrarveiculo > div.row > div.col-md1 > button.btn.btn-primary.btn-sm"
        )
        placa_element.fill(value=placa)
        procurar_element.click()
        page.wait_for_load_state("networkidle")
        page.query_selector("#resultadobuscaplaca").screenshot("VEICULO_CADASTRADO.png")
        page.query_selector("#cadastrarveiculobtn").click()
        page.query_selector(
            "#modalDetalhes > div > div > div.modal-header > button"
        ).click()
    except Exception as e:
        print(f"[ERROR] {str(e)} [ERROR]")
        pass


def get_data_of_cars(page):
    print(">> Iterando sobre dados da tabela de veiculos...")
    lines_of_table = page.query_selector_all('//*[@id="tableveic"]/tbody/tr')
    campos = [
        "placa",
        "icone",
        "situacao",
        "tipo",
        "categoria",
        "rastreador",
        "n_antena",
        "semi_reboque",
        "motorista",
        "operacao",
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
                    f'//*[@id="tableveic"]/tbody/tr[{row_index}]/td[{col_index}]/center'
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
        pd.DataFrame(data).to_csv(f"{path_data}/cars.csv", index=False)
        print("[INFO]>> Data saved in drivers.csv [INFO]")
    else:
        print("[INFO]>> Unable to save data [INFO]")
