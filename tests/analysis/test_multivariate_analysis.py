import numpy as np
import pandas as pd
import pytest

from maison_estimateur.analysis.multivariate_analysis import (
    compute_price_correlation_figure,
    compute_vif_table,
    get_numeric_features_for_price,
    _select_numeric_columns,
)


# ------------------------------
# Tests pour compute_price_correlation_figure
# ------------------------------

def test_corr_price_valid_returns_non_empty_corr_and_figure():
    df = pd.DataFrame({
        "price": [100000, 150000, 200000, 250000],
        "squareMeters": [40, 50, 60, 70],
        "rooms": [2, 3, 3, 4],
    })

    corr_price, fig = compute_price_correlation_figure(df)

    # Tests "forts" : contenu, pas type
    assert not corr_price.empty
    assert "price" in corr_price.index
    assert corr_price.shape[0] >= 1
    assert corr_price.notna().any().any()

    assert fig is not None


def test_corr_price_missing_price_returns_empty_and_none_fig():
    df = pd.DataFrame({
        "squareMeters": [40, 50, 60],
        "rooms": [2, 3, 4],
    })

    corr_price, fig = compute_price_correlation_figure(df)

    assert corr_price.empty
    assert fig is None


def test_corr_price_non_numeric_price_returns_empty_and_none_fig():
    df = pd.DataFrame({
        "price": ["a", "b", "c"],
        "squareMeters": [40, 50, 60],
    })

    corr_price, fig = compute_price_correlation_figure(df)

    assert corr_price.empty
    assert fig is None


# ------------------------------
# Tests pour compute_vif_table
# ------------------------------

def test_vif_not_enough_numeric_returns_empty_df():
    df = pd.DataFrame({
        "price": [1, 2, 3],
        "city": ["a", "b", "c"],
    })

    vif_df = compute_vif_table(df)

    assert isinstance(vif_df, pd.DataFrame)
    assert vif_df.empty


def test_vif_all_nan_rows_returns_empty():
    df = pd.DataFrame({
        "x1": [np.nan, np.nan],
        "x2": [np.nan, np.nan],
    })

    vif_df = compute_vif_table(df)

    assert vif_df.empty


def test_vif_valid_returns_expected_columns_and_values():
    """
    IMPORTANT :
    - On évite la colinéarité parfaite (sinon VIF = inf, ce qui est normal).
    - On veut un VIF fini => variables corrélées mais pas strictement linéaires.
    """
    df = pd.DataFrame({
        "price": [100, 120, 130, 150, 160, 175, 190, 205, 220, 240],
        "x1":    [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        # Corrélé à x1 mais pas parfaitement colinéaire
        "x2":    [1.1, 1.9, 3.2, 3.8, 5.3, 5.7, 7.4, 7.9, 9.1, 10.6],
    })

    vif_df = compute_vif_table(df)

    assert not vif_df.empty
    assert set(vif_df.columns) >= {"variable", "vif"}
    assert set(vif_df["variable"]) == {"x1", "x2"}

    # VIF doit être numérique et pas NaN
    assert vif_df["vif"].notna().all()
    assert np.isfinite(vif_df["vif"]).all()

    # Bonus "test fort" : VIF >= 1 (définition)
    assert (vif_df["vif"] >= 1.0).all()


# ------------------------------
# Tests pour get_numeric_features_for_price
# ------------------------------

def test_numeric_features_for_price_returns_only_numeric_without_price():
    df = pd.DataFrame({
        "price": [100000, 150000, 200000],
        "squareMeters": [40, 50, 60],
        "rooms": [2, 3, 4],
        "city": ["a", "b", "c"],
    })

    feats = get_numeric_features_for_price(df)

    assert set(feats) == {"squareMeters", "rooms"}
    assert "price" not in feats


def test_numeric_features_for_price_without_price_column_still_works():
    df = pd.DataFrame({
        "squareMeters": [40, 50, 60],
        "rooms": [2, 3, 4],
        "city": ["a", "b", "c"],
    })

    feats = get_numeric_features_for_price(df)

    assert set(feats) == {"squareMeters", "rooms"}


# ------------------------------
# Tests pour _select_numeric_columns
# ------------------------------

def test_select_numeric_columns_filters_non_numeric_and_bool():
    df = pd.DataFrame({
        "int_col": [1, 2, 3],
        "float_col": [1.5, 2.5, 3.5],
        "str_col": ["a", "b", "c"],
        "bool_col": [True, False, True],
    })

    numeric_df = _select_numeric_columns(df)

    assert set(numeric_df.columns) == {"int_col", "float_col"}
    assert numeric_df["int_col"].tolist() == [1, 2, 3]
    assert numeric_df["float_col"].tolist() == [1.5, 2.5, 3.5]


def test_select_numeric_columns_returns_copy_not_view():
    df = pd.DataFrame({
        "int_col": [1, 2],
        "str_col": ["x", "y"],
    })

    numeric_df = _select_numeric_columns(df)
    numeric_df.loc[0, "int_col"] = 999

    assert df.loc[0, "int_col"] == 1
    assert "str_col" in df.columns
