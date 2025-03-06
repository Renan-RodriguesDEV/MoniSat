import os
import time
import schedule
import subprocess
import datetime
from main.emails.email_sender import send_email, from_address, to_address, password

BASE_PATH_SCRIPTS = os.path.join(os.getcwd(), "main")


def verify_hours(func):
    def wrapper(*args, **kwargs):
        current_hour = datetime.datetime.now().hour
        if 18 >= current_hour >= 8:
            return func(*args, **kwargs)
        else:
            print(
                f"Script não executado pois não estão dentro das horas de operação (8:00 - 18:00)"
            )
            return None

    return wrapper


def sender_emails_for(
    tittle="Grid",
    to_address=to_address,
    password=password,
    from_address=from_address,
    files=[],
):
    body = f"""
    <html>
        <body>
            <p>Prezado(a), {to_address}</p>
            <p>Segue em anexo os dados solicitados em formato <b>.csv</b>.</p>
            <p>Atenciosamente,</p>
            <p>Equipe VJBots <span color='red'>({datetime.datetime.now().strftime( "%d/%m/%Y, %H:%M")})</span></p>
            <a href='https://vjbots.com.br'>VJBots Technologies</a>
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqXDLqIQoEeMb2QzO_CGQkr85wOX75Zgcjeg&s" alt="VJBots Icon" style="width:50px;height:50px;">
        </body>
    </html>
    """
    print(f">> INFO: Inicializando o arquivo Python {__file__}, aguarde a execução\n")
    send_email(
        subject=f"Email automatico MoniSat ({tittle})",
        body=body,
        _from=from_address,
        _to=to_address,
        passwd=password,
        dir_files=os.path.join(os.getcwd(), "data"),
        files=files,
    )


@verify_hours
def run_scrapper(path_scrapper, tittle="", files=[]):
    if not os.path.exists(path_scrapper):
        print(f'>> {time.strftime("%X")} Arquivo inexistente "{path_scrapper}"')
        return
    try:
        subprocess.run(["python", path_scrapper])
        print(
            f'>> {time.strftime("%X")} Arquivo executado com sucesso ({path_scrapper})'
        )
        sender_emails_for(tittle, files=files)
    except Exception as e:
        print(f">> {time.strftime('%X')} {str(e)}")


if __name__ == "__main__":
    files = ["cars.csv", "drivers.csv", "reboques.csv"]
    path_scrappers_fillers = os.path.join(
        BASE_PATH_SCRIPTS, "pages", "fillers", "filler.py"
    )
    path_scrappers_phones = os.path.join(
        BASE_PATH_SCRIPTS, "pages", "fillers", "phones.py"
    )
    path_scrapper_grid = os.path.join(BASE_PATH_SCRIPTS, "pages", "grid", "gridSat.py")
    path_scrapper_home = os.path.join(BASE_PATH_SCRIPTS, "pages", "home", "scrapper.py")

    # executando os arquivos da pasta de pages/grid
    schedule.every(30).minutes.do(
        run_scrapper,
        path_scrapper=path_scrapper_grid,
        tittle="Grid",
        files=["grids.csv"],
    )

    # # executando os arquivos da pasta de pages/home (TODO: á implementar...)
    # schedule.every(30).minutes.do(run_scrapper, path_scrapper=path_scrapper_home,tittle='Home',files=['home.csv'])

    # executando os arquivos da pasta de pages/fillers/phones.py ás 07:30 AM
    schedule.every(1).day.at("11:56").do(
        run_scrapper,
        path_scrapper=path_scrappers_phones,
        tittle="Telefones",
        files=["phones.csv"],
    )
    # executando os arquivos da pasta de pages/fillers/filler.py as 08:01 AM
    schedule.every(1).day.at("08:01").do(
        run_scrapper,
        path_scrapper=path_scrappers_fillers,
        tittle="Veiculos/Motoristas",
        files=files,
    )
    # executando os arquivos da pasta de pages/fillers/phones.py ás 16:30 PM
    schedule.every(1).day.at("16:45").do(
        run_scrapper,
        path_scrapper=path_scrappers_phones,
        tittle="Telefones",
        files=["phones.csv"],
    )
    # executando os arquivos da pasta de pages/fillers/filler.py ás 17:00 PM
    schedule.every(1).day.at("17:00").do(
        run_scrapper,
        path_scrapper=path_scrappers_fillers,
        tittle="Veiculos/Motoristas",
        files=files,
    )

    while True:
        print(
            f'>> {time.strftime("%X")} aguardando horário correto para envios/scrapper!!',
            end="\r",
        )
        schedule.run_pending()
        time.sleep(1)
