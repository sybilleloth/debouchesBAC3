import streamlit as st
from streamlit_folium import folium_static, st_folium  # Importer folium_static
from streamlit.components.v1 import html
import pandas as pd
import numpy as np

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import folium #https://python-visualization.github.io/folium/latest/getting_started.html ou https://folium.streamlit.app/
import leafmap.foliumap as leafmap

import matplotlib.pyplot as plt
import seaborn as sns


def load_view():
# Fonction pour charger les données
    csv_file = "./data/esr_intersup_nettoye.csv"
    try:
        df = pd.read_csv(csv_file)
        print("Fichier chargé avec succès.")
        df = df
    except FileNotFoundError:
        print(f"Le fichier {csv_file} est introuvable.")
        
    except Exception as e:
        print(f"Une erreur est survenue lors du chargement du fichier: {e}")
        

# affichage et appel pour la vue de la page dataset
    st.title('Présentation du jeu de donnéees nettoyé')
    st.markdown("""
    ### Section 1: Introduction - Description du Projet
    """)

    st.write(f"**Taille du jeu de données (lignes, colonnes):** {df.shape}")
    st.dataframe(df)

    display_map()
    st.header("visualisations facilitant la prise de connaissance des données\n")
    col1, col2 = st.columns(2)
    with col1:
        display_corr_var()
    with col2:
        data_heat()

import streamlit as st
import pandas as pd
import pydeck as pdk

def display_map_pydeck():
    st.header("Carte Interactive des Académies en France")
    # Chargement des données
    csv_file = "./data/esr_nettoye_avec_cities.csv"
    df = pd.read_csv(csv_file)

    st.markdown("### Carte Interactive des Académies en France\n Cette carte du monde présente la répartition géographique de l'ensemble des lignes du dataset. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")
    
    # Filtrer les coordonnées valides
    valid_geo_df = df[
        df['latitude'].between(-90, 90) &
        df['longitude'].between(-180, 180)
    ]
    
    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return
    
    # Configuration de Pydeck pour afficher la carte
    view_state = pdk.ViewState(
        latitude=46.603354,
        longitude=1.888334,
        zoom=6,
        pitch=50,
    )

    layer = pdk.Layer(
        'ScatterplotLayer',
        data=valid_geo_df,
        get_position='[longitude, latitude]',
        get_radius=10000,
        get_color='[200, 30, 0, 160]',
        pickable=True,
    )

    # Rendu de la carte
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Académie: {Académie}\nNombre de sortants: {Nombre de sortants}\nNombre de poursuivants: {Nombre de poursuivants}"}
    )

    st.pydeck_chart(deck)

# Appel de la fonction pour afficher la carte avec Pydeck
if __name__ == "__main__":
    display_map_pydeck()


import streamlit as st
import pandas as pd
import plotly.express as px

def display_map_plotly():
    st.header("Carte Interactive des Académies en France")
    # Chargement des données
    csv_file = "./data/esr_nettoye_avec_cities.csv"
    df = pd.read_csv(csv_file)

    st.markdown("### Carte Interactive des Académies en France\n Cette carte du monde présente la répartition géographique de l'ensemble des lignes du dataset. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")
    
    # Filtrer les coordonnées valides
    valid_geo_df = df[
        df['latitude'].between(-90, 90) &
        df['longitude'].between(-180, 180)
    ]

    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return

    fig = px.scatter_mapbox(valid_geo_df,
                            lat="latitude", lon="longitude",
                            hover_name="Académie",
                            hover_data=["Nombre de sortants", "Nombre de poursuivants"],
                            color_discrete_sequence=["blue"],
                            zoom=5, height=500)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig)

# Appel de la fonction pour afficher la carte avec Plotly
if __name__ == "__main__":
    display_map_plotly()



def display_map_leafmap():
    st.header("Carte Interactive des Académies en France")
    # Chargement des données
    csv_file = "./data/esr_nettoye_avec_cities.csv"
    df = pd.read_csv(csv_file)

    st.markdown("### Carte Interactive des Académies en France\n Cette carte du monde présente la répartition géographique de l'ensemble des lignes du dataset. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")
    
    # Filtrer les coordonnées valides
    valid_geo_df = df[
        df['latitude'].between(-90, 90) &
        df['longitude'].between(-180, 180)
    ]

    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return

    m = leafmap.Map(center=[46.603354, 1.888334], zoom=6)
    m.add_points_from_xy(valid_geo_df, x="longitude", y="latitude", popup=["Académie", "Nombre de sortants", "Nombre de poursuivants"])
    
    m.to_streamlit(width=700, height=500)

# Appel de la fonction pour afficher la carte avec Leafmap
if __name__ == "__main__":
    display_map_leafmap()




def display_corr_var():
    st.markdown("### Corrélation entre les variables\n ")
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)
    # Sélectionner uniquement les colonnes numériques pour le calcul de la corrélation
    numeric_var = df.select_dtypes(include=['float64', 'int64'])

    # Calculer la matrice de corrélation pour les colonnes numériques uniquement
    corr_matrix = numeric_var.corr()

    # Créer une heatmap pour visualiser la matrice de corrélation
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Heatmap de la corrélation des variables')

    # Afficher la figure dans Streamlit
    st.pyplot(plt)



def data_heat():
    st.markdown("### Rapport entre sortants et poursuivants à l'issue des formations étudiées\n ")  
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)

    # Extraction des colonnes d'intérêt
    x = df["Nombre de poursuivants"]
    y = df["Nombre de sortants"]

    # Génération de couleurs et tailles aléatoires pour chaque point
    colors = np.random.rand(len(df))
    sizes = 1000 * np.random.rand(len(df))

    # Création du graphique de dispersion
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='inferno')
    plt.colorbar()  # Affichage de l'échelle des couleurs
    plt.xlabel('Nombre de poursuivants')
    plt.ylabel('Nombre de sortants')
    plt.title('Scatter Plot: Nombre de poursuivants vs Nombre de sortants')

    # Affichage de la figure dans Streamlit
    st.pyplot(plt)

# Exécution des fonctions avec gestion des états
if __name__ == "__main__":
    load_view()