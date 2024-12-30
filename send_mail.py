from time import sleep
from flask_mail import Message
from extensions import mail
import smtplib


def send_email(to, subject, html_body):
    retries = 3 
    for attempt in range(retries):
        try:
            msg = Message(subject, recipients=[to])
            msg.html = html_body
            mail.send(msg)
            print(f"Email sent successfully to {to}")
            break  
        except smtplib.SMTPServerDisconnected as e:
            print(f"SMTPServerDisconnected: {e}, retrying in 5 seconds... (Attempt {attempt + 1}/{retries})")
            sleep(5)  
        except Exception as e:
            print(f"Failed to send email: {e}")
            break  
