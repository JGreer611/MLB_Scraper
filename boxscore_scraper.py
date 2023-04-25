import requests
from bs4 import BeautifulSoup

# <p>Define a class called BoxScore</p>
class BoxScore:
    # <p>Initialize the class with a box_element as an argument</p>
    def __init__(self, box_element):
        self.box_element = box_element

    # <p>Method to get the weather and field conditions from the box_element</p>
    # <p>Here's a picture of the table and code I need to scrape to gather the
    #     time of day and the type of field</p>
    # <p><img src="Time_Field_MLBS.png" alt="" width="257" height="137"></p>
    # <p><img src="Time_Field_code.png" alt="" width="366" height="192"></p>
    def get_weather(self):
        # <p>Find the element with class 'scorebox_meta' in box_element</p>
        time_elements = self.box_element.find(class_='scorebox_meta')
        # <p>Find all 'div' elements within the time_elements</p>
        weather_element = time_elements.find_all('div')
        
        # <p>If there are more than one 'div' elements, extract the text from
        #     the sixth 'div' element (index 5)</p>
        if len(weather_element) > 1:
            time_element = weather_element[5].text
        
        # <p>Remove leading and trailing whitespaces from the extracted text</p>
        conditions = time_element.strip()
        
        # <p>Check if 'Night' or 'Day' is present in the conditions string and
        #     set the time variable accordingly</p>
        if 'Night' in conditions:
            time = 'Night'
        elif 'Day' in conditions:
            time = 'Day'
        else:
            time = ''
        
        # <p>Check if 'grass' or 'turf' is present in the conditions string and
        #     set the field variable accordingly</p>
        if 'grass' in conditions:
            field = 'Grass'
        elif 'turf' in conditions:
            field = 'turf'
        else:
            field = ''
        
        # <p>Return a tuple containing the time and field variables</p>
        return time, field


    # <p>Method to get the hits and errors for both away and home teams</p>
    # <p>Here's a picture of the table and code I need to scrape to gather hits
    #     and errors</p>
    # <p><img src="boxscoreMLBS.png" alt="" width="512" height="132"></p>
    # <p><img src="boxscore_code_MLBS.png" alt="" width="233" height="290"></p>
    def getHitError(self):
        # <p>Find the element with class 'linescore nohover stats_table
        #     no_freeze' in box_element</p>
        boxscore_elements = self.box_element.find(class_='linescore nohover stats_table no_freeze')
        
        # <p>Find all 'tr' elements within the boxscore_elements</p>
        boxscore_element = boxscore_elements.find_all('tr')
        
        # <p>Extract the heading row (first row) and find all 'th' elements
        #     within it</p>
        heading = boxscore_element[0]
        heading_elements = heading.find_all('th')
        
        # <p>Define a tag string to search for the hits ('H') column</p>
        tag = '<th>H</th>'
        indices = 0
        
        # <p>Loop through the heading_elements, and find the index of the 'H'
        #     column</p>
        for i, d in enumerate(heading_elements):
            if tag == str(d):
                indices = i
                break
        
        # <p>Extract the away team row (second row) and find all 'td' elements
        #     within it</p>
        away_team = boxscore_element[1]
        at_elements = away_team.find_all('td')
        
        # <p>Get the hits and errors for the away team using the indices found
        #     earlier</p>
        away_hits = int(at_elements[indices].string.strip())
        away_errors = int(at_elements[indices+1].string.strip())

        # <p>Extract the home team row (third row) and find all 'td' elements
        #     within it</p>
        home_team = boxscore_element[2]
        ht_elements = home_team.find_all('td')
        
        # <p>Get the hits and errors for the home team using the indices found
        #     earlier</p>
        home_hits = int(ht_elements[indices].string.strip())
        home_errors = int(ht_elements[indices+1].string.strip())
        
        # <p>Return a tuple containing the away team's hits and errors, and the
        #     home team's hits and errors</p>
        return away_hits, away_errors, home_hits, home_errors



# <p>Define a class called DataScraper</p>
class DataScraper:
    # <p>Initialize the class with a list of URLs as an argument</p>
    def __init__(self, urls):
        self.urls = urls
        self.home_lineup_list = []
        self.away_lineup_list = []
        self.away_stat_list = []
        self.home_stat_list = []

    # <p>Method to scrape box score information from the given URL</p>
    def boxScrape(self):
        # <p>Get the URL from the instance variable</p>
        url = self.urls

        # <p>Send an HTTP request to the URL and get the content</p>
        response = requests.get(url)
        html_content = response.content

        # <p>Parse the HTML content using BeautifulSoup</p>
        soup = BeautifulSoup(html_content, 'html.parser')

        # <p>Create a BoxScore object with the parsed HTML content</p>
        box_obj = BoxScore(soup)

        # <p>Get the weather and field conditions using the BoxScore object's
        #     get_weather method</p>
        time, field = box_obj.get_weather()

        # <p>Get the hits and errors for both teams using the BoxScore object's
        #     getHitError method</p>
        a_hits, a_errors, h_hits, h_errors = box_obj.getHitError()

        # <p>Return the scraped data as a tuple</p>
        return time, field, a_hits, a_errors, h_hits, h_errors

