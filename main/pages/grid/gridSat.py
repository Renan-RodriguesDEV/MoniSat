import os

import pandas as pd
from __init__ import *
from main.SuperClassMoni import CustomFormatter, MoniSat, ch, logger
from main.uteis import load_page, wait_load_elements

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class GridMoniSAT(MoniSat):
    path_data = os.path.join(os.getcwd(), "data")

    def __init__(self):
        super().__init__()

    def extrator_to_grid(self, map_=True, list_results: bool | dict = True):
        """Extrai dados do grid do MoniSAT

        Args:
            map_ (bool, optional): Mapa sim ou não?. Defaults to True.
            list_results (bool | dict, optional): Grade de resultados não ou dicionario de parametros. Defaults to True.
        """
        try:
            self.login()

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
                self._get_data_of_grid()

            elif isinstance(
                list_results, dict
            ):  # Preenche os campos e tira o screenshot
                self.__extract_to_list(**list_results)
                self._get_data_of_grid()

        except Exception as e:
            logger.error(f"Erro durante a extração: {str(e)}")
            self.fechar()
            pass

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
            wait_load_elements(self.page_monisat, processing_selector)

            logger.info("Tabela carregada completamente!")
            screenshot_path = os.path.join(os.getcwd(), "cards", f"LISTA_GRID.png")
            div_list.screenshot(path=screenshot_path)
            logger.info("Screenshot saved as LISTA_GRID.png")

    def _get_data_of_grid(self):
        print(">> Iterando sobre dados de grids...")
        lines_of_table = self.page_monisat.query_selector_all(
            '//*[@id="tableGridGeral"]/tbody/tr'
        )
        campos = [
            "placa",
            "carreta",
            "reboque",
            "situacao_veiculo",
            "motorista",
            "posicao",
            "localizacao",
            "rota",
            "situacao_viagem",
            "situacao_viagem_per",
            "tempo_ate_destino",
            "situacao_geral",
            "km_ate_destino",
            "operacao",
            "total_parado_dia",
            "sensor_1",
            "acao",
            "faixa_1",
            "bau",
            "checklist",
            "velocidade",
        ]
        data = []
        for row_index, row in enumerate(lines_of_table, start=1):
            row_data = {}
            for col_index, campo in enumerate(campos, start=1):
                try:
                    content = self.page_monisat.query_selector(
                        f'//*[@id="tableGridGeral"]/tbody/tr[{row_index}]/td[{col_index}]/center'
                    )
                    if content:
                        content_text = content.inner_text().strip()
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
            pd.DataFrame(data).to_csv(f"{self.path_data}/grids.csv", index=False)
            print("[INFO]>> Dados salvos em grids.csv [INFO]")
        else:
            print("[INFO]>> Não foi possivel salvar grids.csv [INFO]")


if __name__ == "__main__":
    handler = GridMoniSAT()
    parametros = {
        "placa": "ABC1234",
        "carreta": "XYZ5678",
        "moto": "MOT123",
        "loc": "São Paulo",
        "rota": "Rota 66",
        "st_viagem": "Em andamento",
    }
    try:
        handler.extrator_to_grid(map_=True, list_results=True)
    except Exception as e:
        logger.error(f"Erro na execução do script: {str(e)}")
    finally:
        handler.fechar()
