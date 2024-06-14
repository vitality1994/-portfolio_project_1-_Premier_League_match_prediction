# necessary packages
import requests
import json
from common_functions import get_season_ids

def get_player_ids():

    url = "https://footballapi.pulselive.com/football/players?pageSize=10&altIds=true&type=player"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Sec-Fetch-Mode': 'cors',
        'Host': 'footballapi.pulselive.com',
        'Origin': 'https://www.premierleague.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://www.premierleague.com/',
        'Sec-Fetch-Dest': 'empty',
    }

    season_ids = list(get_season_ids().keys())

    all_player_ids = []
    all_player_names = []

    for season_id in season_ids:

        for page_num in list(range(1000000)):

            params = {
                'page':page_num,
                'compSeasons': int(season_id)
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 404:
                print(response.status_code)
                return None
            
            try:

                # check 
                response.json()

                if len(response.json()['content'])!=0:

                    response = response.json()

                else:
                    print('No more players for current season.')
                    break

            except requests.exceptions.JSONDecodeError:
                return None

            
            player_ids = list(map(lambda x: int(x['id']), response['content']))
            player_names = list(map(lambda x: x['name']['display'], response['content']))

            all_player_ids+=player_ids
            all_player_names+=player_names

            print(f'Season id: {season_id}')
            print(f'Page num: {page_num}')
            print(f'{len(all_player_ids)} of ids were collected.')
            print()
    
    player_id_name = dict(zip(all_player_ids, all_player_names))


    with open('./data/player_data/players_ids_names.json', 'w') as file:
        json.dump(player_id_name, file, indent=4)




if __name__ == '__main__':

    get_player_ids()
