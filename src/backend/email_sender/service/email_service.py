import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

def send_email(
    receiver_email: str,
    subject: str,
    body: str
) -> bool:
    try:

        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT')

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            
            if sender_email and sender_password:
                server.login(sender_email, sender_password)

            server.send_message(message)
            
        return True

    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        return False
