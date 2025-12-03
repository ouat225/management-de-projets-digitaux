import numpy as np
import pandas as pd
import pytest
from maison_estimateur.analysis.estimation import (
    estimate_price,
    train_simple_regression,
)


def _df_small():
    return pd.DataFrame({
        "squareMeters":  [60, 80, 120, 150],
        "cityPartRange": [3, 5, 7, 4],
        "numberOfRooms": [3, 4, 5, 6],
        "cityCode":      [100, 100, 200, 200],
        "price":         [200000, 260000, 400000, 550000],
    })


def _df_perfect_linear():
    return pd.DataFrame({
        "squareMeters":  [50, 100, 150, 200],
        "cityPartRange": [1, 1, 1, 1],
        "numberOfRooms": [2, 2, 2, 2],
        "cityCode":      [100, 100, 100, 100],
        "price":         [50000, 100000, 150000, 200000],
    })


class TestTrainSimpleRegression:

    def test_train_simple_regression_returns_model(self):
        df = _df_perfect_linear()
        model = train_simple_regression(df)

        assert hasattr(model, "params")
        # On vérifie surtout le coefficient de squareMeters et le R²
        assert abs(model.params["squareMeters"] - 1000) < 1e-6
        assert abs(model.rsquared - 1.0) < 1e-6

    def test_train_simple_regression_with_missing_data(self):
        df = _df_perfect_linear()
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [
                        {
                            "squareMeters": np.nan,
                            "cityPartRange": 1,
                            "numberOfRooms": 2,
                            "cityCode": 100,
                            "price": np.nan,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

        model = train_simple_regression(df)
        # la ligne avec NaN doit être ignorée par dropna()
        assert model.nobs == 4

    def test_train_simple_regression_missing_columns(self):
        df = pd.DataFrame(
            {
                "squareMeters": [1, 2, 3],
                "price": [100, 200, 300],
            }
        )

        with pytest.raises(KeyError):
            train_simple_regression(df)

    def test_train_simple_regression_all_constant_features(self):
        df = pd.DataFrame(
            {
                "squareMeters": [100, 100, 100, 100],
                "cityPartRange": [5, 5, 5, 5],
                "numberOfRooms": [3, 3, 3, 3],
                "cityCode": [100, 100, 100, 100],
                "price": [200000, 210000, 220000, 230000],
            }
        )

        model = train_simple_regression(df)

        assert hasattr(model, "params")
        # On vérifie juste qu'on a bien des paramètres calculés
        assert len(model.params) >= 1

    def test_train_simple_regression_empty_dataframe(self):
        df = pd.DataFrame(
            columns=[
                "squareMeters",
                "cityPartRange",
                "numberOfRooms",
                "cityCode",
                "price",
            ]
        )
        with pytest.raises(Exception):
            train_simple_regression(df)


class TestEstimatePrice:

    def test_estimation_returns_float(self):
        df = _df_small()
        est = estimate_price(df, area=80, citypart=5, rooms=3, citycode=100)
        assert isinstance(est, float)

    def test_estimation_changes_with_area(self):
        df = _df_small()
        small = estimate_price(df, 60, 5, 3, 100)
        big = estimate_price(df, 150, 5, 3, 100)
        assert big > small

    def test_estimation_changes_with_citycode(self):
        df = _df_small()
        cheap = estimate_price(df, 80, 5, 4, 100)
        expensive = estimate_price(df, 80, 5, 4, 200)
        assert expensive != cheap

    def test_missing_columns_returns_none(self):
        df = pd.DataFrame(
            {
                "squareMeters": [60, 80],
                "price": [200000, 250000],
            }
        )
        assert estimate_price(df, 80, 5, 3, 100) is None
