import smtplib
from email.mime.text import MIMEText

my_email = "andrediastest@gmail.com"
password = "qsua mtfd klmx jgfz"
smtp_server = "smtp.gmail.com"
smtp_port = 465

recipient = 'andrediastest@yahoo.com'
subject = "Hello"
body = "This is the body of my email"

msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = my_email
msg['To'] = recipient

with smtplib.SMTP_SSL(smtp_server,smtp_port) as smtp_connection:
    smtp_connection.login(user=my_email, password=password)
    smtp_connection.sendmail(
        from_addr=my_email,
        to_addrs="andrediastest@yahoo.com",
        msg=msg.as_string()
    )
print("Email sent")