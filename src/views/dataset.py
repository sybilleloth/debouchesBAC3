import streamlit as st
#import folium
#from streamlit_folium import st_folium  #folium_static, Importer folium_static
import pandas as pd
import numpy as np

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
#import leafmap.foliumap as leafmap
#import pydeck as pdk

import sys #pour aller chercher les classes où il faut
sys.path.append('./src/views')
from population import population


def load_view():
        # chargement dataset nettoyé
    csv_file = "./data/esr_intersup_nettoye 2024_09.csv"
    try:
        df = pd.read_csv(csv_file)
        print("Fichier {csv_file} chargé avec succès pour la page dataset.")
        df = df
    except FileNotFoundError:
        print(f"Le fichier {csv_file} est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue lors du chargement du fichier pour page dataset: {e}")

        # chargement dataset nettoyé avec coordonnées gps pour affichage de carte
    csv_file = "./data/esr_nettoye_avec_cities 2024_09.csv"
    df_cities = pd.read_csv(csv_file)
    print("Fichier avec coordonnées gps chargé avec succès pour page dataset.")
    df_cities = df_cities
    
  
# affichage et appel pour la vue de la page dataset et appel des fonctions
    st.title(':label: Présentation du jeu de données nettoyé')
    
    st.markdown("""
    ### 1. Le tableau des données 
    """)
    st.write(f"**Taille du jeu de données (lignes, colonnes):** {df.shape}")
    with st.expander("visualiser le dataset (jeu de données)") :
        st.dataframe(df)
    
    st.markdown("""
    ### 2. Limites du dataset dans sa version actuelle 
    """)
    limites()

    st.markdown("""
                ### 3. Carte géographique de répartition des lignes du jeu de données par académie en France\n Cette carte du monde présente la répartition géographique des lignes du jeu de données. Il vous suffit de régler le zoom pour visualiser les DROM-COM.
                """)
    display_map_plotly(df_cities) #carte interactive montant la répartion du nombre de lignes du dataset par académie
    
    st.header("Visualisations facilitant la prise de connaissance des données\n")
    with st.expander("afficher les vues"):
        col1, col2 = st.columns(2)
        with col1:
            display_corr_var(df)
        with col2:
            data_heat(df)
    display_factor(df)
    
    st.markdown("""
    ### Répartition sortants et poursuivants par type de diplôme et par région 
    """)
    col1, col2 = st.columns(2)
    with col1 : 
        with st.expander( "voir le graphe par type de diplôme" ):
            sortantspoursuivantstypediplome(df)
    with col2 : 
        with st.expander( "voir le graphe par région" ):
            sortantspoursuivantsregion(df)
    display_majors(df)

    display_spread_time(df)
     
    viz_rank_university(df)
    



def sortantspoursuivantstypediplome(df):
    st.markdown("### Répartition des effectifs par type de diplôme")
    # Créer une instance de la classe population
    pop = population(df)
    #st.write(dir(pop)) pour checker les attributs et méthodes
    # Appeler la méthode etablissement
    df_type_diplome = pop.type_diplome()  # Notez les parenthèses car c'est une méthode
    #st.write(df_type_diplome) #pour check
    # Créer un tableau de répartition par 'Type de diplôme' avec les colonnes 'Nombre de sortants' et 'Nombre de poursuivants'
    df_grouped = df_type_diplome.groupby("Type de diplôme")[['Nombre de sortants', 'Nombre de poursuivants']].sum()

    # Créer une palette de couleurs personnalisée
    colors = ['#abc837', '#77264b', '#006b80']  # pomme, aubergine, canard

    # Créer un graphique à barres empilées (superposées)
    fig, ax = plt.subplots(figsize=(10, 6))
    df_grouped[['Nombre de sortants', 'Nombre de poursuivants']].plot(
        kind='bar', stacked=True, figsize=(5, 3), ax=ax, color=colors[:2])

    # Ajouter des titres et labels
    ax.set_title('Répartition des effectifs par Type de diplôme')
    ax.set_xlabel("Type de diplôme")
    ax.set_ylabel('Effectifs')
    ax.set_xticklabels(df_grouped.index, rotation=45, ha='right')

    # Afficher le graphique
    st.pyplot(fig)

def sortantspoursuivantsregion(df):
    st.markdown("### Répartition des effectifs par Région")

    # Créer une instance de la classe population
    pop = population(df)
    #st.write(dir(pop)) pour checker les attributs et méthodes
    # Appeler la méthode etablissement
    df_region = pop.region()  # parenthèses car c'est une méthode
    #st.write(df_region) pour check cohérence avec graphique
    # Créer un tableau de répartition par 'Région' avec les colonnes 'Nombre de sortants' et 'Nombre de poursuivants'
    df_grouped = df_region.groupby("Région")[['Nombre de sortants', 'Nombre de poursuivants']].sum()

    # Ajouter une colonne pour le total (Nombre de sortants + Nombre de poursuivants)
    df_grouped['Total'] = df_grouped['Nombre de sortants'] + df_grouped['Nombre de poursuivants']

    # Trier les données par ordre décroissant en fonction du total
    df_grouped = df_grouped.sort_values(by='Total', ascending=False)

    # Créer une palette de couleurs personnalisée
    colors = ['#abc837', '#77264b', '#006b80']  # pomme, aubergine, canard

    # Créer un graphique à barres
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Tracer les barres empilées pour chaque région
    df_grouped[['Nombre de sortants', 'Nombre de poursuivants']].plot(
        kind='bar', stacked=True, ax=ax, color=colors[:2])

    # Ajouter des titres et labels
    ax.set_title('Répartition des effectifs par Région (trié par ordre décroissant)')
    ax.set_xlabel("Région")
    ax.set_ylabel('Effectifs')
    ax.set_xticklabels(df_grouped.index, rotation=45, ha='right')

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

def display_factor(df):
    st.markdown("""
    ### Répartition des effectifs entrant sur le marché du travail en salariat après une formation Bac + 3
    """)
    # Créer une instance de la classe population
    pop = population(df)
    #st.write(dir(pop)) pour checker les attributs et méthodes
    # Appeler la méthode etablissement
    df_region_discipline = pop.region_discipline()  # Notez les parenthèses car c'est une méthode
    #st.write(df_region_discipline) #pour check
    with st.expander("détail") :
        # Calculer le nombre de sortants globalement
        total_sortants = df_region_discipline["Nombre de sortants"].sum()
        total_sortants_tous_domaines = df_region_discipline[df_region_discipline["Domaine disciplinaire"] == "Tous domaines disciplinaires"]["Nombre de sortants"].sum()
        total_sortants_autres = df_region_discipline[df_region_discipline["Domaine disciplinaire"] != "Tous domaines disciplinaires"]["Nombre de sortants"].sum()
    
        # Calculer le nombre de poursuivants globalement
        total_poursuivants =  df_region_discipline["Nombre de poursuivants"].sum()
        total_poursuivants_tous_domaines =  df_region_discipline[ df_region_discipline["Domaine disciplinaire"] == "Tous domaines disciplinaires"]["Nombre de poursuivants"].sum()
        total_poursuivants_autres =   df_region_discipline[ df_region_discipline["Domaine disciplinaire"] != "Tous domaines disciplinaires"]["Nombre de poursuivants"].sum()

        col1, col2, col3 = st.columns([1, 0.05, 1])  # Ajout d'une colonne centrale fine pour la barre

        with col1:
            # Afficher le nombre de sortants globalement
            st.markdown(f"**Le nombre total d'étudiants sortant du cadre de l'enseignement est de :** **{total_sortants:,.0f}**".replace(',', ' '))
            st.markdown(f" - dont sortants sans type de discipline spécifique : **{total_sortants_tous_domaines:,.0f}**".replace(',', ' '))
            st.markdown(f" - dont sortants avec discipline spécifique : **{total_sortants_autres:,.0f}**".replace(',', ' '))
            st.markdown(f"**Le nombre total d'étudiants poursuivant leur études est de :** **{total_poursuivants:,.0f}**".replace(',', ' '))
            st.markdown(f" - dont poursuivants sans type de discipline spécifique : **{total_poursuivants_tous_domaines:,.0f}**".replace(',', ' '))
            st.markdown(f" - dont poursuivants avec type de discipline spécifique  : **{total_poursuivants_autres:,.0f}**".replace(',', ' '))


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
 
    # Filtrer le DataFrame pour le premier graphique : "Tous domaines disciplinaires"
    df_tous_domaines =  df_region_discipline[( df_region_discipline["Domaine disciplinaire"] == "Tous domaines disciplinaires")]

    # Filtrer le DataFrame pour le second graphique : Toutes les autres valeurs
    df_autres_domaines = df_region_discipline[( df_region_discipline["Domaine disciplinaire"] != "Tous domaines disciplinaires")]
    
    # Calculer les limites pour l'axe x du second graphique
    min_sortants = df_autres_domaines["Nombre de sortants"].min() - 10
    max_sortants = df_autres_domaines["Nombre de sortants"].max() + 10
    
    # Création de la figure pour contenir les deux graphiques
    fig, axes = plt.subplots(2, 1, figsize=(20, 10), sharex=False)  # Ne pas partager l'axe x
    
    # Définir la couleur pour le premier graphique (vert RVBA = #abc837ff)
    #custom_palette = {"National": "#abc837ff"}
    
    # Premier graphique (avec couleur personnalisée)palette=custom_palette
    sns.barplot(x="Nombre de sortants", y="Domaine disciplinaire", hue="Région", data=df_tous_domaines, ax=axes[0] )
    axes[0].set_title("Graphique pour 'Tous domaines disciplinaires'")
    axes[0].legend_.remove()  # On enlève la légende du premier graphique
    
    # Second graphique (avec ajustement de l'axe x)
    sns.barplot(x="Nombre de sortants", y="Domaine disciplinaire", hue="Région", data=df_autres_domaines, ax=axes[1])
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

def display_majors(df) :

    st.markdown("### Présentation de la répartition des libellés de diplôme par domaine disciplinaire.")
    
    # Créer un selectbox pour choisir un Domaine disciplinaire
    domaines = df['Domaine disciplinaire'].unique()
    selected_domaine = st.selectbox("Sélectionnez un domaine disciplinaire", sorted(domaines))

    # Filtrer les données en fonction du Domaine disciplinaire sélectionné
    df_filtered = df[df['Domaine disciplinaire'] == selected_domaine]

    # Calculer le nombre de valeurs uniques pour le domaine disciplinaire sélectionné
    unique_secteurs = df_filtered['Secteur disciplinaire'].nunique()
    unique_libelles_diplome = df_filtered['Libellé du diplôme'].nunique()

    # Afficher les informations au-dessus du DataFrame
    st.markdown(f"**Nombre de secteurs disciplinaires uniques pour '{selected_domaine}' :** {unique_secteurs}")
    #st.markdown(f"**Nombre de libellés de secteur uniques pour '{selected_domaine}' :** {unique_libelles_secteur}")
    st.markdown(f"**Nombre de libellés de diplôme uniques pour '{selected_domaine}' :** {unique_libelles_diplome}")
    col1,col2 = st.columns([1,1])
    with col1 :
        df_filtered = df_filtered.iloc[:, :-11]
        # Afficher le DataFrame filtré
        st.dataframe(df_filtered, use_container_width=False, height=300)
    with col2 :
        # Ne pas afficher les 11 dernières colonnes
        df_filtered_bis = df[df['Domaine disciplinaire'] == selected_domaine]
        df_filtered_bis = df_filtered_bis.iloc[:,4 :8]
        # Afficher uniquement les valeurs uniques de 'Libellé du diplôme'
        df_filtered_bis_unique = df_filtered_bis.drop_duplicates(subset=['Libellé du diplôme'])
        # Afficher le DataFrame filtré
        st.dataframe(df_filtered_bis_unique, use_container_width=False, height=300)

def display_corr_var(df):
    st.markdown("### Corrélation entre les variables\n ")
    
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

def data_heat(df):
    st.markdown("### Rapport entre sortants et poursuivants à l'issue des formations étudiées\n ")  
    
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

def display_spread_time(df):
    st.markdown("### Espace temporel des données : millésimes des diplômes et analyses des taux d'emploi à la sortie des formations \n ")
    # Créer une instance de la classe population
    pop = population(df)
    #st.write(dir(pop)) #pour checker les attributs et méthodes
    # Appeler la méthode etablissement
    df_millesime = pop.millesime()  #  parenthèses car c'est une méthode
    #st.write(df_millesime) #pour check
    # Création de la figure avec deux sous-graphiques côte à côte
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # 1 ligne, 2 colonnes

    # Groupement des données par Année(s) d'obtention du diplôme prise(s) en compte
    df_grouped_s = df_millesime.groupby("Année(s) d'obtention du diplôme prise(s) en compte")["Nombre de sortants"].sum()
    df_grouped_p = df_millesime.groupby("Année(s) d'obtention du diplôme prise(s) en compte")["Nombre de poursuivants"].sum()

# Plot 1: Nombre de sortants et Nombre de poursuivants par Année(s) d'obtention du diplôme (avant regroupement des millésimes)
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

    ax1.set_xlabel("Année(s) d'obtention du diplôme prise(s) en compte")
    ax1.set_ylabel("Nombre")
    ax1.set_title("Nb sortants / poursuivants par année de diplome")
    ax1.legend(fontsize='small', loc='upper right')  # Réduction de la taille de la légende et positionnement


# Plot 2: Nombre de sortants sondés par période post dimplôme 
    df_grouped = df.groupby("Mois après la diplomation")["Nombre de sortants"].sum().reset_index()
    ax2.bar(df_grouped["Mois après la diplomation"], df_grouped["Nombre de sortants"], color="#abc837")

    # Affichage des valeurs exactes sur l'axe des abscisses
    ax2.set_xticks(df_grouped["Mois après la diplomation"])  # Place les ticks exactement sur les mois disponibles
    ax2.set_xlabel("Mois après la diplomation")
    ax2.set_ylabel("Nombre de sortants")
    ax2.set_title("Nombre de sortants par date d'insertion en emploi")
    # Ajouter les annotations des valeurs exactes au-dessus de chaque barre

    for i in range(len(df_grouped)):
        ax2.annotate(f'{df_grouped["Nombre de sortants"].iloc[i]}', 
                     (df_grouped["Mois après la diplomation"].iloc[i], df_grouped["Nombre de sortants"].iloc[i]), 
                     textcoords="offset points", 
                     xytext=(0, 5), ha='center', fontsize=8)
    # Affichage des graphiques dans Streamlit
    with st.expander("visualiser les répatyion dans le temps et par date d'insertion en emploi des sortants") :
        st.pyplot(fig)

def viz_rank_university(df):
    
    # Ajouter un graphique pour le nombre d'Etablissements par Nombre de formations
    st.markdown("### Répartition des établissements par nombre de formations")
    
   # Calculer le nombre de formations uniques par établissement
    df_unique_formations = df.groupby('Etablissement')['Domaine disciplinaire'].nunique().reset_index()
    df_unique_formations.rename(columns={'Domaine disciplinaire': 'Nombre de formations uniques'}, inplace=True)
    col1, col2 = st.columns(2)  
    with col1:
        # CSS pour centrer verticalement le contenu de col1
        st.markdown(
            """
            <style>
            .centered-content {
                display: flex;
                flex-direction: column;
                justify-content: center;
                height: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        with st.container():
            st.markdown('<div class="centered-content">', unsafe_allow_html=True)
        
            # Afficher un sélecteur pour choisir le nombre de formations au-dessus du DataFrame
            nombre_formations = st.selectbox(
                "**Sélectionnez le nombre de formations**",
                sorted(df_unique_formations['Nombre de formations uniques'].unique())
            )

            # Filtrer les établissements en fonction du nombre de formations sélectionné
            df_filtered = df_unique_formations[df_unique_formations['Nombre de formations uniques'] == nombre_formations]

            # Afficher le DataFrame filtré
            st.write(f"Etablissements avec exactement {nombre_formations} formation(s) unique(s):", df_filtered)

            # Calculer le total des "Nombre de sortants" et "Nombre de poursuivants" par établissement
            df_grouped = df.groupby('Etablissement').agg({
                'Nombre de poursuivants': 'sum',
                'Nombre de sortants': 'sum'
            }).reset_index()

            # Ajouter la colonne "Nombre de formations uniques"
            df_grouped = pd.merge(df_grouped, df_unique_formations, on='Etablissement', how='left')

            st.markdown('</div>', unsafe_allow_html=True)

    formations_count = df_grouped['Nombre de formations uniques'].value_counts().reset_index()
    formations_count.columns = ['Nombre de formations', 'Nombre d\'établissements']

    
    with col2:
        fig_formations = px.bar(
            formations_count, 
            x='Nombre de formations', 
            y="Nombre d'établissements", 
            title="Nombre d'établissements par nombre de formations",
            labels={
                'Nombre de formations': "Nombre de Formations", 
                "Nombre d'établissements": "Nombre d'Etablissements"
            }, 
            color_discrete_sequence=['#77264b']  # Couleur aubergine 
        )
        st.plotly_chart(fig_formations)


    col1, col2 = st.columns(2)  
    with col1:
        # Créer une instance de la classe population
        pop = population(df)
    
        # Appeler la méthode etablissement et afficher les résultats
        df_etablissement = pop.etablissement()
        #st.write(df_etablissement)  # Vérification du DataFrame

        # Calculer le nombre moyen de sortants par formation et par établissement
        df_grouped = df_etablissement.groupby('Etablissement').agg({
            'Nombre de sortants': 'mean',  # Moyenne du nombre de sortants par établissement,
            'Nombre de poursuivants': 'mean',  # Moyenne du nombre de poursuivants par établissement
        }).reset_index()

        # Vérification du calcul avec un scroller
        st.markdown("### Nombre moyen de sortants annuel par établissement et par libellé de formation")

        # Arrondir le 'Nombre de sortants' à l'entier le plus proche
        df_grouped["Nombre de sortants"] = df_grouped["Nombre de sortants"].round()

        # Trier le DataFrame par 'Nombre de sortants' en ordre croissant
        df_sorted = df_grouped[['Etablissement', "Nombre de sortants"]].sort_values(by="Nombre de sortants", ascending=True)

        with st.expander( "voir les données" ):
            # Afficher le DataFrame trié
            st.dataframe(df_sorted)


    
    with col2 :
        # Ajouter une colonne pour le total des sortants et poursuivants
        df_grouped['Total Sortants + Poursuivants'] = df_grouped['Nombre de poursuivants'] + df_grouped['Nombre de sortants']

        # Remplacer les NaN par 0 ou une petite valeur positive pour éviter les erreurs
        df_grouped['Nombre de sortants'].fillna(0, inplace=True)

        # Filtrer les établissements où le total est 0 pour éviter d'afficher des points de taille 0
        df_grouped = df_grouped[df_grouped['Total Sortants + Poursuivants'] > 0]
    
        # Trier par ordre décroissant du nombre moyen de sortants par formation
        df_grouped = df_grouped.sort_values(by='Nombre de sortants', ascending=False)
    
        st.markdown("### Classement des établissements en fonction du Nombre moyen de sortants par formation")
        # Créer une visualisation avec Plotly pour le classement des établissements
        fig = px.scatter(df_grouped, 
                         x='Etablissement', 
                         y='Total Sortants + Poursuivants', 
                         size='Nombre de sortants', 
                         color='Nombre de sortants',
                         hover_name='Etablissement',
                         title="Classement des établissements en fonction de la taille moyenne des promotions par formation",
                         labels={
                             'Total Sortants + Poursuivants': "Total Sortants + Poursuivants",
                             'Etablissement': "Etablissement",
                             'Nombre de sortants': "Nombre Moyen de Sortants par Formation"
                        },color_continuous_scale=["#e1f5c4", "#abc837", "#629e00"])# Palette de verts)  # Couleur verte spécifiée

        # Mettre à jour la disposition pour améliorer l'affichage
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))
        fig.update_layout(height=600, width=800, margin=dict(l=0, r=0, t=30, b=0))
    
        with st.expander( "visualiser" ):
            # Afficher la figure dans Streamlit
            st.plotly_chart(fig)

    # Créer deux colonnes pour afficher les graphiques côte à côte
    col1, col2 = st.columns(2)

# Première colonne: Nombre de Sortants par Région
    with col1:
        st.markdown("### Nombre cumulé de Sortants par Région")
        #Créer une instance de la classe population
        pop = population(df)
        # Appeler la méthode libelle et afficher les résultats
        df_region = pop.region()
        #st.write(df_region)
        
        df_region = df_region.groupby('Région')['Nombre de sortants'].sum().reset_index()
        df_region = df_region.sort_values(by='Nombre de sortants', ascending=False)  # Trier par ordre décroissant
        fig_region = px.bar(df_region, 
                            x='Région', 
                            y='Nombre de sortants', 
                            color='Nombre de sortants',
                            #title="Nombre de Sortants par Région",
                            labels={'Nombre de sortants': "Nombre de Sortants", 'Région': "Région"},color_continuous_scale=["#f0e1ea", "#ab5676", "#77264b"])

        fig_region.update_layout(height=600, margin=dict(l=0, r=0, t=30, b=0))
        with st.expander( "voir le graphe" ):
            st.plotly_chart(fig_region)

# Deuxième colonne: Nombre de Sortants par Académie
    with col2:
        st.markdown("### Nombre cumulé de Sortants par Académie")
        #Créer une instance de la classe population
        pop = population(df)
        # Appeler la méthode libelle et afficher les résultats
        df_academie = pop.academie()
        #st.write(df_academie)
        df_academie = df_academie.groupby('Académie')['Nombre de sortants'].sum().reset_index()
        df_academie = df_academie.sort_values(by='Nombre de sortants', ascending=False)  # Trier par ordre décroissant
        fig_academie = px.bar(df_academie, 
                              x='Académie', 
                              y='Nombre de sortants', 
                              color='Nombre de sortants',
                              #title="Nombre de Sortants par Académie",
                              labels={'Nombre de sortants': "Nombre de Sortants", 'Académie': "Académie"},
                              color_continuous_scale=["#f0e1ea", "#ab5676", "#77264b"]  # Couleur pourpre/violet
                            )

        fig_academie.update_layout(height=600, margin=dict(l=0, r=0, t=30, b=0))
        with st.expander( "voir le graphe" ):
            st.plotly_chart(fig_academie)

def display_map_plotly(df_cities): # Carte interactive des académies en France
    # Filtrer les coordonnées valides (latitude et longitude)
    valid_geo_df = df_cities[df_cities['latitude'].between(-90, 90) & df_cities['longitude'].between(-180, 180)]

    if valid_geo_df.empty:
        st.error("Aucune donnée avec des coordonnées valides n'a été trouvée.")
        return

    # Compter le nombre de lignes pour chaque Académie
    acad_count = valid_geo_df.groupby('Académie').size().reset_index(name='Nombre de lignes')

    # Fusionner les comptages avec les données géographiques
    valid_geo_df = valid_geo_df[['Académie', 'latitude', 'longitude']].drop_duplicates()
    valid_geo_df = pd.merge(valid_geo_df, acad_count, on='Académie')

    # Créer une carte interactive avec Plotly
    fig = px.scatter_mapbox(
        valid_geo_df,
        lat="latitude",
        lon="longitude",
        hover_name="Académie",
        hover_data={"Nombre de lignes": True, "latitude": False, "longitude": False},  # Ne pas afficher latitude/longitude
        size="Nombre de lignes",  # Taille des points proportionnelle au nombre de lignes
        size_max=40,
        color_discrete_sequence=["rgb(171,200,55)"],  # Couleur des points
        zoom=5,
        height=600,
    )

    # Centrer la carte sur Bruyères-Allichamps, France
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": 46.7219, "lon": 2.4371},  # Coordonnées de Bruyères-Allichamps
        mapbox_zoom=5  # Zoom sur la France
    )

    # Ajuster les marges pour un meilleur affichage
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

    # Afficher la carte dans Streamlit
    st.plotly_chart(fig)

def limites(): #texte sur limites et réserves dataset
    #2. Limites du dataset dans sa version actuelle
    # Création d'un bloc déroulable pour les limites
    with st.expander("détail..."):
        st.markdown("""
        **Limites**

        1. L'étude, compte tenu du nettoyage et de l'objectif d'analyse micro, ne porte pas sur l'ensemble de la population Bac+3 :
            - Les promotions dites "à cheval" entre deux années dans le dataset, sont rattachées à la promotion de l'année la plus récente (ex : 2019/2020 -> 2020, etc.).
            - Afin de maximiser le nombre de mentions/diplômes par établissement pour lesquels des indicateurs d'insertion sont disponibles, un cumul avec la promotion précédente est effectué dans le cas où l'effectif est inférieur à 20. Malgré cela, des cas subsistent pour lesquels l'effectif cumulé reste inférieur à 20 et aucun taux d'emploi salarié en France n'est affiché.
        
        2. La qualification de l'insertion et de la stabilité repose sur plusieurs critères :
            - Nature du contrat (CDI, CDD, etc.),
            - Secteur d'activité,
            - Profession et catégorie socio-professionnelle,
            - Rémunération,
            - Quotité de travail.

        3. Le dispositif est assez récent et évolue rapidement par l'extension du nombre d'établissements ou de diplômes considérés.
            - L'étudier dans la durée donnera plus de sens aux analyses.
            - Le dispositif Insersup prévoit d'inclure également l'enrichissement progressif en indicateurs qualifiant les emplois occupés par les sortants du supérieur.

        4. Pour les premières versions dont celle-ci, la population d'intérêt est réduite à celle des étudiants français de moins de 30 ans et ne reprenant pas d'études dans les 2 années suivant la diplomation.
        
        5. Les étudiants qui suivraient un double Bac + 3 ne sont pas isolés ni identifiés. On supposera que rapporté au nombre total, leur quote-part n'est pas significative.
        """)

# Exécution des fonctions avec gestion des états
if __name__ == "__main__":
    load_view()