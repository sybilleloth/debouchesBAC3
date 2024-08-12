import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

def load_view():    
    st.title('Qui suis-je ?')
    st.markdown("""

    ### FACILITATRICE - METHODE - CHALLENGE

    7 ans en audit comptable et financier, autant en conseil RH, et 20 ans en marketing et communication, 
    ont aiguisé mon sens de l'expérience client, de la transparence des chiffres et de leur sens !!    
                
    Nous vivons une période tellement passionnante autour de la data.    
                
    Je serais heureuse d'échanger sur la valeur de l'analyse et de la data 
    dans l'enchantement de la relation client!
                
                
    ## Echangeons ensemble :
    """)
    # Chemin de l'image relative
    image_path = "./src/assets/images/logo_li.png"
    
    # Lire et afficher l'image avec le lien
    try:
        image = Image.open(image_path)
        st.image(image, width=100)  # Largeur en pixels (50px correspond environ à 1.5cm)
        st.markdown("""
        <a href="https://www.linkedin.com/in/sybille-dethoor-loth" target="_blank">
            Visitez mon profil LinkedIn
        </a>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("L'image n'a pas été trouvée à l'adresse de chemin spécifié.")
    
    
if __name__ == "__main__":
    load_view()
