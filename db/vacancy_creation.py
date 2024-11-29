from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.vacancy_model import Vacancy, DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_vacancy(data_dict):
    session = SessionLocal()
    try:
        new_vacancy = Vacancy(**data_dict)
        session.add(new_vacancy)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error creating vacancy: {e}")
    finally:
        session.close()
