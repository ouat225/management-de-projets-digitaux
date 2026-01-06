from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def _mean_price_from_mask(df: pd.DataFrame, mask: pd.Series) -> float | None:
    """
    Calcule le prix moyen sur df[mask, "price"] avec garde-fous.
    Retourne None si aucun match ou moyenne NaN.
    """
    if not mask.any():
        return None

    mean_price = df.loc[mask, "price"].mean()
    if pd.isna(mean_price):
        return None

    return float(round(mean_price, 2))


def get_average_price_by_citycode(
    df: pd.DataFrame,
    city_code: str | int | float,
) -> float | None:
    """
    Retourne le prix moyen pour un cityCode.

    - Compare sur str (robuste aux différences de types)
    - Retourne None si colonnes manquantes, aucune correspondance, ou moyenne NaN
    """
    if "cityCode" not in df.columns or "price" not in df.columns:
        return None

    # Normalisation légère pour éviter "101.0" vs "101" quand l'entrée est float/int-like
    try:
        if isinstance(city_code, float) and city_code.is_integer():
            city_code = int(city_code)
        elif isinstance(city_code, str):
            f = float(city_code)
            if f.is_integer():
                city_code = int(f)
    except Exception:
        pass

    mask = df["cityCode"].astype(str) == str(city_code)
    return _mean_price_from_mask(df, mask)


def get_average_price_by_arrondissement(
    df: pd.DataFrame,
    arrondissement: int | str | float,
) -> float | None:
    """
    Retourne le prix moyen pour un arrondissement (1..20).

    Fonction robuste :
    - si df contient 'arrondissement' -> utilise cette colonne
    - sinon -> utilise 'cityCode' (car dans votre projet cityCode est mappé en arrondissement)

    Retourne None si impossible (colonnes absentes, arr invalide, pas de match, moyenne NaN)
    """
    if "price" not in df.columns:
        return None

    # Parse arrondissement en int
    try:
        arr = int(float(arrondissement))
    except Exception:
        return None

    if not (1 <= arr <= 20):
        return None

    # Choix de la colonne support
    if "arrondissement" in df.columns:
        col = "arrondissement"
    elif "cityCode" in df.columns:
        col = "cityCode"
    else:
        return None

    s = pd.to_numeric(df[col], errors="coerce")
    mask = s == arr
    return _mean_price_from_mask(df, mask)


def train_and_compare_models(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str = "price",
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """
    Entraîne plusieurs modèles de régression et retourne :
    - un DataFrame de métriques (MAE, RMSE, R2)
    - un dict {nom_modele: modele_entraine}
    """
    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    models: dict[str, object] = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=200,
            random_state=random_state,
        ),
        "Ridge": Ridge(alpha=1.0),
    }

    results: list[dict[str, float | str]] = []

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse**0.5
        r2 = r2_score(y_test, y_pred)

        results.append({"model": name, "MAE": mae, "RMSE": rmse, "R2": r2})

    results_df = pd.DataFrame(results).sort_values("RMSE").reset_index(drop=True)
    return results_df, models


def train_random_forest_only(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str = "price",
    random_state: int = 42,
) -> RandomForestRegressor:
    """
    Entraîne uniquement un RandomForestRegressor sur tout le dataset,
    pour prédiction temps réel (sans split).
    """
    X = df[feature_cols]
    y = df[target_col]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=random_state,
    )
    model.fit(X, y)
    return model


def train_best_model_on_full_data(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str = "price",
    random_state: int = 42,
) -> tuple[str, object, pd.DataFrame]:
    """
    1) compare les modèles (split)
    2) choisit automatiquement le meilleur (RMSE min)
    3) ré-entraîne ce modèle sur tout le dataset
    Retourne: (best_model_name, best_model_fitted, results_df)
    """
    results_df, models = train_and_compare_models(
        df=df,
        feature_cols=feature_cols,
        target_col=target_col,
        random_state=random_state,
    )

    best_model_name = str(results_df.loc[0, "model"])

    # Refit sur tout le dataset (prod)
    X = df[feature_cols]
    y = df[target_col]
    best_model = models[best_model_name]
    best_model.fit(X, y)

    return best_model_name, best_model, results_df
