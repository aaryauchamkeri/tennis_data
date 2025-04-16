import bs4
import requests

soup = bs4.BeautifulSoup(requests.get('https://www.atptour.com/en/rankings/singles').text, 'html.parser')
pt1 = soup.select('tbody')[1].select('tr')

output = 'id,name,age,points\n'

i = 0
for player in pt1:
    if player.select('.name'):
        playerRow = player.select('.name')[0]
        info = playerRow.select('a')[0]
        data = info['href'][12:]
        ind = data.index('/') + 1
        id = data[ind:ind+4]
        name = playerRow.select('a')[0].select('span')[0].text
        age = player.select('.age')[0].text
        points = player.select('.points')[0].select('a')[0].text.strip()
        output += f'{id},{name},{age},{points}\n'


print(output)

with open('./rankings.csv', 'w') as file:
    file.write(output)