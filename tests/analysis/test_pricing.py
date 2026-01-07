import pandas as pd
import pytest

from maison_estimateur.analysis.pricing import (
    get_average_price, 
    get_average_price_by_citycode,
    get_average_price_by_arrondissement,
    train_and_compare_models,
    train_best_model_on_full_data,
)

# ==========================================================
# Helpers datasets (réutilisables)
# ==========================================================

def _make_small_regression_df() -> pd.DataFrame:
    # Dataset min, assez grand pour train_test_split (test_size=0.2)
    return pd.DataFrame({
        "x1": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "x2": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        "price": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    })


def _make_perfect_linear_df(n: int = 60) -> pd.DataFrame:
    # Relation parfaitement linéaire : price = 2*x1 + 3*x2 + 5
    x1 = list(range(n))
    x2 = [2 * i for i in range(n)]
    price = [2 * a + 3 * b + 5 for a, b in zip(x1, x2)]
    return pd.DataFrame({"x1": x1, "x2": x2, "price": price})


def test_get_average_price_generic_citycode():
    df = pd.DataFrame({
        "cityCode": [101, 101, 202],
        "price": [100000, 200000, 300000],
    })
    assert get_average_price(df, 101, level="cityCode") == 150000.0


def test_get_average_price_generic_arrondissement_from_column():
    df = pd.DataFrame({
        "arrondissement": [1, 1, 2],
        "price": [100000, 200000, 300000],
    })
    assert get_average_price(df, 1, level="arrondissement") == 150000.0


# ==========================================================
# Tests: Moyennes par cityCode
# ==========================================================

def test_citycode_valid():
    df = pd.DataFrame({
        "cityCode": [101, 101, 202],
        "price": [100000, 200000, 300000],
    })
    assert get_average_price_by_citycode(df, 101) == 150000.0
    assert get_average_price_by_citycode(df, 202) == 300000.0


def test_citycode_not_found():
    df = pd.DataFrame({
        "cityCode": [101, 202],
        "price": [120000, 180000],
    })
    assert get_average_price_by_citycode(df, 999) is None


def test_citycode_missing_columns_returns_none():
    df = pd.DataFrame({"cityCode": [1, 2]})
    assert get_average_price_by_citycode(df, 1) is None


def test_citycode_nan_prices_returns_none():
    df = pd.DataFrame({
        "cityCode": [101, 101],
        "price": [None, None],
    })
    assert get_average_price_by_citycode(df, 101) is None


def test_citycode_empty_df_returns_none():
    df = pd.DataFrame(columns=["cityCode", "price"])
    assert get_average_price_by_citycode(df, 101) is None


def test_citycode_str_input_is_accepted():
    # Cohérent avec l'implémentation: comparaison via astype(str)
    df = pd.DataFrame({
        "cityCode": [101, 101],
        "price": [100000, 200000],
    })
    assert get_average_price_by_citycode(df, "101") == 150000.0


def test_citycode_float_input_is_accepted():
    # L'implémentation normalise 101.0 -> 101, donc ça doit matcher
    df = pd.DataFrame({
        "cityCode": [101, 101],
        "price": [100000, 200000],
    })
    assert get_average_price_by_citycode(df, 101.0) == 150000.0


# ==========================================================
# Tests: Moyennes par arrondissement
# ==========================================================

def test_arrondissement_valid_with_citycode_mapping():
    # arrondissement déduit via cityCode si la colonne 'arrondissement' n'existe pas
    df = pd.DataFrame({
        "cityCode": [1, 1, 2],
        "price": [100000, 200000, 300000],
    })
    assert get_average_price_by_arrondissement(df, 1) == 150000.0
    assert get_average_price_by_arrondissement(df, 2) == 300000.0


def test_arrondissement_valid_with_arrondissement_column():
    df = pd.DataFrame({
        "arrondissement": [1, 1, 2],
        "price": [100000, 200000, 300000],
    })
    assert get_average_price_by_arrondissement(df, 1) == 150000.0
    assert get_average_price_by_arrondissement(df, 2) == 300000.0


def test_arrondissement_invalid_out_of_range_returns_none():
    df = pd.DataFrame({
        "cityCode": [1, 2],
        "price": [100000, 200000],
    })
    assert get_average_price_by_arrondissement(df, 0) is None
    assert get_average_price_by_arrondissement(df, 21) is None


def test_arrondissement_parseable_from_str_and_float():
    df = pd.DataFrame({
        "cityCode": [1, 1],
        "price": [100000, 200000],
    })
    assert get_average_price_by_arrondissement(df, "1") == 150000.0
    assert get_average_price_by_arrondissement(df, 1.0) == 150000.0


def test_arrondissement_missing_price_column_returns_none():
    df = pd.DataFrame({"cityCode": [1, 1]})
    assert get_average_price_by_arrondissement(df, 1) is None


def test_arrondissement_no_match_returns_none():
    df = pd.DataFrame({
        "cityCode": [1, 2],
        "price": [100000, 200000],
    })
    assert get_average_price_by_arrondissement(df, 3) is None


def test_arrondissement_nan_prices_returns_none():
    df = pd.DataFrame({
        "cityCode": [1, 1],
        "price": [None, None],
    })
    assert get_average_price_by_arrondissement(df, 1) is None


# ==========================================================
# Tests: Entraînement & comparaison de modèles
# (structure + capacité à prédire + erreurs)
# ==========================================================

def test_train_and_compare_models_returns_metrics_and_models():
    df = _make_small_regression_df()
    results_df, models = train_and_compare_models(df, feature_cols=["x1", "x2"])

    # Structure du tableau
    assert set(["model", "MAE", "RMSE", "R2"]).issubset(results_df.columns)
    assert len(results_df) == 3
    assert set(results_df["model"].tolist()) == {"Linear Regression", "Random Forest", "Ridge"}

    # Les métriques doivent être finies (pas NaN/inf)
    assert results_df[["MAE", "RMSE", "R2"]].notna().all().all()

    # Structure des modèles
    assert set(models.keys()) == {"Linear Regression", "Random Forest", "Ridge"}
    # Bonus: les modèles doivent avoir fit/predict
    for m in models.values():
        assert hasattr(m, "fit")
        assert hasattr(m, "predict")


def test_train_best_model_on_full_data_returns_fitted_model_that_predicts():
    df = _make_small_regression_df()

    best_name, best_model, results_df = train_best_model_on_full_data(
        df,
        feature_cols=["x1", "x2"],
    )

    assert best_name in {"Linear Regression", "Random Forest", "Ridge"}
    assert set(["model", "MAE", "RMSE", "R2"]).issubset(results_df.columns)

    X = df[["x1", "x2"]]
    preds = best_model.predict(X)

    # Tests "forts"
    assert len(preds) == len(df)
    assert pd.Series(preds).notna().all()
    assert pd.Series(preds).apply(lambda v: pd.notna(v)).all()


def test_train_and_compare_models_raises_if_feature_missing():
    df = _make_small_regression_df()
    with pytest.raises(KeyError):
        train_and_compare_models(df, feature_cols=["x1", "missing_feature"])


def test_train_best_model_on_full_data_raises_if_target_missing():
    df = _make_small_regression_df().drop(columns=["price"])
    with pytest.raises(KeyError):
        train_best_model_on_full_data(
            df,
            feature_cols=["x1", "x2"],
            target_col="price",
        )


# ==========================================================
# Tests: Régression linéaire (cas "parfait" => métriques attendues)
# ==========================================================

def test_linear_regression_is_perfect_on_perfect_linear_data():
    df = _make_perfect_linear_df(60)

    results_df, _ = train_and_compare_models(
        df,
        feature_cols=["x1", "x2"],
        target_col="price",
        test_size=0.2,
        random_state=42,
    )

    lin_row = results_df[results_df["model"] == "Linear Regression"].iloc[0]

    assert lin_row["MAE"] == pytest.approx(0.0, abs=1e-8)
    assert lin_row["RMSE"] == pytest.approx(0.0, abs=1e-8)
    assert lin_row["R2"] == pytest.approx(1.0, abs=1e-12)


def test_ridge_is_near_perfect_on_perfect_linear_data():
    df = _make_perfect_linear_df(60)

    results_df, _ = train_and_compare_models(
        df,
        feature_cols=["x1", "x2"],
        target_col="price",
        test_size=0.2,
        random_state=42,
    )

    ridge_row = results_df[results_df["model"] == "Ridge"].iloc[0]

    # Ridge n'est pas forcément parfait à cause de alpha=1.0 (régularisation)
    assert ridge_row["MAE"] < 0.01
    assert ridge_row["RMSE"] < 0.01
    assert ridge_row["R2"] > 0.999999
