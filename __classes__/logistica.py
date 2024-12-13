def situacao_viagem(page, path, save=False):
    page.querySelector(
        "#navigation > ul > li.has-submenu.open > ul > li.has-submenu.open > ul > li:nth-child(1) > a"
    ).click()
    page.wait_for_load_state("networkidle")
    page.querySelector(".modal-content").screenshot(path=path)
    if save:
        page.querySelector("#situacaoViagemForm > div.float-right > button").click()
        page.querySelector(
            "#modalDetalhes > div > div > div.modal-header > button"
        ).click()


def situacao_veiculo(page, path, pesquisa="", cadastro={"descricao": "", "cor": ""}):
    page.querySelector(
        "#navigation > ul > li.has-submenu.open > ul > li.has-submenu.open > ul > li:nth-child(2) > a"
    ).click()
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
    page.querySelector(seletor_pesquisa).fill(value=pesquisa)
    page.querySelector("#tListSit_wrapper > div:nth-child(2)").screenshot(path=path)
    if cadastro.get("descricao"):
        for key, val in cadastro.items():
            page.querySelector(selectors_cadastro[key]).fill(value=val)

        page.querySelector("#formSitAddBtn").click()
        page.querySelector(
            "#modalDetalhes > div > div > div.modal-header > button"
        ).click()


def c_gestor(page, path, pesquisa="", cadastro={"descricao": "", "cor": ""}):
    selectors_cadastro = {
        "descricao": "#sitDesc",
        "cor": ".select2-search__field",
    }
    page.querySelector(
        "#navigation > ul > li.has-submenu.open > ul > li.has-submenu.open > ul > li:nth-child(3) > a"
    ).click()
    # Selecionar a opção "Todos"
    select_selector = 'select[name="tListSit_length"]'
    seletor_pesquisa = "#tListSit_filter > label > input"
    page.hover(select_selector)  # Passar o mouse
    page.click(select_selector)
    page.select_option(select_selector, value="-1")
    # logger.info("Selecionada a opção 'Todos' no campo select.")
    page.querySelector(seletor_pesquisa).fill(value=pesquisa)
    page.querySelector(".dataTables_scroll").screenshot(path=path)
    if cadastro.get("descricao"):
        page.querySelector(
            "#modalDetalhesConteudo > div.float-right > a > button"
        ).click()
        for k, v in cadastro.items():
            page.querySelector(selectors_cadastro[k]).fill(value=v)

        page.querySelector(".formSitAddBtn").click()


def c_reboque(page, path, pesquisa="", cadastro={"descricao": "", "cor": ""}):
    page.querySelector(
        "#navigation > ul > li.has-submenu.open > ul > li.has-submenu.open > ul > li:nth-child(4) > a"
    ).click()
    selectors_cadastro = {
        "descricao": "#sitDesc",
        "cor": ".select2-search__field",
    }
    page.querySelector(
        "#navigation > ul > li.has-submenu.open > ul > li.has-submenu.open > ul > li:nth-child(3) > a"
    ).click()
    # Selecionar a opção "Todos"
    select_selector = 'select[name="tListSit_length"]'
    seletor_pesquisa = "#tListSit_filter > label > input"
    page.hover(select_selector)  # Passar o mouse
    page.click(select_selector)
    page.select_option(select_selector, value="-1")
    # logger.info("Selecionada a opção 'Todos' no campo select.")
    page.querySelector(seletor_pesquisa).fill(value=pesquisa)
    page.querySelector(".dataTables_scroll").screenshot(path=path)
    if cadastro.get("descricao"):
        page.querySelector(
            "#modalDetalhesConteudo > div.float-right > a > button"
        ).click()
        for k, v in cadastro.items():
            page.querySelector(selectors_cadastro[k]).fill(value=v)

        page.querySelector(".formSitAddBtn").click()


def cad_driver(page, cpf):
    page.querySelector(
        "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
    ).click()
    cpf_element = page.querySelector("#mot-cpf")
    procurar_element = page.querySelector(
        "#cadastrarmotorista > div.row > div.col-md1 > button.btn.btn-sm.btn-primary"
    )
    cpf_element.fill(value=cpf)
    procurar_element.click()
    page.wait_for_load_state("networkidle")
    page.querySelector("#resultadobuscamotorista").screenshot(
        "MOTORISTA_CADASTRADO.png"
    )
    page.querySelector("#cadastrarmotoristabtn").click()
    page.querySelector("#modalDetalhes > div > div > div.modal-header > button").click()


def cad_veiculo(page, placa):
    page.querySelector(
        "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
    ).click()
    placa_element = page.querySelector("#veic-placa")
    procurar_element = page.querySelector(
        "#cadastrarveiculo > div.row > div.col-md1 > button.btn.btn-primary.btn-sm"
    )
    placa_element.fill(value=placa)
    procurar_element.click()
    page.wait_for_load_state("networkidle")
    page.querySelector("#resultadobuscaplaca").screenshot("VEICULO_CADASTRADO.png")
    page.querySelector("#cadastrarveiculobtn").click()
    page.querySelector("#modalDetalhes > div > div > div.modal-header > button").click()
