import pandas as pd
from maison_estimateur.analysis.estimation import estimate_price


def _df_small():
    """Petit DataFrame réaliste pour entraîner une régression simple."""
    return pd.DataFrame({
        "squareMeters":  [60, 80, 120, 150],
        "cityPartRange": [3, 5, 7, 4],
        "numberOfRooms": [3, 4, 5, 6],
        "cityCode":      [100, 100, 200, 200],
        "price":         [200000, 260000, 400000, 550000],
    })


class TestEstimatePrice:

    def test_estimation_returns_float(self):
        df = _df_small()
        est = estimate_price(df, area=80, citypart=5, rooms=3, citycode=100)
        assert isinstance(est, float)

    def test_estimation_changes_with_area(self):
        df = _df_small()
        small = estimate_price(df, 60, 5, 3, 100)
        big   = estimate_price(df, 150, 5, 3, 100)
        assert big > small

    def test_estimation_changes_with_citycode(self):
        df = _df_small()
        cheap = estimate_price(df, 80, 5, 4, 100)
        expensive = estimate_price(df, 80, 5, 4, 200)
        # On ne teste pas les valeurs exactes, juste une différence
        assert expensive != cheap

    def test_missing_columns_returns_none(self):
        df = pd.DataFrame({
            "squareMeters": [60, 80],
            # cityPartRange manquant
            "price": [200000, 250000],
        })
        assert estimate_price(df, 80, 5, 3, 100) is None
