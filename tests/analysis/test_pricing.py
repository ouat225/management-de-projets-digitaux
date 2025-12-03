import pandas as pd
from maison_estimateur.analysis.pricing import (
    get_average_price_by_citycode,
)


class TestGetAveragePriceByCitycode:

    def test_citycode_valid(self):
        df = pd.DataFrame({
            "cityCode": [101, 101, 202],
            "price": [100000, 200000, 300000],
        })
        assert get_average_price_by_citycode(df, 101) == 150000.0
        assert get_average_price_by_citycode(df, 202) == 300000.0

    def test_citycode_not_found(self):
        df = pd.DataFrame({
            "cityCode": [101, 202],
            "price": [120000, 180000],
        })
        assert get_average_price_by_citycode(df, 999) is None

    def test_citycode_missing_columns(self):
        df = pd.DataFrame({"cityCode": [1, 2]})
        assert get_average_price_by_citycode(df, 1) is None

    def test_citycode_nan_prices(self):
        df = pd.DataFrame({
            "cityCode": [101, 101],
            "price": [None, None],
        })
        assert get_average_price_by_citycode(df, 101) is None
