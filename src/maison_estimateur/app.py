# src/MaisonEstimateur/app.py
import streamlit as st

from maison_estimateur.components.layout import topbar
from maison_estimateur.pages.home_page import render as render_home
from maison_estimateur.pages.estimation_page import render as render_estimation
from maison_estimateur.pages.statistics_page import render as render_stats

# Config globale (une seule fois)
st.set_page_config(page_title="MAISONESTIMATEUR", page_icon="🏠", layout="wide")

def run_app():
    """Point d’entrée de l’application : compose les pages en onglets."""
    topbar(title="MAISONESTIMATEUR", show_quit=True)

    tabs = st.tabs(["🏠 Accueil", "🧮 Estimation", "📊 Statistiques"])
    with tabs[0]:
        render_home()
    with tabs[1]:
        render_estimation()
    with tabs[2]:
        render_stats()
