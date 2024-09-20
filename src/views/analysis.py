import streamlit as st
import pandas as pd
import numpy as np
import re

# visualisation 
import plotly.express as px
import random as rnd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
#classes
import sys #pour aller chercher les classes où il faut
sys.path.append('./src/views')
from population import population

# Définition de la fonction de chargement des données et de visualisation principale
def load_view():
    
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye 2024_09.csv"
    df = pd.read_csv(csv_file)
    
    st.title(':mortar_board: Analyses et visualisations')

    st.header("Diversité des diplômes Bac + 3")
    viz_speciality_diploma_type(df)
    
    st.header("Popularité des domaines disciplinaires et des spécialités")
    col1, col2 = st.columns([1,3])
    with col1:
        viz_ranking_discipline(df)
    with col2:
        viz_ranking_speciality(df)
    st.header("Palmarès des régions en termes de taux d'emploi salarié pour les Bac +3")
    col3, col4 = st.columns(2)
    with col3:
        viz_map_ranking(df)
    with col4:
        viz_ranking_region(df)
    viz_employ_rate_diploma_grouped(df)
    viz_rank_university(df)
    viz_rank_university_avge(df)
    visualisation(df)

#ci-dessous, fonctions de visualisationL

def visualisation(df):
    st.header("Visualisation des données")
        
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
        sns.boxplot(x='Académie', y="% d'emplois stables parmi les salariés en France", data=df_filtered_academy)
        plt.title("Répartition du Taux d'insertion par académie")
        plt.xlabel('Académie')
        plt.ylabel("% d'emplois stables parmi les salariés en France")
        st.pyplot(plt)
        
    elif visualisation_type == "Bar Plot":
        # Grouper par académie et calculer les statistiques descriptives
        #stats = df.groupby('Académie')["% d'emplois stables parmi les salariés en France"].describe()
        st.write("Statistiques descriptives du taux d'emploi par académie:")
        #st.write(stats)

        # Calculer la moyenne et l'écart-type par académie
        mean_std = df.groupby('Académie')["% d'emplois stables parmi les salariés en France"].agg(['mean', 'std'])
        st.write("Moyenne et écart-type par académie:")
        #st.write(mean_std)

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
def viz_speciality_diploma_type(df):
    
    # Sélectionner les types de diplôme
    types_diplome = st.multiselect("Sélectionnez les types de diplôme", df['Type de diplôme'].unique(), default=df['Type de diplôme'].unique(), key='type_diplome')
    
    # Filtrer le DataFrame en fonction des types de diplôme sélectionnés
    df_filtered = df[df['Type de diplôme'].isin(types_diplome)]
    print(df_filtered['Domaine disciplinaire'].nunique())
    print(df_filtered['Libellé du diplôme'].nunique())
    # Présenter le nombre de disciplines sur l'ensemble du territoire et pour chacune, le nombre de spécialités
    st.write(f"Le nombre de domaines de discipline enseignés en France pour les types de diplôme sélectionnés est de : {df_filtered['Domaine disciplinaire'].nunique()} correspondant à {df_filtered['Libellé du diplôme'].nunique()} spécialités")
   
    # Grouper par région et compter les libellés de diplôme
    libelle_count = df_filtered.groupby('Région')['Libellé du diplôme'].nunique()
    st.write(f"Nombre de spécialités dispensées avec un diplôme Bac +3 par région :")    
    
    # Grouper par région et compter les valeurs uniques de "Domaine disciplinaire"
    domaine_count = df_filtered.groupby('Région')['Domaine disciplinaire'].nunique()
    
    # Créer un DataFrame combiné pour les annotations
    combined_df = libelle_count.reset_index().merge(domaine_count.reset_index(), on='Région')
    combined_df.columns = ['Région', 'Nombre de libellés de diplôme', 'Nombre de domaines disciplinaires']
    
    # Trier le DataFrame par 'Nombre de libellés de diplôme' en ordre descendant
    combined_df = combined_df.sort_values(by='Nombre de libellés de diplôme', ascending=False)
    
    # Calculer la moyenne nationale
    moyenne_nationale = combined_df['Nombre de libellés de diplôme'].mean()
    
    # Créer un graphique à barres interactif avec Plotly
    fig = px.bar(combined_df, 
                 x='Région', 
                 y='Nombre de libellés de diplôme', 
                 color_discrete_sequence=['#77264B'],
                 hover_data={'Nombre de domaines disciplinaires': True},
                 title='Nombre de libellés de diplôme par région')
    
    fig.update_layout(xaxis_title='Région', yaxis_title='Nombre de libellés de diplôme')

    # Ajouter une ligne représentant la moyenne nationale sur toute la largeur du graphe
    fig.add_shape(
        type='line',
        x0=-0.5,  # Positionner la ligne légèrement avant la première barre
        x1=len(combined_df) - 0.5,  # Positionner la ligne légèrement après la dernière barre
        y0=moyenne_nationale,
        y1=moyenne_nationale,
        line=dict(color='RoyalBlue', width=2, dash='dash'),
        xref='x',  # Référence par rapport à l'axe des x
        yref='y'   # Référence par rapport à l'axe des y
    )
    
    # Ajouter une annotation pour indiquer la moyenne nationale
    fig.add_annotation(
        x=0.5,  # Position relative à l'axe des x, de 0 à 1
        y=moyenne_nationale,
        text=f"Moyenne nationale: {moyenne_nationale:.2f}",
        showarrow=False,
        yshift=10,
        xref="paper",  # Position relative par rapport à l'ensemble du graphique
        yref="y"       # Position en termes de valeur y
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

def viz_ranking_discipline(df):
    # appel des populations discipline 
    pop = population(df)
    df_domaine_discipline = pop.domaine_discipline()
    #st.write(df_domaine_discipline)

    # Calculer le total des "nombre de poursuivants" + "nombre de sortants" pour chaque discipline
    df['Total'] = df_domaine_discipline['Nombre de poursuivants'] + df_domaine_discipline['Nombre de sortants']
    total_by_discipline = df.groupby('Domaine disciplinaire')['Total'].sum().reset_index()
    
    # Sélectionner les 5 disciplines avec les valeurs les plus élevées
    top_5_disciplines = total_by_discipline.nlargest(5, 'Total')
    
    # Créer un graphique en camembert interactif avec Plotly
    fig = px.pie(top_5_disciplines, 
                 values='Total', 
                 names='Domaine disciplinaire', 
                 title='Top 5 des disciplines par nombre de poursuivants et sortants <br> au niveau national',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    
    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

def viz_ranking_speciality(df):
    st.write("***Top 5 des libellés de dipôme par nombre de poursuivants et sortants***")
    # appel des populations discipline 
    pop = population(df)
    df_domaine_discipline = pop.domaine_discipline()
    #st.write(df_domaine_discipline)
    
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
                 #title='Top 5 des disciplines par nombre de poursuivants et sortants',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    
    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)


def viz_map_ranking(df):
    # Remplacer les NaN dans "Nombre de poursuivants" et "Nombre de sortants" par 0
    df['Nombre de poursuivants'].fillna(0, inplace=True)
    df['Nombre de sortants'].fillna(0, inplace=True)

    # Calculer le total des "nombre de poursuivants" + "nombre de sortants" pour chaque discipline
    df['Total'] = df['Nombre de poursuivants'] + df['Nombre de sortants']

    # Calculer le taux d'emploi moyen par région
    taux_emploi_region = df.groupby('Région')['Taux d\'emploi salarié en France'].mean().reset_index()
    
    # Arrondir les résultats à deux chiffres après la virgule
    taux_emploi_region['Taux d\'emploi salarié en France'] = taux_emploi_region['Taux d\'emploi salarié en France'].round(2)

    # Trouver le libellé de discipline le plus significatif par région
    top_discipline_region = df.loc[df.groupby('Région')['Total'].idxmax()][['Région', 'Libellé du diplôme', 'Total']]

    # Fusionner les deux DataFrames
    map_data = pd.merge(taux_emploi_region, top_discipline_region, on='Région')
    map_data.columns = ['Région', 'Taux d\'emploi salarié en France', 'Libellé du diplôme', 'Total']
    
    # Trier les données par taux d'emploi pour obtenir les 5 premières régions
    map_data_sorted = map_data.sort_values(by="Taux d'emploi salarié en France", ascending=False)
    top_5_regions = map_data_sorted.head(5)['Région'].tolist()

    # Ajouter une colonne pour les couleurs (1 pour vert, 0 pour gris)
    map_data['color'] = map_data['Région'].apply(lambda x: 1 if x in top_5_regions else 0)

    # Créer une carte choroplèthe avec Plotly Graph Objects pour un meilleur contrôle des couleurs
    fig = go.Figure(go.Choropleth(
        geojson='https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson',
        featureidkey="properties.nom",
        locations=map_data['Région'],
        z=map_data['color'],
        colorscale=[[0, '#e3e2db'], [1, '#006b80']],  # Gris pour les autres, vert pour les top 5
        showscale=False,  # Ne pas afficher la légende des couleurs
        hovertext=map_data['Région'],
        hoverinfo='text',
        customdata=map_data[['Taux d\'emploi salarié en France', 'Libellé du diplôme', 'Total']].values,
        hovertemplate='<b>%{hovertext}</b><br>' +
                      'Taux d\'emploi: %{customdata[0]}%<br>' +
                      'Discipline: %{customdata[1]}<br>' +
                      'Total: %{customdata[2]}<extra></extra>'
    ))

    fig.update_geos(fitbounds="locations", visible=False)

    # Ajouter un titre à la carte
    fig.update_layout(title_text='Classement par région du Taux d\'emploi salarié et du libellé de la discipline le plus significatif')

    # Afficher la carte dans Streamlit
    st.plotly_chart(fig)

def viz_ranking_region(df):
    
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


def viz_rank_university(df): 
    st.markdown("### Classement des Etablissements d'enseignement en fonction du nombre moyen de Sortants et Poursuivants par année")
    
    # Créer une instance de la classe population
    pop = population(df)

    # Appeler la méthode etablissement
    df_etablissement = pop.etablissement()  # Notez les parenthèses car c'est une méthode
    #st.write(df_etablissement) pour check
    # Utiliser la colonne 'Annee_groupée' pour l'analyse
    #df_etablissement['Année'] = df_etablissement["Annee_groupée"]

    # Calculer le total des "Nombre de sortants" + "Nombre de poursuivants" par établissement et par année
    df_grouped = df_etablissement.groupby(["Etablissement","Annee_groupée"]).agg({
        'Nombre de poursuivants': 'sum',
        'Nombre de sortants': 'sum'
    }).reset_index()

    # Ajouter une colonne pour le total annuel (sortants + poursuivants)
    df_grouped['Total Sortants + Poursuivants'] = df_grouped['Nombre de poursuivants'] + df_grouped['Nombre de sortants']

    # Calculer l'effectif moyen annuel pour chaque établissement
    df_mean = df_grouped.groupby('Etablissement').agg({
    'Total Sortants + Poursuivants': 'mean'
    }).round(0).reset_index()


    # Supprimer "Université de " ou "Université " des noms des établissements
    df_mean['Etablissement'] = df_mean['Etablissement'].str.replace(r'Université de |Université ', '', regex=True)

    # Trier par ordre décroissant du total moyen annuel
    df_mean = df_mean.sort_values(by='Total Sortants + Poursuivants', ascending=False).round(0)
    
    # Afficher les résultats dans Streamlit
    #st.write(df_mean)

    # Créer une visualisation avec Plotly en utilisant une échelle de couleurs
    fig = px.scatter(df_mean, 
                     y='Total Sortants + Poursuivants', 
                     x='Etablissement', 
                     size='Total Sortants + Poursuivants', 
                     color='Total Sortants + Poursuivants',
                     hover_name='Etablissement',
                     labels={
                         'Total Sortants + Poursuivants': "Effectif moyen annuel",
                         'Etablissement': "Etablissement"
                     },
                     color_continuous_scale=[
                         "rgb(0, 43, 51)",  # Tonalité plus foncée de RVB (0, 107, 128)
                         "rgb(0, 107, 128)",  # RVB (0, 107, 128)
                         "rgb(179, 229, 238)"  # Tonalité plus claire de RVB (0, 107, 128)
                     ])

    # Mettre à jour la disposition pour améliorer l'affichage
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))

    # Afficher la figure dans Streamlit
    st.plotly_chart(fig)



def viz_employ_rate_diploma_grouped(df):
    st.markdown("### Taux d'emploi salarié en France moyen par libellé du diplôme")

    # Calculer le taux d'emploi moyen par Libellé du diplôme
    taux_emploi_moyen = df.groupby('Libellé du diplôme')['Taux d\'emploi salarié en France'].mean().reset_index()

    # Créer des tranches de taux d'emploi
    bins = [0, 20, 40, 60, 80, 100]
    labels = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
    taux_emploi_moyen['Tranche'] = pd.cut(taux_emploi_moyen['Taux d\'emploi salarié en France'], bins=bins, labels=labels, right=False)
    
    # Compter le nombre de libellés de diplôme dans chaque tranche
    tranche_count = taux_emploi_moyen['Tranche'].value_counts().sort_index()

    # Créer un DataFrame pour le graphique
    tranche_df = pd.DataFrame({
        'Tranche': tranche_count.index,
        'Nombre de libellés de diplôme': tranche_count.values
    })

    # Création de la figure et des axes pour le graphique général
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Visualisation avec seaborn
    sns.barplot(x='Tranche', y='Nombre de libellés de diplôme', data=tranche_df, palette='BuGn', ax=ax)

    # Ajouter les étiquettes sur les barres
    for i in ax.containers:
        ax.bar_label(i, fmt='%d', label_type='edge')

    # Ajuster l'échelle de l'axe y pour s'adapter aux données
    ax.set_ylim(0, tranche_df['Nombre de libellés de diplôme'].max() * 1.1)

    # Ajouter les labels et le titre
    ax.set_xlabel('Taux d\'emploi salarié en France (%)')
    ax.set_ylabel('Nombre de libellés de diplôme')
    ax.set_title('Répartition des diplômes par tranche de taux d\'emploi salarié')

    # Appliquer les ajustements de layout pour gérer l'espace
    plt.tight_layout()
    
    col7, col8 = st.columns([1.2,0.8])
    with col7 :
        # Afficher la figure dans Streamlit
        st.pyplot(fig)
    with col8 :
    # Ajouter une selectbox pour sélectionner une tranche spécifique
        selected_tranche = st.selectbox("Sélectionnez une tranche pour voir les détails", labels)

    # Filtrer les diplômes selon la tranche sélectionnée
        filtered_df = taux_emploi_moyen[taux_emploi_moyen['Tranche'] == selected_tranche]

    # Afficher les détails des diplômes dans la tranche sélectionnée sous forme de DataFrame
        st.markdown(f"### Détail des diplômes dans la tranche {selected_tranche}")
        if not filtered_df.empty:
            filtered_df_round=filtered_df[['Libellé du diplôme', 'Taux d\'emploi salarié en France']].round(2)
            st.dataframe(filtered_df_round[['Libellé du diplôme', 'Taux d\'emploi salarié en France']])
        else:
            st.write("Aucun diplôme dans cette tranche.")

def viz_rank_university_avge(df):
    st.markdown("### Classement des établissements en fonction du nombre moyen de sortants par formation")

    # Calculer le nombre de formations uniques par établissement
    df_unique_formations = df.groupby('Etablissement')["Libellé du diplôme"].nunique().reset_index()
    df_unique_formations.rename(columns={"Libellé du diplôme": 'Nombre de formations uniques'}, inplace=True)

    # Calculer le total des "Nombre de sortants" et "Nombre de poursuivants" par établissement
    df_grouped = df.groupby('Etablissement').agg({
        'Nombre de poursuivants': 'sum',
        'Nombre de sortants': 'sum'
    }).reset_index()

    # Ajouter la colonne "Nombre de formations uniques"
    df_grouped = pd.merge(df_grouped, df_unique_formations, on='Etablissement')

    # Calculer le nombre moyen de sortants par formation
    df_grouped['Nombre moyen de sortants par formation'] = df_grouped['Nombre de sortants'] / df_grouped['Nombre de formations uniques']

    # Ajouter une colonne pour le total des sortants et poursuivants
    df_grouped['Total Sortants + Poursuivants'] = df_grouped['Nombre de poursuivants'] + df_grouped['Nombre de sortants']

    # Gérer les NaN : Remplacer les valeurs NaN par 0 pour "Nombre moyen de sortants par formation"
    df_grouped['Nombre moyen de sortants par formation'].fillna(0, inplace=True)

    # Filtrer les établissements où le total est supérieur à 0
    df_grouped = df_grouped[df_grouped['Total Sortants + Poursuivants'] > 0]
    
    # Trier par ordre décroissant du nombre moyen de sortants par formation
    df_grouped = df_grouped.sort_values(by='Nombre moyen de sortants par formation', ascending=False)

    # Supprimer "Université de " ou "Université " des noms des établissements
    df_grouped['Etablissement'] = df_grouped['Etablissement'].str.replace(r'Université de |Université ', '', regex=True)

    # Créer une visualisation avec Plotly en transposant les axes et utilisant les tonalités RVB
    fig = px.scatter(df_grouped, 
                     x='Etablissement',  # Utilisation de la colonne correcte pour les établissements
                     y='Total Sortants + Poursuivants',  # Total Sortants + Poursuivants sur l'axe des y
                     size='Nombre moyen de sortants par formation', 
                     color='Nombre moyen de sortants par formation',
                     hover_name='Etablissement',
                     title="Classement des Etablissements en fonction du nombre moyen de sortants par formation",
                     labels={
                         'Total Sortants + Poursuivants': "Total Sortants + Poursuivants",
                         'Etablissement': "Etablissement",
                         'Nombre moyen de sortants par formation': "Nombre moyen de sortants par formation"
                     },
                     color_continuous_scale=[
                         "rgb(86, 100, 32)",  # Tonalité plus foncée de RVB
                         "rgb(171, 200, 55)",  # RVB
                         "rgb(231, 243, 190)"  # Tonalité plus claire de RVB
                     ])

    # Mettre à jour la disposition pour améliorer l'affichage
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # Déplacer la légende en haut du graphique et ajuster la largeur du graphique
    fig.update_layout(
        height=600,
        width=1200,  # Augmenter la largeur du graphique
        margin=dict(l=0, r=0, t=30, b=100),
        xaxis={'tickangle': 45},
        legend=dict(
            orientation="h",  # Layout horizontal
            yanchor="bottom",  # Ancrer en bas
            y=1.02,  # Positionner légèrement au-dessus du graphique
            xanchor="center",  # Centrer horizontalement
            x=0.5  # Position horizontale
        )
    )
    # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

# Exécution de la fonction principale
if __name__ == "__main__":
    load_view()
 