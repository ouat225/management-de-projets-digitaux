from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Optional, Union

# Cache robuste : Streamlit si dispo, sinon LRU cache
try:
    import streamlit as st

    def _cache(func):
        return st.cache_data(show_spinner=False)(func)
except Exception:  # streamlit pas dispo (tests/CI)
    from functools import lru_cache
    def _cache(func):
        return lru_cache(maxsize=8)(func)


def _project_root() -> Path:
    """
    Retourne la racine du projet (le dossier qui contient 'data/').
    Ce fichier est dans: .../src/MaisonEstimateur/data_processing/load_data.py
    Racine = parent de 'src'.
    """
    # __file__/.. = data_processing, /.. = MaisonEstimateur, /.. = src, /.. = racine projet
    return Path(__file__).resolve().parents[3]


def default_data_path() -> Path:
    """Chemin par défaut du CSV."""
    return _project_root() / "data" / "ParisHousing.csv"


@_cache
def _read_csv_cached(path_str: str) -> pd.DataFrame:
    """Lecture CSV avec cache (clé = chemin en string)."""
    return pd.read_csv(path_str, low_memory=False)


def load_data(path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Charge la base de données depuis un CSV.

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

    # Utilise le cache
    return _read_csv_cached(str(csv_path))
