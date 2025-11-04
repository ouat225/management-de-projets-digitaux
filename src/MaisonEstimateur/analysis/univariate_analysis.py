from __future__ import annotations

from typing import Dict, Any
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots


def get_variable_type(df: pd.DataFrame, column: str) -> str:
    """
    Détermine le type de variable pour l'analyse univariée.
    - 'numeric' si dtype numérique et > 10 valeurs uniques
    - sinon 'categorical'
    """
    if column not in df.columns:
        raise KeyError(f"Colonne inconnue: {column}")

    n_unique = df[column].nunique(dropna=False)
    if pd.api.types.is_numeric_dtype(df[column]):
        return "numeric" if n_unique > 10 else "categorical"
    return "categorical"


def generate_univariate_analysis(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Génère une analyse univariée pour une colonne donnée.
    Retourne un dict avec:
      - column, type
      - missing, unique_values
      - stats (dict)
      - fig (plotly Figure)
      - value_counts (Series) si catégoriel
    """
    if column not in df.columns:
        return {"error": f"La colonne {column} n'existe pas dans le dataset."}

    var_type = get_variable_type(df, column)
    analysis: Dict[str, Any] = {
        "column": column,
        "type": var_type,
        "missing": int(df[column].isna().sum()),
        "unique_values": int(df[column].nunique(dropna=False)),
        "stats": {},
    }

    if var_type == "numeric":
        stats = df[column].describe(percentiles=[0.25, 0.5, 0.75])
        # Sécurise les NaN avant arrondi
        def _num(x, default=0.0):
            try:
                return float(x)
            except Exception:
                return default

        analysis["stats"] = {
            "count": int(_num(stats.get("count", 0), 0)),
            "mean": round(_num(stats.get("mean", np.nan), 0.0), 2),
            "std": round(_num(stats.get("std", np.nan), 0.0), 2),
            "min": round(_num(stats.get("min", np.nan), 0.0), 2),
            "25%": round(_num(stats.get("25%", np.nan), 0.0), 2) if "25%" in stats else None,
            "median": round(_num(stats.get("50%", np.nan), 0.0), 2) if "50%" in stats else None,
            "75%": round(_num(stats.get("75%", np.nan), 0.0), 2) if "75%" in stats else None,
            "max": round(_num(stats.get("max", np.nan), 0.0), 2),
        }

        # Figure: histogramme + boxplot côte à côte
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Distribution", "Boîte à moustaches"))
        hist = px.histogram(df, x=column, nbins=50, title=f"Distribution de {column}")
        box = px.box(df, y=column, points=False)

        fig.add_trace(hist.data[0], row=1, col=1)
        fig.add_trace(box.data[0], row=1, col=2)
        fig.update_layout(showlegend=False, height=400)
        analysis["fig"] = fig

    else:
        vc = df[column].value_counts(dropna=False)
        top_val = None
        freq = 0
        if not vc.empty:
            top_val = vc.index[0]
            freq = int(vc.iloc[0])

        analysis["stats"] = {
            "top": top_val,
            "freq": freq,
        }

        # Figure: bar chart des 20 premières modalités
        vc_top = vc.head(20).rename_axis("Valeur").reset_index(name="Nombre")
        fig = px.bar(vc_top, x="Valeur", y="Nombre", title=f"Répartition des valeurs de {column}")
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500,
            showlegend=False,
            xaxis_title="Valeurs",
            yaxis_title="Nombre d'occurrences",
        )
        analysis["fig"] = fig
        analysis["value_counts"] = vc  # Series, pratique pour l'affichage détaillé

    return analysis
