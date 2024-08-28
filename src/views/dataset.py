import streamlit as st
from streamlit_folium import folium_static, st_folium  # Importer folium_static
from streamlit.components.v1 import html
import pandas as pd
import numpy as np

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import folium #https://python-visualization.github.io/folium/latest/getting_started.html ou https://folium.streamlit.app/
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import leafmap.foliumap as leafmap


def load_view():
    # Fonction pour charger les données
    csv_file = "./data/esr_intersup_nettoye.csv"
    try:
        df = pd.read_csv(csv_file)
        print("Fichier chargé avec succès.")
        df = df
    except FileNotFoundError:
        print(f"Le fichier {csv_file} est introuvable.")
        
    except Exception as e:
        print(f"Une erreur est survenue lors du chargement du fichier: {e}")
        

# affichage et appel pour la vue de la page dataset
    st.title(':label: Présentation du jeu de données nettoyé')
    st.markdown("""
    ### Tableau et données 
    """)
    st.write(f"**Taille du jeu de données (lignes, colonnes):** {df.shape}")
    st.dataframe(df)
    display_factor()
    #display_map_leafmap()
    display_spread_time()
    st.header("Visualisations facilitant la prise de connaissance des données\n")
    col1, col2 = st.columns(2)
    with col1:
        display_corr_var()
    with col2:
        data_heat()
    viz_rank_university()


def display_factor():
    st.markdown("""
    ### Répartition des effectifs diplômés sortant et entrant sur le marché du travail comme salarié
    """)
    # Chargement des données
    df = pd.read_csv("./data/esr_intersup_nettoye.csv")
    
    # Filtrer le DataFrame pour le premier graphique : "Tous domaines disciplinaires"
    df_tous_domaines = df[(df["Domaine disciplinaire"] == "Tous domaines disciplinaires") & (df["Région"] == "National")]

    # Filtrer le DataFrame pour le second graphique : Toutes les autres valeurs
    df_autres_domaines = df[(df["Domaine disciplinaire"] != "Tous domaines disciplinaires") & (df["Région"] != "National")]
    
    # Calculer les limites pour l'axe x du second graphique
    min_sortants = df_autres_domaines["Nombre de sortants"].min() - 10
    max_sortants = df_autres_domaines["Nombre de sortants"].max() + 10
    
    # Création de la figure pour contenir les deux graphiques
    fig, axes = plt.subplots(2, 1, figsize=(20, 10), sharex=False)  # Ne pas partager l'axe x
    
    # Définir la couleur pour le premier graphique (vert RVBA = #abc837ff)
    custom_palette = {"National": "#abc837ff"}
    
    # Premier graphique (avec couleur personnalisée)
    sns.boxplot(x="Nombre de sortants", y="Domaine disciplinaire", hue="Région", data=df_tous_domaines, ax=axes[0], palette=custom_palette)
    axes[0].set_title("Graphique pour 'Tous domaines disciplinaires'")
    axes[0].legend_.remove()  # On enlève la légende du premier graphique
    
    # Second graphique (avec ajustement de l'axe x)
    sns.boxplot(x="Nombre de sortants", y="Domaine disciplinaire", hue="Région", data=df_autres_domaines, ax=axes[1])
    axes[1].set_title("Graphique pour les autres domaines disciplinaires")
    axes[1].legend_.remove()  # On enlève la légende du second graphique
    
    # Ajustement des limites de l'axe x du second graphique uniquement
    axes[1].set_xlim(min_sortants, max_sortants)
    
    # Ajout d'une légende commune sous les graphiques (sur 2 lignes)
    handles, labels = axes[1].get_legend_handles_labels()
    num_labels = len(labels)
    fig.legend(handles, labels, loc='lower center', ncol=(num_labels // 2) + (num_labels % 2), bbox_to_anchor=(0.5, -0.15))
    
    # Ajustement de la disposition des graphiques
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Affichage du graphique dans Streamlit
    st.pyplot(fig)

    # Calculer le nombre de sortants globalement
    total_sortants = df["Nombre de sortants"].sum()
    total_sortants_national = df[df["Région"] == "National"]["Nombre de sortants"].sum()
    total_sortants_non_national = df[df["Région"] != "National"]["Nombre de sortants"].sum()
    
    col1, col2, col3 = st.columns([1, 0.05, 1])  # Ajout d'une colonne centrale fine pour la barre

    with col1:
        # Afficher le nombre de sortants globalement
        st.markdown(f"**Le nombre total d'étudiants sortant du cadre de l'enseignement est de :** **{total_sortants:,.0f}**".replace(',', ' '))
        st.markdown(f"**Ce nombre se répartit entre le nombre de sortants titulaires d'un diplôme national sans région spécifique :** **{total_sortants_national:,.0f}**".replace(',', ' '))
        st.markdown(f"**et le nombre de sortants distribués par région :** **{total_sortants_non_national:,.0f}**".replace(',', ' '))


    # Ajouter la barre verticale dans une colonne centrale
    with col2:
        st.markdown(
            """
             <div style='background-color: rgba(119, 38, 75, 1); width: 3px; height: 110px; margin: 0 auto;'></div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(f"**Le nombre total de spécialités étudiées est de :** **{df['Libellé du diplôme'].nunique():,}**")
        st.markdown(f"**Réparties entre :** **{df['Domaine disciplinaire'].nunique():,}** **domaines disciplinaires**")


def display_map_leafmap():
    st.header("Carte Interactive des Académies en France 4")
    # Chargement des données
    csv_file = "./data/esr_nettoye_avec_cities.csv"
    df = pd.read_csv(csv_file)

    st.markdown("### Carte Interactive des Académies en France\n Cette carte du monde présente la répartition géographique de l'ensemble des lignes du dataset. Il vous suffit de régler le zoom pour visualiser les DROM-COM.")
    
    # Filtrer les coordonnées valides
    valid_geo_df = df[
        df['latitude'].between(-90, 90) &
        df['longitude'].between(-180, 180)
    ]

    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return

    m = leafmap.Map(center=[46.603354, 1.888334], zoom=6)
    m.add_points_from_xy(valid_geo_df, x="longitude", y="latitude", popup=["Académie", "Nombre de sortants"])
    
    m.to_streamlit(width=600, height=400)


def display_corr_var():
    st.markdown("### Corrélation entre les variables\n ")
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)
    # Sélectionner uniquement les colonnes numériques pour le calcul de la corrélation
    numeric_var = df.select_dtypes(include=['float64', 'int64'])

    # Calculer la matrice de corrélation pour les colonnes numériques uniquement
    corr_matrix = numeric_var.corr()

    # Créer une heatmap pour visualiser la matrice de corrélation
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Corrélation des variables')

    # Afficher la figure dans Streamlit
    st.pyplot(plt)


def data_heat():
    st.markdown("### Rapport entre sortants et poursuivants à l'issue des formations étudiées\n ")  
    
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)

    # Extraction des colonnes d'intérêt
    x = df["Nombre de poursuivants"]
    y = df["Nombre de sortants"]

    # Génération de couleurs et tailles aléatoires pour chaque point
    colors = np.random.rand(len(df))
    sizes = 1000 * np.random.rand(len(df))

    # Création du graphique de dispersion
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='inferno')
    
    # Ajout de la ligne y = x
    plt.plot([x.min(), x.max()], [x.min(), x.max()], color='blue', linestyle='--', linewidth=2)

    # Affichage de l'échelle des couleurs
    plt.colorbar()
    
    # Ajout des labels et du titre
    plt.xlabel('Nombre de poursuivants')
    plt.ylabel('Nombre de sortants')
    plt.title('Carte de chaleur présentant le rapport entre étudiants poursuivant leur formation et sortants')

    # Affichage de la figure dans Streamlit
    st.pyplot(plt)


def display_spread_time():
    st.markdown("### Espace temporel des données : millésimes des diplômes et analyses des taux d'emploi à la sortie des formations \n ")
    
    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)

    # Création de la figure avec deux sous-graphiques côte à côte
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # 1 ligne, 2 colonnes

    # Groupement des données
    df_grouped_s = df.groupby("Année(s) d'obtention du diplôme prise(s) en compte")["Nombre de sortants"].sum()
    df_grouped_p = df.groupby("Année(s) d'obtention du diplôme prise(s) en compte")["Nombre de poursuivants"].sum()

# Plot 1: Nombre de sortants et Nombre de poursuivants par Année(s) d'obtention du diplôme
    ax1.plot(df_grouped_s.index, df_grouped_s, marker='o', label="Nombre de sortants", color="#abc837")
    ax1.plot(df_grouped_p.index, df_grouped_p, marker='o', label="Nombre de poursuivants", color="#77264b")
    # Ajouter les annotations des valeurs exactes pour chaque point
    for i in range(len(df_grouped_s)):
        ax1.annotate(f'{df_grouped_s.iloc[i]}', 
                     (df_grouped_s.index[i], df_grouped_s.iloc[i]), 
                     textcoords="offset points", 
                     xytext=(0, 5), ha='center', fontsize=8)
    
    for i in range(len(df_grouped_p)):
        ax1.annotate(f'{df_grouped_p.iloc[i]}', 
                     (df_grouped_p.index[i], df_grouped_p.iloc[i]), 
                     textcoords="offset points", 
                     xytext=(0, 5), ha='center', fontsize=8)

    ax1.set_xlabel("Année d'obtention du diplôme")
    ax1.set_ylabel("Nombre")
    ax1.set_title("Nombre d'étudiants sortants vs poursuivant leurs études par année d'obtention du diplôme")
    ax1.legend(fontsize='small', loc='upper right')  # Réduction de la taille de la légende et positionnement


# Plot 2: Nombre de sortants par Date d'insertion en emploi
    df_grouped = df.groupby("Mois après la diplomation")["Nombre de sortants"].sum().reset_index()
    ax2.bar(df_grouped["Mois après la diplomation"], df_grouped["Nombre de sortants"], color="#abc837")

    # Affichage des valeurs exactes sur l'axe des abscisses
    ax2.set_xticks(df_grouped["Mois après la diplomation"])  # Place les ticks exactement sur les mois disponibles
    ax2.set_xlabel("Mois après la diplomation")
    ax2.set_ylabel("Nombre de sortants")
    ax2.set_title("Nombre de sortants par date d'insertion en emploi")

    # Affichage des graphiques dans Streamlit
    st.pyplot(fig)


def viz_rank_university():
    st.markdown("### Classement des Établissements en fonction du Nombre de Sortants Moyens par Formation")

    # Chargement des données
    csv_file = "./data/esr_intersup_nettoye.csv"
    df = pd.read_csv(csv_file)

    # Calculer le nombre de formations uniques par établissement
    df_unique_formations = df.groupby('Établissement')['Domaine disciplinaire'].nunique().reset_index()
    df_unique_formations.rename(columns={'Domaine disciplinaire': 'Nombre de formations uniques'}, inplace=True)

    # Vérification pour s'assurer que la colonne est bien créée
    st.write("Nombre de formations uniques par établissement:", df_unique_formations.head())

    # Calculer le total des "Nombre de sortants" et "Nombre de poursuivants" par établissement
    df_grouped = df.groupby('Établissement').agg({
    'Nombre de poursuivants': 'sum',
    'Nombre de sortants': 'sum'
    }).reset_index()

    # Ajouter la colonne "Nombre de formations uniques"
    df_grouped = pd.merge(df_grouped, df_unique_formations, on='Établissement', how='left')

    # Vérification de la fusion des DataFrames avec un scroller
    st.markdown("### DataFrame après fusion")
    st.dataframe(df_grouped)

    # Calculer le nombre moyen de sortants par formation
    df_grouped['Nombre moyen de sortants par formation'] = df_grouped['Nombre de sortants'] / df_grouped['Nombre de formations uniques']

    # Vérification du calcul avec un scroller
    st.markdown("### Nombre moyen de sortants par formation")
    st.dataframe(df_grouped[['Établissement', 'Nombre moyen de sortants par formation']])

    # Ajouter une colonne pour le total des sortants et poursuivants
    df_grouped['Total Sortants + Poursuivants'] = df_grouped['Nombre de poursuivants'] + df_grouped['Nombre de sortants']

    # Remplacer les NaN par 0 ou une petite valeur positive pour éviter les erreurs
    df_grouped['Nombre moyen de sortants par formation'].fillna(0, inplace=True)

    # Filtrer les établissements où le total est 0 pour éviter d'afficher des points de taille 0
    df_grouped = df_grouped[df_grouped['Total Sortants + Poursuivants'] > 0]
    
    # Trier par ordre décroissant du nombre moyen de sortants par formation
    df_grouped = df_grouped.sort_values(by='Nombre moyen de sortants par formation', ascending=False)

    # Créer une visualisation avec Plotly pour le classement des établissements
    fig = px.scatter(df_grouped, 
                     x='Total Sortants + Poursuivants', 
                     y='Établissement', 
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
    fig.update_layout(height=600, width=800, margin=dict(l=0, r=0, t=30, b=0))
    
    # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

    # Nouvelle visualisation : Nombre de Sortants par Région
    st.markdown("### Nombre de Sortants par Région")
    df_region = df.groupby('Région')['Nombre de sortants'].sum().reset_index()

    fig_region = px.bar(df_region, 
                        x='Région', 
                        y='Nombre de sortants', 
                        color='Nombre de sortants',
                        title="Nombre de Sortants par Région",
                        labels={'Nombre de sortants': "Nombre de Sortants", 'Région': "Région"})

    fig_region.update_layout(height=600, width=800, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_region)

    # Nouvelle visualisation : Nombre de Sortants par Académie
    st.markdown("### Nombre de Sortants par Académie")
    df_academie = df.groupby('Académie')['Nombre de sortants'].sum().reset_index()

    fig_academie = px.bar(df_academie, 
                          x='Académie', 
                          y='Nombre de sortants', 
                          color='Nombre de sortants',
                          title="Nombre de Sortants par Académie",
                          labels={'Nombre de sortants': "Nombre de Sortants", 'Académie': "Académie"})

    fig_academie.update_layout(height=600, width=800, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_academie)


# Exécution des fonctions avec gestion des états
if __name__ == "__main__":
    load_view()