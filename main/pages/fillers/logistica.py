"""
Utilitarios para logistica
"""

import os
from time import sleep

path_cards = os.path.join(os.getcwd(), "cards")
def __option_select_for_logistic(page_monisat):
    """Auxilia a selecionar o campo de logistica no menu."""

    chevron_selector = "#navigation > ul > li:nth-child(3) > a > i.fas.fa-edit"
    page_monisat.hover(chevron_selector)  # Passar o mouse
    page_monisat.click(chevron_selector)  # Clicar no dropdown
    sleep(1)
    option = page_monisat.query_selector(
        "#navigation > ul > li:nth-child(3) > ul > li.has-submenu > a"
    )
    option.click()  # Clicar na opção do menu
    option.hover()


def fill_logistica(
    page_monisat,
    args_viagem=False,
    args_veiculo={"pesquisa": "", "cadastro": {"descricao": "", "cor": "Preto"}},
    args_gestor={"pesquisa": "", "cadastro": {"descricao": "", "cor": "Preto"}},
    args_reboque={"pesquisa": "", "cadastro": {"descricao": "", "cor": "Preto"}},
):
    situacao_viagem(
        page_monisat,
        os.path.join(path_cards, "LOGISTICA_SITUACAO_VIAGEM.png"),
        args_viagem,
    )
    __option_select_for_logistic(page_monisat)
    situacao_veiculo(
        page_monisat,
        os.path.join(path_cards, "LOGISTICA_SITUACAO_VEICULO.png"),
        args_veiculo.get("pesquisa"),
        args_veiculo.get("cadatro"),
    )
    __option_select_for_logistic(page_monisat)
    c_gestor(
        page_monisat,
        os.path.join(path_cards, "LOGISTICA_C_GESTOR.png"),
        args_gestor.get("pesquisa"),
        args_gestor.get("cadastro"),
    )
    __option_select_for_logistic(page_monisat)
    c_reboque(
        page_monisat,
        os.path.join(path_cards, "LOGISTICA_C_REBOQUE.png"),
        args_reboque.get("pesquisa"),
        args_reboque.get("cadastro"),
    )


def situacao_viagem(page, path, save=False):
    try:
        selecao_element = page.query_selector(
            "#navigation > ul > li:nth-child(3) > ul > li.has-submenu > ul > li:nth-child(1) > a"
        )
        selecao_element.click()
        page.wait_for_load_state("networkidle")
        page.query_selector(".modal-content").screenshot(path=path)
        if save:
            page.query_selector(
                "#situacaoViagemForm > div.float-right > button"
            ).click()
        x_button = "#modalDetalhes > div > div > div.modal-header > button"
        page.query_selector(x_button).click()
    except Exception as e:
        print(f"[ERROR] {str(e)} [ERROR]")
        pass


def situacao_veiculo(page, path, pesquisa="", cadastro={"descricao": "", "cor": ""}):
    try:
        selecao_element = page.query_selector(
            "#navigation > ul > li:nth-child(3) > ul > li.has-submenu > ul > li:nth-child(2) > a"
        )
        selecao_element.click()
        # Selecionar a opção "Todos"
        select_selector = 'select[name="tListSit_length"]'
        seletor_pesquisa = "#tListSit_filter > label > input"
        page.hover(select_selector)  # Passar o mouse
        page.click(select_selector)
        page.select_option(select_selector, value="-1")
        # logger.info("Selecionada a opção 'Todos' no campo select.")
        selectors_cadastro = {
            "descricao": "#sitDesc",
            "cor": ".select2-search__field",
        }
        page.query_selector(seletor_pesquisa).fill(value=pesquisa)
        page.query_selector("#tListSit_wrapper > div:nth-child(2)").screenshot(
            path=path
        )
        if cadastro.get("descricao"):
            for key, val in cadastro.items():
                page.query_selector(selectors_cadastro[key]).fill(value=val)

            page.query_selector("#formSitAddBtn").click()
        page.query_selector(
            "#modalDetalhes > div > div > div.modal-header > button"
        ).click()
    except Exception as e:
        print(f"[ERROR] {str(e)} [ERROR]")
        pass


def c_gestor(page, path, pesquisa="", cadastro={"descricao": "", "cor": ""}):
    try:
        selectors_cadastro = {
            "descricao": "#sitDesc",
            "cor": ".select2-search__field",
        }
        selecao_element = page.query_selector(
            "#navigation > ul > li:nth-child(3) > ul > li.has-submenu > ul > li:nth-child(3) > a"
        )
        selecao_element.click()
        # Selecionar a opção "Todos"
        select_selector = 'select[name="tListSit_length"]'
        seletor_pesquisa = "#tListSit_filter > label > input"
        page.hover(select_selector)  # Passar o mouse
        page.click(select_selector)
        page.select_option(select_selector, value="-1")
        # logger.info("Selecionada a opção 'Todos' no campo select.")
        page.query_selector(seletor_pesquisa).fill(value=pesquisa)
        page.query_selector(".dataTables_scroll").screenshot(path=path)
        if cadastro.get("descricao"):
            page.query_selector(
                "#modalDetalhesConteudo > div.float-right > a > button"
            ).click()
            for k, v in cadastro.items():
                page.query_selector(selectors_cadastro[k]).fill(value=v)

            page.query_selector(".formSitAddBtn").click()
    except Exception as e:
        print(f"[ERROR] {str(e)} [ERROR]")
        pass


def c_reboque(page, path, pesquisa="", cadastro={"descricao": "", "cor": ""}):
    try:
        selecao_element = page.query_selector(
            "#navigation > ul > li:nth-child(3) > ul > li.has-submenu > ul > li:nth-child(4) > a"
        )
        selecao_element.click()
        selectors_cadastro = {
            "descricao": "#sitDesc",
            "cor": ".select2-search__field",
        }
        page.query_selector(
            "#navigation > ul > li.has-submenu.open > ul > li.has-submenu.open > ul > li:nth-child(3) > a"
        ).click()
        # Selecionar a opção "Todos"
        select_selector = 'select[name="tListSit_length"]'
        seletor_pesquisa = "#tListSit_filter > label > input"
        page.hover(select_selector)  # Passar o mouse
        page.click(select_selector)
        page.select_option(select_selector, value="-1")
        # logger.info("Selecionada a opção 'Todos' no campo select.")
        page.query_selector(seletor_pesquisa).fill(value=pesquisa)
        page.query_selector(".dataTables_scroll").screenshot(path=path)
        if cadastro.get("descricao"):
            page.query_selector(
                "#modalDetalhesConteudo > div.float-right > a > button"
            ).click()
            for k, v in cadastro.items():
                page.query_selector(selectors_cadastro[k]).fill(value=v)

            page.query_selector(".formSitAddBtn").click()
    except Exception as e:
        print(f"[ERROR] {str(e)} [ERROR]")
        pass


