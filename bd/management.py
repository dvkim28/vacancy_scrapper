from bd.model import Session, Vacancy


def add_vacancy_record(dic):
    session = Session()
    try:
        vac = Vacancy(**dic)
        session.add(vac)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        return dic


def get_all_vacancies():
    session = Session()
    existing_vacancies = set(
        (vac.title, vac.company, vac.description, vac.date)
        for vac in session.query(
            Vacancy.title, Vacancy.company, Vacancy.description, Vacancy.date
        ).all()
    )
    return existing_vacancies
