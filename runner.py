import os
import time
import schedule
import subprocess

BASE_PATH_SCRIPTS = (
    "C:\\Users\\User\\OneDrive\\Documentos\\Python Projects\\MoniSat\\main\\"
)
path_email = os.path.join(BASE_PATH_SCRIPTS, "emails", "email_sender.py")


def run_email(path_email):
    if not os.path.exists(path_email):
        print(f'>> {time.strftime('%X')} Arquivo inexistente "{path_email}"')
        return
    try:
        subprocess.run(["python", path_email])
        print(f'>> {time.strftime("%X")} Arquivo executado com sucesso ({path_email})')
    except Exception as e:
        print(f">> {time.strftime('%X')} {str(e)}")


def run_scrapper(path_scrapper):
    if not os.path.exists(path_scrapper):
        print(f'>> {time.strftime('%X')} Arquivo inexistente "{path_scrapper}"')
        return
    try:
        subprocess.run(["python", path_scrapper])
        print(
            f'>> {time.strftime("%X")} Arquivo executado com sucesso ({path_scrapper})'
        )
        run_email(path_email)
    except Exception as e:
        print(f">> {time.strftime('%X')} {str(e)}")


if __name__ == "__main__":

    path_scrappers_fillers = os.path.join(BASE_PATH_SCRIPTS, "pages", "fillers")
    path_scrapper_grid = os.path.join(BASE_PATH_SCRIPTS, "pages", "grid", "gridSat.py")
    path_scrapper_home = os.path.join(BASE_PATH_SCRIPTS, "pages", "home", "scrapper.py")

    # executando os arquivos da pasta de pages/grid
    schedule.every(30).minutes.do(run_scrapper, path_scrapper=path_scrapper_grid)

    # executando os arquivos da pasta de pages/home
    schedule.every(30).minutes.do(run_scrapper, path_scrapper=path_scrapper_home)

    # executando os arquivos da pasta de pages/fillers ás 17:00 PM
    for file in os.listdir(path_scrappers_fillers):
        if file not in ["__init__.py"] and file.endswith(".py"):
            schedule.every(1).day.at("17:00").do(
                run_scrapper, path_scrapper=os.path.join(path_scrappers_fillers, file)
            )

    # executando os arquivos da pasta de pages/fillers as 07:00 AM
    for file in os.listdir(path_scrappers_fillers):
        if file not in ["__init__.py"] and file.endswith(".py"):
            schedule.every(1).day.at("07:00").do(
                run_scrapper, path_scrapper=os.path.join(path_scrappers_fillers, file)
            )

    while True:
        schedule.run_pending()
        time.sleep(1)
