import os
import smtplib


def SendMail(
    HOST="mail.irides.tohoku.ac.jp",
    PORT=587,
    SENDER="mas@irides.tohoku.ac.jp",
    PASSWORD=None,
    RECIPIENT="mas@irides.tohoku.ac.jp",
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
    pwd = os.environ.get("IRIDES_EMAIL_PWD")
    SendMail(PASSWORD=pwd)
