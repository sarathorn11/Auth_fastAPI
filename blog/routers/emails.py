
import smtplib
from typing import List
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_mail(subject:str,recipient: List, messages:str):
    HOST= "smtp.gmail.com"
    PORT = 587
    FROM_EMAIL = "sarathorn27@gmail.com"
    TO_EMAIL = recipient[0]
    PASSWORD = "x p g c a b c a c f f u l b o m"  #getpass.getpass("Enter password: ")

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = FROM_EMAIL
    message["To"] = TO_EMAIL
    message["Cc"] = FROM_EMAIL
    message["Bcc"] = FROM_EMAIL

    html_part = MIMEText(messages,"html")
    message.attach(html_part)
 
    smtp = smtplib.SMTP(HOST, PORT)

    status_code,response = smtp.ehlo()
    print(f"[*] Echoing the server: {status_code} {response}")

    status_code,response = smtp.starttls()
    print(f"[*] Starting TLS connection: {status_code} {response}")

    status_code,response = smtp.login(FROM_EMAIL,PASSWORD)
    print(f"[*] Logging in: {status_code} {response}")

    smtp.sendmail(FROM_EMAIL,TO_EMAIL,message.as_string())
    smtp.quit()
   