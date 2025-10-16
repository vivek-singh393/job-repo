import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    sender_email = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver_email = sender_email

    with open("job_listings.txt", "r", encoding="utf-8") as f:
        job_content = f.read()

    message = MIMEMultipart("alternative")
    message["Subject"] = "🛠️ Daily DevOps/SRE Job Alerts"
    message["From"] = sender_email
    message["To"] = receiver_email

    part = MIMEText(job_content, "html")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == "__main__":
    send_email()
