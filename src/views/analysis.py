import streamlit as st
# data analysisimport pandas as pd
import pandas as pd
import numpy as np
import random as rnd

# visualisation 
import plotly.express as px
import random as rnd
import seaborn as sns
import matplotlib.pyplot as plt

# Définition de la fonction de chargement des données et de visualisation principale
def load_view():
    st.title('Analyses et visualisations')

    st.header("Diversité des diplômes Bac + 3")
    viz_speciality_diploma_type()
    
    st.header("Popularité des domaines disciplinaires et des spécialités")
    col1, col2 = st.columns(2)
    with col1:
        viz_ranking_discipline()
    with col2:
        viz_ranking_speciality()
    st.header("Palmarès des régions en termes de taux d'emploi salarié pour les Bac +3")
    col3, col4 = st.columns(2)
    with col3:
        viz_map_ranking()
    with col4:
        viz_ranking_region()

#ci-dessous, ajout des visualisations par SDL

def visualisation():
    st.header("Visualisation des données")
    
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)
    
    # Sélection de la visualisation
    visualisation_type = st.selectbox("Choisissez le type de visualisation", ["Box Plot", "Bar Plot"])
    
    if visualisation_type == "Box Plot":
        # Sélection de l'académie
        academies = st.multiselect("Sélectionnez les académies", df['Académie'].unique(), default=df['Académie'].unique())
        df_filtered_academy = df[df['Académie'].isin(academies)]
        
        # Sélection de la région
        regions = st.multiselect("Sélectionnez les régions", df['Région'].unique(), default=df['Région'].unique())
        df_filtered_région = df_filtered_academy[df_filtered_academy['Région'].isin(regions)]

        # Créer un box plot pour visualiser la répartition du Taux d'insertion par académie
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Académie', y="Taux d'emploi", data=df_filtered_academy)
        plt.title("Répartition du Taux d'insertion par académie")
        plt.xlabel('Académie')
        plt.ylabel("Taux d'emploi")
        st.pyplot(plt)
        
    elif visualisation_type == "Bar Plot":
        # Grouper par académie et calculer les statistiques descriptives
        stats = df.groupby('Académie')["Taux d'emploi"].describe()
        st.write("Statistiques descriptives du taux d'emploi par académie:")
        st.write(stats)

        # Calculer la moyenne et l'écart-type par académie
        mean_std = df.groupby('Académie')["Taux d'emploi"].agg(['mean', 'std'])
        st.write("Moyenne et écart-type par académie:")
        st.write(mean_std)

        # Créer un graphique à barres classant les académies selon la moyenne du Taux d'emploi
        fig, ax = plt.subplots(figsize=(12, 8))
        mean_std_sorted = mean_std.sort_values('mean', ascending=False)
        bars = ax.bar(mean_std_sorted.index, mean_std_sorted['mean'], yerr=mean_std_sorted['std'], capsize=5, color='#77264bff')
        ax.set_title("Classement des académies selon la moyenne du Taux d'emploi")
        ax.set_xlabel('Académie')
        ax.set_ylabel("Taux d'emploi moyen")
        ax.set_ylim([mean_std_sorted['mean'].min(), 100]) # Réduction de la taille des barres pour un confort de lecture et amplification des écarts: ne garder que la plage min - 100%
        plt.xticks(rotation=90)  # Rotation des noms d'académie pour meilleure lisibilité
        
        # Ajouter des annotations pour chaque barre
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center', fontsize=10)

        st.pyplot(fig)

# Définition de la fonction présentant la diversité d'offre de formation par région
def viz_speciality_diploma_type():
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)
    
    # Sélectionner les types de diplôme
    types_diplome = st.multiselect("Sélectionnez les types de diplôme", df['Type de diplôme'].unique(), default=df['Type de diplôme'].unique(), key='type_diplome')
    
    # Filtrer le DataFrame en fonction des types de diplôme sélectionnés
    df_filtered = df[df['Type de diplôme'].isin(types_diplome)]
    
    # Présenter le nombre de disciplines sur l'ensemble du territoire et pour chacune, le nombre de spécialités
    st.write(f"Le nombre de domaines de discipline enseignés en France pour les types de diplôme sélectionnés est de : {df_filtered['Domaine disciplinaire'].nunique()} correspondant à {df_filtered['Libellé du diplôme'].nunique()} spécialités")
    
    # Grouper par région et compter les libellés de diplôme
    libelle_count = df_filtered.groupby('Région')['Libellé du diplôme'].nunique()
    st.write(f"Nombre de spécialités dispensées avec un diplôme Bac +3 par région :")
    #st.write(libelle_count)
    
    # Grouper par région et compter les valeurs uniques de "Domaine disciplinaire"
    domaine_count = df_filtered.groupby('Région')['Domaine disciplinaire'].nunique()
    
    # Créer un DataFrame combiné pour les annotations
    combined_df = libelle_count.reset_index().merge(domaine_count.reset_index(), on='Région')
    combined_df.columns = ['Région', 'Nombre de libellés de diplôme', 'Nombre de domaines disciplinaires']
    
    # Trier le DataFrame par 'Nombre de libellés de diplôme' en ordre descendant
    combined_df = combined_df.sort_values(by='Nombre de libellés de diplôme', ascending=False)
    
    # Créer un graphique à barres interactif avec Plotly
    fig = px.bar(combined_df, 
                 x='Région', 
                 y='Nombre de libellés de diplôme', 
                 color_discrete_sequence=['#77264B'],
                 hover_data={'Nombre de domaines disciplinaires': True},
                 title='Nombre de libellés de diplôme par région')
    
    fig.update_layout(xaxis_title='Région', yaxis_title='Nombre de libellés de diplôme')
    
    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

def viz_ranking_discipline():
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)
    
    # Calculer le total des "nombre de poursuivants" + "nombre de sortants" pour chaque discipline
    df['Total'] = df['Nombre de poursuivants'] + df['Nombre de sortants']
    total_by_discipline = df.groupby('Domaine disciplinaire')['Total'].sum().reset_index()
    
    # Sélectionner les 5 disciplines avec les valeurs les plus élevées
    top_5_disciplines = total_by_discipline.nlargest(5, 'Total')
    
    # Créer un graphique en camembert interactif avec Plotly
    fig = px.pie(top_5_disciplines, 
                 values='Total', 
                 names='Domaine disciplinaire', 
                 title='Top 5 des disciplines par nombre de poursuivants et sortants',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    
    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

def viz_ranking_speciality():
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)
    
    # Ajouter des sélections multiples pour le type de diplôme, le domaine disciplinaire et la région
    types_diplome = st.multiselect("Sélectionnez les types de diplôme", df['Type de diplôme'].unique(), default=df['Type de diplôme'].unique(), key='type_diplome_spec')
    domaines_disciplinaires = st.multiselect("Sélectionnez les domaines disciplinaires", df['Domaine disciplinaire'].unique(), default=df['Domaine disciplinaire'].unique(), key='domaine_disciplinaires_spec')
    regions = st.multiselect("Sélectionnez les régions", df['Région'].unique(), default=df['Région'].unique(), key='regions_spec')
    
    # Filtrer le DataFrame en fonction des sélections
    df_filtered = df[df['Type de diplôme'].isin(types_diplome) & df['Domaine disciplinaire'].isin(domaines_disciplinaires) & df['Région'].isin(regions)]
    
    # Calculer le total des "nombre de poursuivants" + "nombre de sortants" pour chaque discipline
    df_filtered['Total'] = df_filtered['Nombre de poursuivants'] + df_filtered['Nombre de sortants']
    total_by_speciality = df_filtered.groupby('Libellé du diplôme')['Total'].sum().reset_index()
    
    # Sélectionner les 5 disciplines avec les valeurs les plus élevées
    top_5_specialities = total_by_speciality.nlargest(5, 'Total')
    
    # Créer un graphique en camembert interactif avec Plotly
    fig = px.pie(top_5_specialities, 
                 values='Total', 
                 names='Libellé du diplôme', 
                 title='Top 5 des disciplines par nombre de poursuivants et sortants',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    
    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)


def viz_map_ranking():
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)

    # Calculer le total des "nombre de poursuivants" + "nombre de sortants" pour chaque discipline
    df['Total'] = df['Nombre de poursuivants'] + df['Nombre de sortants']

    # Calculer le taux d'emploi moyen par région
    taux_emploi_region = df.groupby('Région')['Taux d\'emploi salarié en France'].mean().reset_index()
    
    # Trouver le libellé de discipline le plus significatif par région
    top_discipline_region = df.loc[df.groupby('Région')['Total'].idxmax()][['Région', 'Libellé du diplôme', 'Total']]

    # Fusionner les deux DataFrames
    map_data = pd.merge(taux_emploi_region, top_discipline_region, on='Région')
    map_data.columns = ['Région', 'Taux d\'emploi salarié en France', 'Libellé du diplôme', 'Total']
    
    # Définir une palette de couleurs vertes proches de RVBA = abc837ff
    colorscale = ['#d9e5a1', '#c3db73', '#abc837', '#91b32c', '#779d23']
    
    # Créer une carte choroplèthe avec Plotly
    fig = px.choropleth(map_data, 
                        locations='Région', 
                        locationmode='geojson-id',
                        geojson='https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson',
                        featureidkey="properties.nom",
                        color='Taux d\'emploi salarié en France',
                        color_continuous_scale=colorscale,
                        hover_name='Région',
                        hover_data={
                            'Taux d\'emploi salarié en France': True,
                            'Libellé du diplôme': True,
                            'Total': True,
                        },
                        title='Classement par région du Taux d\'emploi salarié et du libellé de la discipline le plus significatif')

    fig.update_geos(fitbounds="locations", visible=False)

    # Afficher la carte dans Streamlit
    st.plotly_chart(fig)


def viz_ranking_region():
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)

    # Calculer le taux d'emploi moyen par région
    taux_emploi_region = df.groupby('Région')['Taux d\'emploi salarié en France'].mean().reset_index()
    taux_emploi_region = taux_emploi_region.sort_values(by='Taux d\'emploi salarié en France', ascending=False)

    # Créer un graphique à barres horizontales avec Plotly
    fig = px.bar(taux_emploi_region, 
                 x='Taux d\'emploi salarié en France', 
                 y='Région', 
                 orientation='h', 
                 color='Taux d\'emploi salarié en France',
                 color_continuous_scale=px.colors.sequential.Tealgrn,
                 title='Classement des régions par taux d\'emploi salarié')

    fig.update_layout(xaxis_title='Taux d\'emploi salarié en France', yaxis_title='Région')

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)


# Appeler la fonction pour lancer l'application Streamlit
if __name__ == "__main__":
    viz_map_ranking()
    viz_ranking_region()


# Appeler la fonction pour lancer l'application Streamlit
if __name__ == "__main__":
    load_view()
    visualisation()
    viz_speciality_diploma_type()
