import streamlit as st


def load_view():    
    st.title(":anchor: Besoin de relancer l'application ou de vider le cache ?")
    col1, col2 = st.columns([1,3])
    with col1 :
        clear_cache = st.button ("Vider le cache")
        
    with col2 : 
        reload_app = st.button ("Relancer l'application")
    if clear_cache :
        st.cache_data.clear()
        print("cache bien effacé")
    if reload_app :
        st.rerun()

if __name__ == "__main__":
    load_view()
