from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main.vacancy_model import Vacancy, DATABASE_URL

# Создаем движок для подключения к базе данных
engine = create_engine(DATABASE_URL, echo=True)

# Создаем фабрику сессий для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_vacancy(data_dict):
    # Открываем сессию
    session = SessionLocal()
    try:
        # Создаем объект вакансии
        new_vacancy = Vacancy(**data_dict)
        # Добавляем его в сессию
        session.add(new_vacancy)
        # Фиксируем изменения в базе данных
        session.commit()
    except Exception as e:
        # В случае ошибки откатываем изменения
        session.rollback()
        print(f"Error creating vacancy: {e}")
    finally:
        # Закрываем сессию
        session.close()
