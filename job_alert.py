import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def fetch_indeed_jobs():
    url = "https://www.indeed.com/jobs?q=devops+OR+sre+OR+cloud+engineer+OR+linux+administrator&explvl=entry_level"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs_24h = []
    jobs_3d = []

    for card in soup.select("a.tapItem"):
        title = card.select_one("h2.jobTitle").get_text(strip=True)
        company = card.select_one("span.companyName").get_text(strip=True)
        location = card.select_one("div.companyLocation").get_text(strip=True)
        date = card.select_one("span.date").get_text(strip=True).lower()
        link = "https://www.indeed.com" + card["href"]

        job_html = f"""
        <b>{title}</b><br>
        🏢 {company}<br>
        📍 {location}<br>
        📅 {date}<br>
        🔗 {link}View Job</a><br><br>
        """

        if "just posted" in date or "today" in date or "1 day" in date:
            jobs_24h.append(job_html)
        elif "2 day" in date or "3 day" in date:
            jobs_3d.append(job_html)

    return jobs_24h, jobs_3d

def fetch_naukri_jobs():
    url = "https://www.naukri.com/devops-sre-cloud-engineer-linux-administrator-jobs-0-to-3-years"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs_24h = []
    jobs_3d = []

    for job in soup.select("article.jobTuple"):
        title_tag = job.select_one("a.title")
        company_tag = job.select_one("a.subTitle")
        location_tag = job.select_one("li.location")
        date_tag = job.select_one("span.job-post-day")
        if title_tag and company_tag and location_tag and date_tag:
            posted = date_tag.text.strip().lower()
            job_html = f"""
            <b>{title_tag.text.strip()}</b><br>
            🏢 {company_tag.text.strip()}<br>
            📍 {location_tag.text.strip()}<br>
            📅 {posted}<br>
            🔗 {title_tag[View Job</a><br><br>
            """
            if "today" in posted or "just now" in posted or "1 day" in posted or "1d" in posted:
                jobs_24h.append(job_html)
            elif "2 day" in posted or "2d" in posted or "3 day" in posted or "3d" in posted:
                jobs_3d.append(job_html)

    return jobs_24h, jobs_3d

def send_email(jobs_24h, jobs_3d):
    sender_email = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver_email = sender_email

    message = MIMEMultipart("alternative")
    message["Subject"] = "🛠️ DevOps/SRE Job Alerts (0–3 Years)"
    message["From"] = sender_email
    message["To"] = receiver_email

    html_content = "<html><body>"
    html_content += "<h2>🕒 Jobs Posted in Last 24 Hours</h2><br>"
    html_content += "".join(jobs_24h) if jobs_24h else "<p>No jobs found in the last 24 hours.</p><br>"
    html_content += "<hr><h2>📅 Jobs Posted in Last 3 Days</h2><br>"
    html_content += "".join(jobs_3d) if jobs_3d else "<p>No jobs found in the last 3 days.</p><br>"
    html_content += "</body></html>"

    part = MIMEText(html_content, "html")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == "__main__":
    indeed_24h, indeed_3d = fetch_indeed_jobs()
    naukri_24h, naukri_3d = fetch_naukri_jobs()
    jobs_24h = indeed_24h + naukri_24h
    jobs_3d = indeed_3d + naukri_3d
    send_email(jobs_24h, jobs_3d)
