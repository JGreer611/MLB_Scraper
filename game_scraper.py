# <p>Import the necessary libraries</p>
import time
# <p>Define a class called Game to extract information about a single game from
#     a BeautifulSoup element</p>
class Game:
    def __init__(self, game_element):
        # <p>Constructor for the Game class that takes a BeautifulSoup element
        #     for the game's HTML as an argument</p>
        self.game_element = game_element

    def get_date(self):
        # <p>Method to extract the date of the game</p>
        date_element = self.game_element.find_previous_sibling('h3')  # find the previous sibling h3 element
        if date_element:
            return date_element.text  # return the text of the date element
        else:
            return None  # return None if no date element is found

    def get_team_scores(self):
        # <p>Method to extract the scores of both teams in the game</p>
        away_element = self.game_element.find('a', href=True)  # find the a element for the away team
        if away_element:
            away = away_element.text  # extract the text of the a element
            score1_element = away_element.next_sibling  # find the next sibling element of the a element
            if score1_element:
                away_score_text = score1_element.strip()  # extract the text of the next sibling element and remove leading/trailing whitespace
                if '(' in away_score_text and ')' in away_score_text:  # check if the score is inside parentheses
                    start_index = away_score_text.find('(') + 1  # find the start index of the score inside parentheses
                    end_index = away_score_text.find(')')  # find the end index of the score inside parentheses
                    away_score = int(away_score_text[start_index:end_index])  # extract the numeric value of the score inside parentheses
                else:
                    away_score = None  # set the score to None if it's not inside parentheses
            else:
                away_score = None  # set the score to None if no score element is found
        else:
            away = None  # set the away team name to None if no a element is found
            away_score = None  # set the away team score to None if no a element is found

        # <p>Extract the home team's name and score</p>
        home_elements = self.game_element.find_all('a', href=True)  # find all the a elements for the home team
        if len(home_elements) > 1:
            home = home_elements[1].text  # extract the text of the second a element, assuming it's the home team
            score2_element = home_elements[1].next_sibling  # find the next sibling element of the second a element
            if score2_element:
                home_score_text = score2_element.strip()  # extract the text of the next sibling element and remove leading/trailing whitespace
                if '(' in home_score_text and ')' in home_score_text:  # check if the score is inside parentheses
                    start_index = home_score_text.find('(') + 1  # find the start index of the score inside parentheses
                    end_index = home_score_text.find(')')  # find the end index of the score inside parentheses
                    home_score = int(home_score_text[start_index:end_index])  # extract the numeric value of the score inside parentheses
                else:
                    home_score = None  # set the score to None if it's not inside parentheses
            else:
                home_score = None  # set the score to None if no score element is
        else:
            home = None
            home_score = None
        site_elements = home_elements[2]
        url = site_elements.get('href')
        return away, away_score, home, home_score, url

    def get_winner(self):
        away_team, away_score, home_team, home_score, site = self.get_team_scores()
        if home_score is not None and away_score is not None:
            if home_score > away_score:
                return 1
            elif away_score > home_score:
                return 0
            else:
                return None
        else:
            return None


class MLBScraper:
    def __init__(self, urls):
        self.urls = urls
        self.date_list = []
        self.away_team_list = []
        self.away_score_list = []
        self.home_team_list = []
        self.home_score_list = []
        self.winner_list = []
        self.weather_list = []
        self.field_list = []
        self.home_lineup = []
        self.away_lineup = []
        self.home_stat = []
        self.away_stat = []
        self.home_hits_list = []
        self.home_error_list = []
        self.away_hits_list = []
        self.away_error_list = []

    def scrape(self):
        for url in self.urls:
            response = requests.get(url)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            games = soup.find_all('p', class_='game')
            for game in games:
                game_obj = Game(game)
                date = game_obj.get_date()
                away_team, away_score, home_team, home_score, site = game_obj.get_team_scores()
                winner = game_obj.get_winner()
                url2 = 'https://www.baseball-reference.com' + site
                box = DataScraper(url2)
                weather, field, a_hits, a_errors, h_hits, h_errors = box.boxScrape()
                self.date_list.append(date)
                self.away_team_list.append(away_team)
                self.away_score_list.append(away_score)
                self.home_team_list.append(home_team)
                self.home_score_list.append(home_score)
                self.winner_list.append(winner)
                self.weather_list.append(weather)
                self.field_list.append(field)
                self.home_error_list.append(h_errors)
                self.home_hits_list.append(h_hits)
                self.away_error_list.append(a_errors)
                self.away_hits_list.append(a_hits)

                time.sleep(5)

        d = {'Date': self.date_list, 'Weather': self.weather_list, 'Field': self.field_list,
             'Away Team': self.away_team_list, 'Away Score': self.away_score_list, 'Away Hits': self.away_hits_list,
             'Away Errors': self.away_error_list, 'Home Team': self.home_team_list, 'Home Score': self.home_score_list,
             'Home Hits': self.home_hits_list, 'Home Errors': self.home_error_list, 'Winner': self.winner_list}
        df = pd.DataFrame(data=d)
        return df
