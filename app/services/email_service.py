import smtplib
from email.message import EmailMessage
import os
import ssl
import threading


import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.host = os.getenv("EMAIL_HOST")
        self.port = int(os.getenv("EMAIL_PORT",587))
        self.username = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.from_addr = os.getenv("EMAIL_FROM")

    def send_email(self,to:str,subject:str,body:str):
        msg = EmailMessage()
        msg['From'] = self.from_addr
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(self.host, self.port, timeout=10) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.send_message(msg)
        except Exception as e:
            logger.exception("Email sending failed", extra={"to": to, "subject": subject})

    
    def send_email_async(self,to, subject, body):
        thread = threading.Thread(
            target=self.send_email,
            args=(to, subject, body),
            daemon=True
        )
        thread.start()
