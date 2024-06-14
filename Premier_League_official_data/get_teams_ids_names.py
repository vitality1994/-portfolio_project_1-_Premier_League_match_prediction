# necessary packages
import requests
import json
from common_functions import get_season_ids

def get_team_ids():

    headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "If-None-Match": 'W/"05ac3e6621db6a928a24fa531d3ef7f17"',
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Sec-Fetch-Mode": "cors",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.premierleague.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Referer": "https://www.premierleague.com/",
    "Connection": "keep-alive",
    "Host": "footballapi.pulselive.com",
    "Sec-Fetch-Dest": "empty",
    "account": "premierleague"
    }

    url = "https://footballapi.pulselive.com/football/teams?pageSize=100&comps=1&altIds=true&page=0"

    season_ids = list(get_season_ids().keys())

    all_team_ids = []
    all_team_names = []

    for season_id in season_ids:

        params = {
            'compSeasons': int(season_id)
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 404:
            print(response.status_code)
            return None
        
        try:
            response = response.json()
        except requests.exceptions.JSONDecodeError:
            continue

        
        team_ids = list(map(lambda x: int(x['id']), response['content']))
        team_names = list(map(lambda x: x['name'], response['content']))

        all_team_ids+=team_ids
        all_team_names+=team_names
    
    team_id_name = dict(zip(all_team_ids, all_team_names))

    with open('./data/match_data/teams_ids_names.json', 'w') as file:
        json.dump(team_id_name, file, indent=4)


if __name__ == '__main__':

    get_team_ids()

