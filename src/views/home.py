import streamlit as st
from src.views.textcall import Textdisplay

import base64

def load_view():
    st.title("Bienvenue!")
    st.header("Quand je serai grande, je voudrais être ....")

    # Diviser la page en deux colonnes
    col1, col2 = st.columns(2)

    # Affichage de la vidéo dans la première colonne
    with col1:
        # Chemin vers la vidéo locale
        # fille devant son tableau noir : https://www.pexels.com/fr-fr/video/jeune-fille-ecrite-ecole-nombres-8088339/
        video_file = open("./src/assets/images/8088339-hd_720_1280_30fps.mp4", 'rb')
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode('utf-8')

        # Affichage de la vidéo avec autoplay
        video_html = f"""
            <video width="70%" height="auto" controls autoplay>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)


    # Affichage du texte Markdown dans la deuxième colonne
    with col2:
        # Create an instance of the class with 'VF'
        display = Textdisplay('VF') # initialise la méthode
        display.text_homevf()
        display.text_captionvf()

        # Bouton pour afficher la version en français
        if st.button("Read this in English"):
            # Affichage du pop-up avec la version française
            with st.expander("English version"):
                # Create an instance of the class with 'VF'
                display = Textdisplay('UK') # initialise la méthode
                display.text_homeuk()
                display.text_captionuk()

if __name__ == "__main__": #par précaution sur toutes les vues au cas où le script serait importé ailleurs pour garantir son exécution automatique
    load_view()