import streamlit as st

def render():
    """Page d'accueil."""
    st.title("Bienvenue sur **MAISONESTIMATEUR**")
    st.write(
        """
        **MAISONESTIMATEUR** est un outil simple et rapide pour **estimer le prix de votre maison**
        à partir de données du marché et de statistiques descriptives.  
        Vous pouvez :
        - Explorer des **statistiques détaillées** sur vos variables,
        - (Bientôt) Obtenir une **estimation personnalisée** de votre bien 🏡.
        """
    )
    st.success("Utilisez les onglets pour naviguer : **🧮 Estimation** ou **📊 Statistiques**.")
