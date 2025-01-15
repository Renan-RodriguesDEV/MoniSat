import os
from time import sleep

from logistica import (
    c_gestor,
    c_reboque,
    cad_driver,
    cad_veiculo,
    situacao_veiculo,
    situacao_viagem,
)
from SuperClassMoni import CustomFormatter, MoniSat, ch, logger
from uteis import load_page, wait_load_elements

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class CadMoniSAT(MoniSat):
    def __init__(self):
        super().__init__()

    def __option_select_for_logistic(self):
        """Auxilia a selecionar o campo de logistica no menu."""

        chevron_selector = "#navigation > ul > li:nth-child(3) > a > i.fas.fa-edit"
        self.page_monisat.hover(chevron_selector)  # Passar o mouse
        self.page_monisat.click(chevron_selector)  # Clicar no dropdown
        sleep(1)
        option = self.page_monisat.query_selector(
            "#navigation > ul > li:nth-child(3) > ul > li.has-submenu > a"
        )
        option.click()  # Clicar na opção do menu
        option.hover()

    def process_cadastro(
        self,
        params_driver: dict = None,
        params_car: dict = None,
        params_reboque: dict = None,
        params_iscas: dict = None,
        params_pontos: dict = None,
        params_rotograma: dict = None,
        params_logistica: dict = None,
        cadastrar_driver: bool = False,
        cadastrar_car: bool = False,
        cadastrar_reboque: bool = False,
        cadastrar_iscas: bool = False,
        cadastrar_pontos: bool = False,
        cliente_points: bool = False,
        cadastrar_rotograma: bool = False,
        rotas_alternativas: bool = False,
    ):
        """
        Preenche e cadastra informações no sistema MoniSat com base nos dados fornecidos.

        Esta função realiza login no sistema MoniSat, navega pelas opções do menu e preenche
        os formulários correspondentes com os dados fornecidos nos dicionários de parâmetros.
        Cada tipo de cadastro (Motorista, Veículo, Reboque, etc.) é tratado por uma função específica.

        Args:
            params_driver (dict, optional): Parâmetros para cadastro de motorista. Defaults to None.
            params_car (dict, optional): Parâmetros para cadastro de veículo. Defaults to None.
            params_reboque (dict, optional): Parâmetros para cadastro de reboque. Defaults to None.
            params_iscas (dict, optional): Parâmetros para cadastro de iscas. Defaults to None.
            params_pontos (dict, optional): Parâmetros para cadastro de pontos. Defaults to None.
            params_rotograma (dict, optional): Parâmetros para cadastro de rotograma. Defaults to None.
            params_logistica (dict, optional): Parâmetros para cadastro de logística. Defaults to None.
            cadastrar_driver (bool, optional): Indica se deve cadastrar motorista. Defaults to False.
            cadastrar_car (bool, optional): Indica se deve cadastrar veículo. Defaults to False.
            cadastrar_reboque (bool, optional): Indica se deve cadastrar reboque. Defaults to False.
            cadastrar_iscas (bool, optional): Indica se deve cadastrar iscas. Defaults to False.
            cadastrar_pontos (bool, optional): Indica se deve cadastrar pontos. Defaults to False.
            cliente_points (bool, optional): Indica se os pontos são de cliente. Defaults to False.
            cadastrar_rotograma (bool, optional): Indica se deve cadastrar rotograma. Defaults to False.
            rotas_alternativas (bool, optional): Indica se deve considerar rotas alternativas. Defaults to False.
        """
        # Parâmetros com valores padrão vazios, caso não sejam passados
        params_driver = params_driver or {}
        params_car = params_car or {}
        params_reboque = params_reboque or {}
        params_iscas = params_iscas or {}
        params_pontos = params_pontos or {}
        params_rotograma = params_rotograma or {}
        params_logistica = params_logistica or {}

        # Realiza login no sistema MoniSat
        self.login()

        # Seleciona todas as opções do menu de navegação
        selector_options = "#navigation > ul > li:nth-child(3) > ul > li > a"
        options_elements = self.page_monisat.query_selector_all(selector_options)

        # Dicionário que mapeia cada opção do menu para a função correspondente
        dict_func = {
            "Motorista": lambda: (
                self.fill_driver(
                    params_driver.get("nome", ""),
                    params_driver.get("rg", ""),
                    params_driver.get("cpf", ""),
                    params_driver.get("cnh", ""),
                    params_driver.get("tipo", ""),
                    params_driver.get("pussoui_pass", ""),
                    params_driver.get("consulta", ""),
                    params_driver.get("validade", ""),
                    params_driver.get("status", ""),
                    params_driver.get("referencia", ""),
                    cadastrar_driver,
                )
                if params_driver
                else None
            ),
            "Veículo": lambda: (
                self.fill_car(
                    params_car.get("placa", ""),
                    params_car.get("situacao", ""),
                    params_car.get("tipo", ""),
                    params_car.get("categoria", ""),
                    params_car.get("rastreador", ""),
                    params_car.get("n_antena", ""),
                    params_car.get("semi_reboque", ""),
                    params_car.get("motorista", ""),
                    params_car.get("operacao", ""),
                    params_car.get("consulta", ""),
                    params_car.get("validade", ""),
                    params_car.get("status", ""),
                    params_car.get("referencia", ""),
                    cadastrar_car,
                )
                if params_car
                else None
            ),
            "Reboque": lambda: (
                self.fill_reboque(
                    params_reboque.get("placa_reboque", ""),
                    params_reboque.get("chassi", ""),
                    params_reboque.get("renavam", ""),
                    params_reboque.get("subcategoria", ""),
                    params_reboque.get("marca", ""),
                    params_reboque.get("consulta", ""),
                    params_reboque.get("validade", ""),
                    params_reboque.get("status", ""),
                    params_reboque.get("referencia", ""),
                    cadastrar_reboque,
                )
                if params_reboque
                else None
            ),
            "Isca/Redundante": lambda: (
                self.fill_iscas(
                    params_iscas.get("nome", ""),
                    params_iscas.get("marca", ""),
                    params_iscas.get("site", ""),
                    params_iscas.get("telefone", ""),
                    params_iscas.get("login", ""),
                    params_iscas.get("senha", ""),
                    params_iscas.get("obs", ""),
                    cadastrar_iscas,
                )
                if params_iscas
                else None
            ),
            "Pontos": lambda: (
                self.fill_pontos(
                    params_pontos.get("ponto", ""),
                    params_pontos.get("cidade", ""),
                    params_pontos.get("cnpj", ""),
                    params_pontos.get("tipo", ""),
                    params_pontos.get("raio", ""),
                    cliente_points,
                    cadastrar_pontos,
                )
                if params_pontos
                else None
            ),
            "Rotograma": lambda: (
                self.fill_retrograma(
                    params_rotograma.get("id", ""),
                    params_rotograma.get("retrograma", ""),
                    params_rotograma.get("distancia", ""),
                    params_rotograma.get("criado_por", ""),
                    params_rotograma.get("data_hora", ""),
                    rotas_alternativas,
                    cadastrar_rotograma,
                )
                if params_rotograma
                else None
            ),
            "Logística": lambda: (
                self.fill_logistica(
                    params_logistica.get("args_viagem", ""),
                    params_logistica.get("args_veiculo", ""),
                    params_logistica.get("args_gestor", ""),
                    params_logistica.get("args_reboque", ""),
                )
                if params_logistica
                else self.fill_logistica()
            ),
        }

        chevron_selector = "#navigation > ul > li:nth-child(3) > a > i.fas.fa-edit"

        # Iterar sobre as opções no menu e chamar a função correspondente
        for option in options_elements:
            option_text = option.text_content().strip()
            logger.debug(f"Tentando selecionar a opção: {option_text}")

            try:
                # Passar o mouse e clicar no dropdown
                self.page_monisat.hover(chevron_selector)
                self.page_monisat.click(chevron_selector)
                sleep(1)

                # Clicar na opção do menu
                option.click()
                if option_text == "Logística":
                    option.hover()
                if option_text in dict_func and dict_func[option_text]:
                    # Executar a função correspondente
                    dict_func[option_text]()
                else:
                    logger.warning(
                        f"Opção '{option_text}' não reconhecida ou função não executada devido a parâmetros."
                    )
                sleep(5)

            except Exception as e:
                logger.error(f"Erro ao clicar em '{option_text}': {str(e)}")

    def fill_reboque(
        self,
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
        self.page_monisat.hover(select_selector)  # Passar o mouse
        self.page_monisat.click(select_selector)
        self.page_monisat.select_option(select_selector, value="-1")
        logger.info("Selecionada a opção 'Todos' no campo select.")

        # Preencher os campos
        for key, value in data_cadastro.items():
            if value:
                self.page_monisat.fill(selectors[key], value)

        # carrega a tabela por completa
        load_page(self.page_monisat)
        wait_load_elements(self.page_monisat, "#tablesemreb_processing")
        self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
        card = self.page_monisat.query_selector(".dataTables_scroll")
        card.screenshot(path=os.path.join(self.path_cards, "TABLE_REBOQUES.png"))
        if cadastrar:
            save_selector = "#cadastrarveiculobtn"
            self.page_monisat.click(
                "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
            )
            self.page_monisat.click(save_selector)

    def fill_iscas(
        self,
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
        self.page_monisat.hover(select_selector)  # Passar o mouse
        self.page_monisat.click(select_selector)
        self.page_monisat.select_option(select_selector, value="-1")
        logger.info("Selecionada a opção 'Todos' no campo select.")

        for key, value in data_cadastro.items():
            self.page_monisat.fill(selectors[key], value)

        # carrega a tabela por completa
        load_page(self.page_monisat)
        wait_load_elements(self.page_monisat, "#tableIsca_processing")
        self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
        card = self.page_monisat.query_selector(".dataTables_scroll")
        card.screenshot(path=os.path.join(self.path_cards, "TABLE_ISCAS.png"))
        if cadastrar:
            save_selector = "#formSalvarIscaBtn"
            self.page_monisat.fill("#nomeIsca", nome)
            self.page_monisat.fill("#marca", marca)
            self.page_monisat.fill("#site", site)
            self.page_monisat.fill("#telefone", telefone)
            self.page_monisat.fill("#login", login)
            self.page_monisat.fill("#senha", senha)
            self.page_monisat.fill("#obs", obs)
            self.page_monisat.click(
                "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
            )
            self.page_monisat.click(save_selector)

    def fill_pontos(
        self,
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
            self.page_monisat.click(btn_pontos)

        # Selecionar a opção "Todos"
        select_selector = 'select[name="tablePonto_length"]'
        self.page_monisat.hover(select_selector)  # Passar o mouse
        self.page_monisat.click(select_selector)
        self.page_monisat.select_option(select_selector, value="-1")
        logger.info("Selecionada a opção 'Todos' no campo select.")

        if mapa:
            self.page_monisat.click(maximize_minimize)
            self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
            self.page_monisat.wait_for_selector(mapa_selector)
            mapa_element = self.page_monisat.query_selector(mapa_selector)
            mapa_element.screenshot(
                path=os.path.join(self.path_cards, "MAPA_PONTOS.png")
            )
            self.page_monisat.click(maximize_minimize)

        for key, value in data_cadastro.items():
            self.page_monisat.fill(selectors[key], value)
        # carrega a tabela por completa
        load_page(self.page_monisat)
        wait_load_elements(self.page_monisat, "#tablePonto_processing")
        self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
        card = self.page_monisat.query_selector("#tablePonto")
        card.screenshot(path=os.path.join(self.path_cards, "TABLE_PONTOS.png"))
        if cadastrar:
            logger.info("Cadastrando pontos...")

    def fill_retrograma(
        self,
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
            self.page_monisat.click(
                "#conteudoPagina > div > div > div > div > div > div.float-right > button:nth-child(2)"
            )

        # Selecionar a opção "Todos"
        select_selector = 'select[name="tableRotograma_length"]'
        self.page_monisat.hover(select_selector)  # Passar o mouse
        self.page_monisat.click(select_selector)
        self.page_monisat.select_option(select_selector, value="-1")
        logger.info("Selecionada a opção 'Todos' no campo select.")

        for key, value in data_cadastro.items():
            self.page_monisat.fill(selectors[key], value)

        # carrega a tabela por completa
        load_page(self.page_monisat)
        wait_load_elements(self.page_monisat, "#tableRotograma_processing")
        self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
        card = self.page_monisat.query_selector(".dataTables_scroll")
        card.screenshot(path=os.path.join(self.path_cards, "TABLE_RETROGRAMA.png"))
        if cadastrar:
            logger.info("Cadastrando retrogrma...")

    def fill_logistica(
        self,
        args_viagem=False,
        args_veiculo={"pesquisa": "", "cadastro": {"descricao": "", "cor": "Preto"}},
        args_gestor={"pesquisa": "", "cadastro": {"descricao": "", "cor": "Preto"}},
        args_reboque={"pesquisa": "", "cadastro": {"descricao": "", "cor": "Preto"}},
    ):
        situacao_viagem(
            self.page_monisat,
            os.path.join(self.path_cards, "LOGISTICA_SITUACAO_VIAGEM.png"),
            args_viagem,
        )
        self.__option_select_for_logistic()
        situacao_veiculo(
            self.page_monisat,
            os.path.join(self.path_cards, "LOGISTICA_SITUACAO_VEICULO.png"),
            args_veiculo.get("pesquisa"),
            args_veiculo.get("cadatro"),
        )
        self.__option_select_for_logistic()
        c_gestor(
            self.page_monisat,
            os.path.join(self.path_cards, "LOGISTICA_C_GESTOR.png"),
            args_gestor.get("pesquisa"),
            args_gestor.get("cadastro"),
        )
        self.__option_select_for_logistic()
        c_reboque(
            self.page_monisat,
            os.path.join(self.path_cards, "LOGISTICA_C_REBOQUE.png"),
            args_reboque.get("pesquisa"),
            args_reboque.get("cadastro"),
        )

    def fill_car(
        self,
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
        self.page_monisat.hover(select_selector)  # Passar o mouse
        self.page_monisat.click(select_selector)
        self.page_monisat.select_option(select_selector, value="-1")
        logger.info("Selecionada a opção 'Todos' no campo select.")

        logger.info("Preenchendo veículo...")
        for key, value in data_catastro.items():
            self.page_monisat.fill(selectors[key], value)

        # carrega a tabela por completa
        load_page(self.page_monisat)
        wait_load_elements(self.page_monisat, "#tableveic_processing")
        self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
        card = self.page_monisat.query_selector(".dataTables_scroll")
        card.screenshot(path=os.path.join(self.path_cards, "TABLE_CARS.png"))
        if cadastrar:
            cad_veiculo(self.page_monisat, placa)

    def fill_driver(
        self,
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
        self.page_monisat.hover(select_selector)  # Passar o mouse
        self.page_monisat.click(select_selector)  # Clicar no
        self.page_monisat.select_option(select_selector, value="-1")
        logger.info("Selecionada a opção 'Todos' no campo select.")

        for key, value in data_cadastro.items():
            if value:
                self.page_monisat.fill(selectors[key], value)

        # carrega a tabela por completa
        load_page(self.page_monisat)
        wait_load_elements(self.page_monisat, "#tablemot_processing")
        self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
        card = self.page_monisat.query_selector(".dataTables_scroll")

        card.screenshot(path=os.path.join(self.path_cards, "TABLE_MOTORISTA.png"))
        if cadastrar:
            cad_driver(self.page_monisat, cpf)


if __name__ == "__main__":
    handler = CadMoniSAT()
    try:
        params_driver = {
            # "nome": "João Silva",
            # "rg": "123456789",
            # "cpf": "123.456.789-00",
            # "cnh": "1234567890",
            # "tipo": "Motorista",
            # "pussoui_pass": "Sim",
        }
        params_car = {
            # "placa": "ABC-1234",
            # "situacao": "Ativo",
            # "tipo": "Caminhão",
            # "categoria": "Carga",
            # "rastreador": "Sim",
        }
        handler.process_cadastro(params_driver=params_driver)
    except Exception as e:
        logger.error(f"Erro na execução do script: {str(e)}")
        handler.page_monisat.pause()
    finally:
        handler.fechar()
