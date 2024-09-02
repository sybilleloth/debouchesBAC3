import streamlit as st
import utils as utl
import json
import leafmap.foliumap as leafmap
import pandas as pd

from src.views import home, dataset, goal, analysis, conclusion, thanks, login, logout, who
from src.router import get_route, redirect


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
    print(f"La route actuelle est {route}")
    if route == "/home":
        home.load_view()
    
    elif route == "/goal":
        goal.load_view()
    
    elif route == "/dataset":
        dataset.load_view()
        
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
    else:
        home.load_view()
navigation()

