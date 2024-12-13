from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
from SuperClassMoni import CustomFormatter, MoniSat, ch, logger
from time import sleep

from uteis import load_page, wait_load_elements

load_dotenv()


ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class CadMoniSAT(MoniSat):
    def __init__(self):
        super().__init__()

    def get_options(
        self,
        params_driver=None,
        params_car=None,
        params_reboque=None,
        params_iscas=None,
        params_pontos=None,
        params_rotograma=None,
        params_logistica=None,
        cadastrar_driver=False,
        cadastrar_car=False,
        cadastrar_reboque=False,
        cadastrar_iscas=False,
        cadastrar_pontos=False,
        cliente_points=False,
        cadastrar_rotograma=False,
        rotas_alternativas=False,
        cadastrar_logistica=False,
    ):
        # Parâmetros com valores padrão vazios, caso não sejam passados
        params_driver = params_driver or {}
        params_car = params_car or {}
        params_reboque = params_reboque or {}
        params_iscas = params_iscas or {}
        params_pontos = params_pontos or {}
        params_rotograma = params_rotograma or {}
        params_logistica = params_logistica or {}

        self.login()

        selector_options = "#navigation > ul > li:nth-child(3) > ul > li > a"
        options_elements = self.page_monisat.query_selector_all(selector_options)

        # Armazenar referências das funções sem executá-las
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
                else self.fill_driver()
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
                else self.fill_car()
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
                else self.fill_reboque()
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
                else self.fill_iscas()
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
                else self.fill_pontos()
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
                else self.fill_retrograma()
            ),
            "Logística": lambda: (
                self.logistica(params_logistica)
                if params_logistica
                else self.logistica()
            ),
        }

        chevron_selector = "#navigation > ul > li:nth-child(3) > a > i.fas.fa-edit"

        # Iterar sobre as opções no menu e chamar a função correspondente
        for option in options_elements:
            option_text = option.text_content().strip()
            logger.debug(f"Tentando selecionar a opção: {option_text}")

            try:
                self.page_monisat.hover(chevron_selector)  # Passar o mouse
                self.page_monisat.click(chevron_selector)  # Clicar no dropdown
                sleep(1)

                option.click()  # Clicar na opção do menu
                if (
                    option_text in dict_func and dict_func[option_text]
                ):  # Executa apenas se a função não for None

                    dict_func[option_text]()  # Executar a função correspondente
                else:
                    logger.warning(
                        f"Opção '{option_text}' não reconhecida ou função não executada devido a parâmetros."
                    )
                sleep(5)

            except Exception as e:
                logger.error(f"Erro ao clicar em '{option_text}': {str(e)}")
                pass

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
        mapa=False,
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
        btn_cadastro = "#conteudoPagina > div > div > div > div > div > div.float-right > a:nth-child(2) > button"
        maximize_minimize = "#mapPonto > div.leaflet-control-container > div.leaflet-top.leaflet-left > div.leaflet-control-fullscreen.leaflet-bar.leaflet-control > a"
        mapa_selector = "#mapPonto"

        if cliente_points:
            self.page_monisat.click(btn_pontos)

        if mapa:
            self.page_monisat.click(maximize_minimize)
            self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
            self.page_monisat.wait_for_selector(mapa_selector)
            card = self.page_monisat.query_selector(mapa_selector)
            card.screenshot(path=os.path.join(self.path_cards, "MAPA_PONTOS.png"))
            self.page_monisat.click(maximize_minimize)

        # Selecionar a opção "Todos"
        select_selector = 'select[name="tablePonto_length"]'
        self.page_monisat.hover(select_selector)  # Passar o mouse
        self.page_monisat.click(select_selector)
        self.page_monisat.select_option(select_selector, value="-1")
        logger.info("Selecionada a opção 'Todos' no campo select.")

        for key, value in data_cadastro.items():
            self.page_monisat.fill(selectors[key], value)
        # carrega a tabela por completa
        load_page(self.page_monisat)
        wait_load_elements(self.page_monisat, "#tablePonto_processing")
        self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
        card = self.page_monisat.query_selector(".dataTables_scroll")
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

    def logistica(self, **kwargs):
        pass

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
            save_selector = "#cadastrarveiculobtn"
            self.page_monisat.click(
                "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
            )
            self.page_monisat.click(save_selector)

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
            save_selector = "#cadastrarmotoristabtn"
            self.page_monisat.click(
                "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
            )
            self.page_monisat.click(save_selector)


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
        handler.get_options(params_car=params_car, params_driver=params_driver)
    except Exception as e:
        logger.error(f"Erro na execução do script: {str(e)}")
    finally:
        handler.fechar()
