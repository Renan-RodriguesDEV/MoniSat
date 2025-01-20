import logging
import os

from __init__ import *
from dotenv import load_dotenv

from main.SuperClassMoni import CustomFormatter, MoniSat, ch, logger

load_dotenv()

# create logger with 'spam_application'
logger = logging.getLogger("scrapper")
logger.setLevel(logging.DEBUG)


ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class MoniScraper(MoniSat):
    def __init__(self):
        super().__init__()

    def extrator(self):
        try:
            self.login()

            logger.info('Extraindo informações dos elementos div[class="card"].')
            cards = self.page_monisat.query_selector_all('div[class="card"]')

            for index, card in enumerate(cards):
                card_body = card.query_selector('div[class="card-body"]')
                if card_body:
                    h4_element = card_body.query_selector("h4")

                if h4_element:
                    card_info = h4_element.inner_text()
                    logger.info(f"Card {index + 1}: {card_info}")

                    screenshot_path = os.path.join(
                        os.getcwd(), "cards", f'{card_info.replace(".", "")}.png'
                    )
                    card.screenshot(path=screenshot_path)
                    logger.info(f"Screenshot saved as {screenshot_path}")

        except Exception as e:
            logger.error(f"Erro durante a extração: {str(e)}")
            self.fechar()
            raise


if __name__ == "__main__":
    handler = MoniScraper()
    try:
        handler.extrator()
    except Exception as e:
        logger.error(f"Erro na execução do script: {str(e)}")
    finally:
        handler.fechar()
