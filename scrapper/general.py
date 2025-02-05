import random
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from scrapper.djinni import (authorization_on_djinni, create_full_dic,
                             get_python_vacs, parse_djinni_vacs)
from scrapper.dou import parse_dou
from scrapper.work_ua import add_record_to_bd, parse_work_ua

UserAgent = ("Mozilla/5.0 (Linux; Android 6.0; "
             "Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36")

load_dotenv()


def start_parse_process():
    parse_dou()
    parse_work_ua()
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={UserAgent}")
    chrome_options.add_argument("--headless")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        authorization_on_djinni(driver)
        job_links = get_python_vacs(driver)

        vac_list = []
        for link in job_links:
            time.sleep(random.randint(2, 3))
            vac_page, url = parse_djinni_vacs(link, driver)
            vac_list.append((vac_page, url))

        vacancies = create_full_dic(vac_list)
        add_record_to_bd(vacancies)

    finally:
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    start_parse_process()
