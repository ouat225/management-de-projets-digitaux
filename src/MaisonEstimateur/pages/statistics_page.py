# src/MaisonEstimateur/pages/statistics_page.py
import streamlit as st
import pandas as pd

from MaisonEstimateur.data_processing.load_data import load_data
from MaisonEstimateur.analysis.univariate_analysis import generate_univariate_analysis
from MaisonEstimateur.analysis.pricing import get_average_price_by_citycode

from MaisonEstimateur.components.widgets import (
    data_head,
    plot_figure,
    stats_metrics_numeric,
    stats_metrics_categorical,
    value_counts_table,
    citycode_selector_and_metric,
)

def _render_univariate_block(df: pd.DataFrame):
    """Bloc d'analyse univariée (sélection variable, stats, plot, effectifs)."""
    st.header("🔍 Analyse univariée")

    selected_var = st.selectbox(
        "Sélectionnez une variable à analyser",
        options=sorted(df.columns),
        index=0,
        key="stats_selected_var",
    )

    try:
        analysis = generate_univariate_analysis(df, selected_var)
    except Exception as e:
        st.error(f"Erreur pendant l'analyse univariée : {e}")
        return

    if not isinstance(analysis, dict):
        st.warning("Le format retourné par generate_univariate_analysis n'est pas un dict.")
        return

    st.subheader(f"Statistiques descriptives — {selected_var}")
    a_type = analysis.get("type")
    stats = analysis.get("stats", {})

    if a_type == "numeric":
        stats_metrics_numeric(stats, analysis)
    elif a_type == "categorical":
        stats_metrics_categorical(stats, analysis)
    else:
        st.info("Type de variable non reconnu (attendu: 'numeric' ou 'categorical').")

    plot_figure(analysis.get("fig"))

    if a_type == "categorical" and "value_counts" in analysis:
        st.subheader("Détail des effectifs")
        value_counts_table(analysis["value_counts"])

def render():
    """Page Statistiques (analyse univariée + info par cityCode)."""
    st.title("📊 Statistiques")

    # Chargement des données
    try:
        df = load_data()  # par défaut: data/ParisHousing.csv
    except Exception as e:
        st.error(f"Impossible de charger les données : {e}")
        return

    # Aperçu compact
    data_head(df, rows=5, expanded=False, title="Aperçu des données (head)")

    # Analyse
    _render_univariate_block(df)

    # cityCode + prix moyen
    citycode_selector_and_metric(df, get_average_price_by_citycode)
