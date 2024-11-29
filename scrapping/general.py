from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.vacancy_model import DATABASE_URL

from db.vacancy_model import Vacancy

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()


def get_list_of_vacancies():
    try:
        existing_vacancies = session.query(Vacancy).all()
        existing_urls = [vacancy.url for vacancy in existing_vacancies]
        return existing_urls
    except Exception as e:
        print(e)
        return [], None
