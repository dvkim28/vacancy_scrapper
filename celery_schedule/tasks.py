import os
import sys
import time
import random
import requests
from celery import Celery, shared_task
from dotenv import load_dotenv
from datetime import timedelta

from scrapping.general import get_list_of_vacancies

load_dotenv()

WORK_UA_URL = os.getenv("WORK_UA_URL")
BASE_URL = os.getenv("WORK_UA_URL_BASE_URL")
CHAT_ID = os.environ.get("CHAT_ID")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

REDIS_CONNECTION_STRING = os.environ.get("REDIS_CONNECTION_STRING")

app = Celery("tasks", broker=REDIS_CONNECTION_STRING)

app.conf.update(
    broker_connection_retry_on_startup=True,
    broker_url=REDIS_CONNECTION_STRING,
    result_backend=REDIS_CONNECTION_STRING,
    task_track_started=True,
    timezone="UTC",
    beat_schedule={
        "get-full-page-url-every-10-seconds": {
            "task": "tasks.fetch_vacancies",
            "schedule": timedelta(seconds=10),
        },
    },
)

if not all([WORK_UA_URL, BASE_URL, CHAT_ID, BOT_TOKEN]):
    missing_vars = [
        var
        for var in [
            "WORK_UA_URL",
            "BASE_URL",
            "CHAT_ID",
            "BOT_TOKEN",
        ]
        if not globals().get(var)
    ]
    raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")


@shared_task
def fetch_vacancies():
    from scrapping.scrapping_work_ua import get_new_vacancies, parse_single_vacancy

    print("Start fetching vacancies...")
    url = WORK_UA_URL
    while url:
        try:
            vacancies, next_pj = get_new_vacancies(url)
            if not vacancies:
                break
            db_vacancies = get_list_of_vacancies()

            for vac in vacancies:
                link_tag = vac.find("a")
                if link_tag:
                    link = link_tag.attrs.get("href")
                    vacancy_url = BASE_URL + link
                    if vacancy_url not in db_vacancies:
                        print(f"{vacancy_url} is new, parsing...")
                        parse_single_vacancy(vacancy_url)
                        time.sleep(random.uniform(2, 5))
                    else:
                        print(f"Vacancy {vacancy_url} already parsed.")

        except Exception as e:
            print(f"Error during scraping: {e}")

        if next_pj:
            url = BASE_URL + next_pj
            print(f"Next page: {url}")
        else:
            break

    print("Scraping finished.")


@shared_task
def send_telegram_message(vac_data: dict):
    if not BOT_TOKEN or not CHAT_ID:
        print("BOT_TOKEN or CHAT_ID is not set.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = (
        f"There is new vacation: {vac_data['title']}\n"
        f"Platform: {vac_data['source']}\n"
        f"Company: {vac_data['company']}\n"
        f"Description: {vac_data['description']}\n"
        f"Link: {vac_data['url']}"
    )

    params = {"chat_id": CHAT_ID, "text": message}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(f"Message sent: {vac_data['title']}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}, response: {response.text if response else 'No response'}")
