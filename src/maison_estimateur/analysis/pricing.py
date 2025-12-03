from __future__ import annotations

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def get_average_price_by_citycode(
    df: pd.DataFrame,
    city_code: str | int | float,
) -> float | None:
    """
    Return the average property price for a given cityCode.

    - Accepts str/int/float and compares on string (robust to type differences)
    - Returns None if cityCode/price are missing or if no match is found
    """
    if "cityCode" not in df.columns or "price" not in df.columns:
        return None

    mask = df["cityCode"].astype(str) == str(city_code)
    if not mask.any():
        return None

    mean_price = df.loc[mask, "price"].mean()
    if pd.isna(mean_price):
        return None

    return float(round(mean_price, 2))


def train_and_compare_models(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str = "price",
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """
    Train several regression models and return:
    - a DataFrame with performance metrics (MAE, RMSE, R2)
    - a dict {model_name: trained_model}
    """

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    models: dict[str, object] = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=200, random_state=random_state
        ),
        "Ridge": Ridge(alpha=1.0),
        # Si vous préférez Lasso :
        # "Lasso": Lasso(alpha=0.001),
    }

    results: list[dict[str, float | str]] = []

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5
        r2 = r2_score(y_test, y_pred)


        results.append(
            {
                "model": name,
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
            }
        )

    results_df = pd.DataFrame(results).sort_values("RMSE").reset_index(drop=True)

    return results_df, models
