import os
import pandas as pd

import __init__

from main.SuperClassMoni import MoniSat
from main.uteis import wait_load_elements, load_page

path_cards = os.path.join(os.getcwd(), "cards")
path_data = os.path.join(os.getcwd(), "data")


def get_all_phones():
    monisat = MoniSat()

    monisat.login()

    chevron_selector = "#navigation > ul > li:nth-child(3) > a > i.fas.fa-edit"
    # Passar o mouse e clicar no dropdown
    monisat.page_monisat.hover(chevron_selector)
    monisat.page_monisat.click(chevron_selector)
    monisat.page_monisat.click('//*[@id="navigation"]/ul/li[3]/ul/li[1]/a')

    # Selecionar a opção "Todos"
    select_selector = 'select[name="tablemot_length"]'
    monisat.page_monisat.hover(select_selector)  # Passar o mouse
    monisat.page_monisat.click(select_selector)  # Clicar no
    monisat.page_monisat.select_option(select_selector, value="-1")
    print(">> Selecionada a opção 'Todos' no campo select.")

    # carrega a tabela por completa
    load_page(monisat.page_monisat)
    wait_load_elements(monisat.page_monisat, "#tablemot_processing")
    monisat.page_monisat.wait_for_load_state("networkidle", timeout=30000)

    print(">> Iterando sobre telefones de motorista...")
    list_selector = '//*[@id="tablemot"]/tbody/tr'
    phone_selector_icon = '//*[@id="tablemot"]/tbody/tr[{}]/td[11]/center/a[3]/i'
    phone_numbers_selectors = {
        1: "#listTel > div > div.col-5 > div > div > table > tbody > tr > td:nth-child(1)",
        2: "#listTel > div > div.col-5 > div > div > table > tbody > tr:nth-child({}) > td:nth-child(1)",
    }

    phones, identifiers = [], []

    list_phones_selector = monisat.page_monisat.query_selector_all(list_selector)
    print(f"Total de telefones motoristas: {len(list_phones_selector)}")
    for i, _ in enumerate(list_phones_selector):
        print("-" * 50)
        print(f"Motorista: {i}")
        try:
            phone_icon = monisat.page_monisat.query_selector(
                phone_selector_icon.format(i)
            )
            if phone_icon:
                # Força o clique usando JavaScript
                monisat.page_monisat.evaluate("element => element.click()", phone_icon)
                monisat.page_monisat.wait_for_load_state("networkidle")
                if monisat.page_monisat.query_selector(phone_numbers_selectors[1]):
                    phone_element = monisat.page_monisat.query_selector(
                        phone_numbers_selectors[1]
                    )
                else:
                    phones_numbers = monisat.page_monisat.query_selector_all(
                        "#listTel > div > div.col-5 > div > div > table > tbody > tr"
                    )
                    phone_elements = []
                    for i, _ in enumerate(phones_numbers):
                        phone_elements.append(
                            monisat.page_monisat.query_selector(
                                phone_numbers_selectors[2].format(i)
                            )
                        )

                if phone_element:
                    identifier = monisat.page_monisat.query_selector(
                        "#modalDetalhesTitulo"
                    ).text_content()
                    phone = phone_element.text_content()

                    # Força o fechamento do modal usando JavaScript
                    monisat.page_monisat.evaluate(
                        """() => {
                        document.querySelector('#modalDetalhes button.close').click();
                    }"""
                    )

                    phones.append(phone)
                    identifiers.append(identifier)
                    print(f"Identificador: {identifier}, Telefone: {phone}")
                elif phone_elements:
                    phone = ""
                    for phone_element in phone_elements:
                        identifier = monisat.page_monisat.query_selector(
                            "#modalDetalhesTitulo"
                        ).text_content()
                        phone += phone_element.text_content() + ","

                    # Força o fechamento do modal usando JavaScript
                    monisat.page_monisat.evaluate(
                        """() => {
                        document.querySelector('#modalDetalhes button.close').click();
                    }"""
                    )

                    phones.append(phone)
                    identifiers.append(identifier)
                    print(f"Identificador: {identifier}, Telefone: {phone}")
                else:
                    # Fecha o modal mesmo se não encontrar telefone
                    monisat.page_monisat.evaluate(
                        """() => {
                        document.querySelector('#modalDetalhes button.close').click();
                    }"""
                    )
                    print(f"Telefone: Não encontrado")
                print("=" * 100)
            else:
                print(f"Telefone: Não encontrado {phone_selector_icon.format(i)}")
        except Exception as e:
            print(f"[ERROR] {str(e)} [ERROR]")
            # Tenta fechar o modal em caso de erro
            try:
                monisat.page_monisat.evaluate(
                    """() => {
                    document.querySelector('#modalDetalhes button.close').click();
                }"""
                )
            except:
                pass
            continue

    if len(phones) > 0 and len(identifiers) > 0:
        df = pd.DataFrame({"phones": phones, "indentifiers": identifiers})
        df.drop("acao", axis=1, inplace=True, errors="ignore")
        df.to_csv(f"{path_data}/phones.csv", index=False)
        print("[INFO]>> Dados salvos em phones.csv [INFO]")
    else:
        print("[INFO]>> Não foi possivel salvar phones.csv [INFO]")


if __name__ == "__main__":
    get_all_phones()
