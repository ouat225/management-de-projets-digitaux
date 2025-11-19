import pandas as pd
import statsmodels.api as sm

FEATURES = [
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
    "hasGuestRoom"
]


def compute_linear_regression_full(df: pd.DataFrame):
    """Calcule la régression linéaire complète avec coefficients, p-values, R² et R² ajusté."""
    cols = ["price"] + FEATURES
    sub = df[cols].dropna()
    y = sub["price"]
    X = sub[FEATURES]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    #tableau
    results = pd.DataFrame({
        "Variable": model.params.index,
        "Coefficient": model.params.values,
        "p-value": model.pvalues.values,
        "t-stat": model.tvalues.values,
    })

    metrics = {
        "R2": model.rsquared,
        "R2_adj": model.rsquared_adj
    }

    return results, metrics, model
