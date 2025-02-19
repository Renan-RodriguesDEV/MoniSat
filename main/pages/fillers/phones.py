import os
import time
import pandas as pd

import __init__

from main.SuperClassMoni import MoniSat, logger
from main.uteis import wait_load_elements, load_page

path_cards = os.path.join(os.getcwd(), "cards")
path_data = os.path.join(os.getcwd(), "data")


def select_all_options(page_monisat):
    chevron_selector = "#navigation > ul > li:nth-child(3) > a > i.fas.fa-edit"
    # Passar o mouse e clicar no dropdown
    page_monisat.hover(chevron_selector)
    page_monisat.click(chevron_selector)
    page_monisat.click('//*[@id="navigation"]/ul/li[3]/ul/li[1]/a')

    # Selecionar a opção "Todos"
    select_selector = 'select[name="tablemot_length"]'
    page_monisat.hover(select_selector)  # Passar o mouse
    page_monisat.click(select_selector)  # Clicar no
    page_monisat.select_option(select_selector, value="-1")
    print(">> Selecionada a opção 'Todos' no campo select.")


def get_all_phones():
    monisat = MoniSat()

    monisat.login()
    page = monisat.page_monisat

    select_all_options(page)
    # carrega a tabela por completa
    load_page(page)
    wait_load_elements(page, "#tablemot_processing")
    page.wait_for_load_state("networkidle", timeout=30000)

    logger.info(">> Iterando sobre telefones de motorista...")
    phone_list_selector = "i.fas.fa-phone"
    is_whatsapp_selector = (
        "#listTel > div > div.col-5 > div > div > table > tbody > tr > td:nth-child(2)"
    )
    phone_number_selector = (
        "#listTel > div > div.col-5 > div > div > table > tbody > tr > td:nth-child(1)"
    )

    collected_driver_is_whatsapp = []
    collected_driver_phones = []
    collected_driver_identifiers = []
    collected_driver_names = []

    list_phones_selector = page.query_selector_all(phone_list_selector)
    logger.info(f">> Total de telefones motoristas: {len(list_phones_selector)}")
    print("=" * 100)
    for driver_idx, phone_icon in enumerate(list_phones_selector):
        time.sleep(0.5)
        driver_idx += 1
        # page.pause()
        print("-" * 100)
        logger.info(f"[INFO] Motorista: {driver_idx}")
        try:
            if phone_icon:
                logger.info(f"[INFO] Clicando em: {phone_icon} - {driver_idx}")
                # Força o clique usando JavaScript
                page.evaluate("element => element.click()", phone_icon)
                page.wait_for_selector(phone_number_selector)
                if page.query_selector_all(phone_number_selector):
                    print(">> pegando o(s) telefone(s)")

                    phones_elements = page.query_selector_all(phone_number_selector)
                    identifier = page.query_selector(
                        "#modalDetalhesTitulo"
                    ).text_content()
                    is_whatsapps = page.query_selector_all(is_whatsapp_selector)
                    for idx, phone_element in enumerate(phones_elements):
                        phone = phone_element.text_content()
                        inicio = identifier.find("[")
                        fim = identifier.find("]")
                        identifier_code = identifier[inicio + 1 : fim]
                        driver_name = identifier[identifier.find(":") + 1 :]
                        collected_driver_phones.append(phone)
                        collected_driver_identifiers.append(identifier_code)
                        collected_driver_names.append(driver_name)
                        collected_driver_is_whatsapp.append(
                            is_whatsapps[idx].text_content()
                        )
                        logger.debug(f"Identificador: {identifier}, Telefone: {phone}")
                        print("=" * 100)
                    closing_modal(page)

                else:
                    # Fecha o modal mesmo se não encontrar telefone
                    closing_modal(page)
                    logger.warning(f"Telefone: Não encontrado")

                print("=" * 100)
            else:
                logger.warning(
                    f"Telefone: Não encontrado {phone_icon} - {driver_idx} [WARNING]"
                )
        except Exception as e:
            logger.exception(f"[ERROR] {str(e)} [ERROR]")
            # Tenta fechar o modal em caso de erro
            try:
                closing_modal(page)
            except:
                logger.exception(e)
            continue

    if (
        len(collected_driver_phones) > 0
        and len(collected_driver_identifiers) > 0
        and len(collected_driver_is_whatsapp)
    ):
        df = pd.DataFrame(
            {
                "phones": collected_driver_phones,
                "identifiers": collected_driver_identifiers,
                "names": collected_driver_names,
                "is_whatsapp": collected_driver_is_whatsapp,
            }
        )
        df.drop("acao", axis=1, inplace=True, errors="ignore")
        df.to_csv(f"{path_data}/phones.csv", index=False)
        print("[INFO]>> Dados salvos em phones.csv [INFO]")
    else:
        print("[INFO]>> Não foi possivel salvar phones.csv [INFO]")


def closing_modal(page):
    logger.debug(">> Fechando modal...")
    page.evaluate(
        """() => {document.querySelector('#modalDetalhes button.close').click();}"""
    )


if __name__ == "__main__":
    get_all_phones()
