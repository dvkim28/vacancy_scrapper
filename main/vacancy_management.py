from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main.vacancy_model import DATABASE_URL


engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

