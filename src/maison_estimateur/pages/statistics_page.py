from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from maison_estimateur.analysis.multivariate_analysis import (
    compute_price_correlation_figure,
    compute_vif_table,
    get_numeric_features_for_price,
)
from maison_estimateur.analysis.pricing import get_average_price_by_arrondissement
from maison_estimateur.analysis.univariate_analysis import generate_univariate_analysis
from maison_estimateur.components.widgets import (
    arrondissement_selector_and_metric,
    data_head,
    plot_figure,
    stats_metrics_categorical,
    stats_metrics_numeric,
    value_counts_table,
)
from maison_estimateur.data_processing.load_data import load_data


def _render_univariate_block(df: pd.DataFrame) -> None:
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
        st.info(
            "Impossible de calculer les corrélations "
            "(pas de variables numériques ou pas de colonne 'price')."
        )
    else:
        st.dataframe(corr_df, width="stretch")
        plot_figure(corr_fig)

    # VIF
    st.subheader("Analyse de la multicolinéarité (VIF)")
    vif_df = compute_vif_table(df)
    if vif_df.empty:
        st.info("Impossible de calculer le VIF (pas assez de variables numériques).")
    else:
        st.dataframe(vif_df, width="stretch")

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


def _render_regression_block(df: pd.DataFrame) -> None:
    """Bloc de régression linéaire multiple (coeffs, p-values, R²)."""
    st.header("📐 Régression linéaire multiple")

    from maison_estimateur.analysis.linear_regression import compute_linear_regression_full

    try:
        reg_table, reg_metrics, _ = compute_linear_regression_full(df)

        st.subheader("Résumé du modèle")
        st.write(f"**R² :** {reg_metrics['R2']:.4f}")
        st.write(f"**R² ajusté :** {reg_metrics['R2_adj']:.4f}")

        st.subheader("Coefficients du modèle")
        st.dataframe(reg_table, width="stretch")

    except Exception as e:
        st.error(f"Erreur dans la régression linéaire : {e}")


def render() -> None:
    """Page Statistiques avec 3 onglets : univariée, multivariée, régression."""
    st.markdown(
        """
        <div class="big-title">📊 Statistiques</div>
        <p class="subtitle">
            Explorez le jeu de données utilisé pour l’estimation des prix :
            distributions univariées, corrélations avec le prix et modèle de régression linéaire.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Chargement des données
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Impossible de charger les données : {e}")
        return

    # Résumé rapide du dataset
    n_rows, n_cols = df.shape
    nb_numeric = df.select_dtypes(include="number").shape[1]
    has_price = "price" in df.columns

    c1, c2, c3 = st.columns(3)
    c1.metric("Nombre de lignes", f"{n_rows:,}".replace(",", " "))
    c2.metric("Nombre de variables", n_cols)
    c3.metric("Variables numériques", nb_numeric)

    data_head(df, rows=5, expanded=False, title="Aperçu des données (head)")

    tab_univ, tab_multiv, tab_reg = st.tabs(
        ["🔍 Analyse univariée", "📈 Analyse multivariée", "📐 Régression linéaire"]
    )

    with tab_univ:
        _render_univariate_block(df)

        # ✅ Arrondissements 1–20 uniquement + moyenne prix associée
        arrondissement_selector_and_metric(
            df,
            get_average_price_by_arrondissement,
            select_label="Arrondissement (1–20)",
        )

    with tab_multiv:
        _render_multivariate_block(df)

    with tab_reg:
        if not has_price:
            st.warning("La colonne 'price' est nécessaire pour la régression linéaire.")
        else:
            _render_regression_block(df)

