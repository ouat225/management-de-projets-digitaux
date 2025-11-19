import numpy as np
import pandas as pd
import pytest

from maison_estimateur.analysis.linear_regression import (
    compute_linear_regression_full,
    FEATURES,
)


class TestComputeLinearRegressionFull:
    def _make_df(self, n=50):
        rng = np.random.default_rng(0)
        data = {f: rng.integers(0, 2, size=n) for f in FEATURES}
        df = pd.DataFrame(data)
        df["price"] = (
            100000
            + 1000 * df["squareMeters"]
            + 5000 * df["numberOfRooms"]
        )
        return df

    def test_basic_output_shapes(self):
        df = self._make_df()
        results, metrics, model = compute_linear_regression_full(df)

        assert isinstance(results, pd.DataFrame)
        assert set(["Variable", "Coefficient", "p-value", "t-stat"]).issubset(results.columns)
        assert len(results) == len(FEATURES) + 1
        assert "R2" in metrics and "R2_adj" in metrics
        assert isinstance(metrics["R2"], float)
        assert isinstance(metrics["R2_adj"], float)
        assert int(model.nobs) == len(df)

    def test_dropna_rows_affects_nobs(self):
        df = self._make_df()
        df.loc[0, "price"] = np.nan
        df.loc[1, "squareMeters"] = np.nan
        df.loc[2, "hasPool"] = np.nan

        expected_nobs = df[["price"] + FEATURES].dropna().shape[0]
        results, metrics, model = compute_linear_regression_full(df)

        assert not results.empty
        assert int(model.nobs) == expected_nobs

    def test_missing_column_raises_keyerror(self):
        df = self._make_df().drop(columns=[FEATURES[0]])
        with pytest.raises(KeyError):
            compute_linear_regression_full(df)
