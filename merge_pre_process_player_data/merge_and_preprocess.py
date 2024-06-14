import re
import json
import numpy as np
from difflib import SequenceMatcher
import ast
from fuzzywuzzy import fuzz

# Precompile regex for efficiency
number_extractor = re.compile(r'\d+')


def fm_player_pre_processing(data):

    fm_inside_total = {}

    # Cache and reuse these properties for performance
    keys_interest = {'Height', 'Caps / Goals', 'Weight', 'Sell value', 'Wages', 'Unique ID'}

    for player in data:

        max_atts = 20
        max_role_val = 100

        attributes = {attr: float(level) / max_atts for attr, level in zip(player['attribute'], player['level'])}
        other_info = dict(zip(player['player_other_info_keys'], player['player_other_info_values']))
        

        main_roles = {
            role_key: round(float(role_val) / max_role_val, 3)
            for role_key, role_val in zip(player['player_main_roles_keys(suitable)'], player['player_main_roles_values(suitable)'])
        }

        # Processing selective keys for number extraction
        for key in keys_interest:

            if key in other_info:

                if key == 'Caps / Goals':

                    Caps_Goals = other_info[key].split('/')
                    Caps = Caps_Goals[0]
                    Goals = Caps_Goals[1]

                    Caps_value = number_extractor.findall(Caps)[0]
                    Goals_value = number_extractor.findall(Goals)[0]

                    if Caps_value:
                        other_info['Caps'] = float(Caps_value)

                    if Goals_value:
                        other_info['Goals'] = float(Goals_value)   

                    del other_info['Caps / Goals'] 

                else:
                    value = number_extractor.findall(other_info[key].replace(',', ''))
                    if value:
                        other_info[key] = float(value[0])
        
        # Standardizing data structure
        fm_inside = {
            'attributes': attributes,
            'main roles': main_roles,
            'ability': float(player['ability']) / 100,
            'potential': float(player['potential']) / 100 if player['potential'] is not None else None,
            'club_team': player['club_team'],
            'nationality': player['nationality'],
            'age': float(player['age']),
            'positions': player['positions'],
            **other_info
        }

        fm_inside_total[player['name']] = fm_inside

    return fm_inside_total


def are_names_similar(name1, name2, threshold=90):
    # Clean names
    clean_name1 = name1.strip().lower()
    clean_name2 = name2.strip().lower()
    
    # Use fuzzy matching to compare names
    similarity = fuzz.ratio(clean_name1, clean_name2)
    
    return similarity






if __name__ == '__main__':

    # Use context manager to handle files
    with open('/Users/jooyong/github_locals/portfolio_project_1_Premier_League_match_prediction/fm_inside/data/fm_players_stats_2024_1.json') as file:
        fm_raw_data = json.load(file)

    processed_data = fm_player_pre_processing(fm_raw_data)
    
    # with open('/Users/jooyong/github_locals/portfolio_project_1_Premier_League_match_prediction/fm_inside/data/fm_players_stats_2023.json') as file:
    #     fm_raw_data = json.load(file)

    processed_data_2023 = fm_player_pre_processing(fm_raw_data)

    official_data = {}
    with open('/Users/jooyong/github_locals/portfolio_project_1_Premier_League_match_prediction/Premier_League_official_data/data/player_data/all_players_official_stats.json') as f:
        for line in f:
            temp = ast.literal_eval(line.strip().replace("false", "False").replace("true", "True"))
            for key, value in temp.items():
                official_data[key] = value


    processed_data_2 = {}



    for FM_name in list(processed_data.keys()):

        official_data_to_put = {}

        print(FM_name)

        name_similarities = {}


        for official_key, official_value in official_data.items():

            official_name = official_value['all_season']['entity']['name']['display']

            name_similarities[official_key] = are_names_similar(FM_name, official_name)
        
        max_key = max(name_similarities, key=name_similarities.get)
        
        
        print(official_data[max_key]['all_season']['entity']['name']['display'])


        seasons_atts = {}

        for season in official_data[max_key].keys():
                        
            one_season_atts = {}

            for i in official_data[max_key][season]['stats']:
                one_season_atts[list(i.values())[0]] = float(list(i.values())[1])

            seasons_atts[season] = one_season_atts


    
        official_data_to_put['entity']=official_data[max_key]['all_season']['entity']
        
        del official_data[max_key]

        for season, atts in seasons_atts.items():

            official_data_to_put[season] = atts

        temp = processed_data[FM_name]
        processed_data_2[max_key]={}
        processed_data_2[max_key]['FM_data'] = temp
        # processed_data_2[max_key]['FM_data_2023'] = processed_data_2023[FM_name]
        processed_data_2[max_key]['official_data'] = official_data_to_put

    

                

    # Handle file writing
    with open('./data/merged_player_data_2.json', 'w', encoding='utf-8') as file:
        json.dump(processed_data_2, file, ensure_ascii=False, indent=4)
