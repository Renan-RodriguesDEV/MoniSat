import datetime
from email import encoders
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import time
from dotenv import load_dotenv

load_dotenv()

from_address = os.getenv("EMAIL")
password = os.getenv("PASSWD")
to_address = os.getenv("ADDRESS")


def send_email(
    subject="MoniSat email automático",
    body="",
    _from=from_address,
    _to=to_address,
    passwd=password,
    dir_files=os.path.join(os.getcwd(), "data"),
    files: list = [],
):
    msg = MIMEMultipart()

    msg["Subject"] = subject
    msg["From"] = _from
    msg["To"] = _to

    msg.attach(MIMEText(body, "HTML"))

    if not os.path.exists(dir_files):
        print(f'>> {time.strftime("%X")} O diretório {dir_files} não existe.\n')
        return

    for file in os.listdir(dir_files):
        print(f">> {time.strftime('%X')} Acessando os arquivos em {dir_files}\n")
        if files and file in files:
            with open(os.path.join(dir_files, file), "rb") as f:
                attachment = MIMEBase("application", "octet-stream")
                attachment.set_payload(f.read())
                encoders.encode_base64(attachment)

                attachment.add_header(
                    "Content-Disposition",
                    f"attachment; filename={file}",
                )
                msg.attach(attachment)
                print(
                    f'>> {time.strftime("%X")} arquivo adicionado a menssagem "{file}"\n'
                )
    __send_email(_from, _to, passwd, msg.as_string())


def __send_email(_from, _to, passwd, email_message):
    # with smtplib.SMTP("smtp-mail.outlook.com", 587) as smtp_server: #TODO: envios com outlook.com
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
        print(
            f""">> {time.strftime('%X')} subindo o servidor de email de: "{_from} - {passwd}"\n"""
        )
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(_from, passwd)
        smtp_server.sendmail(_from, _to, email_message)
    print(f""">> {time.strftime('%X')} email enviado para: "{_to}\n""")


if __name__ == "__main__":
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
        subject="Email automatico MoniSat (Veiculos)",
        body=body,
        _from=from_address,
        _to=to_address,
        passwd=password,
        dir_files=os.path.join(os.getcwd(), "data"),
        files=["reboques.csv"],
    )
