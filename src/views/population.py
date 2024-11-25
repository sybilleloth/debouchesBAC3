

class population:
    """
    Représente une population (sortants + poursuivants) à calculer.

    Attributes:
        df (df): le jeu de données source pour détermination des populations selons les critères établis dans les définitions.
    """

    def __init__(self, df):
        """
        Initialise une instance de la classe population.

        Attributes:
            df (dataframe) : le jeu de donnée considéré.
        """
        self.df = df

    def group_annee(self):
        """
        Méthode pour créer la colonne 'Année_groupée' en fonction des 4 derniers caractères des années.
        """
        self.df['Année_groupée'] = self.df["Année(s) d'obtention du diplôme prise(s) en compte"].apply(lambda x: str(x)[-4:])
        return self.df

    def libelle(self):
        # Générer la colonne 'Année_groupée'
        self.group_annee()

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
        # Grouper par 'Année(s) d'obtention du diplôme prise(s) en compte'
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

        # Arrondir les résultats
        df_millesime['Nombre de sortants'] = df_millesime['Nombre de sortants'].round(0)
        df_millesime['Nombre de poursuivants'] = df_millesime['Nombre de poursuivants'].round(0)

        # Supprimer la colonne "Mois après la diplomation"
        df_millesime.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_millesime

    def academie(self):
        # Générer la colonne 'Année_groupée'
        self.group_annee()

        # Grouper par 'Académie' et 'Année_groupée'
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

        # Supprimer la colonne "Mois après la diplomation"
        df_academie.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_academie

    def region(self):
        # Générer la colonne 'Année_groupée'
        self.group_annee()

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

        # Arrondir les résultats
        df_region['Nombre de sortants'] = df_region['Nombre de sortants'].round(0)
        df_region['Nombre de poursuivants'] = df_region['Nombre de poursuivants'].round(0)

        # Supprimer la colonne "Mois après la diplomation"
        df_region.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_region

    def discipline(self):
        # Générer la colonne 'Année_groupée'
        self.group_annee()

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

        # Supprimer la colonne "Mois après la diplomation"
        df_discipline.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_discipline

    def domaine_discipline(self):
        # Générer la colonne 'Année_groupée'
        self.group_annee()

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

        # Supprimer la colonne "Mois après la diplomation"
        df_domaine_discipline.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_domaine_discipline

    def etablissement(self):
        # Générer la colonne 'Année_groupée'
        self.group_annee()

        # Grouper par 'Etablissement', 'Année_groupée', 'Libellé du diplôme'
        df_etablissement = self.df.groupby(
            ["Etablissement", "Année_groupée", "Libellé du diplôme"]
        ).agg({
            'Nombre de sortants': 'mean',
            'Nombre de poursuivants': 'mean',
            'Mois après la diplomation': 'nunique'
        }).reset_index()

        # Supprimer la colonne "Mois après la diplomation"
        df_etablissement.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_etablissement

    def region_discipline(self):
        # Générer la colonne 'Année_groupée'
        self.group_annee()

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

        # Supprimer la colonne "Mois après la diplomation"
        df_region_discipline.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_region_discipline

    def type_diplome(self):
        # Générer la colonne 'Année_groupée'
        self.group_annee()

        # Grouper par 'Type de diplome' et 'Année_groupée'
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

        # Supprimer la colonne "Mois après la diplomation"
        df_type_diplome.drop(columns=['Mois après la diplomation'], inplace=True)

        return df_type_diplome
