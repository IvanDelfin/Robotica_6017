from matplotlib import pyplot as plt
import matplotlib.pyplot as mp
import seaborn as sb
import pandas as pd
import numpy as np
import time
import math
import os

def obtencion_de_datos():
    dfMatches = pd.read_csv("Tabla Por Match.csv")
    dfPromedioPorEquipo = pd.read_csv("Promedios_Equipos.csv")
    return dfMatches, dfPromedioPorEquipo

def grafica_de_proceso_general(dfMatches):
    train_data = dfMatches[["Match", "Team", "Score_ind_comp"]]
    fig = plt.subplots(figsize=(25, 8))
    sb.lineplot(data=train_data, x="Match", y="Score_ind_comp", hue="Team", legend="full")
    plt.savefig("Graficas de Equipos/Puntaje individual a lo largo de las partidas.png")
    return train_data
    
def grafica_de_proceso_por_equipo(train_data, dfPromedioPorEquipo):
    list_of_Slope = []
    listTeam = train_data["Team"].unique()
    for i in listTeam:
        temp_team = train_data[train_data["Team"] == i]
        plt.figure(figsize=(25,8))
        sb.lineplot(data=temp_team, x="Match", y="Score_ind_comp").set(title=f"Team: {i}")
        plt.savefig(f"Graficas de Equipos/Equipo {i}/linea puntaje individual.png")
        correlation = temp_team["Score_ind_comp"].corr(temp_team["Match"])
        slope = ((temp_team["Score_ind_comp"].std())/(temp_team["Match"].std())) * correlation
        list_of_Slope.append(slope)
        temp_team = train_data[train_data["Team"] == i]
        plt.figure(figsize=(10,10))
        sb.regplot(data=temp_team, x="Match", y="Score_ind_comp").set(title=f"Team: {i} with slope of {slope}")
        plt.savefig(f"Graficas de Equipos/Equipo {i}/regresión puntaje individual.png")
    dfPromedioPorEquipo.sort_values("Team", inplace=True)
    dfPromedioPorEquipo["Average_Dif"] = list_of_Slope
    dfPromedioPorEquipo.to_csv("Promedios_Equipos.csv", index=False, encoding= 'utf-8-sig')
    return dfPromedioPorEquipo
    
def prediccion_de_futuros_matches(dfPromedioPorEquipo):
    RedScore = 0
    BlueScore = 0
    RedRPActivation = 0
    BlueRPActivation = 0
    RedRPSustanability = 0
    BlueRPSustanability = 0
    amountRP = 0
    list_teams_red = []
    list_teams_blue = []
    for i in range(3):
        team_num = int(input(f"Equipo en Red {i+1}:\n>"))
        list_teams_red.append(team_num)
        temp_team_df = dfPromedioPorEquipo[dfPromedioPorEquipo["Team"] == team_num]
        temp_team_df.reset_index(drop=True, inplace=True)
        
        RedScore += temp_team_df[temp_team_df["Team"] == team_num]["Score_ind_comp"][0]
        RedRPActivation += temp_team_df["Ranking_Point_Activition"][0]
        RedRPSustanability += temp_team_df["Ranking_Point_Sustanability"][0]
    for i in range(3):
        team_num = int(input(f"Equipo en Blue {i+1}:\n>"))
        list_teams_blue.append(team_num)
        temp_team_df = dfPromedioPorEquipo[dfPromedioPorEquipo["Team"] == team_num]
        temp_team_df.reset_index(drop=True, inplace=True)
        
        BlueScore += temp_team_df[temp_team_df["Team"] == team_num]["Score_ind_comp"][0]
        BlueRPActivation += temp_team_df["Ranking_Point_Activition"][0]
        BlueRPSustanability += temp_team_df["Ranking_Point_Sustanability"][0]
        
    if(RedScore > BlueScore):
        print(f"La alianza ROJA ganará con un puntaje de:\n{RedScore} contra {BlueScore}\nEquipo conformado por:")
        print(f"{list_teams_red[0]} {list_teams_red[1]} {list_teams_red[2]}")
        amountRP += 2
    elif(RedScore < BlueScore):
        print(f"La alianza Azul ganará con un puntaje de:\n{BlueScore} contra {RedScore}\nEquipo conformado por:")
        print(f"{list_teams_blue[0]} {list_teams_blue[1]} {list_teams_blue[2]}")
    print(f"{'='*30}\nRanking Points ganados\n{'='*30}\n\nAlianza Roja: {list_teams_red[0]} {list_teams_red[1]} {list_teams_red[2]}")
    
    if((RedRPSustanability/3)>=75):
        print(f"Ranking Point por Sustanability!!!!")
        amountRP += 1
    if((RedRPActivation/3)>=70):
        print(f"Ranking Point por Sustanability!!!!")
        amountRP += 1
    print(f"Tendrán un total de {amountRP} de RP")
    
    amountRP = 0
    
    print(f"{'='*30}\nAlianza Azul: {list_teams_blue[0]} {list_teams_blue[1]} {list_teams_blue[2]}")
    
    if((BlueRPSustanability/3)>=75):
        print(f"Ranking Point por Sustanability!!!!")
        amountRP += 1
    if((BlueRPActivation/3)>=70):
        print(f"Ranking Point por Sustanability!!!!")
        amountRP += 1
    print(f"Tendrán un total de {amountRP} de RP")
    
    stay = input(f"\n\nContinuar?")
    
    
# Main

os.system('cls')

print(f"{'='*40}\nBienvenido al Analizer_6017... mill XD\n{'='*40}")

a = input(f"\nPrimera vez usando el programa? (Y/N)\n>")

if((a == 'Y') | (a == 'y')):
    print(f"Obteniendo datos limpipz generados por 'Clean_Scouter_Cyberius'...")
    dfMatch, dfPromedio = obtencion_de_datos()
    time.sleep(2)
    print("Listo :D")

    print(f"Generando graficas de los equipos y sus desempeños individuales")
    train_df = grafica_de_proceso_general(dfMatch)
    grafica_de_proceso_por_equipo(train_df, dfPromedio)
    time.sleep(2)
    print(f"Listo :D\nPodrá encontrar las graficas en la carpeta 'Graficas de Equipos'\nTambien podrá observar que la tabla de 'Promedios_Equipos' tiene \nla columna nueva de Average_Dif")
    time.sleep(3)

os.system('cls')
print("Ahora si, se viene lo bueno")
time.sleep(2)
os.system('cls')


a = input("Quisiera hacer una predicción de partido? (Y/N)\n>")
while ((a == 'Y') | (a == 'y')):
    prediccion_de_futuros_matches(dfPromedio)
    a = input("Quisiera hacer otra predicción de partido? (Y/N)\n>")
    
print(f"Fue un honor ser utilizando, hasta luego y mucha suerte :D")