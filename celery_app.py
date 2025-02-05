from celery import Celery
from celery.schedules import crontab

app = Celery(
    "config",
    broker="redis://default:YRUxTOoEReluZmHr1Jisb39mwPpF1M16"
           "@redis-11736.c90.us-east-1-3.ec2.redns.redis-cloud.com:11736/0",
    backend="redis://default:YRUxTOoEReluZmHr1Jisb39mwPpF1M16"
            "@redis-11736.c90.us-east-1-3.ec2.redns.redis-cloud.com:11736/0",
    include=["tasks"],
)

app.conf.update(
    result_expires=3600,
    beat_schedule={
        "send-telegram-message-every-30-minutes": {
            "task": "scrapper.general.start_parse_process",
            "schedule": crontab(minute="*/30"),
        },
    },
)
