import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

def display_map_leafmap():
    st.header("Carte Interactive des Académies en France")
    # Chargement des données
    csv_file = "./data/esr_nettoye_avec_cities.csv"
    df = pd.read_csv(csv_file)

    st.markdown("### map_leafmapCarte Interactive des Académies en France\n Cette carte du monde présente la répartition géographique de l'ensemble des lignes du dataset. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")
    
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
