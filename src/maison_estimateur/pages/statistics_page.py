# src/MaisonEstimateur/pages/statistics_page.py
import streamlit as st
import pandas as pd
import plotly.express as px

from maison_estimateur.data_processing.load_data import load_data
from maison_estimateur.analysis.univariate_analysis import generate_univariate_analysis
from maison_estimateur.analysis.pricing import get_average_price_by_citycode
from maison_estimateur.analysis.multivariate_analysis import (
    compute_price_correlation_figure,
    compute_vif_table,
    get_numeric_features_for_price,
)

from maison_estimateur.components.widgets import (
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


def _render_multivariate_block(df: pd.DataFrame) -> None:
    """Bloc d'analyse multivariée (corrélations, VIF, scatter vs price)."""
    st.header("📈 Analyse multivariée")

    # Corrélations avec le prix
    corr_df, corr_fig = compute_price_correlation_figure(df)
    st.subheader("Corrélations avec price")
    if corr_fig is None or corr_df.empty:
        st.info("Impossible de calculer les corrélations (pas de variables numériques ou pas de colonne 'price').")
    else:
        st.dataframe(corr_df, use_container_width=True)
        plot_figure(corr_fig)

    # VIF
    st.subheader("Analyse de la multicolinéarité (VIF)")
    vif_df = compute_vif_table(df)
    if vif_df.empty:
        st.info("Impossible de calculer le VIF (pas assez de variables numériques).")
    else:
        st.dataframe(vif_df, use_container_width=True)

    # Scatter plots interactifs
    st.subheader("Nuages de points (price vs variable explicative)")
    features = get_numeric_features_for_price(df)
    if not features:
        st.info("Aucune variable numérique disponible pour construire un nuage de points.")
        return

    x_var = st.selectbox(
        "Choisissez la variable explicative (axe des x)",
        options=sorted(features),
        index=0,
        key="multivar_scatter_x",
    )

    if "price" not in df.columns:
        st.warning("La colonne 'price' est absente du dataset.")
        return

    scatter_df = df[[x_var, "price"]].dropna()
    if scatter_df.empty:
        st.info("Pas de données disponibles pour ce couple de variables.")
        return

    fig_scatter = px.scatter(
        scatter_df,
        x=x_var,
        y="price",
        trendline="ols",
        title=f"Relation entre {x_var} et price",
    )
    plot_figure(fig_scatter)


def render():
    """Page Statistiques avec 2 onglets : univariée et multivariée."""
    st.title("📊 Statistiques")

    # Chargement des données
    try:
        df = load_data()  # par défaut: data/ParisHousing.csv
    except Exception as e:
        st.error(f"Impossible de charger les données : {e}")
        return

    # Aperçu compact
    data_head(df, rows=5, expanded=False, title="Aperçu des données (head)")

    tab_univ, tab_multiv = st.tabs(["🔍 Analyse univariée", "📈 Analyse multivariée"])

    with tab_univ:
        _render_univariate_block(df)
        citycode_selector_and_metric(df, get_average_price_by_citycode)

    with tab_multiv:
        _render_multivariate_block(df)
