from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import logging
from time import sleep

from uteis import load_page, wait_load_elements

load_dotenv()

# create logger with 'spam_application'
logger = logging.getLogger("scrapper")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class CadMoniSAT:
    def __init__(self):
        # Verificar se as variáveis de ambiente existem
        required_env_vars = ["GERAL", "LOGIN", "SENHA"]
        for var in required_env_vars:
            if not os.getenv(var):
                logger.error(f"Variável de ambiente {var} não encontrada")
                raise ValueError(f"Variável de ambiente {var} não configurada")

        self.user_geral = os.getenv("GERAL")
        self.user_login = os.getenv("LOGIN")
        self.senha = os.getenv("SENHA")
        self.browser = None
        self.path_cards = os.path.join(os.getcwd(), "cards")

        try:
            app_data_path = os.getenv("LOCALAPPDATA")
            user_data_path = os.path.join(
                app_data_path, r"Google\Chrome\User Data\Default\Google Profile"
            )

            logger.info(f"AppData: {app_data_path}")
            # Criar diretório para screenshots se não existir
            os.makedirs(os.path.join(os.getcwd(), "cards"), exist_ok=True)

            # Iniciar o playwright
            self.playwright = sync_playwright().start()
            # self.browser = self.playwright.chromium.launch()
            self.browser = self.playwright.chromium.launch_persistent_context(
                user_data_path,
                headless=False,
                args=["--start-maximized"],
                no_viewport=True,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81",
            )

            self.url = "https://site.monisat.com.br/index.php"
            logger.debug("Classe iniciada com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao inicializar: {str(e)}")
            self.fechar()
            raise

    def login(self):
        try:
            logger.debug("Iniciando extração.")
            self.page_monisat = self.browser.new_page()

            # Adicionar timeout para carregamento da página
            self.page_monisat.goto(self.url, timeout=30000)
            self.page_monisat.wait_for_load_state("networkidle", timeout=30000)

            # Verificar se os elementos de login existem
            selectors = {
                "empresa": 'input[name="userEmpresa"]',
                "usuario": 'input[name="username"]',
                "senha": 'input[name="userpassword"]',
                "submit": 'button[type="submit"]',
            }

            for name, selector in selectors.items():
                if not self.page_monisat.query_selector(selector):
                    raise Exception(f"Elemento {name} não encontrado na página")

            logger.info("Página carregada.")

            logger.info("Preenchendo login.")
            self.page_monisat.fill('input[name="userEmpresa"]', self.user_geral)
            self.page_monisat.fill('input[name="username"]', self.user_login)
            self.page_monisat.fill('input[name="userpassword"]', self.senha)
            self.page_monisat.click('button[type="submit"]')
            sleep(3)

            self.page_monisat.wait_for_load_state("networkidle")
            logger.info("Login efetuado.")

        except Exception as e:
            logger.error(f"Erro durante a extração: {str(e)}")
            self.fechar()
            raise

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
        cadastrar_rotograma=False,
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
                    params_car.get("consulta", ""),
                    params_car.get("validade", ""),
                    params_car.get("status", ""),
                    params_car.get("referencia", ""),
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
                )
                if params_car
                else self.fill_car()
            ),
            "Reboque": lambda: (
                self.fill_reboque(params_reboque)
                if params_reboque
                else self.fill_reboque()
            ),
            "Isca/Redundante": lambda: (
                self.fill_iscas(params_iscas) if params_iscas else self.fill_iscas()
            ),
            "Pontos": lambda: (
                self.fill_pontos(params_pontos) if params_pontos else self.fill_pontos()
            ),
            "Rotograma": lambda: (
                self.fill_rotograma(params_rotograma)
                if params_rotograma
                else self.fill_retrotograma()
            ),
            "Logística": lambda: (
                self.fill_logistica(params_logistica)
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
    ): ...

    def fill_iscas(
        self, nome="", marca="", site="", telefone="", login="", senha="", obs=""
    ): ...

    def fill_pontos(self, ponto="", cidade="", cnpj="", tipo="", raio=""): ...

    def fill_retrograma(
        self, id="", retrograma="", distancia="", criado_por="", data_hora=""
    ): ...
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
    ):
        placa_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th.sorting_asc > center > input"
        situacao_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(3) > center > input"
        tipo_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(4) > center > input"
        categoria_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(5) > center > input"
        rastreador_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(6) > center > input"
        n_antena_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(7) > center > input"
        semi_reboque_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(8) > center > input"
        motorista_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(9) > center > input"
        operacao_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(10) > center > input"
        consulta_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(11) > center > input"
        validade_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(12) > center > input"
        status_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(13) > center > input"
        referencia_selector = "#tableveic_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(14) > center > input"

        # Selecionar a opção "Todos"
        select_selector = 'select[name="tableveic_length"]'
        self.page_monisat.hover(select_selector)  # Passar o mouse
        self.page_monisat.click(select_selector)
        self.page_monisat.select_option(select_selector, value="-1")
        logger.info("Selecionada a opção 'Todos' no campo select.")

        logger.info("Preenchendo veículo...")
        self.page_monisat.fill(placa_selector, placa)
        self.page_monisat.fill(situacao_selector, situacao)
        self.page_monisat.fill(tipo_selector, tipo)
        self.page_monisat.fill(categoria_selector, categoria)
        self.page_monisat.fill(rastreador_selector, rastreador)

        # carrega a tabela por completa
        load_page(self.page_monisat)
        wait_load_elements(self.page_monisat, "#tableveic_processing")
        self.page_monisat.wait_for_load_state("networkidle", timeout=30000)
        card = self.page_monisat.query_selector(".card-body")
        card.screenshot(path=os.path.join(self.path_cards, "TABLE_CARS.png"))

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
        card = self.page_monisat.query_selector(".card-body")

        card.screenshot(path=os.path.join(self.path_cards, "TABLE_MOTORISTA.png"))
        if cadastrar:
            save_selector = "#cadastrarmotoristabtn"
            self.page_monisat.click(
                "#conteudoPagina > div > div > div > div > div > div.float-right > a > button"
            )
            self.page_monisat.click(save_selector)

    def fechar(self):
        try:
            if self.browser:
                self.browser.close()
            if hasattr(self, "playwright"):
                self.playwright.stop()
            logger.debug("Navegador encerrado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao fechar o navegador: {str(e)}")


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
