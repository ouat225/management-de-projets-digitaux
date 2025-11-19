import pandas as pd
import pytest

from maison_estimateur.analysis.univariate_analysis import (
    generate_univariate_analysis,
    get_variable_type,
)


class TestGenerateUnivariateAnalysis:
    """Tests de l'analyse univariée sur différents types de colonnes."""

    def test_univariate_numeric_simple(self):
        """Cas de base : variable numérique propre."""
        df = pd.DataFrame({"num": [1, 2, 3, 4, 5]})
        res = generate_univariate_analysis(df, "num")

        assert isinstance(res, dict)
        assert res.get("type") in ("numeric", "categorical")
        assert "stats" in res
        assert "missing" in res
        assert "unique_values" in res
        assert res.get("fig") is not None

        # Si la variable est bien traitée comme numérique, stats classiques présentes
        if res.get("type") == "numeric":
            for key in ["mean", "std", "min", "max"]:
                assert key in res["stats"]

    def test_univariate_categorical_simple(self):
        """Cas de base : variable catégorielle avec une valeur manquante."""
        df = pd.DataFrame({"cat": ["a", "a", "b", "b", "b", None]})
        res = generate_univariate_analysis(df, "cat")

        assert isinstance(res, dict)
        assert res.get("type") == "categorical"
        assert "stats" in res
        assert "value_counts" in res
        assert res.get("fig") is not None

        stats = res["stats"]
        assert "top" in stats and "freq" in stats
        assert stats["freq"] >= 1
        # Vérifie que la série de fréquences est bien une Series pandas
        assert isinstance(res["value_counts"], pd.Series)

    def test_univariate_numeric_with_missing(self):
        """Variable numérique avec valeurs manquantes : missing doit être correct."""
        df = pd.DataFrame({"num": [1.0, 2.0, None, 4.0, None]})
        res = generate_univariate_analysis(df, "num")

        assert res["missing"] == 2
        assert res["unique_values"] == df["num"].nunique(dropna=False)
        assert res.get("fig") is not None

        # Si numérique, la clé 'count' doit être le nombre de valeurs non nulles
        if res["type"] == "numeric":
            assert res["stats"]["count"] == df["num"].notna().sum()

    def test_univariate_categorical_missing_count(self):
        """Contrôle précis du comptage des valeurs manquantes en catégoriel."""
        df = pd.DataFrame({"cat": ["x", "y", None, None]})
        res = generate_univariate_analysis(df, "cat")

        assert res["type"] == "categorical"
        assert res["missing"] == 2
        # unique_values doit compter la modalité NaN aussi (dropna=False)
        assert res["unique_values"] == df["cat"].nunique(dropna=False)

    def test_univariate_numeric_low_unique_treated_as_categorical(self):
        """
        Variable numérique avec peu de modalités :
        doit être considérée comme 'categorical' (règle get_variable_type).
        """
        df = pd.DataFrame({"num": [1, 1, 2, 2, 3, 3]})  # 3 valeurs uniques
        res = generate_univariate_analysis(df, "num")

        assert res["type"] == "categorical"
        assert "value_counts" in res
        assert isinstance(res["value_counts"], pd.Series)

    def test_univariate_numeric_stats_values(self):
        """Vérifie que les stats numériques sont cohérentes sur un exemple simple."""
        df = pd.DataFrame({"num": list(range(1, 21))})  # 20 valeurs uniques -> numeric
        res = generate_univariate_analysis(df, "num")

        assert res["type"] == "numeric"
        stats = res["stats"]

        # vérif basique des stats
        assert stats["count"] == 20
        assert stats["mean"] == 10.5      # moyenne de 1..20
        assert stats["min"] == 1.0
        assert stats["max"] == 20.0
        assert stats["median"] == 10.5    # médiane de 1..20


    def test_univariate_unknown_column_returns_error(self):
        """Si la colonne n'existe pas, la fonction doit renvoyer un dict avec 'error'."""
        df = pd.DataFrame({"num": [1, 2, 3]})
        res = generate_univariate_analysis(df, "inconnue")

        assert isinstance(res, dict)
        assert "error" in res
        assert "n'existe pas" in res["error"]


class TestGetVariableType:
    """Tests ciblés sur la fonction utilitaire get_variable_type."""

    def test_get_variable_type_numeric_many_unique(self):
        df = pd.DataFrame({"x": list(range(50))})  # 50 valeurs uniques
        var_type = get_variable_type(df, "x")
        assert var_type == "numeric"

    def test_get_variable_type_numeric_few_unique(self):
        df = pd.DataFrame({"x": [1, 1, 2, 2, 3, 3]})  # 3 valeurs uniques
        var_type = get_variable_type(df, "x")
        assert var_type == "categorical"

    def test_get_variable_type_categorical(self):
        df = pd.DataFrame({"x": ["a", "b", "c"]})
        var_type = get_variable_type(df, "x")
        assert var_type == "categorical"

    def test_get_variable_type_unknown_column_raises(self):
        df = pd.DataFrame({"x": [1, 2, 3]})
        with pytest.raises(KeyError):
            get_variable_type(df, "y")
