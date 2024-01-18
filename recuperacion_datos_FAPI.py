from matplotlib import pyplot as plt
import matplotlib.pyplot as mp
import seaborn as sb
import pandas as pd
import numpy as np
import requests
import time
import os

def barraProgreso(segmento, total, longitud, titulo):
    porcentaje = segmento / total
    completado = int(porcentaje * longitud)
    restante = longitud - completado
    barra = f"{titulo}\n[{'#' * completado}{'-' * restante}{porcentaje:.2%}]"
    return barra

def obtencion_de_datos_score(match_num):
    header = {
        "Authorization": "Basic aXZhbnkyMDA6ZjgzNTYwMjctMWE2Yy00YWU5LTliNjEtMTJkMDJjNjI1Y2Rj",
        'If-Modified-Since': ''
    }
    payload = {}
    test_idk = requests.get(f"https://frc-api.firstinspires.org/v3.0/2023/scores/MXMO/Qualification?matchNumber={match_num}", headers=header, data=payload)
    final_df = pd.DataFrame.from_dict(test_idk.json())
    final_df = final_df["MatchScores"].apply(pd.Series)
    final_df = final_df["alliances"].apply(pd.Series)
    blue_al = final_df[0].apply(pd.Series)
    red_al = final_df[1].apply(pd.Series)
    match_stuff = pd.concat([blue_al, red_al], axis=0)
    match_stuff.reset_index(drop=True,inplace=True)
    return match_stuff

def obtencion_de_datos_match():
    header = {
        "Authorization": "Basic aXZhbnkyMDA6ZjgzNTYwMjctMWE2Yy00YWU5LTliNjEtMTJkMDJjNjI1Y2Rj",
        'If-Modified-Since': ''
    }
    test_idk = requests.get("https://frc-api.firstinspires.org/v3.0/2023/matches/MXMO/Qualification", headers=header)
    final_df = pd.DataFrame.from_dict(test_idk.json())
    final_df = final_df["Matches"].apply(pd.Series)
    teams_stuff = final_df["teams"].apply(pd.Series)
    final_df.drop("teams", axis=1, inplace=True)
    team_list = []
    for i in range(6):
        temp_team = teams_stuff[i].apply(pd.Series)
        temp_team.rename(columns={"teamNumber":i}, inplace=True)
        temp_team = temp_team[i]
        team_list.append(temp_team)
        df_team_info = pd.concat(team_list, axis=1)
    final_df = pd.concat([final_df,df_team_info], axis=1)
    final_df.rename(columns={0:"Red1",1:"Red2",2:"Red3",3:"Blue1",4:"Blue2",5:"Blue3"}, inplace=True)
    final_df.drop(["isReplay", "matchVideoLink", "description", "autoStartTime", "actualStartTime", "tournamentLevel", "postResultTime"], axis=1, inplace=True)
    return final_df
    
def save_match_csv(match_df):
    match_df.to_csv("./API_Output/Los_Matches.csv")

def save_score_of_matches(score_details_df, match):
    score_details_df.to_csv(f"./API_Output/Los_Score_Match_{match}.csv")

#Main
print(f"Bienvenido a la Clean_Scouter_Cyberius\n{'='*30}")
a = input(f"¿Te gustaría empezar la limieza de datos? (Y/N)\n>")
if not ((a == 'Y') | (a == 'y')):
    print(f"No os me voy a ch***** a mi madre, no?\nPa que me empiezas si ni me vas a usar >:(")
    time.sleep(3)
    print(f"Ahora, si me permites, me voy as salir pa que no me molestes")
    exit()

print(f"Recuperando datos usando la FMS...")

matches_df = obtencion_de_datos_match()
save_match_csv(matches_df)
total_cosas = len(matches_df["matchNumber"])+1
for i in matches_df["matchNumber"]:
    os.system("cls")
    print(barraProgreso(i, total_cosas, 50, f"Match {i}"))
    save_score_of_matches(obtencion_de_datos_score(i),i)

print(f"Gracias por usar el programa de limpieza de datos\nNos vemos y recuerda que eres una persona increibla :D")
time.sleep(3)