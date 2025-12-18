from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

# ==========================================================
# Cache robuste : Streamlit si dispo, sinon LRU cache
# ==========================================================
try:
    import streamlit as st

    def _cache(func):
        return st.cache_data(show_spinner=False)(func)

except Exception:  # streamlit pas dispo (tests / CI)

    def _cache(func):
        return lru_cache(maxsize=8)(func)


# ==========================================================
# Paths
# ==========================================================
def _project_root() -> Path:
    """
    Retourne la racine du projet (le dossier qui contient 'data/').
    Ce fichier est dans: .../src/maison_estimateur/data_processing/load_data.py
    Racine = parent de 'src'.
    """
    return Path(__file__).resolve().parents[3]


def default_data_path() -> Path:
    """Chemin par défaut du CSV."""
    return _project_root() / "data" / "ParisHousing.csv"


# ==========================================================
# Chargement CSV avec cache
# ==========================================================
@_cache
def _read_csv_cached(path_str: str) -> pd.DataFrame:
    """Lecture CSV avec cache (clé = chemin en string)."""
    return pd.read_csv(path_str, low_memory=False)


# ==========================================================
# Transformation métier : arrondissement
# ==========================================================
def _add_arrondissement(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute une colonne 'arrondissement' (1..20) dérivée de 'cityCode'.

    Dataset fictif → règle déterministe :
        arrondissement = (cityCode % 20) + 1
    """
    if "cityCode" not in df.columns:
        return df

    df = df.copy()

    # Conversion robuste en numérique
    city = pd.to_numeric(df["cityCode"], errors="coerce")

    # Calcul arrondissement (1..20), NaN conservés
    df["arrondissement"] = ((city % 20) + 1).astype("Int64")

    return df


# ==========================================================
# API publique
# ==========================================================
def load_data(path: str | Path | None = None) -> pd.DataFrame:
    """
    Charge la base de données depuis un CSV et ajoute l'arrondissement.

    Parameters
    ----------
    path : str | Path | None
        Chemin du CSV. Si None, on utilise data/ParisHousing.csv à la racine du projet.

    Returns
    -------
    pd.DataFrame
    """
    csv_path = Path(path) if path is not None else default_data_path()

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Fichier introuvable: {csv_path}\n"
            f"Astuce: vérifie que le fichier est bien dans {default_data_path().parent} "
            f"ou passe un chemin explicite à load_data(path=...)."
        )

    df = _read_csv_cached(str(csv_path))
    df = _add_arrondissement(df)

    return df
