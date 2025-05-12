import streamlit as st
from urllib.parse import unquote
import time

def get_route():
    url = st.query_params.get("nav")
    url = url[0] if type(url) == list else url
    route = unquote(url) if url is not None else url
    return route

def redirect(new_route, reload=False):
    if new_route[0] != "/":
        new_route = "/" + new_route #nouveau chemin pour rediriger l'utilisateur et"/" au début de la chaîne pour s'assurer que le format est correct pour une URL.
    st.query_params["nav"]=(new_route)  # met à jour les paramètres de requête (query params) de l'application
    time.sleep(0.1) 
    if reload: #force le rechargement de la page après la redirection.
        st.rerun() 
