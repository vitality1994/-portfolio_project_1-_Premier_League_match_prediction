import ast
import json
import os
import time
from glob import glob
from typing import Dict, List
import requests
from lxml import etree, html
from common_functions import get_season_ids




def read_lines(file_path: str) -> List[str]:
    lines = []
    with open(file_path, 'r') as inf:
        for line in inf:
            lines.append(line.rstrip('\n'))
    return lines




def crawl_match_details(match_id: int) -> Dict:
    # ## OVERRIDE
    # match_id = 66712
    match_url = f'https://www.premierleague.com/match/{match_id}'
    print(match_url)
    page = requests.get(match_url)
    content = html.fromstring(page.content)

    try:
        details = content.xpath('//div[@class="mcTabsContainer"]')[0]
        details = details.get('data-fixture')
        details = json.loads(details)
    except:
        return None
    
    return details



if __name__ == '__main__':

    season_no_to_season_year = get_season_ids()

    for season_no, season_year in zip(list(season_no_to_season_year.keys())[19:]
                                      , list(season_no_to_season_year.values())[19:]):

        season_splitted = season_year.split('/')
        season_first = season_splitted[0]
        season_second = season_splitted[1]
    
        season = os.path.join('./data/match_data/match_generals/', f'season_{season_first}_{season_second}.json')
        with open(f'./data/match_data/match_details/{season[:-5]}.details.json', 'w') as f:
            print(season_year)
            season_name = os.path.basename(season)[7:-5]
            print(season_name)
            matches = read_lines(season)
            #matches = set(matches)
            for match in matches:
                match = ast.literal_eval(match)
                match['id'] = int(match['id'])
                details = crawl_match_details(match['id'])
                f.write(f'{details}\n')
