# src/MaisonEstimateur/app.py
import pathlib
import streamlit as st

from maison_estimateur.components.layout import topbar
from maison_estimateur.pages.home_page import render as render_home
from maison_estimateur.pages.estimation_page import render as render_estimation
from maison_estimateur.pages.statistics_page import render as render_stats

# Dossier courant (là où se trouve app.py)
BASE_DIR = pathlib.Path(__file__).parent

# Config globale
st.set_page_config(
    page_title="MAISONESTIMATEUR",
    page_icon="🏠",
    layout="wide",
)


def inject_custom_css() -> None:
    """Charge le fichier style.css et l'injecte dans la page."""
    css_path = BASE_DIR / "style.css"
    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def run_app():
    """Point d’entrée de l’application : compose les pages en onglets."""
    inject_custom_css()

    # Barre du haut (sans bouton Quitter)
    topbar(title="MAISONESTIMATEUR", show_quit=False)

    # Navigation en onglets
    tabs = st.tabs(["🏠 Accueil", "🧮 Estimation", "📊 Statistiques"])
    with tabs[0]:
        render_home()
    with tabs[1]:
        render_estimation()
    with tabs[2]:
        render_stats()


if __name__ == "__main__":
    run_app()


