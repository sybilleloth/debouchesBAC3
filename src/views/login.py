import streamlit as st
import re
from src.controllers.auth import auth
from src.controllers.signup import signup
from src.router import redirect

def password_valid(password):
    if (len(password) >= 8 and 
        re.search(r"[A-Z]", password) and 
        re.search(r"[a-z]", password) and 
        re.search(r"\d", password) and 
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return True
    return False

def load_view():
    st.title('Veuillez vous identifier')

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
                st.success("Login in progress")
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
                st.error("Cette adresse mail est déjà enregistrée avec son propre mode de passe. Merci de vous identifier.")
            else:
                st.success("enregistrement de vos identifiants en cours! ")
                redirect("home", reload=True)

if __name__ == "__main__":
    load_view()
