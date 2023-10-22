from matplotlib import pyplot as plt
import matplotlib.pyplot as mp
import seaborn as sb
import pandas as pd
import numpy as np
import time
import os

def obtencion_de_datos():
    dfScouting = pd.read_csv("ScoutingVenturaTest.csv")
    return dfScouting

def limpieza_y_tranformación(dfScouting):
    dfScouting = dfScouting.drop(["Marca temporal", "Scouter", "Auto Comentarios Extra", "TeleOp Comentarios Extras", 'Disconnection Time '], axis=1)
    dictPuntos = {"Si":1, "No":0, "Docked (Not touching the ground, but not balanced)":8, "Engaged (Balanced)":12, "Nothing":0, "Engaged":10, "Docked  (Not touching the ground, CS not Balanced)":6}
    dfScouting.replace(dictPuntos, inplace=True)
    dfScouting.fillna(0, inplace=True)
    return dfScouting

def score_definition(dfScouting):
    dfScouting["Score_ind_comp"] = ((dfScouting["Autonomous Cubos [AutoCubo1]"]*3)+
                                    (dfScouting["Autonomous Cubos [AutoCubo2]"]*4)+
                                    (dfScouting["Autonomous Cubos [AutoCubo3]"]*6)+
                                    (dfScouting["Autonomous Conos [AutCono1]"]*3)+
                                    (dfScouting["Autonomous Conos [AutoCono2]"]*4)+
                                    (dfScouting["Autonomous Conos [AutoCono3]"]*6)+
                                    (dfScouting["Auto Mobility: Left Community"]*3)+
                                    (dfScouting["Auto Charge station"])+
                                    (dfScouting["Teleop Cubos [TOCubo1]"]*2)+
                                    (dfScouting["Teleop Cubos [TOCubo2]"]*3)+
                                    (dfScouting["Teleop Cubos [TOCubo3]"]*5)+
                                    (dfScouting["Teleop Conos [TOCono1]"]*2)+
                                    (dfScouting["Teleop Conos [TOCono2]"]*3)+
                                    (dfScouting["Teleop Conos [TOCono3]"]*5)+
                                    (dfScouting["Teleop Park"]*2)+
                                    (dfScouting["Teleop Charge Station"]))

    dfScouting["Score_ind_piezas"] = ((dfScouting["Autonomous Cubos [AutoCubo1]"]*3)+
                                    (dfScouting["Autonomous Cubos [AutoCubo2]"]*4)+
                                    (dfScouting["Autonomous Cubos [AutoCubo3]"]*6)+
                                    (dfScouting["Autonomous Conos [AutCono1]"]*3)+
                                    (dfScouting["Autonomous Conos [AutoCono2]"]*4)+
                                    (dfScouting["Autonomous Conos [AutoCono3]"]*6)+
                                    (dfScouting["Teleop Cubos [TOCubo1]"]*2)+
                                    (dfScouting["Teleop Cubos [TOCubo2]"]*3)+
                                    (dfScouting["Teleop Cubos [TOCubo3]"]*5)+
                                    (dfScouting["Teleop Conos [TOCono1]"]*2)+
                                    (dfScouting["Teleop Conos [TOCono2]"]*3)+
                                    (dfScouting["Teleop Conos [TOCono3]"]*5))
    return dfScouting

def piece_score_and_ranking_definition(dfScouting):
    num_of_match = dfScouting["Match"].max()
    dfScouting['Ranking_Point_Activition'] = ''
    dfScouting['Ranking_Point_Sustanability'] = ''
    dfScouting['Score_team_pieces'] = ''
    for i in range(num_of_match+1):
        temp_match_df = dfScouting[dfScouting["Match"] == i]
        has_ranking_activation_red = 0
        has_ranking_activation_blue = 0
        has_ranking_sustanability_red = 0
        has_ranking_sustanability_blue = 0
        temp_match_red_df = temp_match_df[temp_match_df["Aliance"] == 'Red']
        temp_match_blue_df = temp_match_df[temp_match_df["Aliance"] == 'Blue']
        pieces_points_red = temp_match_red_df["Score_ind_piezas"].sum()
        pieces_points_blue = temp_match_blue_df["Score_ind_piezas"].sum()
        charge_points_red = temp_match_red_df["Auto Charge station"].sum() + temp_match_red_df["Teleop Charge Station"].sum()
        charge_points_blue = temp_match_blue_df["Auto Charge station"].sum() + temp_match_blue_df["Teleop Charge Station"].sum()
        if (charge_points_red >= 26):
            has_ranking_activation_red = 1
        if (charge_points_blue >= 26):
            has_ranking_activation_blue = 1
        if (pieces_points_red >= 36):
            has_ranking_sustanability_red = 1
        if (pieces_points_blue >= 36):
            has_ranking_sustanability_blue = 1
        
        dfScouting.loc[(dfScouting["Match"]==i) & (dfScouting["Aliance"]=='Red'), 'Ranking_Point_Activition'] = has_ranking_activation_red
        dfScouting.loc[(dfScouting["Match"]==i) & (dfScouting["Aliance"]=='Blue'), 'Ranking_Point_Activition'] = has_ranking_activation_blue
        dfScouting.loc[(dfScouting["Match"]==i) & (dfScouting["Aliance"]=='Red'), 'Ranking_Point_Sustanability'] = has_ranking_sustanability_red
        dfScouting.loc[(dfScouting["Match"]==i) & (dfScouting["Aliance"]=='Blue'), 'Ranking_Point_Sustanability'] = has_ranking_sustanability_blue
        dfScouting.loc[(dfScouting["Match"]==i) & (dfScouting["Aliance"]=='Red'), 'Score_team_pieces'] = pieces_points_red
        dfScouting.loc[(dfScouting["Match"]==i) & (dfScouting["Aliance"]=='Blue'), 'Score_team_pieces'] = pieces_points_blue
    return dfScouting

def tabla_por_match(dfScouting):
    dfScouting = dfScouting.sort_values(["Match", "Aliance"])
    dfScouting.to_csv("Tabla Por Match.csv", index=False, encoding= 'utf-8-sig')
    
def tabla_de_promedios(dfScouting):
    if ("Aliance" in dfScouting.columns):
        dfScouting.drop(["Aliance"], axis=1, inplace=True)
    df_mean_all = dfScouting.groupby(["Team"], as_index=False).mean()
    df_mean_all.sort_values("Score_ind_comp", ascending=False).to_csv("Promedios_Equipos.csv", index=False, encoding= 'utf-8-sig')
    return df_mean_all
    
def creacion_de_graficas(dfMeanAll, ShowGraf):
    plt.figure(figsize=(25,25))
    sb.heatmap(dfMeanAll.corr(), annot=True)
    if ShowGraf:
        mp.show()
    plt.savefig("Graficas de Estadistica/Correlacion_promedio.png")
    
    plt.figure(figsize=(15,10))
    sb.violinplot(dfMeanAll[["Teleop Cubos [TOCubo3]", "Teleop Cubos [TOCubo2]", "Teleop Cubos [TOCubo1]", "Teleop Conos [TOCono1]", "Teleop Conos [TOCono2]", "Teleop Conos [TOCono3]"]])
    if ShowGraf:
        mp.show()
    plt.savefig("Graficas de Estadistica/violin_promedio_grid_teleop.png")
    
#Main
print(f"Bienvenido a la Clean_Scouter_Cyberius\n{'='*30}")
a = input(f"¿Te gustaría empezar la limieza de datos? (Y/N)\n>")
if not ((a == 'Y') | (a == 'y')):
    print(f"No os me voy a ch***** a mi madre, no?\nPa que me empiezas si ni me vas a usar >:(\nP****jo")
    time.sleep(3)
    print(f"Ahora si me permites, me voy as salir pa que no me molestes")
    exit()

a = input(f"Antes de empezar, favor de asegurarte que el documento de scouting este en formato CSV y se llame 'ScoutingVenturaTest.csv'\n(Inserte (Y) cuando esté listo)\n>")
if not ((a == 'Y') | (a == 'y')):
    print(f"No os me voy a ch***** a mi madre, no?\nPa que me empiezas si ni me vas a usar >:(\nP****jo")
    time.sleep(3)
    print(f"Ahora si me permites, me voy as salir pa que no me molestes")
    exit()

print(f"empezando la limpieza de datos...")

df_final = piece_score_and_ranking_definition(score_definition(limpieza_y_tranformación(obtencion_de_datos())))
time.sleep(1)
os.system('cls')

a = input(f"Limpieza completada :D\n¿Que quiere hacer con los datos? (Favor de introducir la letra indicada en el parentesis)\n>(M) Creación de tabla por match\n>(P) Creación de tabla promedio\n>(G) Creación de graficas\n>(T) Todas las opciónes\n>(S) Salir\n\n>")
while (not ((a == 'S') | (a == 's'))):
    if ((a == 'M') | (a == 'm')):
        tabla_por_match(df_final)
    elif (((a == 'P') | (a == 'P'))):
        tabla_de_promedios(df_final)
    elif (((a == 'G') | (a == 'G'))):
        creacion_de_graficas(tabla_de_promedios(df_final), True)
    elif (((a == 'T') | (a == 't'))):
        tabla_por_match(df_final)
        dfMean = tabla_de_promedios(df_final)
        creacion_de_graficas(dfMean, False)
    elif (((a == 'S') | (a == 's'))):
        print(f"Gracias por usar el programa de limpieza de datos\nNos vemos y recuerda que eres una persona increibla :D")
        time.sleep(3)
        exit()
    else:
        print(f"Perdón pero su respuesta no fue una entrada valida...\nFavor de introducir la letra indicada en el parentesis")
        time.sleep(3)
        
    os.system('cls')
    a = input(f"¿Que quiere hacer con los datos? (Favor de introducir la letra indicada en el parentesis)\n>(M) Creación de tabla por match\n>(P) Creación de tabla promedio\n>(G) Creación de graficas\n>(T) Todas las opciónes\n>(S) Salir\n\n>")
    
print(f"Gracias por usar el programa de limpieza de datos\nNos vemos y recuerda que eres una persona increibla :D")
time.sleep(3)