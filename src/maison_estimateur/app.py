# src/maison_estimateur/app.py
import pathlib
import streamlit as st

from maison_estimateur.components.layout import topbar
from maison_estimateur.pages.home_page import render as render_home
from maison_estimateur.pages.estimation_page import render as render_estimation
from maison_estimateur.pages.statistics_page import render as render_stats
from maison_estimateur.pages.comparison_page import render as render_comparison
from maison_estimateur.pages.aide_page import render as render_aide

BASE_DIR = pathlib.Path(__file__).parent

st.set_page_config(
    page_title="MAISONESTIMATEUR",
    page_icon="🏠",
    layout="wide",
)


def inject_custom_css() -> None:
    """Charge le fichier style.css et l'injecte dans la page."""
    css_path = BASE_DIR / "style.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def run() -> None:
    """Point d’entrée de l’application : compose les pages en onglets."""
    inject_custom_css()

    topbar(title="MAISONESTIMATEUR", show_quit=False)

    tabs = st.tabs([
        "🏠 Accueil",
        "🧮 Estimation",
        "📊 Statistiques",
        "⚖️ Comparaison",
        "🆘 Aide & Documentation",
    ])

    with tabs[0]:
        render_home()
    with tabs[1]:
        render_estimation()
    with tabs[2]:
        render_stats()
    with tabs[3]:
        render_comparison()
    with tabs[4]:
        render_aide()


if __name__ == "__main__":
    run()



