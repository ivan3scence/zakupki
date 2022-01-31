import mimetypes
import smtplib
from email.mime.text import MIMEText as mimes
from email.mime.multipart import MIMEMultipart as mult
from email.mime.base import MIMEBase
from email import encoders
import datetime

def send_email(filename):
    date = '.'.join(datetime.date.today().strftime("%d/%m/%Y").split('/')) 
    mess = f"Добый день, отправляю контракты за {date}.\n\nИван"
    subtype = "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    sender = "ivan.gorichenk@gmail.com"
    password = "Vadimovich2001"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        server.login(sender, password)
        msg = mult()
        msg.attach(mimes(mess))
        msg["Subject"] = "Контракты"
        msg["To"] = "ivan.gorich@gmail.com"
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(filename, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'%(filename))
        msg.attach(part)

        server.sendmail(sender, "ivan.gorich@gmail.com", msg.as_string())
        return "Email was successfuly sent!\n"
    except Exception as _ex:
        return f"{_ex}\n Check yr login or pass!\n"
# send_email("zakupki_29_01_2022.xlsx")