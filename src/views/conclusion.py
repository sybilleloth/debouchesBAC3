import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import plotly.express as px

def load_view():
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)

    st.title(':medal: Et pour finir...')

    st.header("Tout démarre !!! ")

    # Diviser la page en deux colonnes
    col1, col2 = st.columns(2)

    # Affichage de la vidéo dans la première colonne
    with col1:
        video_file = open("./src/assets/images/8284321-hd_1080_1920_30fps.mp4", 'rb')
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode('utf-8')

        video_html = f"""
            <video width="70%" height="auto" controls autoplay>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)

    # Affichage du texte Markdown dans la deuxième colonne
    with col2:
        total_sortants = df["Nombre de sortants"].sum()
        total_poursuivants = df["Nombre de poursuivants"].sum()
        total_regions = df["Région"].nunique()
        total_etablissements = df["Établissement"].nunique()
        total_academies = df["Académie"].nunique()
        total_disciplines = df["Discipline"].nunique()
        total_periodes = df["Année(s) d'obtention du diplôme prise(s) en compte"].nunique()

        st.title('Retenons de cette exploration...')
        st.header("En synthèse, les données : ")

        donnees_globales = {
            "Périodes de diplomation considérées": total_periodes,
            "Total Effectif des étudiants sortants": total_sortants,
            "Total Effectif des étudiants poursuivant leurs études": total_poursuivants,
            "Nombre de disciplines diplômantes": total_disciplines,
            "Nombre de régions": total_regions,
            "Nombre d'académies": total_academies,
            "Nombre d'établissements": total_etablissements,
        }   

        for i, (legende, value) in enumerate(donnees_globales.items(), start=1):
            st.write(f"{i}. {legende} : {round(value)}")

    st.header("Les marches du podium :")    

    # Chargement des données avec coordonnées
    csv_filec = "./data/esr_nettoye_avec_cities.csv"
    dfc = pd.read_csv(csv_filec)

    # Calcul du nombre moyen de "Libellé du diplôme" par "Académie"
    moyenne_diplomes_par_academie = dfc.groupby('Académie')['Libellé du diplôme'].nunique().mean()
    st.write(f"Nombre moyen de Libellé du diplôme par Académie : {round(moyenne_diplomes_par_academie)}")

    # Calcul du nombre moyen de "Sortants" par "Libellé du diplôme" et par "Académie"
    moyenne_sortants_par_diplome_academie = dfc.groupby(['Académie', 'Libellé du diplôme'])['Nombre de sortants'].mean().mean()
    st.write(f"Nombre moyen de Sortants par Libellé du diplôme et par Académie : {round(moyenne_sortants_par_diplome_academie)}")

    # Calculs par académie pour la carte
    df_academie = dfc.groupby('Académie').agg(
        latitude=('latitude', 'mean'),
        longitude=('longitude', 'mean'),
        moyenne_sortants_academie=('Nombre de sortants', 'mean')
    ).reset_index()

    # Ajout d'une colonne pour le nombre moyen de sortants par libellé du diplôme
    df_academie['moyenne_sortants_par_diplome_academie'] = dfc.groupby(['Académie', 'Libellé du diplôme'])['Nombre de sortants'].mean().groupby('Académie').mean().values

    # Vérifier les données avant de créer la carte
    st.write("Données de l'académie pour la carte:")
    st.write(df_academie.head())  # Affiche les premières lignes pour vérification

    # Préparation des données pour la visualisation
    chart_data = df_academie[['latitude', 'longitude', 'moyenne_sortants_academie', 'moyenne_sortants_par_diplome_academie']].dropna()

    # Affichage de la carte avec pydeck
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=chart_data['latitude'].mean(),
                longitude=chart_data['longitude'].mean(),
                zoom=6,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=chart_data,
                    get_position=['longitude', 'latitude'],
                    get_color=[200, 30, 0, 160],
                    get_radius="moyenne_sortants_par_diplome_academie",
                    pickable=True,
                ),
            ],
            tooltip={
                "html": "<b>Académie:</b> {Académie}<br/><b>Moyenne Sortants par Académie:</b> {moyenne_sortants_academie}<br/><b>Moyenne Sortants par Diplôme par Académie:</b> {moyenne_sortants_par_diplome_academie}",
                "style": {"backgroundColor": "steelblue", "color": "white"}
            }
        )
    )
        # Diviser la page en deux colonnes
    col3, col4 = st.columns(2)
    with col3 : 
        top3_formation("Libellé du diplôme", "formations","Taux d'emploi","taux d'emploi")
    with col4 : 
        top3_formation("Libellé du diplôme", "formations","Mois après la diplomation","temps nécessaire à la prise de poste en emploi")
def top3_formation(criteria, texte1,cible,texte2):
    # Affiche les 3 formations avec le taux d'emploi le plus favorable pour chaque type de diplôme.
    # Chemin vers le fichier CSV
    csv_file = "./data/esr_intersup_nettoye.csv"

    # Charger les données depuis le fichier CSV
    df = pd.read_csv(csv_file)
    
    st.write(f"Les 3 {texte1} dont le {texte2} est le plus favorable par typologie de diplôme : Licence pro, Master ou MEEF")

    # Filtrer les données pertinentes
    df_filtered = df[["Type de diplôme", criteria, cible]].dropna()

    # Vérification des valeurs uniques dans la colonne "Type de diplôme"
    unique_diplomes = df_filtered["Type de diplôme"].unique()
    #st.write("Types de diplômes présents dans les données :", unique_diplomes)

    # Filtrer et trier pour chaque type de diplôme
    diplomes = ["Licence professionnelle", "Master LMD", "Master MEEF"]

    # Concaténer les top 3 pour chaque diplôme
    top_formations = pd.DataFrame()

    for diplome in diplomes:
        df_diplome = df_filtered[df_filtered["Type de diplôme"] == diplome]
        top_3_formations = df_diplome.sort_values(by=cible, ascending=False).head(3)
        top_formations = pd.concat([top_formations, top_3_formations])

    # Vérification des données concaténées
    st.write("Top formations par diplôme :", top_formations)

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
        title="Le top 3 avec le {texte2} le plus favorable par type de diplôme"
    )

    # Afficher le graphique
    st.plotly_chart(fig)

# Exécution de la fonction principale
if __name__ == "__main__":
    load_view()

    st.write("Les 3 formations menant le plus rapidement les étudiants dits sortants vers la prise de poste : licence pro, Master ou MEEF")
    st.write("Les 3 régions dont le taux d'emploi est le plus favorable sur l'ensemble des formations : licence pro, Master ou MEEF")
    st.write("Les 3 régions menant le plus rapidement les étudiants dits sortants vers la prise de poste : licence pro, Master ou MEEF")
    st.write("Les 3 formations comprenant le plus fort taux d'étudiants poursuivant après l'obtention de leur BAC + 3 : licence pro, Master ou MEEF")
    st.write("Les 3 régions comprenant le plus fort taux d'étudiants poursuivant après l'obtention de leur BAC + 3 : licence pro, Master ou MEEF")
