import os
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

DJINNI = os.getenv("DJINNI")
DJINNI_VAC_URLS = os.getenv("DJINNI_VAC_URLS")


def authorization_on_djinni(driver, url=None):
    if url is None:
        url = DJINNI

    print(f"Opening URL: {url}")
    driver.get(url)

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        password_input = driver.find_element(By.ID, "password")
        dj_user = os.environ.get("DJINNI_USER")
        dj_password = os.environ.get("DJINNI_PASS")
        email_input.send_keys(dj_user)
        password_input.send_keys(dj_password)
        password_input.send_keys(Keys.ENTER)

        print("Успешно авторизовались!")
        time.sleep(2)
    except Exception as e:
        print(f"Ошибка при авторизации: {e}")


def get_python_vacs(driver):
    driver.get(DJINNI_VAC_URLS)
    all_pages_html = ""
    next_page = True

    while next_page:
        all_pages_html += driver.page_source
        try:
            next_button = driver.find_element(
                By.CSS_SELECTOR, ".bi.bi-chevron-right.page-item--icon"
            )
            next_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Ошибка или нет кнопки: {e}")
            next_page = False
    return get_soup(all_pages_html)


def get_soup(all_pages_html):
    soup = BeautifulSoup(all_pages_html, "html.parser")
    job_links = []
    job_items = soup.find_all("a", class_="job-item__title-link")

    for job_item in job_items:
        link = job_item.attrs.get("href")
        if link:
            job_links.append(link)
    return job_links


def parse_djinni_vacs(link, driver):
    url = "https://djinni.co" + link  # Формируем полный URL вакансии
    driver.get(url)
    return driver.page_source, url  # Возвращаем HTML-страницу и URL


def create_full_dic(vac_list):
    vacs = []

    for idx, (page, url) in enumerate(vac_list, start=1):
        vac = {}
        soup = BeautifulSoup(page, "html.parser")

        vac["source"] = url

        try:
            vac["title"] = soup.find("h1").get_text(strip=True)
        except Exception as e:
            print(f"Ошибка при парсинге title: {e}")
            vac["title"] = None

        try:
            vac["description"] = soup.find(
                "div", {"class": "mb-4 job-post__description"}
            ).get_text(strip=True)
        except Exception as e:
            print(f"Ошибка при парсинге description: {e}")
            vac["description"] = None

        try:
            date_section = soup.find("div", {"id": "job-publication-info"})
            if date_section:
                date = date_section.find("div").find("span").get_text(strip=True)
                vac["date"] = date if date else None
            else:
                vac["date"] = None
        except Exception as e:
            print(f"Ошибка при парсинге даты: {e}")
            vac["date"] = None

        try:
            company_section = soup.find("div", {"class": "col"}).find(
                "a", {"class": "text-reset"}
            )
            vac["company"] = (
                company_section.get_text(strip=True) if company_section else None
            )
        except Exception as e:
            print(f"Ошибка при парсинге компании: {e}")
            vac["company"] = None

        try:
            salary_section = soup.find("h1").find("span").find("span")
            if salary_section:
                vac["salary"] = salary_section.get_text()
            else:
                vac["salary"] = None
        except Exception as e:
            print(f"Ошибка при парсинге компании: {e}")
            vac["salary"] = None

        vac["location"] = "Remote"

        vacs.append(vac)

    return vacs
