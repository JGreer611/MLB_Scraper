# <p>Import necessary libraries</p>
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
# <p>Import the DataScraper class from the boxscore_scraper module</p>
from boxscore_scraper import DataScraper

# <p>Define a class called Game</p>
class Game:
    # <p>Initialize the class with a game_element as an argument</p>
    def __init__(self, game_element):
        self.game_element = game_element

    # <p>Method to get the date of the game from the game_element</p>
    def get_date(self):
        # <p>Find the previous sibling element with the 'h3' tag</p>
        date_element = self.game_element.find_previous_sibling('h3')
        
        # <p>If a date_element is found, return its text content, otherwise
        #     return None</p>
        if date_element:
            return date_element.text
        else:
            return None

    # <p>Method to get the away team name and its score from the game_element
    # </p>
    # <p><img src="Score_MLBS.png" alt="" width="465" height="37"></p>
    # <p><img src="Score_MLBS_code.png" alt="" width="480" height="207"></p>
    def get_team_scores(self):
        # <p>Find the first 'a' element with an href attribute within the
        #     game_element</p>
        away_element = self.game_element.find('a', href=True)
        
        # <p>If an away_element is found, extract the team name and score</p>
        if away_element:
            # <p>Get the away team name from the text content of the
            #     away_element</p>
            away = away_element.text
            
            # <p>Get the score element by finding the next sibling of
            #     away_element</p>
            score1_element = away_element.next_sibling
            
            # <p>If a score1_element is found, extract the away team's score</p>
            if score1_element:
                away_score_text = score1_element.strip()
                # <p>If the score text is surrounded by parentheses, extract the
                #     score as an integer</p>
                if '(' in away_score_text and ')' in away_score_text:
                    start_index = away_score_text.find('(') + 1
                    end_index = away_score_text.find(')')
                    away_score = int(away_score_text[start_index:end_index])
                else:
                    away_score = None
            else:
                away_score = None
        else:
            away = None
            away_score = None

        # <p>Find all 'a' elements with an href attribute within the
        #     game_element</p>
        home_elements = self.game_element.find_all('a', href=True)
        
        # <p>If there are more than one home_elements, extract the home team
        #     name and score</p>
        if len(home_elements) > 1:
            # <p>Get the home team name from the text content of the second
            #     home_element</p>
            home = home_elements[1].text
            
            # <p>Get the score element by finding the next sibling of the second
            #     home_element</p>
            score2_element = home_elements[1].next_sibling
            
            # <p>If a score2_element is found, extract the home team's score</p>
            if score2_element:
                home_score_text = score2_element.strip()
                # <p>If the score text is surrounded by parentheses, extract the
                #     score as an integer</p>
                if '(' in home_score_text and ')' in home_score_text:
                    start_index = home_score_text.find('(') + 1
                    end_index = home_score_text.find(')')
                    home_score = int(home_score_text[start_index:end_index])
                else:
                    home_score = None
            else:
                home_score = None
        else:
            home = None
            home_score = None
        
        # <p>Get the site element from the third home_element and extract its
        #     href attribute value as the URL</p>
        site_elements = home_elements[2]
        url = site_elements.get('href')
        
        # <p>Return the away team, away score, home team, home score, and URL as
        #     a tuple</p>
        return away, away_score, home, home_score, url

    # <p>Method to determine the winner of the game</p>
    def get_winner(self):
        # <p>Get the team scores and URL using the get_team_scores method</p>
        away_team, away_score, home_team, home_score, site = self.get_team_scores()
        
        # <p>If both home_score and away_score are not None, determine the
        #     winner</p>
        if home_score is not None and away_score is not None:
            if home_score > away_score:
                return 1  # Home team wins
            elif away_score > home_score:
                return 0  # Away team wins
            else:
                return None  # Tie or unknown result
        else:
            return None  # Unable to determine the winner


# <p>Define a class called MLBScraper</p>
class MLBScraper:
    # <p>Initialize the class with a list of URLs as an argument</p>
    def __init__(self, urls):
        self.urls = urls
        # <p>Initialize lists to store scraped data</p>
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

    # <p>Method to scrape the data from the provided URLs</p>
    def scrape(self):
        # <p>Iterate through each URL in the list</p>
        for url in self.urls:
            # <p>Request the URL and get the HTML content</p>
            response = requests.get(url)
            html_content = response.content
            # <p>Parse the HTML content with BeautifulSoup</p>
            soup = BeautifulSoup(html_content, 'html.parser')
            # <p>Find all game elements with the 'p' tag and 'game' class</p>
            games = soup.find_all('p', class_='game')
            # <p>Iterate through each game element</p>
            for game in games:
                # <p>Create a Game object with the game element</p>
                game_obj = Game(game)
                # <p>Get the date, team scores, and winner of the game</p>
                date = game_obj.get_date()
                away_team, away_score, home_team, home_score, site = game_obj.get_team_scores()
                winner = game_obj.get_winner()
                # <p>Construct the box score URL</p>
                url2 = 'https://www.baseball-reference.com' + site
                # <p>Create a DataScraper object with the box score URL</p>
                box = DataScraper(url2)
                # <p>Get weather, field, and hit/error data from the box score
                # </p>
                weather, field, a_hits, a_errors, h_hits, h_errors = box.boxScrape()
                # <p>Append the data to the respective lists</p>
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

                # <p>Wait for 5 seconds before the next request to avoid
                #     overloading the server</p>
                time.sleep(5)

        # <p>Create a dictionary to organize the scraped data</p>
        d = {'Date': self.date_list, 'Weather': self.weather_list, 'Field': self.field_list,
             'Away Team': self.away_team_list, 'Away Score': self.away_score_list, 'Away Hits': self.away_hits_list,
             'Away Errors': self.away_error_list, 'Home Team': self.home_team_list, 'Home Score': self.home_score_list,
             'Home Hits': self.home_hits_list, 'Home Errors': self.home_error_list, 'Winner': self.winner_list}
        # <p>Convert the dictionary to a pandas DataFrame</p>
        df = pd.DataFrame(data=d)
        # <p>Return the DataFrame</p>
        return df

