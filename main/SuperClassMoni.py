"""
Classe mãe dos scrappers
"""

import logging


from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
from time import sleep

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


load_dotenv()


ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class MoniSat:
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
            self.page_monisat = (
                self.browser.pages[0] if self.browser.pages else self.browser.new_page()
            )

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

    def fechar(self):
        try:
            if self.browser:
                self.browser.close()
            if hasattr(self, "playwright"):
                self.playwright.stop()
            logger.debug("Navegador encerrado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao fechar o navegador: {str(e)}")
