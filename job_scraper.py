import requests
from bs4 import BeautifulSoup

def fetch_naukri_jobs():
    url = "https://www.naukri.com/devops-sre-jobs"
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
            🔗 <a href="{title_tag['href']}br>
            """
            if "today" in posted or "just now" in posted or "1 day" in posted or "1d" in posted:
                jobs_24h.append(job_html)
            elif "2 day" in posted or "2d" in posted or "3 day" in posted or "3d" in posted:
                jobs_3d.append(job_html)

    return jobs_24h, jobs_3d

def save_jobs(jobs_24h, jobs_3d):
    with open("job_listings.txt", "w", encoding="utf-8") as f:
        f.write("<html><body>")
        f.write("<h2>🕒 DevOps/SRE Jobs Posted in Last 24 Hours</h2><br>")
        f.write("".join(jobs_24h) if jobs_24h else "<p>No jobs found in the last 24 hours.</p><br>")
        f.write("<hr><h2>📅 DevOps/SRE Jobs Posted in Last 3 Days</h2><br>")
        f.write("".join(jobs_3d) if jobs_3d else "<p>No jobs found in the last 3 days.</p><br>")
        f.write("</body></html>")

if __name__ == "__main__":
    jobs_24h, jobs_3d = fetch_naukri_jobs()
    save_jobs(jobs_24h, jobs_3d)
``
