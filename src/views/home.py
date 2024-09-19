import streamlit as st
from src.router import redirect
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
        st.markdown("""
        Slight introduction : Overview of opportunities for young graduates in professional/global/LMD & MEEF Masters provided by French universities

        ### Author and editor of the present investigation : French " Ministère de l'Enseignement Supérieur et de la Recherche".

        On the dataset basis provided by Ministère de l'Enseignement Supérieur et de la Recherche, those pages displayed through this streamlit app, help us understand 
        how the French educational system is spread all over French régions ans West Indies and how they all deliver a diploma opening the doors of working world.

        The analysis pages underline how wide the range of matters and majors is.

    
        ## investigation hypothesis
        
        1. Evaluate the accuracy of the data provided regarding the period of graduation between 2019 and 2021
        2. Clean and keep accurate data that can be efficient to analyse
        3. Acquire a relevant knowledge of the provided data in order to answer the initial question
        4. Analyze and explore the data
        5. Visualize and present the final conclusion
     
        In  a few words : does the French educational system lead to work all over France equally, are there some favorable universities and how high is the rate of students resuming their studies when they graduate with a BAC + 3 ? 
        """)
        st.caption(" this streamlit app has been developed and set up in Sept. 2024 thanks to open source tools introduced in page (MERCI)")

        # Bouton pour afficher la version en français
        if st.button("lire la version en français"):
            # Affichage du pop-up avec la version française
            with st.expander("Version en français"):
                st.markdown("""
                ### Tour d'horizon des débouchés des formations licences professionnelles, générales, Master LMD et Master MEEF dispensées par les établissements d'enseignement supérieur

                #### Auteur et éditeur de l'enquête : Ministère français de l'Enseignement Supérieur et de la Recherche.
            
                Sur la base des données fournies par le Ministère de l'Enseignement Supérieur et de la Recherche, ces pages affichées à travers cette application Streamlit, 
                nous aident à comprendre comment le système éducatif français est réparti sur toutes les régions françaises et Drom-Com, comment ils délivrent tous un 
                diplôme ouvrant les portes du monde du travail.

                Les pages d'analyse soulignent à quel point la gamme de matières et de majeures est vaste.

                #### Hypothèses de l'enquête
            
                1. Évaluer l'exactitude des données fournies concernant la période de diplomation entre 2019 et 2021.
                2. Nettoyer et conserver des données précises qui peuvent être efficaces pour l'analyse.
                3. Acquérir une connaissance pertinente des données fournies conduisant à une conclusion valide confirmant la question initiale.
                4. Analyser et explorer les données.
                5. Visualiser et présenter la conclusion finale.

                En quelques mots : le système éducatif français mène-t-il au travail de manière égale dans toute la France, y a-t-il des universités plus favorables et quel est le taux d'étudiants poursuivant leurs études lorsqu'ils obtiennent un BAC + 3 ?
                """)
                st.caption(" cette application a été élaborée en septembre 2024 avec le concours d'outils open source présentés en rubrique 'MERCI' ")

if __name__ == "__main__":
    load_view()