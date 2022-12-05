import os
import smtplib
import params as par

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
    try:
        server.sendmail(SENDER, RECIPIENT, MESSAGE)
        server.quit()
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")


if __name__ == "__main__":
    pwd = os.environ.get(par.EMAIL_PWD)
    SendMail(PASSWORD=pwd)
