# tests/unit/test_estimation_logic.py
import pandas as pd
from MaisonEstimateur.analysis.estimation import estimate_price_rule

def _df_citypart():
    # cityPartRange = 3 -> prix moyens = (100k + 200k) / 2 = 150k
    # cityPartRange = 7 -> prix moyens = (300k + 500k) / 2 = 400k
    return pd.DataFrame({
        "cityPartRange": [3, 3, 7, 7],
        "price":          [100_000, 200_000, 300_000, 500_000]
    })


def test_estimate_price_rule_valid_baseline():
    """
    Cas nominal : citypart présent, area=60, rooms=3, pas de jardin.
    Les coefficients valent 1 → estimation = prix moyen du citypart.
    """
    df = _df_citypart()
    est = estimate_price_rule(df, citypart=3, area=60, rooms=3, has_garden=False)
    assert isinstance(est, float)
    assert round(est, 2) == 150_000.00  # moyenne du citypart 3

    # Avec jardin, on attend +10%
    est_garden = estimate_price_rule(df, citypart=3, area=60, rooms=3, has_garden=True)
    assert round(est_garden, 2) == round(150_000 * 1.10, 2)


def test_estimate_price_rule_returns_none_when_citypart_not_found():
    """Si le citypart n'existe pas dans le DF, la fonction doit renvoyer None."""
    df = _df_citypart()
    est = estimate_price_rule(df, citypart=9, area=60, rooms=3, has_garden=False)
    assert est is None


def test_estimate_price_rule_monotonic_effects():
    """
    Vérifie des tendances simples :
    - plus de surface → estimation plus élevée (à citypart constant)
    - plus de pièces → estimation plus élevée
    """
    df = _df_citypart()
    base = estimate_price_rule(df, citypart=7, area=60, rooms=3, has_garden=False)
    bigger_area = estimate_price_rule(df, citypart=7, area=100, rooms=3, has_garden=False)
    more_rooms = estimate_price_rule(df, citypart=7, area=60, rooms=5, has_garden=False)

    assert isinstance(base, float)
    assert bigger_area > base
    assert more_rooms > base
