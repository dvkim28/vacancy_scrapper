import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URI = os.getenv("DATABASE_URI")
engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Vacancy(Base):
    __tablename__ = "Vacancy"
    id = Column(Integer, primary_key=True)
    source = Column(String)
    title = Column(String)
    description = Column(String)
    date = Column(String)
    company = Column(String)
    location = Column(String)
    salary = Column(String, nullable=True)


Base.metadata.create_all(engine)


vacancies = session.query(Vacancy).all()
session.close()
