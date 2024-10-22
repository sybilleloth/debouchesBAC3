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
    st.subheader("La vaste étendue des académies enseignantes ") 
    with st.expander("Voir la répartition des effectifs étudiants sur une carte de France") :
        carte()

    st.subheader("Le top 3 des universités")
    with st.expander("Voir les universités lauréates") : 
        afficher_top3_universites(df)
    
    st.subheader("Le top 3 des diplômes ") 
    with st.expander("Voir les lauréats à travers la période étudiée") :
        # Diviser la page en deux colonnes
        col3, col4 = st.columns(2)
        with col3 : 
            top3_formation("Libellé du diplôme", "formations","% d'emplois stables parmi les salariés en France","% d'emplois stables parmi les salariés en France",df)
        with col4 : 
            top3_formation("Libellé du diplôme", "formations","Mois après la diplomation","temps nécessaire à la prise de poste en emploi",df)
    
    st.subheader("Le top 3 des régions ") 
    with st.expander("Voir les graphes pour les régions avec les taux de poursuites et les taux d'emploi moyens les plus élevés") : 
        col5, col6 = st.columns(2)
        with col5 :
            maxi_poursuite(df)  
        with col6 : 
            maxi_region(df)  
    with st.expander("Voir les lauréates par année et par discipline") : 
        timeline(df)
    with st.expander("Voir les lauréates des taux d'emplois stables salarié par année") : 
        afficher_top3_regions_par_annee_groupée(df) 
    with st.expander("Voir les lauréates  taux d'emploi salarié par année") : 
        afficher_top3_regions_par_annee_groupée_taux_groupe(df)

def metriques(df):
    pop = population(df) # Créer une instance de la classe population
    #st.write(dir(pop)) pour checker les attributs et méthodes
    
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
        st.error("problème avec le fichier CSV : vide ou introuvable.")
        return
    #appel classe population avec avec dfc pour fonction academie
    pop = population(dfc)
    df_academie = pop.academie() #effectifs par académie
    
    # Calculer la latitude et la longitude moyennes pour chaque académie
    df_academie_coords = dfc.groupby('Académie').agg(
        latitude=('latitude', 'mean'),
        longitude=('longitude', 'mean')
    ).reset_index()

    # Fusionner les données académiques avec les coordonnées
    df_academie = pd.merge(df_academie, df_academie_coords, on="Académie")

    # check coordonnées et suppression des lignes vides parsécurité mais inutile car déjà fait dans la construction de dfc
    df_academie = df_academie.dropna(subset=['latitude', 'longitude'])
    if df_academie.empty:
        st.error("Aucune académie avec des coordonnées valides.")
        return
    
    # Vérification des données avant de créer la carte dans la vf
    #st.write("Données de l'académie pour la carte:") # test de validité et complétude des données en raison des diff. d'affichage rencontrées
    #st.write(df_academie)  # Affiche df pour vérification
    
    #calcul des moyennes de sortants et poursuivants par académie
    df_academie_moyenne = df_academie.groupby('Académie').agg({
        'latitude': 'mean',  # Moyenne des coordonnées pour chaque académie
        'longitude': 'mean',
        'Nombre de sortants': 'mean',  # Moyenne des sortants par académie
        'Nombre de poursuivants': 'mean'  # Moyenne des poursuivants par académie
    }).reset_index()

    # Arrondir les moyennes par cohérence
    df_academie_moyenne['Nombre de sortants'] = df_academie_moyenne['Nombre de sortants'].round(0)
    df_academie_moyenne['Nombre de poursuivants'] = df_academie_moyenne['Nombre de poursuivants'].round(0)
    
    # Préparation des données pour la visualisation
    chart_data = df_academie_moyenne[["Académie", "latitude", "longitude", "Nombre de sortants", "Nombre de poursuivants"]]

    if chart_data.empty:
        st.error("Aucune donnée à afficher sur la carte.")
        return

    # Affichage de la carte avec pydeck https://deckgl.readthedocs.io/en/latest/view_state.html
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v10',
            # Centrage de la carte sur la France
            initial_view_state=pdk.ViewState(
                latitude=46.7683,  # Latitude centre de la France Bruyère Allichamp
                longitude=2.4325,  # Longitude centre de la France Bruyère Allichamp
                zoom=5,  # Niveau de zoom adapté pour voir tout le pays
                pitch=50 # test visualisation inclinaison de la carte à 50°,
            ),
            # les couches pydeck https://deck.gl/docs/api-reference/layers 
            # Scatterplotlayer pour choix des nuages de points :https://deck.gl/docs/api-reference/layers/scatterplot-layer
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=chart_data,
                    get_position=['longitude', 'latitude'],
                    get_color=[119, 38, 75, 255],  # AUBERGINE
                    get_radius="Nombre de sortants",  # Ajuster le rayon pour mieux voir les points
                    radius_scale=30000,  # Échelle pour ajuster la taille des cercles
                    pickable=True,  # Pour rendre les cercles interactifs
                ),
            ],
            # Affichage d'un point de données sur la carte et affichage par tooltip sur infobulles 
            # https://deckgl.readthedocs.io/en/latest/tooltip.html
            tooltip={
                "html": "<b>Académie:</b> {Académie}<br/><b>Nombre moyen de Sortants :</b> {Nombre de sortants}<br/><b>Nombre moyen de Poursuivants:</b> {Nombre de poursuivants}",
                "style": {"backgroundColor": "steelblue", "color": "white"}
            }
        )
    )
  
def top3_formation(criteria, texte1, cible, texte2,df):
    #top3_formation("Libellé du diplôme", "formations","% d'emplois stables parmi les salariés en France","% d'emplois stables parmi les salariés en France")
    #top3_formation("Libellé du diplôme", "formations","Mois après la diplomation","temps nécessaire à la prise de poste en emploi")
    # Affiche les 3 formations avec le taux d'emploi le plus favorable pour chaque type de diplôme.
    
    st.write(f"Les {texte1} dont le {texte2} est le plus favorable par typologie de diplôme")

    # Filtrer les données pertinentes
    df_filtered = df[["Type de diplôme", criteria, cible]].dropna()

    if cible == "% d'emplois stables parmi les salariés en France" : 
        # Compter le nombre de formations avec un taux d'emploi de 100%
        formations_100 = df_filtered[df_filtered[cible] >97][criteria].nunique()
    else :   
        # Compter le nombre de formations avec une entrée sur le marché du travail de 6 mois
        formations_100 = df_filtered[df_filtered[cible] == 6][criteria].nunique()
        # Afficher le nombre de formations avec un taux d'emploi de 100% en gras
        st.markdown(f"**Nombre de -{criteria}- concernés : {formations_100}**")

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
        "Master MEEF": "#006b80",
        "Licence générale": "#dd6b77"
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
    
    # Filtrer les données pour ne conserver que les lignes avec un nombre de poursuivants et de sortants
    filtered_data = df.dropna(subset=['Nombre de poursuivants', 'Nombre de sortants'])

    # Ajouter une colonne pour calculer le taux de poursuite d'études
    filtered_data['Taux de poursuite'] = filtered_data['Nombre de poursuivants'] / (filtered_data['Nombre de sortants']+filtered_data['Nombre de poursuivants']) * 100

    # Calculer le taux de poursuite moyen global
    global_poursuit_tx = filtered_data['Taux de poursuite'].mean()

    # Grouper les données par région et calculer le taux de poursuite moyen par région
    region_poursuit_tx = filtered_data.groupby('Région')['Taux de poursuite'].mean().reset_index()

    # Trier les régions par taux de poursuite d'études décroissant
    top_regions = region_poursuit_tx.sort_values(by='Taux de poursuite', ascending=False).head(3)

    # Afficher les résultats
    st.markdown("Les 3 régions avec le plus fort taux de poursuite d'études après Bac +3")
        
    # Créer un graphique avec les couleurs spécifiques et taille fixée
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ["#abc837", "#77264b", "#006b80"]
    bars = ax.barh(top_regions['Région'], top_regions['Taux de poursuite'], color=colors)
    
    # Inverser l'ordre des régions pour avoir une pyramide inversée
    ax.invert_yaxis()
    
    # Ajouter les annotations sur chaque barre
    for bar in bars:
        width = bar.get_width() #au lieu de height = bar.get_height()
        ax.annotate(f'{width:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, width),
                    xytext=(0, 3),  # 3 points de décalage en vertical
                    textcoords="offset points",
                    ha='center', va='center')
    
    # Ajouter une ligne horizontale pour le taux de poursuite moyen global puis la légende et transposer ade ax.axhline à axvline
    ax.axvline(global_poursuit_tx, color='red', linestyle='--', linewidth=2, label=f'Moyenne nationale: {global_poursuit_tx:.2f}%')
    ax.legend()

    ax.set_xlabel("Taux de poursuite (%)")
    ax.set_ylabel("Région")
    ax.set_title("Top 3 des régions par taux de poursuite d'études après Bac +3")


    # Afficher le graphique dans Streamlit
    st.pyplot(fig)
    st.caption("le % exprimé correspond au rapport Nombre de poursuivants / Effectif")

def maxi_region(df):
       
    # Calculer le taux d'emploi moyen par région
    region_employment_rate = df.groupby('Région')['Taux d\'emploi salarié en France'].mean().reset_index()

    # Calculer le taux d'emploi moyen national
    national_employment_rate = df['Taux d\'emploi salarié en France'].mean()
    
    # Trier les régions par taux d'emploi décroissant et sélectionner les 3 premières
    top_regions = region_employment_rate.sort_values(by='Taux d\'emploi salarié en France', ascending=False).head(3)

    st.markdown("Les 3 régions dont le taux d'emploi moyen est le plus favorable") 
    
    # Créer un graphique en pyramide (barh pour barres horizontales inversées) avec taille fixée
    fig, ax = plt.subplots(figsize=(6, 6))
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
        
    # Ajouter une ligne verticale rouge pour la moyenne nationale
    ax.axvline(national_employment_rate, color='red', linestyle='--', linewidth=2, label=f'Moyenne nationale: {national_employment_rate:.2f}%')
    # Ajouter la légende
    ax.legend()
    ax.set_xlabel("Taux d'emploi salarié en France (%)")
    ax.set_ylabel("Région")
    ax.set_title("Top 3 des régions par taux d'emploi moyen")

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)


    #st.write("Les 3 formations menant le plus rapidement les étudiants dits sortants vers la prise de poste : licence pro ou générale, Master LMD ou MEEF")
    #st.write("Les 3 régions dont le taux d'emploi est le plus favorable sur l'ensemble des formations : licence pro ou générale, Master LMD ou MEEF")
    #st.write("Les 3 régions menant le plus rapidement les étudiants dits sortants vers la prise de poste : licence pro ou générale, Master ou MEEF")
    #st.write("Les 3 formations comprenant le plus fort taux d'étudiants poursuivant après l'obtention de leur BAC + 3 : licence pro ou générale, Master LMD ou MEEF")

def timeline(df):
    #Top 3 des régions par discipline et année selon la moyenne du % d'emplois stables
    
    # Vérification que les colonnes nécessaires existent dans le DataFrame
    required_columns = [
        "Discipline", 
        "Année_groupée", 
        "Région", 
        "% d'emplois stables parmi les salariés en France"
    ]
    for col in required_columns:
        if col not in df.columns:
            st.error(f"La colonne '{col}' est manquante dans le DataFrame.")
            return

    # Agréger les données par année, discipline, région
    df_grouped = df.groupby(
        ["Année_groupée", "Discipline", "Région"]
    ).agg({
        "% d'emplois stables parmi les salariés en France": 'mean'
    }).reset_index()
    
    df_grouped["% d'emplois stables parmi les salariés en France"] = df_grouped["% d'emplois stables parmi les salariés en France"].round(2)

    # Permettre à le choix l'utilisateur  via selectboxes
    available_years = df_grouped['Année_groupée'].unique()
    selected_year = st.selectbox("Choisissez une année", available_years)
    available_disciplines = df_grouped['Discipline'].unique()
    selected_discipline = st.selectbox("Choisissez une discipline", available_disciplines)
    
    # Filtrer les données par l'année et la discipline sélectionnées
    df_filtered = df_grouped[
        (df_grouped['Année_groupée'] == selected_year) & 
        (df_grouped['Discipline'] == selected_discipline)
    ]
    # Filtrer les données par l'année sélectionnée
    #df_filtered = df_grouped[df_grouped['Année_groupée'] == selected_year]

    # Trier les données par discipline et % d'emplois stables
    df_sorted = df_filtered.sort_values(
        by=["% d'emplois stables parmi les salariés en France"],
        ascending=[False]  
    )

    # Pour chaque discipline, sélectionner les 3 premières régions
    df_top3 = df_sorted.groupby("Discipline").head(3)
    
    # Message caption si les données ne sont pas suffisamment exhaustives pour afficher 3 régions 
    if len(df_top3) < 3:
        st.markdown(
            """
            <p style="color:purple;">
            Les données ne permettent pas une mesure sur l'ensemble des régions en 2024, 
            mais l'enrichissement progressif des enquêtes Insertion Professionnelle (Insersup) 
            permettra la complétude au fil des semestres.
            </p>
            """, unsafe_allow_html=True
        )
    # Créer un graphique en barres avec Plotly
    
    colors = ['#abc837', '#77264b', '#006b80']  # pomme, aubergine, canard / Créer une palette de couleurs personnalisée
    fig = px.bar(
        df_top3,
        x="Région",
        y="% d'emplois stables parmi les salariés en France",
        color="Région",  # Couleurs différenciées par région
        facet_col="Discipline",  # Séparation des graphes par discipline
        title=f"Top 3 des régions par discipline pour l'année {selected_year} selon la moyenne du % d'emplois stables",
        labels={
            "% d'emplois stables parmi les salariés en France": "% d'emplois stables (moyenne)",
            "Région": "Région"
        },
        height=600,
        color_discrete_sequence=colors
    )

    # Mettre à jour la mise en page pour une meilleure lisibilité
    fig.update_layout(legend_title_text='Région', margin={"r":0,"t":50,"l":0,"b":0})

    # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

def afficher_top3_regions_par_annee_groupée(df):
    #appel fonction ajout colonne année groupée
    pop = population(df)
    df_group_annee = pop.group_annee()
       
    # Agréger les données par Année_groupée, région et calculer la moyenne du % d'emplois stables
    df_grouped = df_group_annee.groupby(
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
    df_top3 ["% d'emplois stables parmi les salariés en France"]= df_top3 ["% d'emplois stables parmi les salariés en France"].round(2)
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
            "Taux d'emploi salarié en France": (x["Taux d'emploi salarié en France"] * x["Nombre de sortants"]).sum() / x["Nombre de sortants"].sum().round(2)
        })
    ).reset_index()

    # Trier les données par Année_groupée et par % d'emplois stables de façon décroissante
    df_sorted = df_grouped.sort_values(
        by=["Année_groupée", "Taux d'emploi salarié en France"],
        ascending=[True, False]
    )

    # Sélectionner les 3 premières régions pour chaque Année_groupée
    df_top3 = df_sorted.groupby("Année_groupée").head(3)
    df_top3 ["Taux d'emploi salarié en France"] =   df_top3 ["Taux d'emploi salarié en France"].round(2)
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

def afficher_top3_universites(df):
    
    st.markdown("### Classement des Etablissements d'enseignement")
    
    # Créer une instance de la classe population
    pop = population(df)

    # Appeler la méthode etablissement pour obtenir les données des établissements
    df_etablissement = pop.etablissement()
    
    # Ajouter un sélecteur pour choisir le type de classement
    option_classement = st.selectbox(
        "Choisissez un critère de classement:",
        ("Total Sortants + Poursuivants", "Nombre moyen de diplômés par formation")
    )

    if option_classement == "Total Sortants + Poursuivants":
        # Calcul du total des sortants + poursuivants par établissement et année
        df_grouped = df_etablissement.groupby(["Etablissement", "Année_groupée"]).agg({
            'Nombre de poursuivants': 'sum',
            'Nombre de sortants': 'sum'
        }).reset_index()

        # Ajouter une colonne pour le total annuel (sortants + poursuivants)
        df_grouped['Total Sortants + Poursuivants'] = df_grouped['Nombre de poursuivants'] + df_grouped['Nombre de sortants']

        # Calculer l'effectif moyen annuel pour chaque établissement
        df_mean = df_grouped.groupby('Etablissement').agg({
            'Total Sortants + Poursuivants': 'mean'
        }).round(0).reset_index()

        # Calculer la moyenne nationale
        moyenne_nationale = df_mean['Total Sortants + Poursuivants'].mean()

        # Trier par ordre décroissant du total moyen annuel et prendre les 3 premiers
        df_mean = df_mean.sort_values(by='Total Sortants + Poursuivants', ascending=False).head(3)

        # Créer une visualisation
        fig = px.scatter(df_mean, 
                         y='Total Sortants + Poursuivants', 
                         x='Etablissement', 
                         size='Total Sortants + Poursuivants', 
                         color='Total Sortants + Poursuivants',
                         hover_name='Etablissement',
                         labels={
                             'Total Sortants + Poursuivants': "Effectif moyen annuel",
                             'Etablissement': "Établissement"
                         },
                         color_continuous_scale=[
                             "rgb(0, 43, 51)",  # Tonalité plus foncée de RVB (0, 107, 128)
                             "rgb(0, 107, 128)",  # RVB (0, 107, 128)
                             "rgb(179, 229, 238)"  # Tonalité plus claire de RVB (0, 107, 128)
                         ])

        # Ajouter la ligne de la moyenne nationale
        fig.add_hline(y=moyenne_nationale, line_dash="dash", 
                      annotation_text=f"Moyenne nationale ({moyenne_nationale:.0f})", 
                      annotation_position="top right", 
                      line_color="red")

    elif option_classement == "Nombre moyen de diplômés par formation":
        # Calcul du nombre moyen de diplômés (entrants + sortants) par libellé de formation
        df_grouped_formation = df_etablissement.groupby(["Etablissement", "Libellé du diplôme"]).agg({
            'Nombre de sortants': 'mean',
            'Nombre de poursuivants': 'mean'
        }).reset_index()

        # Ajouter une colonne pour le total moyen des diplômés (entrants + sortants)
        df_grouped_formation['Total Diplômés Moyens'] = df_grouped_formation['Nombre de sortants'] + df_grouped_formation['Nombre de poursuivants']

        # Calculer l'effectif moyen annuel pour chaque établissement par formation
        df_mean_formation = df_grouped_formation.groupby('Etablissement').agg({
            'Total Diplômés Moyens': 'mean'
        }).round(0).reset_index()

        # Calculer la moyenne nationale pour le total des diplômés moyens
        moyenne_nationale_formation = df_mean_formation['Total Diplômés Moyens'].mean()

        # Trier par ordre décroissant du nombre moyen de diplômés et prendre les 3 premiers
        df_mean_formation = df_mean_formation.sort_values(by='Total Diplômés Moyens', ascending=False).head(3)

        # Créer une visualisation
        fig = px.scatter(df_mean_formation, 
                         y='Total Diplômés Moyens', 
                         x='Etablissement', 
                         size='Total Diplômés Moyens', 
                         color='Total Diplômés Moyens',
                         hover_name='Etablissement',
                         labels={
                             'Total Diplômés Moyens': "Moyenne des diplômés (Entrants + Sortants)",
                             'Etablissement': "Établissement"
                         },
                         color_continuous_scale=[
                             "rgb(51, 0, 51)",  # Tonalité plus foncée de violet
                             "rgb(153, 0, 153)",  # Tonalité de violet moyen
                             "rgb(255, 179, 255)"  # Tonalité plus claire de violet
                         ])

        # Ajouter la ligne de la moyenne nationale
        fig.add_hline(y=moyenne_nationale_formation, line_dash="dash", 
                      annotation_text=f"Moyenne nationale ({moyenne_nationale_formation:.0f})", 
                      annotation_position="top right", 
                      line_color="red")

    # Mettre à jour la disposition pour améliorer l'affichage
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))

    # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

# Exécution de la fonction principale
if __name__ == "__main__":
    load_view()
 