import bs4
import requests
import csv


def extract_data(pid: str):
    page = bs4.BeautifulSoup(requests.get(f'https://www.ultimatetennisstatistics.com/playerProfileTab?playerId={pid}').text, 'lxml')

    data_wanted = ['Age','Height','Plays','Backhand']
    player_data = page.select('table')[0].select('tr')
    player_data_dict = {}
    for tr in player_data:
        player_data_dict[tr.select('th')[0].text] = tr.select('td')[0].text
    # print(player_data_dict)

    data_string = ''
    for wanted_data in data_wanted:
        if wanted_data in player_data_dict:
            cur = player_data_dict[wanted_data]
            if wanted_data == 'Age':
                data_string += cur[0:cur.index(' ')]
            elif wanted_data == 'Height':
                data_string += cur[0:cur.index(' ')]
            elif wanted_data == 'Plays':
                data_string += 'r' if cur[0] == 'R' else 'l'
            elif wanted_data == 'Backhand':
                data_string += '2' if cur[0] == 'T' else '1'
        data_string += ','

    return data_string

with open('./rankings.csv', 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)

    result = 'age,height,plays,bh\n'
    for row in csv_reader:
        result += extract_data(row[1]) + '\n'

    with open('./player_data.csv', 'w') as file:
        file.write(result)
