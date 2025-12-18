from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
from statsmodels.stats.outliers_influence import variance_inflation_factor


def _select_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne uniquement les colonnes numériques du DataFrame."""
    return df.select_dtypes(include=[np.number]).copy()


def compute_price_correlation_figure(df: pd.DataFrame) -> tuple[pd.DataFrame, object]:
    """Calcule la matrice de corrélation (numérique) et retourne une figure heatmap centrée sur price.

    Retourne (corr_df, fig).
    """
    num_df = _select_numeric_columns(df)
    if "price" not in num_df.columns:
        return pd.DataFrame(), None

    corr = num_df.corr()

    # On garde uniquement les corrélations avec price pour une lecture plus simple
    corr_price = corr[["price"]].sort_values(by="price", ascending=False)

    fig = px.imshow(
        corr_price,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Corrélation entre price et les autres variables",
        labels={"color": "Corrélation"},
    )
    return corr_price, fig


def compute_vif_table(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule le VIF pour chaque variable numérique (hors price).

    Retourne un DataFrame avec colonnes: variable, vif.
    """
    num_df = _select_numeric_columns(df)
    if "price" in num_df.columns:
        num_df = num_df.drop(columns=["price"])
    if num_df.shape[1] < 2:
        return pd.DataFrame(columns=["variable", "vif"])

    # Drop lignes avec NaN pour le calcul du VIF
    x = num_df.dropna()
    if x.empty:
        return pd.DataFrame(columns=["variable", "vif"])

    vif_data: list[dict[str, float | str]] = []
    for i, col in enumerate(x.columns):
        try:
            vif_val = float(variance_inflation_factor(x.values, i))
        except Exception:
            vif_val = np.nan
        vif_data.append({"variable": col, "vif": vif_val})

    vif_df = pd.DataFrame(vif_data)
    vif_df = vif_df.sort_values("vif", ascending=False)
    return vif_df


def get_numeric_features_for_price(df: pd.DataFrame) -> list[str]:
    """Renvoie la liste des variables numériques pouvant être utilisées comme explicatives de price."""
    num_df = _select_numeric_columns(df)
    if "price" in num_df.columns:
        return [c for c in num_df.columns if c != "price"]
    return list(num_df.columns)
