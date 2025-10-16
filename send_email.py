import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    sender_email = os.environ.get("EMAIL_ADDRESS")
    sender_password = os.environ.get("EMAIL_PASSWORD")
    receiver_email = sender_email

    if os.path.exists("job_listings.txt"):
        with open("job_listings.txt", "r", encoding="utf-8") as f:
            job_content = f.read()
    else:
        job_content = "No job listings found."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Daily DevOps/SRE Job Alerts"

    message.attach(MIMEText(job_content, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == "__main__":
    main()
