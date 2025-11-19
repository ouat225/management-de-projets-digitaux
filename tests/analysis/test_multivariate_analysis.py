import numpy as np
import pandas as pd
import pytest
from maison_estimateur.analysis.multivariate_analysis import (
    compute_price_correlation_figure,
    compute_vif_table,
    get_numeric_features_for_price,
)


class TestMultivariateAnalysis:

    def test_corr_price_valid(self):
        df = pd.DataFrame({
            "price": [100000, 150000, 200000, 250000],
            "squareMeters": [40, 50, 60, 70],
            "rooms": [2, 3, 3, 4],
        })
        corr_price, fig = compute_price_correlation_figure(df)

        assert isinstance(corr_price, pd.DataFrame)
        assert "price" in corr_price.index
        assert fig is not None

    def test_corr_price_missing_price(self):
        df = pd.DataFrame({
            "squareMeters": [40, 50, 60],
            "rooms": [2, 3, 4],
        })
        corr_price, fig = compute_price_correlation_figure(df)

        assert corr_price.empty
        assert fig is None

    def test_corr_price_non_numeric(self):
        df = pd.DataFrame({
            "price": ["a", "b", "c"],
            "squareMeters": [40, 50, 60],
        })
        corr_price, fig = compute_price_correlation_figure(df)

        assert corr_price.empty
        assert fig is None

    def test_vif_not_enough_numeric(self):
        df = pd.DataFrame({
            "price": [1, 2, 3],
            "city": ["a", "b", "c"],
        })
        vif_df = compute_vif_table(df)

        assert isinstance(vif_df, pd.DataFrame)
        assert vif_df.empty

    def test_vif_nan_rows(self):
        df = pd.DataFrame({
            "x1": [np.nan, np.nan],
            "x2": [np.nan, np.nan],
        })
        vif_df = compute_vif_table(df)

        assert vif_df.empty
    @pytest.mark.filterwarnings("ignore:divide by zero encountered in scalar divide:RuntimeWarning")
    def test_vif_valid(self):
        df = pd.DataFrame({
            "price": [100000, 150000, 200000, 250000],
            "x1": [1.0, 2.0, 3.0, 4.0],
            "x2": [2.0, 4.0, 6.0, 8.0],
        })
        vif_df = compute_vif_table(df)

        assert not vif_df.empty
        assert set(vif_df["variable"]) == {"x1", "x2"}
        assert vif_df["vif"].notna().all()

    def test_numeric_features_with_price(self):
        df = pd.DataFrame({
            "price": [100000, 150000, 200000],
            "squareMeters": [40, 50, 60],
            "rooms": [2, 3, 4],
            "city": ["a", "b", "c"],
        })
        feats = get_numeric_features_for_price(df)

        assert set(feats) == {"squareMeters", "rooms"}

    def test_numeric_features_without_price(self):
        df = pd.DataFrame({
            "squareMeters": [40, 50, 60],
            "rooms": [2, 3, 4],
            "city": ["a", "b", "c"],
        })
        feats = get_numeric_features_for_price(df)

        assert set(feats) == {"squareMeters", "rooms"}
