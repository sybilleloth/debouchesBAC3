import pandas as pd
import numpy as np

class population:
    def __init__(self, df):
        self.df = df

    def libelle(self):
        # Créer la nouvelle colonne 'Annee_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Annee_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Libellé du diplôme' et 'Annee_groupée'
        df_libelle = self.df.groupby(
            ["Libellé du diplôme", "Annee_groupée"]
        ).agg({
            'Nombre de sortants': 'sum',
            'Nombre de poursuivants': 'sum',
            'Mois après la diplomation': 'nunique'
        }).reset_index()

        # Diviser le nombre de sortants et poursuivants par le nombre de mois uniques
        df_libelle['Nombre de sortants'] = df_libelle['Nombre de sortants'] / df_libelle['Mois après la diplomation']
        df_libelle['Nombre de poursuivants'] = df_libelle['Nombre de poursuivants'] / df_libelle['Mois après la diplomation']

        # Supprimer la colonne "Mois après la diplomation" après l'opération
        df_libelle.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_libelle
    
    def academie(self):
        # Créer la nouvelle colonne 'Annee_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Annee_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Academie' et 'Annee_groupée'
        df_academie = self.df.groupby(
            ["Académie", "Annee_groupée"]
        ).agg({
            'Nombre de sortants': 'sum',
            'Nombre de poursuivants': 'sum',
            'Mois après la diplomation': 'nunique'
        }).reset_index()

        # Diviser le nombre de sortants et poursuivants par le nombre de mois uniques
        df_academie['Nombre de sortants'] = df_academie['Nombre de sortants'] / df_academie['Mois après la diplomation']
        df_academie['Nombre de poursuivants'] = df_academie['Nombre de poursuivants'] / df_academie['Mois après la diplomation']

        # Supprimer la colonne "Mois après la diplomation" après l'opération
        df_academie.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_academie  
    
    def region(self):
        # Créer la nouvelle colonne 'Annee_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Annee_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Région' et 'Annee_groupée'
        df_region = self.df.groupby(
            ["Région", "Annee_groupée"]
        ).agg({
            'Nombre de sortants': 'sum',
            'Nombre de poursuivants': 'sum',
            'Mois après la diplomation': 'nunique'
        }).reset_index()

        # Diviser le nombre de sortants et poursuivants par le nombre de mois uniques
        df_region['Nombre de sortants'] = df_region['Nombre de sortants'] / df_region['Mois après la diplomation']
        df_region['Nombre de poursuivants'] = df_region['Nombre de poursuivants'] / df_region['Mois après la diplomation']

        # Supprimer la colonne "Mois après la diplomation" après l'opération
        df_region.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_region
    
    def discipline(self):
        # Créer la nouvelle colonne 'Annee_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Annee_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Région' et 'Annee_groupée'
        df_discipline = self.df.groupby(
            ["Région", "Annee_groupée"]
        ).agg({
            'Nombre de sortants': 'sum',
            'Nombre de poursuivants': 'sum',
            'Mois après la diplomation': 'nunique'
        }).reset_index()

        # Diviser le nombre de sortants et poursuivants par le nombre de mois uniques
        df_discipline['Nombre de sortants'] = df_discipline['Nombre de sortants'] / df_discipline['Mois après la diplomation']
        df_discipline['Nombre de poursuivants'] = df_discipline['Nombre de poursuivants'] / df_discipline['Mois après la diplomation']

        # Supprimer la colonne "Mois après la diplomation" après l'opération
        df_discipline.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_discipline
    
    def domaine_discipline(self):
        # Créer la nouvelle colonne 'Annee_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Annee_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Domaine disciplinaire' et 'Annee_groupée'
        df_domaine_discipline = self.df.groupby(
            ["Domaine disciplinaire", "Annee_groupée"]
        ).agg({
            'Nombre de sortants': 'sum',
            'Nombre de poursuivants': 'sum',
            'Mois après la diplomation': 'nunique'
        }).reset_index()

        # Diviser le nombre de sortants et poursuivants par le nombre de mois uniques
        df_domaine_discipline['Nombre de sortants'] = df_domaine_discipline['Nombre de sortants'] / df_domaine_discipline['Mois après la diplomation']
        df_domaine_discipline['Nombre de poursuivants'] = df_domaine_discipline['Nombre de poursuivants'] / df_domaine_discipline['Mois après la diplomation']

        # Supprimer la colonne "Mois après la diplomation" après l'opération
        df_domaine_discipline.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_domaine_discipline
    
    def etablissement(self):
        # Créer la nouvelle colonne 'Annee_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Annee_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Etablissement', 'Annee_groupée', 'Libellé du diplôme' et calculer la moyenne
        df_etablissement = self.df.groupby(
            ["Etablissement", "Annee_groupée", "Libellé du diplôme"]
        ).agg({
            'Nombre de sortants': 'mean',  # Calculer la moyenne des sortants
            'Nombre de poursuivants': 'mean',  # Calculer la moyenne des poursuivants
            'Mois après la diplomation': 'nunique'  # Nombre unique de mois après la diplomation
        }).reset_index()

        
        # Supprimer la colonne "Mois après la diplomation" après l'opération
        df_etablissement.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_etablissement

    def group_annee(self):
        # ne conserver que les 4 derniers caractères des années pour regrouper par année
        self.df['Annee_groupée'] = self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str[-4:]

        # Filtrer les années qui ne sont ni 2020, ni 2021, ni 2022
        #self.df['Annee_groupée'] = self.df['Annee_groupée'].where(self.df['Annee_groupée'].isin(['2020', '2021', '2022']), 'Autre')

        return self.df

    """ appel des fonctions depuis les pages de vue :
     Créer une instance de la classe population
    pop = population(df)
    # Appeler la méthode libelle et afficher les résultats
    df_region = pop.region()
    st.write(df_region)
    """ 