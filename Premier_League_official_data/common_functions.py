import requests

# Scraped Premier League seasons and those IDs ######
#####################################################

def get_season_ids():

    url = "https://footballapi.pulselive.com/football/competitions/1/compseasons?page=0&pageSize=100"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Sec-Fetch-Mode': 'cors',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.premierleague.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
        'Referer': 'https://www.premierleague.com/',
        'Connection': 'keep-alive',
        'Host': 'footballapi.pulselive.com',
        'Sec-Fetch-Dest': 'empty',
        'account': 'premierleague',
    }

    response = requests.get(url, headers=headers)

    season_id = response.json()['content']

    seasons = list(map(lambda x: x['label'], season_id))
    ids = list(map(lambda x: int(x['id']), season_id))

    season_id_dict = dict(zip(ids[:-1], seasons[:-1]))

    return season_id_dict

#####################################################
#####################################################

if __name__ == '__main__':

    print(get_season_ids())
