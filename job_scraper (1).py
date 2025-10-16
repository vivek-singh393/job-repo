import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_indeed_jobs():
    url = "https://www.indeed.com/jobs?q=devops+OR+sre&fromage=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    for div in soup.find_all(name="div", attrs={"class":"job_seen_beacon"}):
        title = div.find("h2", {"class": "jobTitle"})
        company = div.find("span", {"class": "companyName"})
        location = div.find("div", {"class": "companyLocation"})
        link = div.find("a", href=True)
        if title and company and location and link:
            job = {
                "title": title.text.strip(),
                "company": company.text.strip(),
                "location": location.text.strip(),
                "link": "https://www.indeed.com" + link["href"]
            }
            jobs.append(job)
    return jobs

def save_jobs(jobs, filename="job_listings.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for job in jobs:
            f.write(f"{job['title']} at {job['company']} ({job['location']})\n{job['link']}\n\n")

if __name__ == "__main__":
    jobs = fetch_indeed_jobs()
    save_jobs(jobs)
