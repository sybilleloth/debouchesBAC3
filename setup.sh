#bin/bash
#Ce script shell a pour objectif de préparer l'environnement et de lancer une application Streamlit en suivant les 3 étapes suivantes:
# il permet d'automatiser l'installation et l'exécution de l'application avec une seule commande dans le terminal, en exécutant simplement ce script.
pip install -r requirements.txt #installe les librairies utiles à l'appli listées dans requirements
python3 setup.py #execution d'un script de configuration setup.py qui pourrait configurer le projet
streamlit run sortiebac3enFrance.py # lance l'application Streamlit en exécutant sortiebac3enFrance.py.