import os
import pandas as pd
from __init__ import *
from main.SuperClassMoni import MoniSat, CustomFormatter, ch, logger
from main.uteis import load_page, wait_load_elements

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class Checklist(MoniSat):
    path_data = os.path.join(os.getcwd(), "data")
    path_cards = os.path.join(os.getcwd(), "cards")

    def __init__(self):
        super().__init__()

    def extract_checklist(self):
        # acessa a pagina e seleciona o campo checklist
        self.login()
        self.page_monisat.hover('//a[text()="Gerenciamento "]')
        self.page_monisat.hover('//a[text()="Checklist"]')
        self.page_monisat.click('//a[text()="Histórico Checklist"]')

        logger.info("Carregando a pagina!!")
        self.page_monisat.wait_for_load_state("load")
        self.page_monisat.wait_for_selector(
            '//*[@id="tableCklHistorico_wrapper"]/div[3]/div[1]/div/table'
        )

        # Selecionar a opção "Todos"
        select_selector = 'select[name="tableCklHistorico_length"]'
        self.page_monisat.hover(select_selector)  # Passar o mouse
        self.page_monisat.click(select_selector)  # Clicar no
        self.page_monisat.select_option(select_selector, value="-1")
        logger.info("Selecionada a opção 'Todos' no campo select.")

        # carrega a tabela completa
        load_page(self.page_monisat)

        wait_load_elements(self.page_monisat, "#tableCklHistorico_processing")
        self.get_data_of_checklist()

    def get_data_of_checklist(self):

        # definindo os campos que retornam de cada coluna
        campos = [
            "placa",
            "empresa",
            "operacao",
            "resultado",
            "status",
            "validade",
            "data_validade",
            "data_execucao",
            "acao",
        ]

        # Seleciona a tabela completa, linhas
        selector_lines_table = '//*[@id="tableCklHistorico"]/tbody/tr'
        lines_tables_elements = self.page_monisat.query_selector_all(
            selector_lines_table
        )
        data = []
        for row_index, _ in enumerate(lines_tables_elements, start=1):
            row_data = {}
            for col_index, campo in enumerate(campos, start=1):
                try:
                    content = self.page_monisat.query_selector(
                        f'//*[@id="tableCklHistorico"]/tbody/tr[{row_index}]/td[{col_index}]/center'
                    )
                    if content:
                        content_text = content.text_content().strip()
                        print(f"{campo} | {content_text}")
                        row_data[campo] = content_text
                    else:
                        print(f"{campo} | ")
                        row_data[campo] = ""
                except Exception as e:
                    print(f"[ERROR] {str(e)} [ERROR]")
                    continue
            data.append(row_data)
            print("=" * 100)

        if data:
            df = pd.DataFrame(data)
            df.drop("operacao", axis=1, inplace=True, errors="ignore")
            df.drop("acao", axis=1, inplace=True, errors="ignore")
            df.drop("resultado", axis=1, inplace=True, errors="ignore")
            # Limpa e transforma a coluna "validade"
            df["validade"] = df["validade"].map(
                lambda x: x.lower().replace("dias", "").replace("!", "").strip()
            )
            # Remove linhas onde "validade" é igual a "vencido"
            df.drop(
                df[df["validade"] == "vencido"].index,
                inplace=True,
                axis=0,
                errors="ignore",
            )
            df.to_csv(f"{self.path_data}/checklist.csv", index=False)
            print("[INFO]>> Dados salvos em checklist.csv [INFO]")
        else:
            print("[INFO]>> Não foi possivel salvar checklist.csv [INFO]")


if __name__ == "__main__":
    checklist = Checklist()
    checklist.extract_checklist()
