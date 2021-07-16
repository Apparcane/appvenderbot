# scraper.py
import requests
from bs4 import BeautifulSoup

res = []


def ongoing_all(pages):
    page = pages

    while True:
        url = 'https://animevost.am/ongoing/page/' + str(page) + "/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        names = soup.find_all('div', class_='shortstoryHead')

        if(len(names)):
            for el in names:
                h = el.find('h2')
                name = h.find('a')
                res.append(name.text + '\n')

        else:
            break
        page += 1

    return res


def ongoing(pages):
    page = pages

    url = 'https://animevost.am/ongoing/page/' + str(page) + "/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    names = soup.find_all('div', class_='shortstoryHead')

    for el in names:
        h = el.find('h2')
        name = h.find('a')
        res.append(name.text + '\n')

    return res
