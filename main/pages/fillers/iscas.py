import os

import pandas as pd
from main.uteis import load_page, wait_load_elements
from main.SuperClassMoni import CustomFormatter, ch, logger

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

path_cards = os.path.join(os.getcwd(), "cards")
path_data = os.path.join(os.getcwd(), "data")


def fill_iscas(
    page_monisat,
    nome="",
    marca="",
    site="",
    telefone="",
    login="",
    senha="",
    obs="",
    cadastrar=False,
):
    data_cadastro = {
        "nome": nome,
        "marca": marca,
        "site": site,
        "telefone": telefone,
        "login": login,
        "senha": senha,
        "obs": obs,
    }
    selectors = {
        "nome": "#tableIsca_wrapper > div:nth-child(2) > div > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th.sorting_asc > center > input",
        "marca": "#tableIsca_wrapper > div:nth-child(2) > div > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(2) > center > input",
        "site": "#tableIsca_wrapper > div:nth-child(2) > div > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(3) > center > input",
        "telefone": "#tableIsca_wrapper > div:nth-child(2) > div > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(4) > center > input",
        "login": "#tableIsca_wrapper > div:nth-child(2) > div > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(5) > center > input",
        "senha": "#tableIsca_wrapper > div:nth-child(2) > div > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(6) > center > input",
        "obs": "#tableIsca_wrapper > div:nth-child(2) > div > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(7) > center > input",
    }
    # Selecionar a opção "Todos"
    select_selector = 'select[name="tableIsca_length"]'
    page_monisat.hover(select_selector)  # Passar o mouse
    page_monisat.click(select_selector)
    page_monisat.select_option(select_selector, value="-1")
    logger.info("Selecionada a opção 'Todos' no campo select.")

    for key, value in data_cadastro.items():
        page_monisat.fill(selectors[key], value)

    # carrega a tabela por completa
    load_page(page_monisat)
    wait_load_elements(page_monisat, "#tableIsca_processing")
    page_monisat.wait_for_load_state("networkidle", timeout=30000)
    card = page_monisat.query_selector(".dataTables_scroll")
    card.screenshot(path=os.path.join(path_cards, "TABLE_ISCAS.png"))
    if cadastrar:
        save_selector = "#formSalvarIscaBtn"
        page_monisat.fill("#nomeIsca", nome)
        page_monisat.fill("#marca", marca)
        page_monisat.fill("#site", site)
        page_monisat.fill("#telefone", telefone)
        page_monisat.fill("#login", login)
        page_monisat.fill("#senha", senha)
        page_monisat.fill("#obs", obs)
        page_monisat.click(
            "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
        )
        page_monisat.click(save_selector)

    get_data_of_iscas(page_monisat)


def get_data_of_iscas(page):
    print(">> Iterando sobre dados de iscas...")
    lines_of_table = page.query_selector_all('//*[@id="tableIsca"]/tbody/tr')
    campos = [
        "nome",
        "marca",
        "site",
        "telefone",
        "login",
        "senha",
        "obs",
    ]
    data = []
    for row_index, row in enumerate(lines_of_table, start=1):
        row_data = {}
        for col_index, campo in enumerate(campos, start=1):
            try:
                content = page.query_selector(
                    f'//*[@id="tableIsca"]/tbody/tr[{row_index}]/td[{col_index}]/center'
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
        df.to_csv(f"{path_data}/iscas.csv", index=False)
        print("[INFO]>> Dados salvos em iscas.csv [INFO]")
    else:
        print("[INFO]>> Não foi possivel salvar iscas.csv [INFO]")
