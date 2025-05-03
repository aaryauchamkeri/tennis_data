import requests
import bs4


soup = bs4.BeautifulSoup(requests.get('https://tennisabstract.com/reports/atp_elo_ratings.html').text, 'lxml')
playerData = soup.select('#reportable')[0].select('tbody')[0].select('tr')
# print(len(playerData))

csv = 'er,name,age,elo,her,he,cer,ce,ger,ge\n'

for row in playerData:
    td = row.select('td')
    name = td[1].select('a')[0].text
    csv += f'{td[0].text},{name},{td[2].text},{td[3].text},{td[5].text},{td[6].text},{td[7].text},{td[8].text},{td[9].text},{td[10].text}\n'


with open('./elo.csv', 'w') as file:
    file.write(csv)
