import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

from maison_estimateur.analysis.linear_regression import (
    compute_linear_regression_full,
    FEATURES,
)


class TestComputeLinearRegressionFull:
    def _make_df(self, n: int = 50) -> pd.DataFrame:
        rng = np.random.default_rng(0)
        data = {f: rng.integers(0, 2, size=n) for f in FEATURES}
        df = pd.DataFrame(data)

        # Relation déterministe => métriques stables et testables
        df["price"] = 100000 + 1000 * df["squareMeters"] + 5000 * df["numberOfRooms"]
        return df

    def test_basic_output_structure_and_values(self):
        df = self._make_df()
        results, metrics, model = compute_linear_regression_full(df)

        # -----------------------
        # Structure
        # -----------------------
        assert isinstance(results, pd.DataFrame)
        assert {"Variable", "Coefficient", "p-value", "t-stat"}.issubset(results.columns)
        assert len(results) == len(FEATURES) + 1  # + intercept
        assert {"R2", "R2_adj"}.issubset(metrics.keys())
        assert int(model.nobs) == len(df)

        # -----------------------
        # Valeurs (au lieu de isinstance(float))
        # -----------------------
        r2 = float(metrics["R2"])
        r2_adj = float(metrics["R2_adj"])
        assert np.isfinite(r2)
        assert np.isfinite(r2_adj)
        assert 0.0 <= r2 <= 1.0
        assert 0.0 <= r2_adj <= 1.0

        # Bonus: pas de NaN dans les colonnes clés du tableau de résultats
        assert results["Coefficient"].notna().all()
        assert results["p-value"].notna().all()
        assert results["t-stat"].notna().all()

    def test_model_predicts_perfectly_on_deterministic_relation(self):
        """
        Test "fort" : sur une relation parfaitement linéaire, le modèle doit
        reproduire exactement y (à tolérance numérique).
        """
        df = self._make_df(n=80)
        _, metrics, model = compute_linear_regression_full(df)

        # IMPORTANT: le modèle OLS a été entraîné avec add_constant => il faut la même exog ici
        X = sm.add_constant(df[FEATURES], has_constant="add")
        y = df["price"]
        y_pred = model.predict(X)

        # Erreur de prédiction ~ 0
        assert np.max(np.abs(y_pred - y)) == pytest.approx(0.0, abs=1e-8)

        # Et donc R2 ~ 1
        assert float(metrics["R2"]) == pytest.approx(1.0, abs=1e-12)

    def test_dropna_rows_affects_nobs(self):
        df = self._make_df()
        df.loc[0, "price"] = np.nan
        df.loc[1, "squareMeters"] = np.nan
        df.loc[2, "hasPool"] = np.nan

        expected_nobs = df[["price"] + FEATURES].dropna().shape[0]
        results, metrics, model = compute_linear_regression_full(df)

        assert not results.empty
        assert int(model.nobs) == expected_nobs

        # R2 reste calculable et borné
        r2 = float(metrics["R2"])
        assert np.isfinite(r2)
        assert 0.0 <= r2 <= 1.0

    def test_missing_column_raises_keyerror(self):
        df = self._make_df().drop(columns=[FEATURES[0]])
        with pytest.raises(KeyError):
            compute_linear_regression_full(df)
