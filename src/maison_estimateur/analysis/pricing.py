from __future__ import annotations

from typing import Optional, Union
import pandas as pd


def get_average_price_by_citycode(
    df: pd.DataFrame, city_code: Union[str, int, float]
) -> Optional[float]:
    """
    Renvoie le prix moyen des logements pour un cityCode donné.
    - Accepte str/int/float et compare en string (robuste).
    - Retourne None si cityCode/price manquent ou si aucun match.
    """
    if "cityCode" not in df.columns or "price" not in df.columns:
        return None

    mask = df["cityCode"].astype(str) == str(city_code)
    if not mask.any():
        return None

    mean_price = df.loc[mask, "price"].mean()
    if pd.isna(mean_price):
        return None

    return float(round(mean_price, 2))

def get_average_price_by_citypart(
    df: pd.DataFrame, city_part: Union[str, int, float]
) -> Optional[float]:
    """
    Renvoie le prix moyen des logements pour un niveau de prestige (cityPartRange).
    - cityPartRange est une valeur entre 1 et 10.
    """
    if "cityPartRange" not in df.columns or "price" not in df.columns:
        return None

    mask = df["cityPartRange"].astype(str) == str(city_part)
    if not mask.any():
        return None

    mean_price = df.loc[mask, "price"].mean()
    if pd.isna(mean_price):
        return None

    return float(round(mean_price, 2))