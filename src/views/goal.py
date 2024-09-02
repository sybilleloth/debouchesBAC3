import streamlit as st
import pandas as pd

import numpy as np
import pandas as pd


def load_view():    
    
    st.title(":dart: tour d'horizon des débouchés des formations licences professionnelles, Master LMD et Master MEEF dispensées par les établissements d'enseignement supérieur")
    st.header("Contexte et objectif du projet")
    st.markdown("### 1 : Introduction : pourquoi ? \n La pratique professionnelle met en lumière combien la formation générale et technique reste malgré tous les bouleversements économiques, sanitaires, innovants... essentielle au démarrage d'une vie professionnelle.    \nLes carrières individuelles peuvent souvent ne pas être linéaires! Or, notre système éducatif supérieur français ouvre un champ très large aux jeunes dans le choix des formations et de leurs spécialités.  \nCeci pose la question de l'égalité des chances à l'entrée dans le monde du travail que nous considérerons au démarrage d'une carrière, comme celui de l'entrée dans le système salarié.    \n")

    st.markdown("### 2 : Objectif \n Cette application vise donc à étudier s'il existe des écarts selon les régions et les types de formations, sur le délai d'arrivée sur le marché du travail, à l'issue des formations \n MASTER LMD et \n licences professionnelles spécialités. \n")

    st.markdown("### 3 : Quelle base de travail ? \n Nous disposons d'un jeu de données publiées au second semestre 2023 (mis à disposition en octobre 2023) sur le site data.gouv.fr \n")

    st.title("Présentation du dataset (jeu de données) original")
    csv_file = "./data/fr-esr-insersup.csv"
    
    try:
        df = pd.read_csv(csv_file, sep = ";")
        print("Fichier chargé avec succès.")
        df = df
    except FileNotFoundError:
        print(f"Le fichier {csv_file} est introuvable.")
        
    except Exception as e:
        print(f"Une erreur est survenue lors du chargement du fichier: {e}")
    

    st.markdown("Les résultats présentés sont issus de l'enquête nationale sur l'insertion professionnelle des diplômés de l’université. Elle a pour objet d'évaluer la situation professionnelle, 18 mois puis 30 mois après l’obtention du diplôme, des diplômés français issus de la formation initiale, n'ayant pas poursuivi ou repris d'études dans les deux années suivant l'obtention de leur diplôme. Le dispositif d'enquête annuelle est coordonné par le ministère de l'Enseignement supérieur et de la Recherche et administré par les universités. Résultats de l'enquête sur les diplômés 2020 : Enquête réalisée entre décembre 2022 et mai 2023 \n ces résultat présentent les données relatives à l Insertion professionnelle des diplômés des établissements d’enseignement supérieur – Dispositif InserSup")
    
    # df est bien un DataFrame ?
    if isinstance(df, pd.DataFrame):
        st.write(f"Taille du jeu de données (lignes et colonnes) : {df.shape} \n")
        st.dataframe(df)
    else:
        st.error("Erreur : le fichier CSV n'a pas été chargé correctement en DataFrame.")
        print("Erreur : le fichier CSV n'a pas été chargé correctement en DataFrame.")

   
if __name__ == "__main__":
    load_view()
