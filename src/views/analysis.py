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
    st.title(':mortar_board: Analyses et visualisations')

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
    viz_employ_rate_diploma_grouped()
    viz_rank_university()
    viz_rank_university_avge()

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
    print(df_filtered['Domaine disciplinaire'].nunique())
    print(df_filtered['Libellé du diplôme'].nunique())
    # Présenter le nombre de disciplines sur l'ensemble du territoire et pour chacune, le nombre de spécialités
    st.write(f"Le nombre de domaines de discipline enseignés en France pour les types de diplôme sélectionnés est de : {df_filtered['Domaine disciplinaire'].nunique()} correspondant à {df_filtered['Libellé du diplôme'].nunique()} spécialités")
   
    # Grouper par région et compter les libellés de diplôme
    libelle_count = df_filtered.groupby('Région')['Libellé du diplôme'].nunique()
    st.write(f"Nombre de spécialités dispensées avec un diplôme Bac +3 par région :")
    st.write(libelle_count)
    
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

def viz_rank_university():
        st.markdown("### Classement des Établissements en fonction du Nombre de Sortants et Poursuivants")

    # Chargement des données
        csv_file = "./data/esr_intersup_nettoye.csv"
        df = pd.read_csv(csv_file)

    # Calculer le total des "Nombre de sortants" + "Nombre de poursuivants" par établissement
        df_grouped = df.groupby('Établissement').agg({
            'Nombre de poursuivants': 'sum',
            'Nombre de sortants': 'sum'
        }).reset_index()

    # Ajouter une colonne pour le total
        df_grouped['Total Sortants + Poursuivants'] = df_grouped['Nombre de poursuivants'] + df_grouped['Nombre de sortants']

    # Remplacer les NaN par 0 ou une petite valeur positive pour éviter les erreurs
        df_grouped['Total Sortants + Poursuivants'].fillna(0, inplace=True)

    # Filtrer les établissements où le total est 0 pour éviter d'afficher des points de taille 0
        df_grouped = df_grouped[df_grouped['Total Sortants + Poursuivants'] > 0]
    
    # Trier par ordre décroissant du total
        df_grouped = df_grouped.sort_values(by='Total Sortants + Poursuivants', ascending=False)



    # Créer une visualisation avec Plotly
        fig = px.scatter(df_grouped, 
                         x='Total Sortants + Poursuivants', 
                         y='Établissement', 
                             size='Total Sortants + Poursuivants', 
                         color='Total Sortants + Poursuivants',
                         hover_name='Établissement',
                         title="Classement des Établissements en fonction du Nombre de Sortants et Poursuivants",
                         labels={
                             'Total Sortants + Poursuivants': "Total Sortants + Poursuivants",
                             'Etablissement actuel': "Établissement"
                         })

        # Mettre à jour la disposition pour améliorer l'affichage
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))
        fig.update_layout(height=600, width=800, margin=dict(l=0, r=0, t=30, b=0))
    
    # Afficher la figure dans Streamlit
        st.plotly_chart(fig)

def viz_employ_rate_diploma_grouped():
    st.markdown("### Taux d'emploi salarié en France moyen par libellé du diplôme")

    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)

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

def viz_rank_university_avge():
    st.markdown("### Classement des Établissements en fonction du Nombre de Sortants Moyens par Formation")

    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)

    # Calculer le nombre de formations uniques par établissement
    df_unique_formations = df.groupby('Établissement')["Libellé du diplôme"].nunique().reset_index()
    df_unique_formations.rename(columns={"Libellé du diplôme": 'Nombre de formations uniques'}, inplace=True)

    # Calculer le total des "Nombre de sortants" et "Nombre de poursuivants" par établissement
    df_grouped = df.groupby('Établissement').agg({
        'Nombre de poursuivants': 'sum',
        'Nombre de sortants': 'sum'
    }).reset_index()

    # Ajouter la colonne "Nombre de formations uniques"
    df_grouped = pd.merge(df_grouped, df_unique_formations, on='Établissement')

    # Calculer le nombre moyen de sortants par formation
    df_grouped['Nombre moyen de sortants par formation'] = df_grouped['Nombre de sortants'] / df_grouped['Nombre de formations uniques']

    # Ajouter une colonne pour le total des sortants et poursuivants
    df_grouped['Total Sortants + Poursuivants'] = df_grouped['Nombre de poursuivants'] + df_grouped['Nombre de sortants']

    # Remplacer les NaN par 0 ou une petite valeur positive pour éviter les erreurs
    df_grouped['Nombre moyen de sortants par formation'].fillna(0, inplace=True)

    # Filtrer les établissements où le total est 0 pour éviter d'afficher des points de taille 0
    df_grouped = df_grouped[df_grouped['Total Sortants + Poursuivants'] > 0]
    
    # Trier par ordre décroissant du nombre moyen de sortants par formation
    df_grouped = df_grouped.sort_values(by='Nombre moyen de sortants par formation', ascending=False)
    
    # Créer une visualisation avec Plotly en transposant les axes
    fig = px.scatter(df_grouped, 
                     x=df_grouped['Établissement'],  # Établissements sur l'axe des x
                     y='Total Sortants + Poursuivants',  # Total Sortants + Poursuivants sur l'axe des y
                     size='Nombre moyen de sortants par formation', 
                     color='Nombre moyen de sortants par formation',
                     hover_name='Établissement',
                     title="Classement des Établissements en fonction du Nombre Moyen de Sortants par Formation",
                     labels={
                         'Total Sortants + Poursuivants': "Total Sortants + Poursuivants",
                         'Établissement': "Établissement",
                         'Nombre moyen de sortants par formation': "Nombre Moyen de Sortants par Formation"
                     })

    # Mettre à jour la disposition pour améliorer l'affichage
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # Déplacer la légende en haut du graphique et ajuster la largeur du graphique
    fig.update_layout(
        height=600,
        width=1200,  # Augmenter la largeur du graphique
        margin=dict(l=0, r=0, t=30, b=100),
        xaxis={'tickangle': 45},
        legend=dict(
            orientation="h",  # Horizontal layout
            yanchor="bottom",  # Ancrer au bas du cadre de légende
            y=1.02,  # Positionner légèrement au-dessus du graphique
            xanchor="center",  # Centrer la légende
            x=0.5  # Centrer la légende horizontalement
        )
    )

    # Afficher la figure dans Streamlit
    st.plotly_chart(fig)




# Appeler la fonction pour lancer l'application Streamlit
if __name__ == "__main__":
    load_view()
    visualisation()
    viz_speciality_diploma_type()
    viz_map_ranking()
    viz_ranking_region()
    viz_employ_rate_diploma_grouped()
    viz_rank_university()
    viz_rank_university_avge()