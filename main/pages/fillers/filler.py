from time import sleep
from __init__ import *

from main.SuperClassMoni import CustomFormatter, MoniSat, ch, logger
from main.pages.fillers.car import fill_car
from main.pages.fillers.driver import fill_driver
from main.pages.fillers.iscas import fill_iscas
from main.pages.fillers.logistica import fill_logistica
from main.pages.fillers.pontos import fill_pontos
from main.pages.fillers.reboque import fill_reboque
from main.pages.fillers.retrograma import fill_retrograma

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class CadMoniSAT(MoniSat):
    def __init__(self):
        super().__init__()

    def process_cadastro(
        self,
        params_driver: dict = None,
        all_drivers: bool = True,
        params_car: dict = None,
        all_cars: bool = True,
        params_reboque: dict = None,
        all_reboques: bool = True,
        params_iscas: dict = None,
        all_iscas: bool = True,
        params_pontos: dict = None,
        all_pontos: bool = True,
        params_retograma: dict = None,
        all_retogramas: bool = True,
        params_logistica: dict = None,
        all_logisticas: bool = True,
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
        params_retograma = params_retograma or {}
        params_logistica = params_logistica or {}

        # Realiza login no sistema MoniSat
        self.login()

        # Seleciona todas as opções do menu de navegação
        selector_options = "#navigation > ul > li:nth-child(3) > ul > li > a"
        options_elements = self.page_monisat.query_selector_all(selector_options)

        # Dicionário que mapeia cada opção do menu para a função correspondente
        dict_func = {
            "Motorista": lambda: (
                fill_driver(
                    self.page_monisat,
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
                else fill_driver(self.page_monisat) if all_drivers else None
            ),
            "Veículo": lambda: (
                fill_car(
                    self.page_monisat,
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
                else fill_car(self.page_monisat) if all_cars else None
            ),
            "Reboque": lambda: (
                fill_reboque(
                    self.page_monisat,
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
                else fill_reboque(self.page_monisat) if all_reboques else None
            ),
            "Isca/Redundante": lambda: (
                fill_iscas(
                    self.page_monisat,
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
                else fill_iscas(self.page_monisat) if all_iscas else None
            ),
            "Pontos": lambda: (
                fill_pontos(
                    self.page_monisat,
                    params_pontos.get("ponto", ""),
                    params_pontos.get("cidade", ""),
                    params_pontos.get("cnpj", ""),
                    params_pontos.get("tipo", ""),
                    params_pontos.get("raio", ""),
                    cliente_points,
                    cadastrar_pontos,
                )
                if params_pontos
                else fill_pontos(self.page_monisat) if all_pontos else None
            ),
            "Rotograma": lambda: (
                fill_retrograma(
                    self.page_monisat,
                    params_retograma.get("id", ""),
                    params_retograma.get("retrograma", ""),
                    params_retograma.get("distancia", ""),
                    params_retograma.get("criado_por", ""),
                    params_retograma.get("data_hora", ""),
                    rotas_alternativas,
                    cadastrar_rotograma,
                )
                if params_retograma
                else fill_retrograma(self.page_monisat) if all_retogramas else None
            ),
            "Logística": lambda: (
                fill_logistica(
                    self.page_monisat,
                    params_logistica.get("args_viagem", ""),
                    params_logistica.get("args_veiculo", ""),
                    params_logistica.get("args_gestor", ""),
                    params_logistica.get("args_reboque", ""),
                )
                if params_logistica
                else fill_logistica(self.page_monisat) if all_logisticas else None
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
        handler.process_cadastro()
    except Exception as e:
        logger.error(f"Erro na execução do script: {str(e)}")
        handler.page_monisat.pause()
    finally:
        handler.fechar()
