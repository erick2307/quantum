import smtplib


def SendMail(
    HOST="mail.irides.tohoku.ac.jp",
    PORT=587,
    SENDER="mas@irides.tohoku.ac.jp",
    PASSWORD="mveojrr75c",
    RECIPIENT="mas@irides.tohoku.ac.jp",
    MESSAGE="this is a test",
):
    server = smtplib.SMTP(host=HOST, port=PORT)
    # server.connect(host=HOST, port=PORT)
    # server.ehlo()
    server.starttls()
    # server.ehlo()
    server.login(user=SENDER, password=PASSWORD)
    try:
        server.sendmail(SENDER, RECIPIENT, MESSAGE)
        server.quit()
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")


if __name__ == "__main__":
    SendMail()
