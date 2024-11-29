Vacancy Scrapper
This project is a web scraper designed to fetch and process job vacancies from the Work.ua website. Once processed, it sends notifications about new vacancies directly to your Telegram account via a bot.

Features
Scrapes job listings from Work.ua
Processes and filters retrieved data
Checks for new vacancies not already in the database
Sends notifications for new vacancies through a Telegram bot
Getting Started

Prerequisites
You'll need Python 3 and the following libraries installed:
```
Alembic
Amqp
Beautiful Soup 4
Billiard
Black
Celery
... (full list omitted for brevity)
Installation
```

Clone the Repository:
```
git clone https://github.com/your_project_link
cd vacancy_scrapper'''
```
Create and Activate a Virtual Environment:

For Linux/Mac:
```
python3 -m venv .venv
source .venv/bin/activate
```
For Windows:
```

python -m venv .venv
.\venv\Scripts\activate
```
Install Dependencies:
```
pip install -r requirements.txt
```
Configure Environment Variables:

Create 1  a file named .env in the project's root directory and add the following lines, replacing the placeholders with your information:  

```
WORK_UA_URL="https://example.com/vacancies"
WORK_UA_URL_BASE_URL="https://example.com"
REDIS_CONNECTION_STRING="redis://:password@localhost:6379/0"
CHAT_ID="your_telegram_chat_id"
BOT_TOKEN="your_telegram_bot_token"
```
Running the Project

Start Redis Server:

If already installed, use the following command:

```
redis-server
```
Run Celery Worker:
This process handles tasks like scraping and processing:

```
celery -A tasks worker --loglevel=INFO
```
Run Celery Beat Scheduler:
This schedules the scraping task to run periodically:

```
celery -A tasks beat -l info
```
How it Works

The fetch_vacancies task scrapes job listings from the specified Work.ua URL.
The retrieved data is processed and filtered.
The script checks the database for existing vacancies.
If a new vacancy is found, the send_telegram_message task triggers, sending a notification to your Telegram chat using the configured bot.
Scheduling Tasks

The beat_schedule configuration within the Celery Beat settings determines the frequency of the scraping task. This can be adjusted to your preference.

Troubleshooting

Ensure all dependencies are correctly installed using pip install -r requirements.txt.
Verify that Redis is running and accessible via the provided connection string.
Double-check the Telegram bot credentials and URLs in your .env file.