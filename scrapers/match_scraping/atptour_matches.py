import requests
import bs4
import traceback

soup = bs4.BeautifulSoup(requests.get('https://www.atptour.com/en/scores/results-archive',
                                      headers={
                                          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}).text,
                         'lxml')

links = soup.select('.results')

csv = 'tourney_id,matchId,tourney_name,surface,winner_id,loser_id,best_of,minutes,w_sr,w_rr,w_ace,w_df,w_svpt,w_1stIn,w_1stWon,w_2ndWon,w_SvGms,w_bpSaved,w_bpFaced,'
csv += 'l_sr,l_rr,l_ace,l_df,l_svpt,l_1stIn,l_1stWon,l_2ndWon,l_SvGms,l_bpSaved,l_bpFaced\n'


for link in links:
    split_link = link['href'].split('/')
    tourneyId = split_link[5]
    tourneySoup = bs4.BeautifulSoup(requests.get(f'https://www.atptour.com{link["href"]}').text, 'lxml')
    matches = tourneySoup.select('.match-cta > a:nth-child(2)')  # only need the match link for the match id
    for match in matches:
        matchCommaSplit = match['href'].split('/')
        matchId = matchCommaSplit[-1]
        try:
            link = f'https://www.atptour.com/-/Hawkeye/MatchStats/Complete/2025/{tourneyId}/{matchId}'
            data = requests.get(link).json()

            # print(link)

            tourn_name = data['Tournament']['EventDisplayName']
            surface = data['Tournament']['Court']
            drawSize = data['Tournament']['Singles']
            total_sets = data['Match']['NumberOfSets']
            winnerId = data['Match']['WinningPlayerId'].lower()
            message = data['Match']['Message']

            # still need to find out how to scrape the score properly
            # score = None
            #
            # if message is not None and len(message) > 0:
            #     score = message[message.find('wins the match ') + 15: -1].strip()

            time = None
            try:
                time = data['Match']['PlayerTeam']['SetScores'][0]['Stats']['Time'].split(':')
                time = int(time[0]) * 60 + int(time[1])
            except:
                pass

            overall_player1 = data['Match']['PlayerTeam']['SetScores'][0]['Stats']
            p1_return_data = overall_player1['ReturnStats']
            p1_id = data['Match']['PlayerTeam']['Player']['PlayerId'].lower()
            p1_sr = overall_player1['ServiceStats']['ServeRating']['Number']
            p1_aces = overall_player1['ServiceStats']['Aces']['Number']
            p1_first_serve_in = overall_player1['ServiceStats']['FirstServe']['Dividend']
            p1_first_serve_faults = overall_player1['ServiceStats']['FirstServe']['Divisor'] - p1_first_serve_in
            p1_first_serve_pts_won = overall_player1['ServiceStats']['FirstServePointsWon']['Dividend']
            p1_snd_serve_pts_won = overall_player1['ServiceStats']['SecondServePointsWon']['Dividend']
            p1_serve_total_pts = overall_player1['ServiceStats']['FirstServePointsWon']['Divisor'] + \
                                     overall_player1['ServiceStats']['SecondServePointsWon']['Divisor']
            p1_service_games_played = overall_player1['ServiceStats']['ServiceGamesPlayed']['Number']
            p1_df = overall_player1['ServiceStats']['DoubleFaults']['Number']
            p1_rr = p1_return_data['ReturnRating']['Number']
            p1_bpc = p1_return_data['BreakPointsConverted']['Dividend']
            p1_bpf = p1_return_data['BreakPointsConverted']['Divisor']

            overall_player2 = data['Match']['OpponentTeam']['SetScores'][0]['Stats']
            p2_return_data = overall_player2['ReturnStats']
            p2_id = data['Match']['OpponentTeam']['Player']['PlayerId'].lower()
            p2_sr = overall_player2['ServiceStats']['ServeRating']['Number']
            p2_aces = overall_player2['ServiceStats']['Aces']['Number']
            p2_first_serve_in = overall_player2['ServiceStats']['FirstServe']['Dividend']
            p2_first_serve_faults = overall_player2['ServiceStats']['FirstServe']['Divisor'] - p2_first_serve_in
            p2_first_serve_pts_won = overall_player2['ServiceStats']['FirstServePointsWon']['Dividend']
            p2_snd_serve_pts_won = overall_player2['ServiceStats']['SecondServePointsWon']['Dividend']
            p2_serve_total_pts = overall_player2['ServiceStats']['FirstServePointsWon']['Divisor'] + \
                                     overall_player2['ServiceStats']['SecondServePointsWon']['Divisor']
            p2_service_games_played = overall_player2['ServiceStats']['ServiceGamesPlayed']['Number']
            p2_df = overall_player2['ServiceStats']['DoubleFaults']['Number']
            p2_rr = p2_return_data['ReturnRating']['Number']
            p2_bpc = p2_return_data['BreakPointsConverted']['Dividend']
            p2_bpf = p2_return_data['BreakPointsConverted']['Divisor']
            p2_serve_rating = overall_player2['ServiceStats']['ServeRating']['Number']

            sets_played = len(data['Match']['PlayerTeam']['SetScores']) - 1

            loserId = None
            if winnerId == p1_id:
                loserId = p2_id
            else:
                loserId = p1_id

            tourn_dt = f'{tourneyId},{matchId},{tourn_name},{surface},{winnerId},{loserId},{total_sets},{time},'
            p1_dt = f'{p1_sr},{p1_rr},{p1_aces},{p1_df},{p1_serve_total_pts},{p1_first_serve_in},{p1_first_serve_pts_won},{p1_snd_serve_pts_won},{p1_service_games_played},{p2_bpf - p2_bpc},{p2_bpf},'
            p2_dt = f'{p2_sr},{p2_rr},{p2_aces},{p2_df},{p2_serve_total_pts},{p2_first_serve_in},{p2_first_serve_pts_won},{p2_snd_serve_pts_won},{p2_service_games_played},{p1_bpf - p1_bpc},{p1_bpf},'

            if winnerId == p1_id:
                tourn_dt += p1_dt + p2_dt[0:-1]
            else:
                tourn_dt += p2_dt + p1_dt[0:-1]

            csv += tourn_dt + '\n'
        except Exception as e:
            traceback.print_exc()
            print(e)
            print(f'https://www.atptour.com/-/Hawkeye/MatchStats/Complete/2025/{tourneyId}/{matchId}')  # no data


with open('./matches1.csv', 'w') as file:
    file.write(csv)
