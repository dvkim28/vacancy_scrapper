import os
from celery import Celery
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

REDIS_CONNECTION_STRING = os.environ.get("REDIS_CONNECTION_STRING")

app = Celery("tasks", broker=REDIS_CONNECTION_STRING)

app.autodiscover_tasks(["celery_schedule", "scrapping"])

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
