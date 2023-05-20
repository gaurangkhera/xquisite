from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

s = requests.session()
url = s.get('https://www.hindustantimes.com/cricket/ipl/points-table', headers=headers).text
bs = BeautifulSoup(url, 'html.parser')
table = bs.find('table', class_='medalsTally')

team_data = []
for row in table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) > 1:
        index = cells[0].text
        team_name_element = cells[1].find('span', class_='fullName whiteColorText')
        wins_element = cells[3]
        losses_element = cells[4]
        points_element = cells[8]
        
        team_name = team_name_element.text.strip() if team_name_element else None
        wins = wins_element.text.strip() if wins_element else None
        losses = losses_element.text.strip() if losses_element else None
        points = points_element.text.strip() if points_element else None
        
        team_data.append({'Index': index, 'Team': team_name, 'Wins': wins, 'Losses': losses, 'Points': points})

