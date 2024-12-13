# from playwright.sync_api import Page


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
        page.query_selector(
            "#modalDetalhes > div > div > div.modal-header > button"
        ).click()
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
