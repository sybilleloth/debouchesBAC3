import pandas as pd
import numpy as np

class population:
    def __init__(self, df):
        self.df = df

    def libelle(self):
        # Créer la nouvelle colonne 'Année_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Année_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Libellé du diplôme' et 'Année_groupée'
        df_libelle = self.df.groupby(
            ["Libellé du diplôme", "Année_groupée"]
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
    
    def millesime(self):
        # Grouper par 'Libellé du diplôme' et "Année(s) d'obtention du diplôme prise(s) en compte"
        df_millesime = self.df.groupby(
            ["Année(s) d'obtention du diplôme prise(s) en compte"]
        ).agg({
            'Nombre de sortants': 'sum',
            'Nombre de poursuivants': 'sum',
            'Mois après la diplomation': 'nunique'
        }).reset_index()

        # Diviser le nombre de sortants et poursuivants par le nombre de mois uniques
        df_millesime['Nombre de sortants'] = df_millesime['Nombre de sortants'] / df_millesime['Mois après la diplomation']
        df_millesime['Nombre de poursuivants'] = df_millesime['Nombre de poursuivants'] / df_millesime['Mois après la diplomation']
        df_millesime['Nombre de sortants'] = df_millesime['Nombre de sortants'].round(0)
        df_millesime['Nombre de poursuivants'] = df_millesime['Nombre de poursuivants'].round(0)
        # Supprimer la colonne "Mois après la diplomation" après l'opération
        df_millesime.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_millesime
    
    def academie(self):
        # Créer la nouvelle colonne 'Année_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Année_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Academie' et 'Année_groupée'
        df_academie = self.df.groupby(
            ["Académie", "Année_groupée"]
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
        # Créer la nouvelle colonne 'Année_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Année_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Région' et 'Année_groupée'
        df_region = self.df.groupby(
            ["Région", "Année_groupée"]
        ).agg({
            'Nombre de sortants': 'sum',
            'Nombre de poursuivants': 'sum',
            'Mois après la diplomation': 'nunique'
        }).reset_index()

        # Diviser le nombre de sortants et poursuivants par le nombre de mois uniques
        df_region['Nombre de sortants'] = df_region['Nombre de sortants'] / df_region['Mois après la diplomation']
        df_region['Nombre de poursuivants'] = df_region['Nombre de poursuivants'] / df_region['Mois après la diplomation']
        df_region['Nombre de sortants'] = df_region['Nombre de sortants'].round(0)
        df_region['Nombre de poursuivants'] = df_region['Nombre de poursuivants'].round(0)
        # Supprimer la colonne "Mois après la diplomation" après l'opération
        df_region.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_region
    
    def discipline(self):
        # Créer la nouvelle colonne 'Année_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Année_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Région' et 'Année_groupée'
        df_discipline = self.df.groupby(
            ["Région", "Année_groupée"]
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
        # Créer la nouvelle colonne 'Année_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Année_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Domaine disciplinaire' et 'Année_groupée'
        df_domaine_discipline = self.df.groupby(
            ["Domaine disciplinaire", "Année_groupée"]
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
        # Créer la nouvelle colonne 'Année_groupée' basée sur la dernière année (2020, 2021, etc.)
        self.df['Année_groupée'] = np.where(
            self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
            np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                    'Autre'
                )
            )
        )

        # Grouper par 'Etablissement', 'Année_groupée', 'Libellé du diplôme' et calculer la moyenne
        df_etablissement = self.df.groupby(
            ["Etablissement", "Année_groupée", "Libellé du diplôme"]
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
        self.df['Année_groupée'] = self.df["Année(s) d'obtention du diplôme prise(s) en compte"].apply(
        lambda x: str(x)[-4:])
        
        return self.df

    def region_discipline(self):
            # Créer la nouvelle colonne 'Année_groupée' basée sur la dernière année (2020, 2021, etc.)
            self.df['Année_groupée'] = np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                    np.where(
                        self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                        'Autre'
                    )
                )
            )

            # Grouper par 'Région', 'Domaine disciplinaire' et 'Année_groupée'
            df_region_discipline = self.df.groupby(
                ["Région", 'Domaine disciplinaire', "Année_groupée"]
            ).agg({
                'Nombre de sortants': 'sum',
                'Nombre de poursuivants': 'sum',
                'Mois après la diplomation': 'nunique'
            }).reset_index()

            # Diviser le nombre de sortants et poursuivants par le nombre de mois uniques
            df_region_discipline['Nombre de sortants'] = df_region_discipline['Nombre de sortants'] / df_region_discipline['Mois après la diplomation']
            df_region_discipline['Nombre de poursuivants'] = df_region_discipline['Nombre de poursuivants'] / df_region_discipline['Mois après la diplomation']

            # Supprimer la colonne "Mois après la diplomation" après l'opération
            df_region_discipline.drop(columns=['Mois après la diplomation'], inplace=True)

            return df_region_discipline
    
    def type_diplome(self):
            # Créer la nouvelle colonne 'Année_groupée' basée sur la dernière année (2020, 2021, etc.)
            self.df['Année_groupée'] = np.where(
                self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2020'), '2020',
                np.where(
                    self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2021'), '2021',
                    np.where(
                        self.df['Année(s) d\'obtention du diplôme prise(s) en compte'].astype(str).str.endswith('2022'), '2022',
                        'Autre'
                    )
                )
            )

            # Grouper par 'Région', 'Domaine disciplinaire' et 'Année_groupée'
            df_type_diplome = self.df.groupby(
                ["Type de diplôme", "Année_groupée"]
            ).agg({
                'Nombre de sortants': 'sum',
                'Nombre de poursuivants': 'sum',
                'Mois après la diplomation': 'nunique'
            }).reset_index()

            # Diviser le nombre de sortants et poursuivants par le nombre de mois uniques
            df_type_diplome['Nombre de sortants'] = df_type_diplome['Nombre de sortants'] / df_type_diplome['Mois après la diplomation']
            df_type_diplome['Nombre de poursuivants'] = df_type_diplome['Nombre de poursuivants'] / df_type_diplome['Mois après la diplomation']
            df_type_diplome['Nombre de sortants']=df_type_diplome['Nombre de sortants'].round(0)
            df_type_diplome['Nombre de poursuivants']=df_type_diplome['Nombre de poursuivants'].round(0)
            # Supprimer la colonne "Mois après la diplomation" après l'opération
            df_type_diplome.drop(columns=['Mois après la diplomation'], inplace=True)

            return df_type_diplome

# appel des fonctions depuis les pages de vue :
#Créer une instance de la classe population
#pop = population(df)
# Appeler la méthode libelle et afficher les résultats
#df_region = pop.region()
#st.write(df_region)
        