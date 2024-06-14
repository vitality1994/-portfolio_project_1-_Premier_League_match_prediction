import json
import warnings

import pandas as pd
import numpy as np

import lightgbm as lgb
from sklearn.metrics import classification_report, \
                            confusion_matrix, \
                            accuracy_score

import warnings
warnings.filterwarnings("ignore")


def read_jsonl_file(path):
    json_lines = []
    with open(path, 'r') as f:
        for line in f:
            json_lines.append(json.loads(line.strip()))
    return json_lines


def get_df_for_lightGBM(matches, merged_data):

    x = []
    y = []

    df = pd.DataFrame()

    match_results = []

    for match in matches:

        if match['season']=='2023_24':

            print(match['season'])

            match_results.append(match['match_result'])

            list_att_home = {}
            list_att_away ={}

            home_atts_count = {}
            away_atts_count = {}

            for idx, player_id in enumerate(match['home_players']):

                str_id = str(player_id)

                # try:
                #     print(merged_data[str_id]['official_data']['entity']['name'])
                # except:
                #     print('no matching')

                try:
                    for fm_att_name, fm_att_value in merged_data[str_id]['FM_data']['attributes'].items():

                        if f'home_{fm_att_name}' not in list_att_home.keys():

                            list_att_home[f'home_{fm_att_name}'] = fm_att_value
                            home_atts_count[f'home_{fm_att_name}'] = 1
                        
                        else:

                            list_att_home[f'home_{fm_att_name}'] += fm_att_value
                            home_atts_count[f'home_{fm_att_name}'] += 1
                except:
                    None

            
            for idx, player_id in enumerate(match['away_players']):
                
                str_id = str(player_id)

                # try:
                #     print(merged_data[str_id]['official_data']['entity']['name'])
                # except:
                #     print('no matching')

                try:
                    for fm_att_name, fm_att_value in merged_data[str_id]['FM_data']['attributes'].items():

                        if f'away_{fm_att_name}' not in list_att_away.keys():

                            list_att_away[f'away_{fm_att_name}'] = fm_att_value
                            away_atts_count[f'away_{fm_att_name}'] = 1
                        else:

                            list_att_away[f'away_{fm_att_name}'] += fm_att_value    
                            away_atts_count[f'away_{fm_att_name}'] += 1            
                except:
                    None

            


            home_att_dict = {}
            away_att_dict = {}

            for key, value in list_att_home.items():
                
                att_count = home_atts_count[key]

                avg_att_value = value/att_count

                home_att_dict[key] = avg_att_value

            for key, value in list_att_away.items():

                att_count = away_atts_count[key]

                avg_att_value = value/att_count

                away_att_dict[key] = avg_att_value


            all_data = {**home_att_dict, **away_att_dict}

            match_df = pd.DataFrame([all_data])
            df = pd.concat([df, match_df], ignore_index=True)


            print(len(df.columns))



    



    df['match_results'] = match_results

    return df




if __name__ == '__main__':

    matches = read_jsonl_file('/Users/jooyong/github_locals/portfolio_project_1_Premier_League_match_prediction/Experiments/litghGBM/team_ids_player_ids.jsonl')
    
    with open('/Users/jooyong/github_locals/portfolio_project_1_Premier_League_match_prediction/merge_pre_process_player_data/data/merged_player_data_2.json') as f:
        dataset = json.load(f)

    df = get_df_for_lightGBM(matches, dataset)
    df = df.replace(np.nan, 0)
    df = df.dropna()

    print(df.shape)

    X_train = df[:-80].drop('match_results', axis=1)
    y_train = df[:-80]['match_results']

    X_test = df[-80:].drop('match_results', axis=1)
    y_test = df[-80:]['match_results']    

    lr = lgb.LGBMClassifier()
    lr.fit(X=X_train, y=y_train)
    pred = lr.predict(X_test)

    accuracy = accuracy_score(y_test, pred)
    conf_matrix = confusion_matrix(y_test, pred)
    class_report = classification_report(y_test, pred)

    print("Accuracy:", accuracy)
    print("Confusion Matrix:\n", conf_matrix)
    print("Classification Report:\n", class_report)

    
