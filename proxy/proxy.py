import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv

import requests
import random
load_dotenv()

PROXY_URL = os.environ.get('PROXY_URL')
def get_proxy_list():
    proxy_list = []
    r = requests.get(PROXY_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('tbody')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            first_cell = row.find('td')
            for cell in first_cell:
                proxy_list.append(cell.text)
    else:
        print("Таблица не найдена.")
    return proxy_list
