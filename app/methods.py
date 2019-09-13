import requests
import http.client
import json
from bs4 import BeautifulSoup
import re

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
headers = {'User-Agent': user_agent}


class Crawler:

    def trade_spider(self, home_team, away_team):
        scores = []
        full_time = []
        url = 'http://wildstat.com/p/2301/ch/all/club1/'+home_team+'/club2/'+away_team
        #url = 'http://wildstat.com/p/2301/ch/all/club1/ENG_Liverpool_FC/club2/ENG_Arsenal_London'
        source_code = requests.get(url, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for stats in soup.findAll('span', id=re.compile("score_")):
            for full_score in stats.findAll('b'):
                full_time.append(full_score.text)
        return full_time

    def get_price(url):
        source_code = requests.get(url, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for item in soup.findAll('div', {'class': 'price'}):
           return item.string

    def get_countries(url):
        countries = {}
        source_code = requests.get(url, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for item in soup.find_all('div', {'class': 'dmn-left-g'}):
            for country in item.find_all('a', href=True):
                countries[re.sub('[^A-Za-z0-9]+', '', item.text)] = re.sub('[^A-Za-z0-9]+', '', country['href'])[1:]
        return countries

    def get_leagues(url):
        leagues = {}
        class_list = ['smn-left-g', 'smn-left-w', 'smn-left-gn']
        source_code = requests.get(url, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for item in soup.find_all('div', class_=class_list):
            for league in item.find_all('a', href=True):
                leagues[re.sub('[^A-Za-z0-9]+', '', item.text)] = re.sub('[^A-Za-z0-9]+', '', league['href'])[1:]
        return leagues

    def get_years(url):
        years = {}
        source_code = requests.get(url, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for item in soup.find_all('a', {'class': 'year'}):
            years[re.sub('[^A-Za-z0-9]+', '', item.text)] = item['href']
        return years

    def get_club(url):
        clubs = {}
        source_code = requests.get(url, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for item in soup.find_all('table', {'class': 'championship'}):
            for tr in item.find_all('tr'):
                for td in tr.find_all('td', {'align': 'left'}):
                    for a in td.find_all('a', href=True):
                        if not str.isdigit(a.text) and not re.match("^[0-9.]*$", a.text):
                            clubs[a.text] = a['href']
        return clubs

    def get_week(url):
        weeks = {}
        source_code = requests.get(url, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for div in soup.find_all('div', {'class': 'tour'}):
            for item in div('select', {'class': 'toursel'}):
                for option in item.find_all('option'):
                    weeks[option.text] = option['value']
        return weeks

    def get_week_club(url):
        clubs = {}
        source_code = requests.get(url, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for item in soup.find_all('table', {'class': 'championship'}):
            for tr in item.find_all('tr'):
                for td in tr.find_all('td', {'align': 'left'}):
                    for a in td.find_all('a', href=True):
                        if not str.isdigit(a.text) and not re.match("^[0-9.]*$", a.text):
                            clubs[a.text] = a['href']
        return clubs

    def get_table(url):
        clubs = []
        source = requests.get(url, headers=headers)
        plain_text = source.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for item in soup.find_all('table', {'class': 'championship'}):
            for tr in item.find_all('tr'):
                data = []
                for td in tr.find_all('td'):
                    if td.text:
                        data.append(td.text)
                if data:
                    data.pop(0)
                    if len(data) == 18:
                        data.pop(7)
                    clubs.append(data)
            break
        return clubs[2:]

    def f(f_a):
        list=f_a.split('-')
        return int(list[0])

    def a(f_a):
        list=f_a.split('-')
        return int(list[1])


class FootballAPI:
    def get_data(self):
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': 'b62b5ab1be29464ba47452d9fff08380'}
        connection.request('GET', '/v2/competitions/2021/matches?season=2018', None, headers)
        response = json.loads(connection.getresponse().read().decode())
        return response
