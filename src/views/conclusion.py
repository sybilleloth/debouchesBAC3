import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import plotly.express as px
import matplotlib.pyplot as plt

import sys #pour aller chercher les classes où il faut
sys.path.append('./src/views') # répertoires à consulter pour importer les modules
from population import population

def load_view():
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye 2024_09.csv"
    df = pd.read_csv(csv_file)

    st.title(':medal: Et pour finir...')
    st.header("Tout démarre !!! ")

    # Diviser la page en deux colonnes
    col1, col2 = st.columns(2)
    with col1:
        # Affichage de la vidéo dans la première colonne
        appel_video()

    with col2:
        # Affichage du texte Markdown dans la deuxième colonne
        # Calcul puis affichage des différentes métriques globales relatives aux données analysées
        metriques(df)

    carte()

    # Diviser la page en deux colonnes
    col3, col4 = st.columns(2)
    with col3 : 
        top3_formation("Libellé du diplôme", "formations","% d'emplois stables parmi les salariés en France","% d'emplois stables parmi les salariés en France",df)
    with col4 : 
        top3_formation("Libellé du diplôme", "formations","Mois après la diplomation","temps nécessaire à la prise de poste en emploi",df)
    
    # Diviser la page en deux colonnes
    st.subheader("Les régions championnes") 
    col5, col6 = st.columns(2)
    with col5 :
        maxi_poursuite(df)  
    with col6 : 
        maxi_region(df)  
    
    timeline(df)
    afficher_top3_regions_par_annee_groupée(df) 
    afficher_top3_regions_par_annee_groupée_taux_groupe(df)

def metriques(df):
    # Créer une instance de la classe population
    pop = population(df)
    #st.write(dir(pop)) pour checker les attributs et méthodes
    # Appeler la méthode etablissement

    # Calcul des différentes métriques
    df_total_effectifs = pop.region_discipline()
    total_sortants = int(df_total_effectifs["Nombre de sortants"].sum().round(0))
    total_poursuivants =int(df_total_effectifs["Nombre de poursuivants"].sum().round(0))
    total_regions = df["Région"].nunique()
    total_etablissements = df["Etablissement"].nunique()
    total_academies = df["Académie"].nunique()
    total_disciplines = df["Discipline"].nunique()
    total_libelles = df["Libellé du diplôme"].nunique()
    df_total_periodes = pop.group_annee() 
    total_periodes = df_total_periodes['Année_groupée'].nunique()
    # Pondérer les taux d'emploi par le nombre de sortants
    taux_emploi_pondere = (
        (df["Taux d'emploi salarié en France"] * df_total_effectifs["Nombre de sortants"]).sum() / total_sortants
    ).round(2)

    taux_emploi_stable_pondere = (
        (df["% d'emplois stables parmi les salariés en France"] * df_total_effectifs["Nombre de sortants"]).sum() / total_sortants
    ).round(2)

    # Titre et sous-titre
    st.header('Retenons de cette exploration...')
    st.header("En synthèse, les données :")

    # Dictionnaire contenant les données globales
    donnees_globales = {
        "Périodes de diplomation considérées": total_periodes,
        "Total Effectif des étudiants sortants": total_sortants,
        "Total Effectif des étudiants poursuivant leurs études": total_poursuivants,
        "Nombre de disciplines diplômantes": total_disciplines,
        "Nombre de libellés du diplôme": total_libelles,
        "Nombre de régions": total_regions,
        "Nombre d'académies": total_academies,
        "Nombre d'établissements": total_etablissements,
        "Taux moyen d'emploi salarié en France pondéré en %": taux_emploi_pondere,
        "% moyen d'emplois stables parmi les salariés en France pondéré en %": taux_emploi_stable_pondere
    }

    # Afficher les données globales dans Streamlit
    for key, value in donnees_globales.items():
        st.write(f"{key}: {value}")

def appel_video():
    video_file = open("./src/assets/images/8284321-hd_1080_1920_30fps.mp4", 'rb')
    video_bytes = video_file.read()
    video_base64 = base64.b64encode(video_bytes).decode('utf-8')

    # Code HTML pour afficher la vidéo avec une largeur de 70%
    video_html = f"""
        <video width="60%" controls autoplay>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    """
    st.markdown(video_html, unsafe_allow_html=True)
        
def carte():
    st.header("Les marches du podium :")   

    # Chargement des données avec coordonnées
    csv_filec = "./data/esr_nettoye_avec_cities 2024_09.csv"
    dfc = pd.read_csv(csv_filec)

    # Vérification du chargement des données
    if dfc.empty:
        st.error("Le fichier CSV est vide ou introuvable.")
        return

    # Calcul du nombre moyen de "Libellé du diplôme" par "Académie"
    moyenne_diplomes_par_academie = dfc.groupby('Académie')['Libellé du diplôme'].nunique().mean().round(2)
    st.write(f"Nombre moyen de Libellés de diplôme par Académie : {round(moyenne_diplomes_par_academie)}")

    # Calcul du nombre moyen de "Sortants" par "Libellé du diplôme" et par "Académie"
    moyenne_sortants_par_diplome_academie = dfc.groupby(['Académie', 'Libellé du diplôme'])['Nombre de sortants'].mean().mean().round(2)
    st.write(f"Nombre moyen de Sortants par Libellé du diplôme et par Académie : {round(moyenne_sortants_par_diplome_academie)}")

    # Calculs par académie pour la carte
    df_academie = dfc.groupby('Académie').agg(
        latitude=('latitude', 'mean'),
        longitude=('longitude', 'mean'),
        moyenne_sortants_academie=('Nombre de sortants', 'mean')
    ).reset_index()

    # Arrondir la colonne 'moyenne_sortants_academie' à 0 décimale
    df_academie['moyenne_sortants_academie'] = df_academie['moyenne_sortants_academie'].round(0)
    
    # Vérification des coordonnées et suppression des lignes vides
    df_academie = df_academie.dropna(subset=['latitude', 'longitude'])

    if df_academie.empty:
        st.error("Aucune académie avec des coordonnées valides.")
        return

    # Ajout d'une colonne pour le nombre moyen de sortants par libellé du diplôme
    df_academie['moyenne_sortants_par_diplome_academie'] = dfc.groupby(['Académie', 'Libellé du diplôme'])['Nombre de sortants'].mean().groupby('Académie').mean().round(0).values

    # Vérification des données avant de créer la carte
    #st.write("Données de l'académie pour la carte:") #v test de validité et complétude des données en raison des diff. d'affichage rencontrées
    #st.write(df_academie.head())  # Affiche les premières lignes pour vérification

    # Préparation des données pour la visualisation
    chart_data = df_academie[['Académie', 'latitude', 'longitude', 'moyenne_sortants_academie', 'moyenne_sortants_par_diplome_academie']].dropna()

    if chart_data.empty:
        st.error("Aucune donnée à afficher sur la carte.")
        return

    # Affichage de la carte avec pydeck
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v10',
            # Centrage de la carte sur la France
            initial_view_state=pdk.ViewState(
                latitude=46.7683,  # Latitude centre de la France Bruyère Allichamp
                longitude=2.4325,  # Longitude centre de la France Bruyère Allichamp
                zoom=5,  # Niveau de zoom adapté pour voir tout le pays
                pitch=50,
            ),
     
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=chart_data,
                    get_position=['longitude', 'latitude'],
                    get_color=[119, 38, 75, 255],
                    get_radius="moyenne_sortants_par_diplome_academie * 1000",  # Ajuster le rayon pour mieux voir les points
                    pickable=True,
                ),
            ],
            # Affichage d'un point de données sur la carte
            tooltip={
                "html": "<b>Académie:</b> {Académie}<br/><b>Moyenne Sortants par Académie:</b> {moyenne_sortants_academie}<br/><b>Moyenne Sortants par Diplôme par Académie:</b> {moyenne_sortants_par_diplome_academie}",
                "style": {"backgroundColor": "steelblue", "color": "white"}
            }
        )
    )
    
def top3_formation(criteria, texte1, cible, texte2,df):
    #top3_formation("Libellé du diplôme", "formations","% d'emplois stables parmi les salariés en France","% d'emplois stables parmi les salariés en France")
    #top3_formation("Libellé du diplôme", "formations","Mois après la diplomation","temps nécessaire à la prise de poste en emploi")
    # Affiche les 3 formations avec le taux d'emploi le plus favorable pour chaque type de diplôme.
    
    
    st.write(f"Les {texte1} dont le {texte2} est le plus favorable par typologie de diplôme : Licence pro, Master ou MEEF")

    # Filtrer les données pertinentes
    df_filtered = df[["Type de diplôme", criteria, cible]].dropna()

    if cible == "Taux d'emploi" : 
        # Compter le nombre de formations avec un taux d'emploi de 100%
        formations_100 = df_filtered[df_filtered[cible] == 100].shape[0]
    else :   
        # Compter le nombre de formations avec une entrée sur le marché du travail de 6 mois
        formations_100 = df_filtered[df_filtered[cible] == 6].shape[0]
                
    print(formations_100)


    # Afficher le nombre de formations avec un taux d'emploi de 100% en gras
    st.markdown(f"**Nombre de {criteria} dont l'indice {texte2} est idéal : {formations_100}**")

    # Filtrer et trier pour chaque type de diplôme
    diplomes = df["Type de diplôme"].unique().tolist()

    # Concaténer les top 3 pour chaque diplôme
    top_formations = pd.DataFrame()

    for diplome in diplomes:
        df_diplome = df_filtered[df_filtered["Type de diplôme"] == diplome]
        if cible == "% d'emplois stables parmi les salariés en France" : 
            top_3_formations = df_diplome.sort_values(by=cible, ascending=False).head(3)
        else : top_3_formations = df_diplome.sort_values(by=cible, ascending=True).head(3)
        top_formations = pd.concat([top_formations, top_3_formations])

    # Vérification des données concaténées
    st.write("Top formations par diplôme :", top_formations)

    # Calculer la valeur minimale et maximale du critère cible
    min_value = top_formations[cible].min()
    max_value = top_formations[cible].max()

    # Calculer les limites pour l'axe y
    y_min = min_value * 0.9
    y_max = max_value * 1.1

    # Créer un diagramme à barres groupées avec des couleurs personnalisées
    color_map = {
        "Licence professionnelle": "#abc837",
        "Master LMD": "#77264b",
        "Master MEEF": "#006b80"
    }

    # Créer un diagramme à barres groupées
    fig = px.bar(
        top_formations, 
        x=criteria, 
        y=cible, 
        color="Type de diplôme", 
        color_discrete_map=color_map,  # Appliquer les couleurs personnalisées
        barmode="group",
        title=f"Le top  avec le {texte2} le plus favorable par type de diplôme"
    )

    # Appliquer la plage personnalisée à l'axe y
    fig.update_yaxes(range=[y_min, y_max])

    # Formater les noms des abscisses sur trois lignes
    fig.update_xaxes(tickvals=top_formations[criteria],
                     ticktext=[label.replace(' ', '\n', 2) for label in top_formations[criteria]])

    # Afficher le graphique
    st.plotly_chart(fig)

def maxi_poursuite(df):
    
    # Filtrer les données pour inclure uniquement les lignes avec un nombre de poursuivants et de sortants
    filtered_data = df.dropna(subset=['Nombre de poursuivants', 'Nombre de sortants'])

    # Ajouter une colonne pour calculer le taux de poursuite d'études
    filtered_data['Taux de poursuite'] = filtered_data['Nombre de poursuivants'] / filtered_data['Nombre de sortants'] * 100

    # Grouper les données par région et calculer le taux de poursuite moyen par région
    region_pursuit_rate = filtered_data.groupby('Région')['Taux de poursuite'].mean().reset_index()

    # Trier les régions par taux de poursuite d'études décroissant
    top_regions = region_pursuit_rate.sort_values(by='Taux de poursuite', ascending=False).head(3)

    # Afficher les résultats
    st.markdown("Les 3 régions avec le plus fort taux de poursuite d'études après Bac +3")
        
    # Créer un graphique avec les couleurs spécifiques et taille fixée
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#abc837", "#77264b", "#006b80"]
    bars = ax.bar(top_regions['Région'], top_regions['Taux de poursuite'], color=colors)
    
    # Ajouter les annotations sur chaque barre
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points de décalage en vertical
                    textcoords="offset points",
                    ha='center', va='bottom')

    ax.set_xlabel("Région")
    ax.set_ylabel("Taux de poursuite (%)")
    ax.set_title("Top 3 des régions par taux de poursuite d'études après Bac +3")

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)
    st.caption("le % exprimé correspond au rapport Nombre de poursuivants / Nombre de sortants")

def maxi_region(df):
       
    # Calculer le taux d'emploi moyen par région
    region_employment_rate = df.groupby('Région')['Taux d\'emploi salarié en France'].mean().reset_index()

    # Trier les régions par taux d'emploi décroissant et sélectionner les 3 premières
    top_regions = region_employment_rate.sort_values(by='Taux d\'emploi salarié en France', ascending=False).head(3)

    st.markdown("Les 3 régions dont le taux d'emploi moyen est le plus favorable") 
    
    # Créer un graphique en pyramide (barh pour barres horizontales inversées) avec taille fixée
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#abc837", "#77264b", "#006b80"]
    bars = ax.barh(top_regions['Région'], top_regions['Taux d\'emploi salarié en France'], color=colors)

    # Inverser l'ordre des régions pour avoir une pyramide inversée
    ax.invert_yaxis()
    
    # Ajouter les annotations sur chaque barre
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width:.2f}%',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),  # 3 points de décalage en horizontal
                    textcoords="offset points",
                    ha='left', va='center')

    ax.set_xlabel("Taux d'emploi salarié en France (%)")
    ax.set_ylabel("Région")
    ax.set_title("Top 3 des régions par taux d'emploi moyen")

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)


    st.write("Les 3 formations menant le plus rapidement les étudiants dits sortants vers la prise de poste : licence pro, Master ou MEEF")
    st.write("Les 3 régions dont le taux d'emploi est le plus favorable sur l'ensemble des formations : licence pro, Master ou MEEF")
    st.write("Les 3 régions menant le plus rapidement les étudiants dits sortants vers la prise de poste : licence pro, Master ou MEEF")
    st.write("Les 3 formations comprenant le plus fort taux d'étudiants poursuivant après l'obtention de leur BAC + 3 : licence pro, Master ou MEEF")
 
def timeline(df):
    st.header("Top 3 des régions par discipline et année selon la moyenne du % d'emplois stables")

    # Vérification que les colonnes nécessaires existent dans le DataFrame
    required_columns = [
        "Année(s) d'obtention du diplôme prise(s) en compte", "Discipline", 
        "Région", "% d'emplois stables parmi les salariés en France"
    ]
    for col in required_columns:
        if col not in df.columns:
            st.error(f"La colonne '{col}' est manquante dans le DataFrame.")
            return

    # Agréger les données par académie, discipline, année, région
    df_grouped = df.groupby(
        ["Année(s) d'obtention du diplôme prise(s) en compte", "Discipline", "Région"]
    ).agg({
        "% d'emplois stables parmi les salariés en France": 'mean'
    }).reset_index()

    # Trier les données pour chaque combinaison d'année et discipline par ordre décroissant du % d'emplois stables
    df_sorted = df_grouped.sort_values(
        by=["Année(s) d'obtention du diplôme prise(s) en compte", "Discipline", "% d'emplois stables parmi les salariés en France"],
        ascending=[True, True, False] # Décroissant pour % d'emplois stables
    )

    # Pour chaque année et chaque discipline, sélectionner les 3 premières académies
    df_top3 = df_sorted.groupby(["Année(s) d'obtention du diplôme prise(s) en compte", "Discipline"]).head(3)

    # Créer la visualisation en ligne avec Plotly
    fig = px.line(
        df_top3,
        x="Année(s) d'obtention du diplôme prise(s) en compte",
        y="% d'emplois stables parmi les salariés en France",
        color="Région",  # Couleurs différenciées par région
        line_group="Région",  # Les lignes représentent chaque académie
        hover_name="Région",
        #facet_col="Discipline",  # Séparation des graphes par discipline
        title="Top 3 des régions par discipline et année selon la moyenne du % d'emplois stables",
        labels={
            "% d'emplois stables parmi les salariés en France": "% d'emplois stables (moyenne)",
            "Année(s) d'obtention du diplôme prise(s) en compte": "Année(s) d'obtention du diplôme"
        },
        height=600,
    )

    # Mettre à jour la mise en page pour une meilleure lisibilité
    fig.update_layout(legend_title_text='Région', margin={"r":0,"t":50,"l":0,"b":0})

    # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

def afficher_top3_regions_par_annee_groupée(df):
    # Ajouter la colonne Année_groupée
    df = ajouter_colonne_annee_groupée(df)

    # Agréger les données par Année_groupée, région et calculer la moyenne du % d'emplois stables
    df_grouped = df.groupby(
        ["Année_groupée", "Région"]
    ).agg({
        "% d'emplois stables parmi les salariés en France": 'mean'
    }).reset_index()

    # Trier les données par Année_groupée et par % d'emplois stables de façon décroissante
    df_sorted = df_grouped.sort_values(
        by=["Année_groupée", "% d'emplois stables parmi les salariés en France"],
        ascending=[True, False]
    )

    # Sélectionner les 3 premières régions pour chaque Année_groupée
    df_top3 = df_sorted.groupby("Année_groupée").head(3)

    # Afficher les résultats en tableau pour vérification
    st.write("Top 3 des régions par Année_groupée avec le % d'emplois stables le plus élevé:")
    #st.write(df_top3)

    # Couleurs RVB spécifiques pour chaque région
    colors = {
        "Bourgogne-Franche-Comté" : "rgb(171, 200, 55,1)",  # RVB (171, 200, 55)
        "Hauts-de-France": "rgb(119, 38, 75,1)",   # RVB (119, 38, 75)
        "Grand Est": "rgb(221, 107, 119,1)", # RVB (221, 107, 119)
        "Auvergne-Rhône-Alpes": "rgb(0, 107, 128,1)"    # RVB (0, 107, 128)
    }

    # Créer une visualisation avec Plotly
    fig = px.bar(
        df_top3,
        x="Année_groupée",
        y="% d'emplois stables parmi les salariés en France",
        color="Région",  # Chaque région sera représentée par une couleur différente
        barmode="group",  # Les barres seront regroupées par Année_groupée
        title="Top 3 des régions avec le % d'emplois stables le plus élevé par Année_groupée",
        labels={
            "% d'emplois stables parmi les salariés en France": "% d'emplois stables",
            "Année_groupée": "Année regroupée"
        },
        height=600,
        color_discrete_map=colors  # Appliquer les couleurs RVB spécifiques aux régions
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

def afficher_top3_regions_par_annee_groupée_taux_groupe(df):
    # appeler le df avec Année_groupée
    pop = population(df)
    df =pop.group_annee()

    # Calculer le taux pondéré par région
    df_grouped = df.groupby(["Année_groupée", "Région"]).apply(
        lambda x: pd.Series({
            "Taux d'emploi salarié en France": (x["Taux d'emploi salarié en France"] * x["Nombre de sortants"]).sum() / x["Nombre de sortants"].sum()
        })
    ).reset_index()

    # Trier les données par Année_groupée et par % d'emplois stables de façon décroissante
    df_sorted = df_grouped.sort_values(
        by=["Année_groupée", "Taux d'emploi salarié en France"],
        ascending=[True, False]
    )

    # Sélectionner les 3 premières régions pour chaque Année_groupée
    df_top3 = df_sorted.groupby("Année_groupée").head(3)

    # Afficher les résultats en tableau pour vérification
    st.write("Top 3 des régions par année avec le 'Taux d'emploi salarié en France' le plus élevé (pondéré par le nombre de sortants) :")

    # Couleurs RVB spécifiques pour chaque région
    colors = {
        "Bourgogne-Franche-Comté" : "rgb(171, 200, 55,1)",  # RVB (171, 200, 55)
        "Normandie": "rgb(119, 38, 75,1)",   # RVB (119, 38, 75)
        "Pays de la Loire": "rgb(221, 107, 119,1)", # RVB (221, 107, 119)
        "Centre_Val de Loire": "rgb(0, 107, 128,1)"    # RVB (0, 107, 128)
    }

    # Créer une visualisation avec Plotly
    fig = px.bar(
        df_top3,
        x="Année_groupée",
        y="Taux d'emploi salarié en France",
        color="Région",  # Chaque région sera représentée par une couleur différente
        barmode="group",  # Les barres seront regroupées par Année_groupée
        title="Top 3 des régions avec le 'Taux d'emploi salarié en France' le plus élevé par Année",
        labels={
            "Taux d'emploi salarié en France": "Taux d'emploi salarié",
            "Année_groupée": "Année du diplôme"
        },
        height=600,
        color_discrete_map=colors  # Appliquer les couleurs RVB spécifiques aux régions
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

def afficher_top3_regions(df):
    # Agréger les données par année, région et calculer la moyenne du % d'emplois stables
    df_grouped = df.groupby(
        ["Année(s) d'obtention du diplôme prise(s) en compte", "Région"]
    ).agg({
        "% d'emplois stables parmi les salariés en France": 'mean'
    }).reset_index()

    # Trier les données par année et par % d'emplois stables de façon décroissante
    df_sorted = df_grouped.sort_values(
        by=["Année(s) d'obtention du diplôme prise(s) en compte", "% d'emplois stables parmi les salariés en France"],
        ascending=[True, False]
    )

    # Sélectionner les 3 premières régions pour chaque année
    df_top3 = df_sorted.groupby("Année(s) d'obtention du diplôme prise(s) en compte").head(3)

    # Afficher les résultats en tableau pour vérification
    st.write("Top 3 des régions par année avec le % d'emplois stables le plus élevé:")
    st.write(df_top3)

    # Créer une visualisation avec Plotly
    fig = px.bar(
        df_top3,
        x="Année(s) d'obtention du diplôme prise(s) en compte",
        y="% d'emplois stables parmi les salariés en France",
        color="Région",  # Chaque région sera représentée par une couleur différente
        barmode="group",  # Les barres seront regroupées par année
        title="Top 3 des régions avec le % d'emplois stables le plus élevé par année",
        labels={
            "% d'emplois stables parmi les salariés en France": "% d'emplois stables",
            "Année(s) d'obtention du diplôme prise(s) en compte": "Année(s) d'obtention du diplôme"
        },
        height=600
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

# Exécution de la fonction principale
if __name__ == "__main__":
    load_view()
 