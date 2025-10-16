import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_naukri_jobs():
    url = "https://www.naukri.com/devops-sre-jobs"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    for job_card in soup.select('.jobTuple'):
        title = job_card.select_one('.title').get_text(strip=True)
        company = job_card.select_one('.companyName').get_text(strip=True)
        location = job_card.select_one('.location').get_text(strip=True)
        jobs.append(f"Naukri: {title} at {company} in {location}")
    return jobs

def fetch_ziprecruiter_jobs():
    url = "https://www.ziprecruiter.com/candidate/search?search=DevOps+SRE"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    for job_card in soup.select('.job_content'):
        title_tag = job_card.select_one('.job_title')
        company_tag = job_card.select_one('.company_name')
        location_tag = job_card.select_one('.location')
        if title_tag and company_tag and location_tag:
            title = title_tag.get_text(strip=True)
            company = company_tag.get_text(strip=True)
            location = location_tag.get_text(strip=True)
            jobs.append(f"ZipRecruiter: {title} at {company} in {location}")
    return jobs

def main():
    all_jobs = []
    all_jobs.extend(fetch_naukri_jobs())
    all_jobs.extend(fetch_ziprecruiter_jobs())

    with open("job_listings.txt", "w", encoding="utf-8") as f:
        if all_jobs:
            f.write("\n".join(all_jobs))
        else:
            f.write("No job listings found in the last 24 hours.")

if __name__ == "__main__":
    main()
``
