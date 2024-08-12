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
        video_file = open("./data/8088339-hd_720_1280_30fps.mp4", 'rb')
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode('utf-8')

        # Affichage de la vidéo avec autoplay
        video_html = f"""
            <video width="100%" height="auto" controls autoplay>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)


    # Affichage du texte Markdown dans la deuxième colonne
    with col2:
        st.markdown("""
        Tour d'horizon des débouchés des formations licences professionnelles, Master LMD et Master MEEF dispensées par les établissements d'enseignement supérieur"

        ### Author and editor of the present investigation : French " Ministère de l'Enseignement Supérieur et de la Recherche".

        on the data basis provided by Ministère de l'Enseignement Supérieur et de la Recherche, thos pages trhough the app, help us understand *
        how the French educational system is spread all over French régions ans West Indies and how they all deliver a diploma opening the doors of working world.

        The analysis pages underline how wide is the range of matters and majors.

    
        ## investigation Hypothesis
        
        1. evaluate the accuracy of the differents years provided
        2. clean and keep accurate data that can be efficient to analyse
        3. acquire a relevant knowledge of the provided data leading to an valid conclusion confirming the initial question
        4. Analyze and explore the data
        5. Visualize  and present the final conclusion
     
        Knowing from a training set of samples listing passengers who survived or did not survive the Titanic disaster, can our model determine based on a given test dataset not containing the survival information, if these passengers in the test dataset survived or not.
        We may also want to develop some early understanding about the domain of our problem. This is described on the Kaggle competition description page here. Here are the highlights to note.

        """)

if __name__ == "__main__":
    load_view()