import streamlit as st
import re
from src.controllers.auth import auth
from src.controllers.signup import signup
from src.router import redirect
import base64

def password_valid(password):
    if (len(password) >= 8 and 
        re.search(r"[A-Z]", password) and 
        re.search(r"[a-z]", password) and 
        re.search(r"\d", password) and 
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return True
    return False

def load_view():
    # Chemin vers la vidéo locale
    video_file = open("./data/7945680-hd_1920_1080_25fps.mp4", 'rb')
    video_bytes = video_file.read()
    video_base64 = base64.b64encode(video_bytes).decode('utf-8')

    # Affichage de la vidéo avec autoplay et indication de la taille de la vidéo dans la page
    video_html = f"""
        <video width="50%" height="auto" controls autoplay>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    """
    st.markdown(video_html, unsafe_allow_html=True)

        
        
        
    st.title("Veuillez vous identifier pour accéder aux pages de l'analyse")
    agree = st.checkbox(
        "Je donne mon accord pour entrer mon adresse mel me permettant d'accéder aux fonctionnalités de l'application. "
        "Cette adresse permet de vérifier que vous êtes un humain et ne sera utilisée à aucune autre fin que celle de l'accès à l'application."
)
    if agree : 
        st.write('Parfait !')
    else : st.write('Cette application, pour des raisons de sécurité, ne peut être accessible sans coordonnées mail')
    email = st.text_input('Email', '')
    password = st.text_input('Mot de passe', '', type='password')
    col1, col2 = st.columns([1, 1], gap="small")
    with col1:
        log_in_button = st.button('Vous connecter avec vos identifiants')
    with col2:
        sign_up_button = st.button('Créer vos identifiants')

    if log_in_button:
        if not password_valid(password):
            st.error("""Votre mot de passe doit comporter un minimum de 8 caractères
                      dont au moins un caractère spécial, 
                      un chiffre, 
                      une lettre minuscule et une lettre majuscule.""")
        else:
            res = auth(email, password)
            if not res:
                st.error("Wrong Account")
            else:
                st.success("Connexion en cours")
                redirect("home", reload=True)
    
    elif sign_up_button:
        if not password_valid(password):
            st.error("""Votre mot de passe doit comporter un minimum de 8 caractères
                      dont au moins un caractère spécial, 
                      un chiffre, 
                      une lettre minuscule et une lettre majuscule.""")
        else:
            res = signup(email, password)
            if not res:
                st.error("Cette adresse mail est déjà enregistrée avec son propre mode de passe. Merci de vous identifier à nouveau.")
            else:
                st.success("Enregistrement de vos identifiants et connexion en cours! ")
                redirect("home", reload=True)

if __name__ == "__main__":
    load_view()
