import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import os




def load_view():
    st.title('Présentation du Dataset nettoyé')
    st.markdown("### Section 1 : Introduction - Description du projet. \n This is the legendary Titanic ML competition – the best, first challenge for you to dive into ML competitions and familiarize yourself with how the Kaggle platform works. The competition is simple: use machine learning to create a model that predicts which passengers survived the Titanic shipwreck. \nRead on or watch the video below to explore more details. Once you’re ready to start competing, click on the Join Competition button to create an account and gain access to the competition data. Then check out Alexis Cook’s Titanic Tutorial that walks you through step by step how to make your first submission!")
    #lecture du fichier  esr_insersup_nettoye
    csv_file = "./data/esr_intersup_nettoye.csv"

    
    try:
        df = pd.read_csv(csv_file, sep=';')
        print("File loaded successfully")
        # Manipulation des données
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    df = pd.read_csv(csv_file)
    st.dataframe(df)
    