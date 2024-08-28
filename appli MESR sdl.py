import streamlit as st
import utils as utl
import json
from src.views import home, dataset, goal, analysis, conclusion, thanks, login, logout, who
from src.router import get_route, redirect
import leafmap.foliumap as leafmap
import pandas as pd

st.set_page_config(layout="wide", page_title='Navbar sample')
# st.set_option('deprecation.showPyplotGlobalUse', False) inutile avec la nouvelle version de streamlitVersion 1.37.0 Release date: July 25, 2024
utl.inject_custom_css()
utl.navbar_component()

def navigation():  

    #Loading Cookies
    with open('session.json') as json_file:
        SESSION = json.load(json_file)
    
    #Non user in cookies 
    if SESSION["email"] == "":
        redirect("login")
    
    route = get_route()
    st.write(f"La route actuelle est {route}")
    if route == "/home":
        home.load_view()
    
    elif route == "/goal":
        goal.load_view()
    
    elif route == "/dataset":
        dataset.load_view()
        
        def display_map_leafmap2():
            st.header("Carte Interactive des Académies en France ")
            # Chargement des données
            csv_file = "./data/esr_nettoye_avec_cities.csv"
            df = pd.read_csv(csv_file)

            st.markdown("### Carte Interactive des Académies en France\n Cette carte du monde présente la répartition géographique de l'ensemble des lignes du dataset. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")
            
            # Filtrer les coordonnées valides
            valid_geo_df = df[
                df['latitude'].between(-90, 90) &
                df['longitude'].between(-180, 180)
            ]

            print("ok1")
            if valid_geo_df.empty:
                st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
                return
            print("ok2")
            m = leafmap.Map(center=[46.603354, 1.888334], zoom=6)
            print("ok3")
            m.add_points_from_xy(valid_geo_df, x="longitude", y="latitude", popup=["Académie", "Nombre de sortants"])
            print("ok4")   
            m.to_streamlit(width=600, height=400)
            print("ok5")   
        display_map_leafmap2()
    elif route == "/analysis":
        analysis.load_view()
        
    elif route == "/conclusion":
        conclusion.load_view()

    elif route == "/who":
        who.load_view()

    elif route == "/thanks":
        thanks.load_view() 

    elif route == "/logout":
        logout.load_view()
    elif route == "/login":
        login.load_view()

    #else:
        #redirect("/home")
        #home.load_view()

navigation()

