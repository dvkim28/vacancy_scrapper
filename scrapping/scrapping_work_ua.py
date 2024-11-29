import os
import random
import re
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from celery_schedule.tasks import send_telegram_message
from db.vacancy_creation import create_vacancy

load_dotenv()

WORK_UA_URL = os.getenv("WORK_UA_URL")
BASE_URL = os.getenv("WORK_UA_URL_BASE_URL")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/116.0.5845.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko)"
    " Firefox/95.0 Safari/537.36",
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept": "text/html,application/xhtml+xml,"
    "application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers",
}


def get_new_vacancies(url=None):
    if url is None:
        url = WORK_UA_URL
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        vacancies = soup.find_all(name="div", class_=re.compile(r"card.*wordwrap"))
        next_pj = get_next_page(soup)
        return vacancies, next_pj
    except Exception as e:
        print(f"Error fetching vacancies: {e}")
        return None, None


def get_next_page(page):
    try:
        next_pj = (
            page.find(name="li", class_="no-style add-left-default")
            .find("a")
            .attrs.get("href")
        )
        return next_pj
    except Exception as e:
        print(f"Error finding next page: {e}")
        return None


def parse_single_vacancy(vacancy_url):
    try:
        response = requests.get(vacancy_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.text if title_tag else "Title not found"

        company_tag = soup.find(name="a", class_="inline")
        company = (
            company_tag.find(name="span", class_="strong-500").text
            if company_tag
            else "Company not found"
        )

        description_tag = soup.find(name="div", class_="company-description")
        description = (
            description_tag.text if description_tag else "Description not found"
        )

        created_at_tag = soup.find(name="time")
        created_at = created_at_tag.attrs.get("datetime", "Date not found")[:10]

        vac_data = {
            "title": title,
            "url": vacancy_url,
            "company": company,
            "description": description,
            "created_at": created_at,
            "source": BASE_URL,
        }
        create_vacancy(vac_data)
        send_telegram_message(vac_data)

    except Exception as e:
        print(f"Error parsing vacancy {vacancy_url}: {e}")
