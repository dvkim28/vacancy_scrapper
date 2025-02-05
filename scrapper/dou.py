import os
import random
import re
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from scrapper.work_ua import add_record_to_bd

chrome_options = Options()
chrome_options.add_argument("--headless")

load_dotenv()

UserAgent = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0;"
                  " Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
}


def parse_dou(url=None):
    driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    more_vac = True
    try:
        if url is None:
            url = os.getenv("DOU_VAC")
            if url is None:
                return
            driver.get(url)
            while more_vac:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                try:
                    more_jobs_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, "Більше вакансій"))
                    )
                    if more_jobs_button.is_displayed():
                        time.sleep(random.randint(2, 3))
                        more_jobs_button.click()
                except Exception as e:
                    print(e)
                    more_vac = False
                finally:
                    get_list_of_vac(driver.page_source)

    except Exception as e:
        driver.quit()
        print(f"Произошла ошибка: {e}")


def get_list_of_vac(page):
    list_vacancies = []
    soup = BeautifulSoup(page, "html.parser")
    links = soup.find_all("a", class_="vt")
    hrefs = [link.get("href") for link in links]
    for link in tqdm(hrefs, desc="Parsing each vac", unit=" vacancy"):
        new_vac = parse_each_vac(link)
        list_vacancies.append(new_vac)
    return add_record_to_bd(list_vacancies)


def parse_each_vac(url):
    vac = {}
    response = requests.get(url, headers=UserAgent)
    soup = BeautifulSoup(response.text, "html.parser")
    if response.status_code == 200:
        vac["source"] = url
        vac["title"] = soup.find("h1").get_text()

        vac["description"] = soup.find("div", {"class": "vacancy-section"}).get_text()
        vac["description"] = re.sub(r"[\n\xa0]+", " ", vac["description"])

        vac["date"] = soup.find("div", {"class": "date"}).get_text(
            separator=" ", strip=True
        )
        company_section = (
            soup.find("div", {"class": "info"}).find("div", {"class": "l-n"}).find("a")
        )
        vac["company"] = company_section.get_text()
        vac["location"] = soup.find("div", {"class": "sh-info"}).find("span").get_text()
        try:
            salary = soup.find("div", {"class": "salary"})
            if salary:
                vac["salary"] = salary
            else:
                vac["salary"] = "No specified"
        except Exception as e:
            print(e)
    return vac


if __name__ == "__main__":
    parse_dou()
