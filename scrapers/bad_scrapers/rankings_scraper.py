import requests
import json

res = requests.get('https://www.ultimatetennisstatistics.com/rankingsTableTable?current=1&rowCount=-1&sort%5Brank%5D=asc&searchPhrase=&rankType=RANK&season=&date=&_=1744587937303')
res = res.json()

pretty_json = json.dumps(res, indent=4)
# print(pretty_json)

csv = 'rank,pId,name,country,points\n'

print(type(res))

res = res['rows']
print(res)

for player in res:
    print(player)
    rank = player['rank']
    pid = player['playerId']
    name = player['name']
    country = player['country']['id']
    points = player['points']
    row = f'{rank},{pid},{name},{country},{points}\n'
    csv += row

print(csv)

with open('../player_scrapers/rankings.csv', 'w') as w:
    w.write(csv)