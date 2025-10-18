# src/functions/data_viz.py
import pandas as pd
import plotly.express as px

def load_data(path: str) -> pd.DataFrame:
    """Charge la base de données depuis un CSV."""
    return pd.read_csv(path)

def plot_price_distribution(df: pd.DataFrame):
    """Affiche la distribution des prix."""
    fig = px.histogram(df, x="price", nbins=50, title="Distribution des prix")
    return fig

def plot_surface_vs_price(df: pd.DataFrame):
    """Affiche la relation entre surface et prix."""
    fig = px.scatter(df, x="squareMeters", y="price",
                     title="Surface vs Prix",
                     trendline="ols")
    return fig

def get_average_price_by_citycode(df, city_code: int) -> float:
    """
    Renvoie le prix moyen des logements pour un cityCode donné.
    """
    if city_code not in df["cityCode"].unique():
        return None
    mean_price = df[df["cityCode"] == city_code]["price"].mean()
    return round(mean_price, 2)

