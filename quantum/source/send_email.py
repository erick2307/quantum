import os
import smtplib
import params as par
from email.message import EmailMessage

def SendMail(
    HOST=par.SERVER_HOST,
    PORT=par.PORT,
    SENDER=par.EMAIL,
    PASSWORD=par.EMAIL_PWD,
    RECIPIENT=par.EMAIL,
    MESSAGE="Your simulation has finished",
):
    server = smtplib.SMTP(host=HOST, port=PORT)
    server.starttls()
    server.login(user=SENDER, password=PASSWORD)
    msg = create_message(TEXT=MESSAGE)
    try:
        server.sendmail(SENDER, RECIPIENT, MESSAGE)
        server.quit()
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")
    return

def create_message(
    SUBJECT="##Simulation##",
    FROM=par.EMAIL,
    TO=par.EMAIL,
    TEXT="Your simulation has finished",
):
    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = FROM
    msg["To"] = TO
    msg.set_content(TEXT)
    return msg

if __name__ == "__main__":
    pwd = os.environ.get(par.EMAIL_PWD)
    SendMail(PASSWORD=pwd)
