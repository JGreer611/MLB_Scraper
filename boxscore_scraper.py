import requests
from bs4 import BeautifulSoup


class BoxScore:
    def __init__(self, box_element):
        self.box_element = box_element

    def get_weather(self):
        time_elements = self.box_element.find(class_='scorebox_meta')
        weather_element = time_elements.find_all('div')
        if len(weather_element) > 1:
            time_element = weather_element[5].text
        conditions = time_element.strip()
        if 'Night' in conditions:
            time = 'Night'
        elif 'Day' in conditions:
            time = 'Day'
        else:
            time = ''
        if 'grass' in conditions:
            field = 'Grass'
        elif 'turf' in conditions:
            field = 'turf'
        else:
            field = ''
        return time, field

    def getHitError(self):
        boxscore_elements = self.box_element.find(class_='linescore nohover stats_table no_freeze')
        boxscore_element = boxscore_elements.find_all('tr')
        heading = boxscore_element[0]
        heading_elements = heading.find_all('th')
        tag = '<th>H</th>'
        indices = 0
        for i, d in enumerate(heading_elements):
            if tag == str(d):
                indices = i
                break
        away_team = boxscore_element[1]
        at_elements = away_team.find_all('td')
        away_hits = at_elements[indices]
        away_hits = int(away_hits.string.strip())
        away_errors = at_elements[indices+1]
        away_errors = int(away_errors.string.strip())

        home_team = boxscore_element[2]
        ht_elements = home_team.find_all('td')
        home_hits = ht_elements[indices]
        home_hits = int(home_hits.string.strip())
        home_errors = ht_elements[indices+1]
        home_errors = int(home_errors.string.strip())
        return away_hits, away_errors, home_hits, home_errors


class DataScraper:
    def __init__(self, urls):
        self.urls = urls
        self.home_lineup_list = []
        self.away_lineup_list = []
        self.away_stat_list = []
        self.home_stat_list = []

    def boxScrape(self):
        url = self.urls
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        box_obj = BoxScore(soup)
        time, field = box_obj.get_weather()
        a_hits, a_errors, h_hits, h_errors = box_obj.getHitError()
        return time, field, a_hits, a_errors, h_hits, h_errors
