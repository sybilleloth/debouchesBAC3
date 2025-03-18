import streamlit as st
import re
from src.controllers.auth import auth
from src.controllers.signup import signup, email_exists
from src.router import redirect
import base64
import random
import string
from captcha.image import ImageCaptcha

@st.cache_data

def password_valid(password):
    """ Vérification du respect des critères de sécurité du mot de passe """
    return (len(password) >= 12 and
            bool(re.search(r"[A-Z]", password)) and
            bool(re.search(r"[a-z]", password)) and
            bool(re.search(r"\d", password)) and
            bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)))
# génération du code captcha
def generate_captcha():
    """ Génère un CAPTCHA et l'initialise dans la session """
    if "Captcha" not in st.session_state:
        st.session_state['Captcha'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        st.session_state['captcha_valid'] = False
        st.session_state['captcha_text'] = ""
        st.session_state['button_clicked'] = False  # État du bouton

# Mise à jour du texte saisi
def update_captcha_text():
    if "captcha_input" in st.session_state:
        st.session_state["captcha_text"] = st.session_state["captcha_input"].strip()
        print("Mise à jour du texte CAPTCHA :", st.session_state["captcha_text"])

#  Mise à jour de l'état du bouton
def button_click():
    st.session_state["button_clicked"] = True
    print("Mise à jour de l'état du bouton:", st.session_state["button_clicked"])

#  Affichage du CAPTCHA
def display_captcha():
    """ Affichage du CAPTCHA avec gestion de l'état """
    st.subheader(" Vérification CAPTCHA")

    generate_captcha()  # génère le captcha si n'existe pas

    col1, col2 = st.columns([1, 2])

    with col1:
        image = ImageCaptcha(width=100, height=50)
        captcha_image = image.generate(st.session_state['Captcha'])
        st.image(captcha_image, caption="Recopiez le texte", use_column_width=True)

    with col2:
        print(f" CAPTCHA attendu : `{st.session_state['Captcha']}`")  # Debug

        # Champ de saisie avec `on_change`
        st.text_input(
            " Entrez le CAPTCHA :",
            key="captcha_input",
            on_change=update_captcha_text
        )

        print(f"Texte enregistré : `{st.session_state.get('captcha_text', '')}`")  # Debug

        # Bouton de validation avec gestion d'état
        if st.session_state.get("captcha_text", "").strip():
            if st.button("✅ Valider le CAPTCHA", on_click=button_click):
                pass  # `button_click` met à jour l'état

    # Vérification après clic
    if st.session_state.get("button_clicked", False):
        if st.session_state["captcha_text"].lower() == st.session_state['Captcha'].lower():
            st.success(" CAPTCHA validé !")
            st.session_state['captcha_valid'] = True
            del st.session_state['Captcha']  # Supprime le CAPTCHA validé
            st.rerun()
        else:
            st.error("❌ CAPTCHA incorrect. Essayez encore.")
            st.session_state["button_clicked"] = False  # Réinitialise l'état du bouton

    # Bloquer processus tant que le CAPTCHA n'est pas validé
    if not st.session_state.get('captcha_valid', False):
        st.warning("Veuillez valider le CAPTCHA avant de continuer.")
        st.stop()

def load_view():
    video_file = open("./src/assets/images/7945680-hd_1920_1080_25fps.mp4", 'rb')
    video_bytes = video_file.read()
    video_base64 = base64.b64encode(video_bytes).decode('utf-8')

    video_html = f"""
        <video width="50%" height="auto" controls autoplay>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    """
    st.markdown(video_html, unsafe_allow_html=True)

    st.title("Veuillez vous identifier pour accéder aux pages de l'analyse")
    agree = st.checkbox(
        "Je donne mon accord pour entrer mon adresse mail me permettant d'accéder aux fonctionnalités de l'application. "
        "Cette adresse permet de vérifier que vous êtes un humain et ne sera utilisée à aucune autre fin que celle de l'accès à l'application."
    )

    if not agree:
        st.warning('Cette application, pour des raisons de sécurité, ne peut être accessible sans coordonnées mail')
        return

    email = st.text_input('Email', '')
    password = st.text_input('Mot de passe', '', type='password')
    confirm_password = st.text_input('Confirmez votre mot de passe', '', type='password')

    st.write("Que souhaitez-vous faire ?")
    col1, col2 = st.columns([1, 1], gap="small")
    log_in_button = col1.button('Vous connecter avec vos identifiants')
    sign_up_button = col2.button('Créer vos identifiants')

    if log_in_button:
        if not password_valid(password):
            st.error("""Votre mot de passe doit comporter un minimum de 12 caractères
                      dont au moins un caractère spécial,
                      un chiffre,
                      une lettre minuscule et une lettre majuscule,
                      ne pas comprendre de mots ni suite de chiffres ou de lettres ni information personnelle.""")
            return
        print("couple email / mdp valide")
        if not st.session_state.get('captcha_valid', False):
            display_captcha()
            return
        
        print("passage à l'authentification")
        res = auth(email, password)
        if res:
            st.success("Identification réussie. Redirection en cours")
            st.session_state['logged_in'] = True
            redirect("home", reload=True)
        else:
            st.error("Erreur d'adresse mail ou de mot de passe ou bien manque de consentement")

    elif sign_up_button:
        if email_exists(email):
            st.error("⚠️ Cet email est déjà utilisé. Veuillez choisir un autre email ou vous connecter.")
            return

        if not password_valid(password):
            st.error("""Votre mot de passe doit comporter un minimum de 12 caractères
                      dont au moins un caractère spécial,
                      un chiffre,
                      une lettre minuscule et une lettre majuscule,
                      ne pas comprendre de mots ni suite de chiffres ou de lettres ni information personnelle.""")
        elif password != confirm_password:
            st.error("Les mots de passe ne correspondent pas. Veuillez les saisir à nouveau.")
        else:
            res = signup(email, password)
            if not res:
                st.error("Cette adresse mail est déjà enregistrée avec son propre mode de passe. Merci de vous identifier à nouveau.")
            else:
                st.success("Enregistrement de vos identifiants et connexion en cours! ")
                redirect("home", reload=True)

if __name__ == "__main__":
    load_view()
