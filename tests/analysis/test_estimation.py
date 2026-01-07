import numpy as np
import pandas as pd
import pytest

from maison_estimateur.analysis.estimation import (
    estimate_price,
    train_simple_regression,
)


def _df_small() -> pd.DataFrame:
    return pd.DataFrame({
        "squareMeters":  [60, 80, 120, 150],
        "cityPartRange": [3, 5, 7, 4],
        "numberOfRooms": [3, 4, 5, 6],
        "cityCode":      [100, 100, 200, 200],
        "price":         [200000, 260000, 400000, 550000],
    })


def _df_perfect_linear() -> pd.DataFrame:
    # price = 1000 * squareMeters (relation parfaite)
    return pd.DataFrame({
        "squareMeters":  [50, 100, 150, 200],
        "cityPartRange": [1, 1, 1, 1],
        "numberOfRooms": [2, 2, 2, 2],
        "cityCode":      [100, 100, 100, 100],
        "price":         [50000, 100000, 150000, 200000],
    })


class TestTrainSimpleRegression:

    def test_train_simple_regression_returns_expected_params_and_r2(self):
        df = _df_perfect_linear()
        model = train_simple_regression(df)

        # Structure minimale du modèle (statsmodels)
        assert hasattr(model, "params")
        assert "squareMeters" in model.params.index

        # Valeurs attendues (parfaitement linéaire)
        assert model.params["squareMeters"] == pytest.approx(1000.0, abs=1e-8)
        assert model.rsquared == pytest.approx(1.0, abs=1e-12)

    def test_train_simple_regression_with_missing_data_drops_na(self):
        df = _df_perfect_linear()
        df = pd.concat(
            [
                df,
                pd.DataFrame([{
                    "squareMeters": np.nan,
                    "cityPartRange": 1,
                    "numberOfRooms": 2,
                    "cityCode": 100,
                    "price": np.nan,
                }]),
            ],
            ignore_index=True,
        )

        model = train_simple_regression(df)

        # la ligne avec NaN doit être ignorée
        assert int(model.nobs) == 4

    def test_train_simple_regression_missing_columns_raises_keyerror(self):
        df = pd.DataFrame({
            "squareMeters": [1, 2, 3],
            "price": [100, 200, 300],
        })

        with pytest.raises(KeyError):
            train_simple_regression(df)

    def test_train_simple_regression_all_constant_features_still_fits(self):
        df = pd.DataFrame({
            "squareMeters": [100, 100, 100, 100],
            "cityPartRange": [5, 5, 5, 5],
            "numberOfRooms": [3, 3, 3, 3],
            "cityCode": [100, 100, 100, 100],
            "price": [200000, 210000, 220000, 230000],
        })

        model = train_simple_regression(df)

        assert hasattr(model, "params")
        # On vérifie que le modèle a produit des coefficients (pas juste "un objet")
        assert len(model.params) >= 1
        assert np.isfinite(model.rsquared)

    def test_train_simple_regression_empty_dataframe_raises(self):
        df = pd.DataFrame(columns=[
            "squareMeters",
            "cityPartRange",
            "numberOfRooms",
            "cityCode",
            "price",
        ])

        # On n'impose pas un type d'exception précis (dépend de l'implémentation),
        # mais on veut bien un échec explicite.
        with pytest.raises(Exception):
            train_simple_regression(df)


class TestEstimatePrice:

    def test_estimation_returns_finite_positive_value(self):
        df = _df_small()
        est = estimate_price(df, area=80, citypart=5, rooms=3, citycode=100)

        # Tests de valeur (au lieu de isinstance(float))
        assert est is not None
        assert np.isfinite(est)
        assert est > 0
        # borne haute "raisonnable" pour éviter des dérapages (à adapter si besoin)
        assert est < 100_000_000

    def test_estimation_increases_with_area(self):
        df = _df_small()
        small = estimate_price(df, 60, 5, 3, 100)
        big = estimate_price(df, 150, 5, 3, 100)

        assert small is not None and big is not None
        assert np.isfinite(small) and np.isfinite(big)
        assert big > small

    def test_estimation_changes_with_citycode(self):
        df = _df_small()
        cheap = estimate_price(df, 80, 5, 4, 100)
        expensive = estimate_price(df, 80, 5, 4, 200)

        assert cheap is not None and expensive is not None
        assert np.isfinite(cheap) and np.isfinite(expensive)

        # comportement attendu : changer le quartier doit impacter l'estimation
        assert expensive != cheap

    def test_missing_columns_returns_none(self):
        df = pd.DataFrame({
            "squareMeters": [60, 80],
            "price": [200000, 250000],
        })

        assert estimate_price(df, 80, 5, 3, 100) is None
