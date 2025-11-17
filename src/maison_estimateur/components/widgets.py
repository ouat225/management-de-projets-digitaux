from __future__ import annotations
import streamlit as st
import pandas as pd
from typing import Optional, Union

def data_head(df: pd.DataFrame, rows: int = 5, expanded: bool = False, title: str = "Aperçu des données (head)") -> None:
    """Affiche un aperçu des premières lignes dans un expander."""
    with st.expander(title, expanded=expanded):
        st.dataframe(df.head(rows), use_container_width=True)

def plot_figure(fig) -> None:
    """Affiche une figure Plotly en pleine largeur avec gestion d'erreurs douce."""
    if fig is None:
        st.info("Pas de figure à afficher.")
        return
    try:
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.warning("Le graphique fourni n'est pas compatible avec plotly_chart.")

def stats_metrics_numeric(stats: dict, analysis: dict) -> None:
    """Affiche les métriques pour variable numérique (3 colonnes)."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Moyenne", f"{stats.get('mean', float('nan')):,.2f}")
        st.metric("Médiane", f"{stats.get('median', float('nan')):,.2f}")
        st.metric("Écart-type", f"{stats.get('std', float('nan')):,.2f}")
    with col2:
        st.metric("Minimum", f"{stats.get('min', float('nan')):,.2f}")
        st.metric("25%", f"{stats.get('25%', float('nan')):,.2f}")
        st.metric("75%", f"{stats.get('75%', float('nan')):,.2f}")
    with col3:
        st.metric("Maximum", f"{stats.get('max', float('nan')):,.2f}")
        st.metric("Valeurs uniques", f"{analysis.get('unique_values', 0):,}")
        st.metric("Valeurs manquantes", f"{analysis.get('missing', 0):,}")

def stats_metrics_categorical(stats: dict, analysis: dict) -> None:
    """Affiche les métriques pour variable catégorielle (2 colonnes)."""
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Valeurs uniques", analysis.get('unique_values', 0))
        st.metric("Valeur la plus fréquente", stats.get('top', '—'))
    with col2:
        st.metric("Fréquence (valeur la plus fréquente)", stats.get('freq', '—'))
        st.metric("Valeurs manquantes", analysis.get('missing', 0))

def value_counts_table(vc: Union[pd.Series, pd.DataFrame, list, dict]) -> None:
    """Affiche le tableau des effectifs d'une variable catégorielle."""
    try:
        if isinstance(vc, pd.Series):
            vc_df = (
                vc.sort_values(ascending=False)
                  .rename_axis("Valeur")
                  .reset_index(name="Nombre")
            )
        elif isinstance(vc, pd.DataFrame):
            if set(vc.columns) >= {"Valeur", "Nombre"}:
                vc_df = vc.sort_values("Nombre", ascending=False)
            else:
                cols = list(vc.columns)
                if len(cols) >= 2:
                    vc_df = vc[[cols[0], cols[1]]].copy()
                    vc_df.columns = ["Valeur", "Nombre"]
                    vc_df = vc_df.sort_values("Nombre", ascending=False)
                else:
                    vc_df = vc.copy()
        else:
            # list/dict → DataFrame par défaut
            vc_df = pd.DataFrame(vc)
            if list(vc_df.columns)[:2] != ["Valeur", "Nombre"]:
                vc_df.columns = ["Valeur", "Nombre"][: len(vc_df.columns)]
        st.dataframe(vc_df, use_container_width=True)
    except Exception as e:
        st.warning(f"Impossible d'afficher les effectifs : {e}")

def citycode_selector_and_metric(
    df: pd.DataFrame,
    get_mean_fn,
    select_label: str = "Choisissez un quartier (cityCode)"
) -> None:
    """
    Sélecteur de cityCode (en str) + affiche la métrique du prix moyen.
    get_mean_fn: fonction (df, city_code) -> float | None
    """
    if "cityCode" not in df.columns:
        return

    counts = df["cityCode"].value_counts(dropna=False)
    if not counts.empty:
        top_city = str(counts.index[0])
        top_count = int(counts.iloc[0])
        st.info(f"🏙️ Le cityCode le plus fréquent : **{top_city}** avec **{top_count}** occurrences")

    codes = sorted(df["cityCode"].dropna().astype(str).unique().tolist())
    if not codes:
        return

    sel = st.selectbox(select_label, options=codes, index=0, key="citycode_selector")

    try:
        mean_price = get_mean_fn(df, sel)
    except Exception as e:
        mean_price = None
        st.warning(f"Erreur lors du calcul du prix moyen pour {sel} : {e}")

    if mean_price is None:
        st.warning("Impossible de calculer le prix moyen pour ce quartier.")
    else:
        st.metric("Prix moyen dans ce quartier", f"{mean_price:,.2f} €")
        st.success(f"💰 Prix moyen pour le quartier {sel} : **{mean_price:,.0f} €**.")
