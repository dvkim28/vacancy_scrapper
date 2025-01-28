import os
import random
import re
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from bd.management import add_vacancy_record, get_all_vacancies

load_dotenv()

WORK_UA_URL = "https://www.work.ua"
WORK_UA_VAC = os.getenv("WORK_UA_VAC")


def parse_work_ua(url: None):
    if url:
        all_vacancies = []
        next_pg = True
        while next_pg:
            try:
                time.sleep(random.uniform(0.1, 1))
                response = requests.get(url)
                if response.status_code == 200:  # Добавлена проверка на успешный ответ
                    soup = BeautifulSoup(response.text, "html.parser")
                    vacancies = soup.find_all("div", {"class": "card"})
                    all_vacancies.extend(vacancies)
                    next_pg = get_next_page(soup)
                    if next_pg:
                        url = WORK_UA_URL + next_pg
                    else:
                        break
                else:
                    print(
                        f"Failed to retrieve page {url}"
                        f" with status code {response.status_code}"
                    )
                    break
            except Exception as e:
                print(f"Error during request: {e}")
                break
        return get_single_vacancy(all_vacancies)


def get_next_page(soup):
    pagination = soup.find("ul", {"class": "pagination"})
    if pagination:
        next_page = pagination.find("li", {"class": "add-left-default"})
        if next_page:
            link_tag = next_page.find("a")
            if link_tag:
                link = link_tag.get("href")
                return link
    return None


def get_single_vacancy(soup):
    list_vacancies = []
    for vac in soup:
        try:
            get_link = vac.find("h2").find("a").get("href")
            if get_link:
                vacancy_link = WORK_UA_URL + get_link
                vac_dict = parse_single_vacancy(vacancy_link)
                list_vacancies.append(vac_dict)
        except Exception:
            print(f"Error parsing: {get_link}")
    return add_record_to_bd(list_vacancies)


def parse_single_vacancy(vacancy_link):
    time.sleep(random.uniform(0.1, 1))
    response = requests.get(vacancy_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
    vac = {
        "title": "",
        "source": vacancy_link,
        "description": "",
        "date": "",
        "company": "",
        "location": "",
        "salary": "",
    }
    try:
        title = soup.find("h1")
        vac["title"] = title.get_text(strip=True) if title else "Title not find"

        description = soup.find("div", {"class": "company-description"})
        vac["description"] = (
            description.get_text(strip=True) if description else "Description not found"
        )

        date = soup.find("time")
        vac["date"] = date.get("datetime") if date else "Date not found"

        company_block = soup.find("span", {"title": re.compile(r"Дані про компанію")})
        if company_block:
            vac["company"] = (
                company_block.next_sibling.get_text(strip=True)
                if company_block
                else "Company not found"
            )
        else:
            vac["company"] = "Company not found"

        location_span = soup.find("span", {"title": re.compile(r"Місце роботи")})
        if not location_span:
            location_span = soup.find("span", {"title": re.compile(r"Адреса роботи")})
        if location_span and location_span.next_sibling:
            vac["location"] = location_span.next_sibling.get_text(strip=True)
        else:
            vac["location"] = "Location not found"

        salary_sections = soup.find_all("span", string=re.compile(r"грн"))
        if salary_sections:
            for section in salary_sections:
                salary_text = section.get_text(strip=True)
                salary_text = salary_text.replace("\u202f", " ")
                salary_text = salary_text.replace("\xa0", " ")
                salary_text = salary_text.replace("\u2009", " ")
                vac["salary"] = salary_text
        else:
            vac["salary"] = "Salary not found"
    except Exception as e:
        print(e)
    return vac


def add_record_to_bd(list):
    existing_vacancies = get_all_vacancies()
    new_records = [
        vac
        for vac in list
        if (vac["title"], vac["company"], vac["description"]) not in existing_vacancies
    ]

    if new_records:
        for record in new_records:
            add_vacancy_record(record)


if __name__ == "__main__":
    parse_work_ua(WORK_UA_VAC)
