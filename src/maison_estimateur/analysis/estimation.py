# src/MaisonEstimateur/analysis/estimation.py
from __future__ import annotations
from typing import Optional
import pandas as pd
from .pricing import get_average_price_by_citypart


def estimate_price_rule(
    df: pd.DataFrame,
    citypart: int,
    area: float,
    rooms: int,
    has_garden: bool
) -> Optional[float]:
    """
    Estimation simple basée sur :
    - le prix moyen du quartier (cityPartRange)
    - la surface
    - le nombre de pièces
    - la présence d’un jardin

    Cette fonction ne fait aucun affichage (pas de Streamlit).
    Elle renvoie simplement un prix estimé.
    """

    mean_price = get_average_price_by_citypart(df, citypart)
    if mean_price is None:
        return None

    # Coefficients d'ajustement (règle simple)
    coeff_surface = 1 + (area - 60) / 400      # base 60m²
    coeff_rooms = 1 + (rooms - 3) * 0.05       # +5% par pièce au-dessus de 3
    coeff_garden = 1.10 if has_garden else 1.0 # +10% si jardin

    estimated_price = mean_price * coeff_surface * coeff_rooms * coeff_garden
    return float(round(estimated_price, 2))
