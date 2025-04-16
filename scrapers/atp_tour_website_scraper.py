import json

from bs4 import BeautifulSoup
import requests

res = requests.get('https://www.atptour.com/en/scores/archive/brisbane/339/2025/results')
soup = BeautifulSoup(res.text, 'lxml')

match_divs = soup.select('div .match-cta')

matches = []

for match in match_divs:
    matchId = str(match.select('a')[1])[-25:-11]
    matchJsonLink = 'https://www.atptour.com/-/Hawkeye/MatchStats/Complete/' + matchId
    response = requests.get(matchJsonLink)
    matches.append(response.json())

jsonString = json.dumps(matches)

with open('match_data/brisbane_unprocessed.json', 'w') as file:
    file.write(jsonString)
