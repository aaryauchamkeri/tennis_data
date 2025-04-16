
corrected = ''
with open('../player_data.csv', 'r') as file:
    rows = file.read().split('\n')
    corrected += rows[0] + '\n'
    for row in rows[1:]:
        corrected += row[0:-1] + '\n'

    with open('../player_data.csv', 'w') as file:
        file.write(corrected)