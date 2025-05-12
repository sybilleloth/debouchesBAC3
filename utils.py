import streamlit as st
import base64
from streamlit.components.v1 import html

from PATHS import NAVBAR_PATHS, SETTINGS #fichier correspondance entre titres du menu et nom des pages d'exécution et visualisation


def inject_custom_css(): #injection des styles CSS dans l'app par la lecture du fichier css : styles puis en l'injectant dans le HTML de l'app via st.markdown avec le paramètre unsafe_allow_html=True
    with open('src/assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 
        # écrire du Markdown/html etc. dans l'application
        #  enveloppage du contenu de styles.css dans <style> (balise) et l'injecte ensuite dans l'app
        # unsafe_allow_html=True #rend brut l'html et le css dans l'app

def navbar_component(): #créer la barre de navigation dans STr. avec gestion dynamique des éléments de navigation et un menu déroulant pour les paramètres
    # Elle utilise une combinaison de HTML, CSS, JavaScript et Streamlit 
    with open("src/assets/images/picto reglage sdl.png", "rb") as image_file: #ouverture du fichier puis lecture en binaire 
        image_as_base64 = base64.b64encode(image_file.read()) #encodage de l'image en base 64
        #with -> fermeture du fichier
#   génération dynamique des liens de navigation dans l'app web à partir du dictionnaire de chemins dans fichiers PATHS (menu du haut) et SETTINGS (sous la roue)
    navbar_items = ''
    for key, value in NAVBAR_PATHS.items():
        navbar_items += (f'<a class="navitem" href="/?nav=%2F{value}">{key}</a>')

    settings_items = ''
    for key, value in SETTINGS.items():
        settings_items += (
            f'<a href="/?nav={value}" class="settingsNav">{key}</a>')

    component = rf'''
            <nav class="container navbar" id="navbar">
                <ul class="navlist">
                {navbar_items}
                </ul>
                <div class="dropdown" id="settingsDropDown">
                    <img class="dropbtn" src="data:image/png;base64, {image_as_base64.decode("utf-8")}"/>
                    <div id="myDropdown" class="dropdown-content">
                        {settings_items}
                    </div>
                </div>
            </nav>
            '''
    st.markdown(component, unsafe_allow_html=True)
    js = '''
    <script>
        // navbar elements
        var navigationTabs = window.parent.document.getElementsByClassName("navitem");
        var cleanNavbar = function(navigation_element) {
            navigation_element.removeAttribute('target')
        }
        
        for (var i = 0; i < navigationTabs.length; i++) {
            cleanNavbar(navigationTabs[i]);
        }
        
        // Dropdown hide / show
        var dropdown = window.parent.document.getElementById("settingsDropDown");
        dropdown.onclick = function() {
            var dropWindow = window.parent.document.getElementById("myDropdown");
            if (dropWindow.style.visibility == "hidden"){
                dropWindow.style.visibility = "visible";
            }else{
                dropWindow.style.visibility = "hidden";
            }
        };
        
        var settingsNavs = window.parent.document.getElementsByClassName("settingsNav");
        var cleanSettings = function(navigation_element) {
            navigation_element.removeAttribute('target')
        }
        
        for (var i = 0; i < settingsNavs.length; i++) {
            cleanSettings(settingsNavs[i]);
        }
    </script>
    '''
    html(js)
