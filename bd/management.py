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
    existing_vacancies = [vac.source for vac in session.query(Vacancy.source).all()]

    return existing_vacancies
