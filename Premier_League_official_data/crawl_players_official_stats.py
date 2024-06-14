# necessary packages
import requests
import json
from typing import List
from common_functions import get_season_ids


# Defined Functions

def read_lines(file_path: str) -> List[str]:
    lines = []
    with open(file_path, 'r') as inf:
        for line in inf:
            lines.append(line.rstrip('\n'))
    return lines


def crawl_players(player_id):
    
    headers = {
        'authority': 'footballapi.pulselive.com',
        'accept': '*/*',
        'accept-language': 'en,ko-KR;q=0.9,ko;q=0.8,fr;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://www.premierleague.com',
        'referer': 'https://www.premierleague.com/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
    }


    params = {
        'comps': '1',
    }

    response = requests.get(f'https://footballapi.pulselive.com/football/stats/player/{player_id}', params=params, headers=headers)
    
    if response.status_code == 404:
        print(response.status_code)
        return None
    try:
        response = response.json()
    except requests.exceptions.JSONDecodeError:
        return None

    results = {'all_season': response}

    # For every season

    season_no_to_season_year = get_season_ids()

    print()

    for season_id, season_name in season_no_to_season_year.items():

        params = {
            'comps': '1',
            'compSeasons': season_id,
        }

        response = requests.get(f'https://footballapi.pulselive.com/football/stats/player/{player_id}', params=params, headers=headers)

        if response.status_code == 404:
            continue
        try:
            response = response.json()
        except requests.exceptions.JSONDecodeError:
            continue

        if 'stats' not in response or len(response['stats']) < 1:
            continue
        
        results[season_id] = response

    return results


if __name__ == '__main__':

    with open('./data/player_data/players_ids_names.json', 'r') as f:
                players = json.load(f)
                players_ids = [int(player) for player in players.keys()]


    with open(f'./data/player_data/all_players_official_stats.json', 'w') as f:
        for i, player_id in enumerate(players_ids[6836:], start=1):
            print(f'{i}/{len(players_ids[6836:])}\t{player_id}')
            result = crawl_players(player_id)
            if result is not None:
                res = {player_id: result}
                f.write(f'{json.dumps(res)}\n')


