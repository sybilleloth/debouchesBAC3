import streamlit as st
from streamlit_folium import folium_static, st_folium  # Importer folium_static
from streamlit.components.v1 import html
import pandas as pd

import folium
from folium.plugins import MarkerCluster
import folium #https://python-visualization.github.io/folium/latest/getting_started.html

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import os


def load_view():
    st.title('Présentation du Dataset Nettoyé')
    st.markdown("""
    ### Section 1: Introduction - Description du Projet
    This is the legendary Titanic ML competition – the best, first challenge for you to dive into ML competitions and familiarize yourself with how the Kaggle platform works. The competition is simple: use machine learning to create a model that predicts which passengers survived the Titanic shipwreck.

    Read on or watch the video below to explore more details. Once you’re ready to start competing, click on the Join Competition button to create an account and gain access to the competition data. Then check out Alexis Cook’s Titanic Tutorial that walks you through step by step how to make your first submission!
    """)

    # Lecture du fichier esr_intersup_nettoye.csv
    csv_file = "./data/esr_intersup_nettoye.csv"

    try:
        df = pd.read_csv(csv_file, sep=';')
        st.success("Fichier chargé avec succès.")
    except FileNotFoundError:
        st.error(f"Le fichier {csv_file} est introuvable.")
        return
    except Exception as e:
        st.error(f"Une erreur est survenue lors du chargement du fichier: {e}")
        return

    st.write(f"**Taille du jeu de données (lignes, colonnes):** {df.shape}")
    st.dataframe(df)

def display_map():
    st.header("Carte Interactive des Académies en France")
    st.markdown("### Carte Interactive des Académies en France\n Cette carte du monde présente la répartion géographique de l'ensemble des lignes du dataset. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")
   

    # Chemin vers le fichier CSV contenant les coordonnées géographiques
    file_path = './data/esr_nettoye_avec_cities.csv'

    geo_df = pd.read_csv(file_path)
     

    # Vérification des colonnes nécessaires
    required_columns = ['Académie', 'latitude', 'longitude', 'Nombre de sortants', 'Nombre de poursuivants']
    if not all(column in geo_df.columns for column in required_columns):
        st.error("Les colonnes requises ne sont pas présentes dans le fichier de données.")
        return

    # Filtrer les coordonnées valides
    valid_geo_df = geo_df[
        geo_df['latitude'].between(-90, 90) &
        geo_df['longitude'].between(-180, 180)
    ]

    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return

    # Création de la carte centrée sur la France
    france_map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Ajout d'un cluster de marqueurs
    marker_cluster = MarkerCluster().add_to(france_map)

    # Ajout des marqueurs pour chaque académie
    for _, row in valid_geo_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=(
                f"<strong>Académie:</strong> {row['Académie']}<br>"
                f"<strong>Nombre de sortants:</strong> {row['Nombre de sortants']}<br>"
                f"<strong>Nombre de poursuivants:</strong> {row['Nombre de poursuivants']}"
            ),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)

    # Affichage de la carte dans Streamlit
    folium_static(france_map, width=700, height=500)

# Exécution des fonctions
if __name__ == "__main__":
    load_view()
    display_map()
