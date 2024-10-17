import streamlit as st 

class Textdisplay:
    def __init__ (self, version) :
        self.version = version #travaille sur la base de la langue demandée en page home
    
    def text_homevf(self) : #appelle le texte en vf
        if self.version == "VF" :
            st.markdown("""
            ### Tour d'horizon des débouchés des formations licences professionnelles, générales, Master LMD et Master MEEF dispensées par les établissements d'enseignement supérieur

            #### Auteur et éditeur de l'enquête : Ministère français de l'Enseignement Supérieur et de la Recherche.
            
            Sur la base des données fournies par le Ministère de l'Enseignement Supérieur et de la Recherche, ces pages affichées à travers cette application Streamlit, 
            nous aident à comprendre comment le système éducatif français est réparti sur toutes les régions françaises et Drom-Com, comment ils délivrent tous un 
            diplôme ouvrant les portes du monde du travail.

            Les pages d'analyse soulignent à quel point la gamme de matières et de majeures est vaste.

            #### Hypothèses de l'enquête
            
            1. Évaluer l'exactitude des données fournies concernant la période de diplomation entre 2019 et 2021.
            2. Nettoyer et conserver des données précises qui peuvent être efficaces pour l'analyse.
            3. Acquérir une connaissance pertinente des données fournies conduisant à une conclusion valide confirmant la question initiale.
            4. Analyser et explorer les données.
            5. Visualiser et présenter la conclusion finale.

            En quelques mots : le système éducatif français mène-t-il au travail de manière égale dans toute la France, y a-t-il des universités plus favorables et quel est le taux d'étudiants poursuivant leurs études lorsqu'ils obtiennent un BAC + 3 ?
            """)

    def text_homeuk(self) : #appel le texte en VUK
        st.markdown("""
        Slight introduction : Overview of opportunities for young graduates in professional/global/LMD & MEEF Masters provided by French universities

        ### Author and editor of the present investigation : French " Ministère de l'Enseignement Supérieur et de la Recherche".

        On the dataset basis provided by Ministère de l'Enseignement Supérieur et de la Recherche, those pages displayed through this streamlit app, help us understand 
        how the French educational system is spread all over French regions ans West Indies and how they all deliver a diploma opening the doors of working world.

        The analysis pages underline how wide the range of matters and majors is.

    
        ## investigation hypothesis
        
        1. Evaluate the accuracy of the data provided regarding the period of graduation between 2019 and 2021
        2. Clean and keep accurate data that can be efficient to analyse
        3. Acquire a relevant knowledge of the provided data in order to answer the initial question
        4. Analyze and explore the data
        5. Visualize and present the final conclusion
     
        In  a few words : does the French educational system lead to work all over France equally, are there some favorable universities and how high is the rate of students resuming their studies when they graduate with a BAC + 3 ? 
        """)
    
    def text_captionvf(self) : #caption page home en VF
        if self.version == "VF" : 
            st.caption(" cette application a été élaborée en septembre 2024 avec le concours d'outils open source présentés en rubrique 'MERCI' ")

    def text_captionuk(self) : #caption page home en VUK
            st.caption(" this streamlit app has been developed and set up in Sept. 2024 thanks to open source tools introduced in page (MERCI)")
    