import os
import time

import requests
from groq import Groq
import groq
from dotenv import load_dotenv
from bd.model import Session, Vacancy

load_dotenv()


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CROQ = os.getenv("AI_API_KEY")
client = Groq(
    api_key=CROQ,
)


def get_cover(text: str):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in writing professional cover letters."
                        " Write a concise "
                        "and tailored cover letter (maximum 50 words)"
                        " that highlights only the "
                        "skills and experiences provided by the user"
                        " if skills are relevant, and "
                        "directly addresses the requirements mentioned "
                        "in the job description. Do "
                        "not include any irrelevant information "
                        "or skills not explicitly mentioned "
                        "by the user."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Write a cover letter based on data about me:"
                        f" My name is Dima, and I am "
                        f"a Python Developer with experience "
                        f"in Django and Django Rest Framework "
                        f"(DRF), with one year of commercial experience."
                        f" I have knowledge of HTML "
                        f"and CSS. Also, I used to speak a lot with customers."
                        f" I specialize in "
                        f"designing RESTful APIs and implementing OOP principles. "
                        f"I have an "
                        f"upper-intermediate level of English. "
                        f"I am experienced in relational "
                        f"databases such as MySQL and PostgreSQL."
                        f" My background as a project manager "
                        f"gives me strong knowledge"
                        f" of how to create a product and make it "
                        f"customer-centric and tailored to their needs. "
                        f"I'm not just coding, I'm "
                        f"helping customers achieve their goals. "
                        f"Additionally, I have experience "
                        f"with web scraping and parsing data using "
                        f"Python libraries such as "
                        f"BeautifulSoup and Scrapy. "
                        f"I am also quick to learn new technologies and "
                        f"adapt to new challenges. "
                        f"job description:\n{text}"
                    ),
                },
            ],
            model="mixtral-8x7b-32768",
        )

        return chat_completion.choices[0].message.content
    except groq.RateLimitError as e:
        # Check if the error message is a string
        error_message = str(e)  # Convert to string if it's not

        # Try to extract the retry time from the error message
        if "retry after" in error_message.lower():
            retry_time_str = (
                error_message.split("retry after")[-1].strip().replace("s", "")
            )
            retry_time = float(retry_time_str)

            print(f"Rate limit exceeded, retrying in {retry_time} seconds.")
            time.sleep(retry_time)  # Wait before retrying

            # Retry the request after the pause
            return get_cover(text)
        else:
            # If the error is not related to rate limits, print the error message
            print(f"Unexpected error: {error_message}")
            return None
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")
        return None


def send_telegram_message(record):
    answr = get_cover(record.description)
    message = f"I recommend this for {record.title}:" f"{answr}"
    url = (
        f"https://api.telegram.org/bot{TOKEN}"
        f"/sendMessage?chat_id={CHAT_ID}&text={message}"
    )
    requests.get(url)


def get_vac_from_bd():
    session = Session()
    existing_vacancies = session.query(Vacancy).limit(10).all()
    return existing_vacancies


if __name__ == "__main__":
    vacancies = get_vac_from_bd()
    for vacancy in vacancies:
        send_telegram_message(vacancy)
