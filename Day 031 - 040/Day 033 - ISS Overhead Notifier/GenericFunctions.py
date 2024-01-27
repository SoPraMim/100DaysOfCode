# Required imports:
import os

# Generic variables:
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Generic functions:
def cls(): 
    """Clears the terminal."""
    os.system('cls' if os.name=='nt' else 'clear') #check OS and gives the proper command
    
def set_y_or_n(text):
    """Checks the user input for 'y' or 'n' and returns True or False."""
    while True:
        true_or_false = input(text).lower()
        if true_or_false in "yn" and len(true_or_false)==1:
            break
    if true_or_false == "y":
        true_or_false = True
    if true_or_false == "n":
        true_or_false = False
    return true_or_false

def send_mail(subject, body, recipients):
    """Send an email using the andrediastest@gmail.com account."""
    if not isinstance(recipients,list):
        raise TypeError("Recipients must be a list.")
    user = "andrediastest@gmail.com"
    password = "qsua mtfd klmx jgfz"
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
            to_addrs="andrediastest@yahoo.com",
            msg=msg.as_string()
        )