import ast
import json
import os
from glob import glob
from typing import List


def read_lines(file_path: str) -> List[str]:
    lines = []
    with open(file_path, 'r') as inf:
        for line in inf:
            lines.append(line.rstrip('\n'))
    return lines


def create_features_for_single_sample(match):
    match = ast.literal_eval(match)
    
    home_id = match['teamLists'][0]['teamId']
    away_id = match['teamLists'][1]['teamId']
    assert match['teams'][0]['team']['id'] == home_id
    assert match['teams'][1]['team']['id'] == away_id
    home_score = int(match['teams'][0]['score'])
    away_score = int(match['teams'][1]['score'])
    if home_score > away_score:
        match_result = 2
    elif home_score == away_score:
        match_result = 1
    else:
        match_result = 0
    home_players = []
    away_players = []
    for player in match['teamLists'][0]['lineup']:
        player_id = player['id']
        home_players.append(player_id)
    for player in match['teamLists'][1]['lineup']:
        player_id = player['id']
        away_players.append(player_id)
    if len(home_players) != 11 or len(away_players) != 11:

        return None
    return {'home_id': home_id, 'away_id': away_id, 'match_result': match_result, 'home_players': home_players, 'away_players': away_players}




if __name__ == '__main__':
    # one-hot encode clubs
    with open('/Users/jooyong/github_locals/portfolio_project_1_Premier_League_match_prediction/Premier_League_official_data/data/match_data/teams_ids_names.json', 'r') as f:
        all_clubs = json.load(f)

    with open('/Users/jooyong/github_locals/portfolio_project_1_Premier_League_match_prediction/Premier_League_official_data/data/player_data/players_ids_names.json', 'r') as f:
        players = json.load(f)

    season_matches = glob(os.path.join('/Users/jooyong/github_locals/portfolio_project_1_Premier_League_match_prediction/Premier_League_official_data/data/match_data', 'season_*.details.json'))
    season_matches = sorted(season_matches)
    
    season_samples = {}
    all_samples = []
    for season_match in season_matches[15:]:

        matches = read_lines(season_match)
        season_name = os.path.basename(season_match)
        season_name = season_name.replace('season_', '').replace('.details.json', '')
        print(season_name)
        season_samples[season_name] = []
        for match in matches:
            sample = create_features_for_single_sample(match)
            if sample is not None:
                season_samples[season_name].append(sample)
                sample['season'] = season_name
                all_samples.append(sample)


    with open(f'./team_ids_player_ids.jsonl', 'w') as f:
        for sample in all_samples:
            f.write(f'{json.dumps(sample)}\n')