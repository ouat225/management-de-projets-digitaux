import pandas as pd
from maison_estimateur.analysis.estimation import estimate_price_rule


def _df_citypart():
    return pd.DataFrame({
        "cityPartRange": [3, 3, 7, 7],
        "price":          [100_000, 200_000, 300_000, 500_000]
    })


class TestEstimatePriceRule:

    def test_baseline(self):
        df = _df_citypart()
        est = estimate_price_rule(df, citypart=3, area=60, rooms=3, has_garden=False)
        assert est == 150_000.00

        est_garden = estimate_price_rule(df, citypart=3, area=60, rooms=3, has_garden=True)
        assert est_garden == round(150_000 * 1.10, 2)

    def test_citypart_not_found(self):
        df = _df_citypart()
        est = estimate_price_rule(df, citypart=99, area=60, rooms=3, has_garden=False)
        assert est is None

    def test_monotonic_effects(self):
        df = _df_citypart()
        base = estimate_price_rule(df, citypart=7, area=60, rooms=3, has_garden=False)
        bigger_area = estimate_price_rule(df, citypart=7, area=100, rooms=3, has_garden=False)
        more_rooms = estimate_price_rule(df, citypart=7, area=60, rooms=5, has_garden=False)

        assert bigger_area > base
        assert more_rooms > base

    def test_surface_below_reference(self):
        df = _df_citypart()
        base = estimate_price_rule(df, citypart=3, area=60, rooms=3, has_garden=False)
        smaller = estimate_price_rule(df, citypart=3, area=40, rooms=3, has_garden=False)
        assert smaller < base

    def test_rooms_below_reference(self):
        df = _df_citypart()
        base = estimate_price_rule(df, citypart=3, area=60, rooms=3, has_garden=False)
        fewer = estimate_price_rule(df, citypart=3, area=60, rooms=1, has_garden=False)
        assert fewer < base
