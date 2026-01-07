from __future__ import annotations

import pandas as pd
import statsmodels.api as sm


FEATURES: list[str] = [
    "squareMeters",
    "numberOfRooms",
    "hasYard",
    "hasPool",
    "floors",
    "cityCode",
    "cityPartRange",
    "numPrevOwners",
    "made",
    "isNewBuilt",
    "hasStormProtector",
    "basement",
    "attic",
    "garage",
    "hasStorageRoom",
    "hasGuestRoom",
]


def _prepare_regression_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prépare (X, y) pour la régression OLS:
    - sélectionne price + FEATURES
    - dropna
    - ajoute la constante
    """
    cols = ["price", *FEATURES]
    sub = df[cols].dropna()

    y = sub["price"]
    X = sub[FEATURES]
    X = sm.add_constant(X, has_constant="add")  # évite double-const si déjà présente
    return X, y


def compute_linear_regression_full(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, float], object]:
    """
    Calcule la régression linéaire complète (OLS) et retourne:
    - results: DataFrame avec coefficients, p-values, t-stats
    - metrics: dict {"R2", "R2_adj"}
    - model: objet statsmodels fitted (pour predict(), nobs, etc.)
    """
    X, y = _prepare_regression_data(df)

    model = sm.OLS(y, X).fit()

    results = pd.DataFrame(
        {
            "Variable": model.params.index,
            "Coefficient": model.params.values,
            "p-value": model.pvalues.values,
            "t-stat": model.tvalues.values,
        }
    )

    metrics: dict[str, float] = {
        "R2": float(model.rsquared),
        "R2_adj": float(model.rsquared_adj),
    }

    return results, metrics, model
