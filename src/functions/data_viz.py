# src/functions/data_viz.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Tuple, Dict, Any, Union, List

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

def get_variable_type(df: pd.DataFrame, column: str) -> str:
    """Détermine le type de variable pour l'analyse univariée."""
    n_unique = df[column].nunique()
    if pd.api.types.is_numeric_dtype(df[column]):
        return 'numeric' if n_unique > 10 else 'categorical'
    return 'categorical'

def generate_univariate_analysis(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Génère une analyse univariée pour une colonne donnée.
    Retourne un dictionnaire contenant les statistiques et les figures.
    """
    if column not in df.columns:
        return {"error": f"La colonne {column} n'existe pas dans le dataset."}
    
    var_type = get_variable_type(df, column)
    analysis = {
        "column": column,
        "type": var_type,
        "missing": df[column].isna().sum(),
        "unique_values": df[column].nunique(),
        "stats": {}
    }
    
    # Statistiques descriptives
    if var_type == 'numeric':
        stats = df[column].describe(percentiles=[.25, .5, .75])
        analysis["stats"] = {
            "count": int(stats["count"]),
            "mean": round(stats["mean"], 2),
            "std": round(stats["std"], 2) if not np.isnan(stats["std"]) else 0,
            "min": round(stats["min"], 2) if not np.isnan(stats["min"]) else 0,
            "25%": round(stats["25%"], 2) if "25%" in stats else None,
            "median": round(stats["50%"], 2) if "50%" in stats else None,
            "75%": round(stats["75%"], 2) if "75%" in stats else None,
            "max": round(stats["max"], 2) if not np.isnan(stats["max"]) else 0
        }
        
        # Création des graphiques pour variables numériques
        fig = make_subplots(rows=1, cols=2, 
                          subplot_titles=('Distribution', 'Boîte à moustaches'))
        
        # Histogramme
        hist = px.histogram(df, x=column, nbins=50, 
                           title=f'Distribution de {column}')
        fig.add_trace(hist.data[0], row=1, col=1)
        
        # Boxplot
        box = px.box(df, y=column, points=False)
        fig.add_trace(box.data[0], row=1, col=2)
        
        fig.update_layout(showlegend=False, height=400)
        analysis["fig"] = fig
        
    else:  # Variables catégorielles
        value_counts = df[column].value_counts().reset_index()
        value_counts.columns = ['Valeur', 'Nombre']
        
        analysis["stats"] = {
            "top": df[column].mode().iloc[0] if not df[column].empty else None,
            "freq": int(df[column].value_counts().iloc[0]) if not df[column].empty else 0
        }
        
        # Création des graphiques pour variables catégorielles
        if len(value_counts) > 20:  # Si trop de catégories, on affiche les 20 premières
            value_counts = value_counts.head(20)
            
        fig = make_subplots(rows=1, cols=2, 
                          subplot_titles=('Top 20 des valeurs', 'Répartition'))
        
        # Bar plot
        bar = px.bar(value_counts, x='Valeur', y='Nombre',
                     title=f'Top 20 des valeurs de {column}')
        fig.add_trace(bar.data[0], row=1, col=1)
        
        # Pie chart (uniquement si pas trop de catégories)
        if len(value_counts) <= 10:
            pie = px.pie(value_counts, names='Valeur', values='Nombre',
                        title=f'Répartition de {column}')
            fig.add_trace(pie.data[0], row=1, col=2)
        
        fig.update_layout(showlegend=False, height=500)
        analysis["fig"] = fig
        analysis["value_counts"] = value_counts.to_dict('records')
    
    return analysis
