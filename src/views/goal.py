import streamlit as st
import pandas as pd
import numpy as np


def load_view():    
    st.title(":dart: Tour d'horizon des débouchés des formations licences professionnelles, Master LMD et Master MEEF dispensées par les établissements d'enseignement supérieur")
    
    with st.expander("Contexte et objectif du projet"):
        st.markdown("### 1 : Introduction : pourquoi ? \n La pratique professionnelle met en lumière combien la formation générale et technique reste malgré tous les bouleversements économiques, sanitaires, innovants... essentielle au démarrage d'une vie professionnelle.    \nLes carrières individuelles peuvent souvent ne pas être linéaires! Or, notre système éducatif supérieur français ouvre un champ très large aux jeunes dans le choix des formations et de leurs spécialités.  \nCeci pose la question de l'égalité des chances à l'entrée dans le monde du travail que nous considérerons (pour les besoins de l'exercice) au démarrage d'une carrière, comme celui de l'entrée dans le système salarié.    \n")

        st.markdown("### 2 : Objectif \n Cette application vise donc à étudier s'il existe des écarts selon les régions et les types de formations, sur le délai d'arrivée sur le marché du travail, à l'issue des formations \n MASTER LMD et \n licences professionnelles spécialités. \n")

        st.markdown("### 3 : Quelle base de travail ? \n Nous disposons d'un jeu de données publié au second semestre 2024 (13 août 2024) sur le site data.gouv.fr \n")

    st.title("Présentation du dataset (jeu de données) original")
    csv_file = "./data/fr-esr-insersup 2024_09.csv"
    
    try:
        df = pd.read_csv(csv_file, sep=";")
        print("Fichier dans page goal chargé avec succès.")
    except FileNotFoundError:
        print(f"Le fichier {csv_file} est introuvable.")
        df = None
    except Exception as e:
        print(f"Une erreur est survenue lors du chargement du fichier en page goal : {e}")
        df = None

    with st.expander("Description du dataset"):
        st.markdown("Les résultats présentés sont issus de l'enquête nationale sur l'insertion professionnelle des diplômés de l’université...")

        if isinstance(df, pd.DataFrame):
            st.write(f"Taille du jeu de données (lignes et colonnes) : {df.shape}")
            st.dataframe(df)
        else:
            st.error("Erreur : le fichier CSV n'a pas été chargé correctement.")

    # Afficher le bouton de téléchargement
    dwnload()
    legendes()

    # Lancer le traitement si le fichier a été chargé
    if df is not None:
        with st.expander("Traitement de nettoyage du jeu de données"):
            traitement(df)


def traitement(df):
    st.markdown("Les axes de traitement du dataset ont été les suivants pour répondre à l'objectif de tri des régions, des taux d'emplois, des taux de poursuite/sortie des études des étudiants à l'issue d'un bac+3")
    st.markdown("1. Suppression des colonnes et lignes vides et non significatives voire redondantes")
    st.markdown("2. Conservation des seules formations rattachées à une région précise")
    st.markdown("3. Élimination des lignes pour lesquelles les effectifs poursuivants + sortants sont à zéro")
    st.markdown("4. Élimination des lignes pour lesquelles les taux d'insertion sont tous nuls")
    st.markdown("5. Traitement de forme des libellés, de gestion des minuscules/ majuscules dans les titres et valeurs des différentes colonnes")


def legendes():
    with st.expander("Légendes"):
        st.markdown("""
            ***Taux d'emploi salarié en France*** : part des diplômés en emploi salarié en France parmi l'ensemble des diplômés actifs (en emploi ou en recherche) ou inactifs.
        """)
        st.markdown("**Fonction :**")

        st.latex(r"""
        \frac{\textit{nb\ diplômés\ occupant\ un\ emploi\ salarié\ en}\ \textcolor{red}{\textit{France}}}
        {\textit{nb\ de\ diplômés\ occupant\ un\ emploi} + \textit{nb\ de\ diplômés\ au\ chômage} + \textcolor{red}{\textit{nb\ de\ diplômés\ en\ inactivité}}}
        """)

        st.markdown("""
            ***Sortants et Poursuivants***: La population d’intérêt étant celle des étudiants français de moins de 30 ans, diplômés de Licence ou Master d’une session annuelle N, et ne poursuivant pas d’études en N+1 ou N+2.
            A l'inverse, les sortants sont les étudiants qui quittent le fichier des étudiants inscrits dans un établissement sous tutelle du Ministère de l’enseignement supérieur ou Fichier des apprentis en CFA.
            
            ***Nombre de mois après la diplomation***: correspond à une observation aux dates suivantes :
            - 6 mois décembre de l’année N (1ère semaine du mois)
            - 12 mois juin de l’année N+1 (2nde semaine du mois)
            - 18 mois décembre de l’année N+1 (1ère semaine du mois)
            - 24 mois juin de l’année N+2 (2nde semaine du mois)
            - 30 mois décembre de l’année N+2 (1ère semaine du mois)
            
            ***Flag***: Désigne les promotions de petites taille (<=20) et qui sont groupées sur deux millésimes successifs
        """)


def dwnload():
    fichier_url = "https://raw.githubusercontent.com/datarockstars/projet-fil-rouge-sybilleloth/refs/heads/main/data/fr-esr-insersup%202024_09.csv?token=GHSAT0AAAAAACWWH4A75U34FA5DDJ25PT7EZXK4ERA"
    st.markdown(f"""
        <a href="{fichier_url}" download>
            <button style="padding:10px 20px; font-size:18px;">Télécharger le fichier CSV</button>
        </a>
    """, unsafe_allow_html=True)


# Appel de la fonction dans Streamlit
if __name__ == "__main__":
    load_view()
