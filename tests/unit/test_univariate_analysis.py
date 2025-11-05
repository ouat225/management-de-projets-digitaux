# tests/unit/test_univariate_analysis.py
import pandas as pd
from MaisonEstimateur.analysis.univariate_analysis import generate_univariate_analysis

def test_univariate_numeric():
    df = pd.DataFrame({"num": [1, 2, 3, 4, 5]})
    res = generate_univariate_analysis(df, "num")

    assert isinstance(res, dict)
    assert res.get("type") in ("numeric", "categorical")  # selon nb de valeurs uniques
    assert "stats" in res
    assert "missing" in res
    assert "unique_values" in res
    # une figure doit être renvoyée (plotly)
    assert res.get("fig") is not None
    # si numeric, on s'attend à des clés stats standard
    if res.get("type") == "numeric":
        for key in ["mean", "std", "min", "max"]:
            assert key in res["stats"]


def test_univariate_categorical():
    df = pd.DataFrame({"cat": ["a", "a", "b", "b", "b", None]})
    res = generate_univariate_analysis(df, "cat")

    assert isinstance(res, dict)
    assert res.get("type") == "categorical"
    assert "stats" in res
    assert "value_counts" in res  # Series attendue
    assert res.get("fig") is not None

    stats = res["stats"]
    assert "top" in stats and "freq" in stats
    assert stats["freq"] >= 1
