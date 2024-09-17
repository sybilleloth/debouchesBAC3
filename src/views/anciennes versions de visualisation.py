import streamlit as st
import pandas as pd
import pydeck as pdk
import leafmap, folium
from folium import st_folium


def national(): #à supprimer dans la version de septembre
    st.header("Cas hors norme : les formations nationales auxquelles ne sont affectées aucune formation ni académie")
    # Chargement des données
    df = pd.read_csv("./data/esr_intersup_nettoye 2024_09.csv")
    df_national = df[df["Académie"] == "National"]
    st.write(f"Le DataFramecorrespondant contient {df_national.shape[0]} lignes et {df_national.shape[1]} colonnes.")
    st.dataframe(df_national)

def map_simple():
    st.header("Carte interactive des académies en France")

    # Chargement des données
    csv_file = "./data/esr_nettoye_avec_cities 2024_09.csv"
    
    df = pd.read_csv(csv_file)

    st.markdown("### Carte interactive des académies en France\n Cette carte du monde présente la répartition géographique de l'ensemble des lignes du dataset. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")
   
    # Filtrer les coordonnées valides
    valid_geo_df = df[
        df['latitude'].between(-90, 90) &
        df['longitude'].between(-180, 180)
    ]

    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return

    # Compter le nombre de lignes pour chaque académie
    acad_count = valid_geo_df.groupby('Académie').size().reset_index(name='Nombre de lignes')
    st.dataframe(acad_count)
    # Vérification des colonnes
    #st.write("Colonnes après groupby:", acad_count.columns)

    # Fusionner avec les données valides pour récupérer les coordonnées
    valid_geo_df = valid_geo_df[['Académie', 'latitude', 'longitude']].drop_duplicates()
    valid_geo_df = pd.merge(valid_geo_df, acad_count, on='Académie')

    # Vérifier le DataFrame fusionné
    #st.write(valid_geo_df.head())  # Vérification des colonnes après fusion
    
    # Création de la carte avec Folium
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Ajouter des points pour chaque académie avec le nombre de lignes dans le popup
    for _, row in valid_geo_df.iterrows():
        # Vérification du contenu de 'row'
        #st.write(f"Row content: {row}")
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Académie: {row['Académie']}<br>Nombre de lignes: {row['Nombre de lignes']}"
        ).add_to(m)

    # Afficher la carte dans Streamlit
    st_folium(m, width=700, height=500)
    st.write("fin")


def display_map_pydeck2():
    st.header("Carte interactive avec PyDeck")

    # Chargement des données
    csv_file = "./data/esr_nettoye_avec_cities 2024_09.csv"
    df = pd.read_csv(csv_file)

    # Filtrer les coordonnées valides
    valid_geo_df = df[df['latitude'].between(-90, 90) & df['longitude'].between(-180, 180)]

    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return

    # Créer une carte PyDeck
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=valid_geo_df,
        get_position='[longitude, latitude]',
        get_radius=10000,
        get_color=[255, 0, 0],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=46.603354,
        longitude=1.888334,
        zoom=6,
        pitch=50,
    )

    # Afficher la carte dans Streamlit
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))



def display_map_pydeck():
    st.header("Carte interactive des académies en France")
    st.markdown("### Carte Interactive des Académies en France\n Cette carte du monde présente la répartition géographique des lignes du jeu de données. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")

    # Chargement des données
    csv_file = "./data/esr_nettoye_avec_cities 2024_09.csv"
    df = pd.read_csv(csv_file)

    # Filtrer les coordonnées valides
    valid_geo_df = df[df['latitude'].between(-90, 90) & df['longitude'].between(-180, 180)]

    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return

    # Créer une couche Scatterplot avec les coordonnées des académies
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=valid_geo_df,
        get_position='[longitude, latitude]',
        get_radius=50000,  # Taille des points
        get_color=[30, 144, 255],  # Couleur des points en RGB
        pickable=True,
    )

    # Définir l'état de vue (centre et zoom)
    view_state = pdk.ViewState(
        latitude=46.603354,
        longitude=1.888334,
        zoom=5,
        pitch=0,
    )

    # Créer une carte PyDeck avec un style clair
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v9'  # Style clair
    )


def display_map_leafmap():
    st.header("Carte interactive des académies en France")

    # Chargement des données
    csv_file = "./data/esr_nettoye_avec_cities 2024_09.csv"
    df = pd.read_csv(csv_file)
    st.write("ok1")
    st.markdown("### Carte Interactive des Académies en France\n Cette carte du monde présente la répartition géographique de l'ensemble des lignes du dataset. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")
    st.write("ok2!")
    # Filtrer les coordonnées valides
    valid_geo_df = df[
        df['latitude'].between(-90, 90) &
        df['longitude'].between(-180, 180)
    ]
    st.write("ok3!")
    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return
    st.write("ok4!")
    #st.write(valid_geo_df[['longitude', 'latitude']].describe()) vérifier que les données gps sont ok dans leur prise en charge
    m = leafmap.Map(center=[46.603354, 1.888334], zoom=6)
    st.write("ok5!")
    m.add_points_from_xy(valid_geo_df, x="longitude", y="latitude", popup=["Académie", "Nombre de sortants", "Nombre de poursuivants"])
    st.write("ok6!")    
    m.to_streamlit(width=700, height=500)
    st.write("ok7!")