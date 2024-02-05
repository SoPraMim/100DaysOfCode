import os
import smtplib
from email.mime.text import MIMEText
from flight_data import FlightData

RECIPIENTS = [os.environ.get("TO_TEST_EMAIL")]

class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""
    def __init__(self,flights:list[FlightData],user:dict) -> None:
        self.flights = flights
        self.recipients = [user["eMail"]]
        
        message_subject = "New flight deal!!!"
        message_body = self.build_message_body()
        self.send_mail(subject=message_subject,body=message_body,recipients=self.recipients)

    def send_mail(self,subject: str, body: str, recipients: list):
        """Send an email using the test email account."""
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
                to_addrs=msg['To'],
                msg=msg.as_string()
            )
            
    def build_message_body(self):
        body = f"{len(self.flights)} new flight"
        if len(self.flights) == 1:
            body += " was found!\n"
        elif len(self.flights) > 1:
            body += "s were found!\n"
            
        for flight in self.flights:
            body += f"\nOnly {flight.price} EUR to fly from {flight.cityFrom}({flight.cityCodeFrom}) to {flight.cityFrom}({flight.cityCodeFrom}).\n"
            body += f"Fly from {flight.utc_departure_date} {flight.utc_departure_time} until {flight.utc_departure_date} {flight.utc_departure_time}!\n"
            body += f"Don't miss the deal. Follow the link to know more:\n"
            body += f"{flight.deep_link}\n"
            
        return body