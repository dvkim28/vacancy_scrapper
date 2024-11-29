import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()

Base = declarative_base()

class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    company = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    url = Column(String, nullable=False)
    source = Column(String, nullable=True)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
