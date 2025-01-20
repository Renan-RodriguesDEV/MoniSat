import os
from main.uteis import load_page, wait_load_elements
from main.SuperClassMoni import CustomFormatter, ch, logger

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

path_cards = os.path.join(os.getcwd(), "cards")


def fill_driver(
    page_monisat,
    nome="",
    rg="",
    cpf="",
    cnh="",
    tipo="",
    pussoui_pass="",
    consulta="",
    validade="",
    status="",
    referencia="",
    cadastrar=False,
):
    data_cadastro = {
        "nome": nome,
        "rg": rg,
        "cpf": cpf,
        "cnh": cnh,
        "tipo": tipo,
        "possui_pass": pussoui_pass,
        "consulta": consulta,
        "validade": validade,
        "status": status,
        "referencia": referencia,
    }
    selectors = {
        "nome": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th.sorting_asc > center > input",
        "rg": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(2) > center > input",
        "cpf": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(3) > center > input",
        "cnh": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(4) > center > input",
        "tipo": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(5) > center > input",
        "possui_pass": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(6) > center > input",
        "consulta": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(7) > center > input",
        "validade": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(8) > center > input",
        "status": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(9) > center > input",
        "referencia": "#tablemot_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(10) > center > input",
    }

    # Selecionar a opção "Todos"
    select_selector = 'select[name="tablemot_length"]'
    page_monisat.hover(select_selector)  # Passar o mouse
    page_monisat.click(select_selector)  # Clicar no
    page_monisat.select_option(select_selector, value="-1")
    logger.info("Selecionada a opção 'Todos' no campo select.")

    for key, value in data_cadastro.items():
        if value:
            page_monisat.fill(selectors[key], value)

    # carrega a tabela por completa
    load_page(page_monisat)
    wait_load_elements(page_monisat, "#tablemot_processing")
    page_monisat.wait_for_load_state("networkidle", timeout=30000)
    card = page_monisat.query_selector(".dataTables_scroll")

    card.screenshot(path=os.path.join(path_cards, "TABLE_MOTORISTA.png"))
    if cadastrar:
        cad_driver(page_monisat, cpf)


def cad_driver(page, cpf):
    try:
        selecao_element = page.query_selector(
            "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
        )
        selecao_element.click()
        cpf_element = page.query_selector("#mot-cpf")
        procurar_element = page.query_selector(
            "#cadastrarmotorista > div.row > div.col-md1 > button.btn.btn-sm.btn-primary"
        )
        cpf_element.fill(value=cpf)
        procurar_element.click()
        page.wait_for_load_state("networkidle")
        page.query_selector("#resultadobuscamotorista").screenshot(
            "MOTORISTA_CADASTRADO.png"
        )
        page.query_selector("#cadastrarmotoristabtn").click()
        page.query_selector(
            "#modalDetalhes > div > div > div.modal-header > button"
        ).click()
    except Exception as e:
        print(f"[ERROR] {str(e)} [ERROR]")
        pass
