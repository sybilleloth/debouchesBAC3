import streamlit as st

def load_view():
    st.title('Merci !')
    col1, col2 = st.columns(2)
    with col1:
        st.image('https://images.pexels.com/photos/225250/pexels-photo-225250.jpeg', caption='Markus Spiske - Pexels', width=300)
        st.subheader (':two: Les vidéos')
        st.markdown ("- Les vidéos sont produites par la communauté ***Pexels***.")
        st.write("- Lien vers l'image de cette page : [Pexels Image](https://www.pexels.com/fr-fr/photo/ordinateur-ecran-programmation-logiciel-225250/)")
        st.write("- Lien vers la vidéo de la page d'accueil : [Pexels Image](https://www.pexels.com/fr-fr/video/jeune-fille-ecrite-ecole-nombres-8088339/)")
        st.write("- Lien vers la vidéo de la page de conclusion : [Pexels Image](https://www.pexels.com/fr-fr/video/femme-ecole-debout-porte-8284321/)")    
        
    with col2:
        # retrouver les liens des emojis ici : https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
        st.header('Un environnement humain et technique enthousiasmant :sparkles:')
        st.subheader (':one: Les pictos, couleurs et la police')
        st.markdown ("Les pictos et les codes de la charte graphique sont conçus maison à partir de l'outil ***Inkscape***.")
        st.image('./src/assets/images/palette_color.png', width=400)
        st.markdown ("La police est ***Exo***, libre de droits.")
        st.write("")
        
        st.subheader (':three: Les outils de code')
        st.markdown("""
        - La rédaction du code est réalisée en langage Python (v. 3.12.3), SQL et Html sur l'éditeur de code ***Visual Studio***.  
        - Le versioning est géré sur ***GitHub***.
        """)

        st.subheader (':four: Last but not least : les hommes')
        st.markdown ("Un grand merci aux équipes de ***Datarockstars*** pour leur patience, leur soutien et optimisme indéfectibles durant cette période d'apprentissage intense ! Ils se reconnaitront...")

if __name__ == "__main__":
    load_view()