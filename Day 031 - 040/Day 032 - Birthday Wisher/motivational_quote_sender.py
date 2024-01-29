# --- Imports --- #
import datetime as dt
import smtplib
from email.mime.text import MIMEText
import random
import os

# --- Variables --- #
ROOT = "Day 031 - 040/Day 032 - Birthday Wisher/"
recipients = [os.environ.get("TO_TEST_EMAIL")]

# --- Functions --- #
def send_mail(subject, body, recipients):
    """Send an email using the andrediastest@gmail.com account."""
    user = os.environ.get("FROM_TEST_EMAIL")
    password = os.environ.get("FROM_TEST_EMAIL_PASSWORD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 465


    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL(smtp_server,smtp_port) as smtp_connection:
        smtp_connection.login(user=user, password=password)
        smtp_connection.sendmail(
            from_addr=user,
            to_addrs=os.environ.get("TO_TEST_EMAIL"),
            msg=msg.as_string()
        )
        
# --- Program --- #
if __name__ == "__main__":
    now = dt.datetime.now()
    if now.weekday() == 3:
        with open(ROOT + "quotes.txt", "r") as file:
            quotes = file.readlines()
            quote = random.choice(quotes)
        
        send_mail("Motivational quote",quote, recipients)
        print("Quote sent.")
