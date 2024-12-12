from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import logging
from time import sleep

from uteis import load_page

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


class MoniSAT:
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

    def extrator_to_grid(self, map_=True, list_results: bool | dict = True):
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

            # Navegar até o grid
            grid_element = "#navigation > ul > li:nth-child(4) > a"
            full_screen_element = "#mapaGrid > div.leaflet-control-container > div.leaflet-top.leaflet-left > div.leaflet-control-fullscreen.leaflet-bar.leaflet-control > a"
            grid_map_element = "#mapaGrid"
            logger.info(f"Extraindo informações dos elementos {grid_element}")
            self.page_monisat.click(grid_element)

            if map_:
                self.page_monisat.click(full_screen_element)
                grid_map = self.page_monisat.locator(grid_map_element)
                screenshot_path = os.path.join(os.getcwd(), "cards", f"MAP.png")
                self.page_monisat.wait_for_load_state("networkidle")
                grid_map.screenshot(path=screenshot_path)
                logger.info(f"Screenshot saved as {screenshot_path}")
                self.page_monisat.click(
                    "#mapaGrid > div.leaflet-control-container > div.leaflet-top.leaflet-left > div.leaflet-control-fullscreen.leaflet-bar.leaflet-control > a"
                )

            # Verificação da lista
            if list_results is True:  # Apenas tira o screenshot da lista completa
                logger.info("Capturando tela da lista sem filtros...")
                self.__extract_to_list()
            elif isinstance(
                list_results, dict
            ):  # Preenche os campos e tira o screenshot
                self.__extract_to_list(**list_results)

        except Exception as e:
            logger.error(f"Erro durante a extração: {str(e)}")
            self.fechar()
            raise

    def __extract_to_list(self, **kwargs):
        elements = {
            "placa": "#GGPLACA > center > input",
            "carreta": "#GGSEMIREBOQUE > center > input",
            "reboque": "#select2-SGGSITUACAOVEICULO4-container",
            "st_veiculo": "#select2-SGGSITUACAOVEICULO-container",
            "moto": "#GGMOTORISTA > center > input",
            "posicao": "#GGPOSICAO > center > input",
            "loc": "#GGLOCALIZACAO > center > input",
            "rota": "#GGROTA > center > input",
            "st_viagem": "#GGSITUACAOVIAGEM > center > input",
            "st_viagem_per": "#GGSITUACAOVIAGEMDET > center > input",
            "temp_viagem": "#GGTEMPORESTANTEVIAGEM > center > input",
            "st_geral": "#GGSITUACAOGERAL > center > input",
            "km": "#GGKMRESTANTEVIAGEM > center > input",
            "operacao": "#GGOPERACAO > center > input",
            "tt_parado": "#GGSTOTALPARADO > center > input",
            "sensor_1": "#GGTEMPSENSOR1 > center > input",
            "acao": "#GGACAO > center > input",
            "fx_1": "#GGTEMPFAIXA1 > center > input",
            "bau": "#GGSPORTABAU > center > input",
            "checklist": "#GGSCHECLIST > center > input",
            "velocidade": "#GGVELOCIDADE > center > input",
        }

        if kwargs:
            # Preenche os campos se houver parâmetros
            for key, value in kwargs.items():
                if key in elements:
                    self.page_monisat.fill(selector=elements[key], value=value)
                else:
                    logger.warning(
                        f"Parâmetro '{key}' não reconhecido e será ignorado."
                    )
        else:
            logger.info("Nenhum filtro fornecido. Capturando lista completa...")

        # Captura de tela da lista
        div_list_element = "#tableGridGeral_wrapper"
        load_page(self.page_monisat)
        div_list = self.page_monisat.locator(div_list_element)
        processing_selector = "#tableGridGeral_processing"
        if div_list:
            self.page_monisat.wait_for_function(
                f"() => getComputedStyle(document.querySelector('{processing_selector}')).display === 'none'",
                timeout=60_000,
            )

            logger.info("Tabela carregada completamente!")
            screenshot_path = os.path.join(os.getcwd(), "cards", f"LISTA_GRID.png")
            div_list.screenshot(path=screenshot_path)
            logger.info("Screenshot saved as LISTA_GRID.png")

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
    handler = MoniSAT()
    parametros = {}
    try:
        handler.extrator_to_grid(map_=False, list_results=True)
    except Exception as e:
        logger.error(f"Erro na execução do script: {str(e)}")
    finally:
        handler.fechar()
