import os

import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(record):
    max_length = 100
    description = record["description"]
    description = " ".join(description)
    if len(description) > max_length:
        short_description = description[:max_length].rsplit(" ", 1)[0] + "..."
    else:
        short_description = description

    if record:
        message = (
            f"{record['title']} at {record['company']}.\n"
            f"Location: {record['location']}\n"
            f"Date posted: {record['date']}\n"
            f"Description: {short_description}\n"
            f"Salary: {record['salary']}\n"
            f"Link: {record['source']}"
        )

        url = (
            f"https://api.telegram.org/bot{TOKEN}"
            f"/sendMessage?chat_id={CHAT_ID}&text={message}"
        )
        requests.get(url)
