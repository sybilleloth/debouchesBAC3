import streamlit as st
from src.router import redirect
import base64

def load_view():
    st.title('Et pour finir...')

    st.header("Tout démarre !!! ")

    # Diviser la page en deux colonnes
    col1, col2 = st.columns(2)

    # Affichage de la vidéo dans la première colonne
    with col1:
        # Chemin vers la vidéo locale
        # lien vers la vidéo https://www.pexels.com/fr-fr/video/femme-ecole-debout-porte-8284321/ verticale de leeloo the first
        video_file = open("./data/8284321-hd_1080_1920_30fps.mp4", 'rb')
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode('utf-8')

        # Affichage de la vidéo avec autoplay et indication de la taille de la vidéo dans la page
        video_html = f"""
            <video width="70%" height="auto" controls autoplay>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)


    # Affichage du texte Markdown dans la deuxième colonne
    with col2:
        st.title('retenons et explorons ... ')
        st.header("blablabla !!! ")
