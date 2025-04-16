import requests
import json

matches = []
cnt = 1
while True:
    try:
        r = requests.get(
            f'https://ultimatetennisstatistics.com/tournamentEventsTable?current={cnt}&rowCount=100&sort%5Bdate%5D=desc&searchPhrase=&season=&level=&surface=&indoor=&speed=&tournamentId=&_=1742878577234')
        cnt += 1
        if len(r.json()['rows']) == 0: break
        for match in r.json()['rows']:
            matches.append(match)
    except:
        break

data = json.dumps(matches)

with open('../match_data/matches.json', 'w') as file:
    file.write(data)


