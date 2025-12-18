from __future__ import annotations

from typing import Any

import pandas as pd

from maison_estimateur.analysis.pricing import get_average_price_by_citycode


def build_insights(
    df: pd.DataFrame,
    features: dict[str, Any],
    estimated_price: float,
    model_name: str,
) -> list[str]:
    """
    Génère quelques insights simples, explicables et utiles dans un PDF.
    (Règles déterministes, pas d’IA.)
    """
    insights: list[str] = []

    # Infos principales
    area = _safe_float(features.get("squareMeters"))
    rooms = _safe_int(features.get("numberOfRooms"))
    citycode = features.get("cityCode")

    if area and area > 0:
        eur_m2 = estimated_price / area
        insights.append(f"Prix estimé au m² : {eur_m2:,.0f} € / m².")
    else:
        insights.append("Prix au m² : non calculable (surface manquante).")

    # Comparaison à la moyenne du quartier
    try:
        mean_city = get_average_price_by_citycode(df, citycode)
    except Exception:
        mean_city = None

    if mean_city is not None:
        if estimated_price > mean_city:
            insights.append("Le bien est estimé au-dessus de la moyenne de son quartier (cityCode).")
        elif estimated_price < mean_city:
            insights.append("Le bien est estimé en-dessous de la moyenne de son quartier (cityCode).")
        else:
            insights.append("Le bien est estimé très proche de la moyenne de son quartier (cityCode).")
        insights.append(f"Prix moyen du quartier (proxy) : {mean_city:,.0f} €.")
    else:
        insights.append("Prix moyen du quartier : indisponible (proxy non calculable pour ce cityCode).")

    # Positionnement dans le dataset (percentiles)
    if "price" in df.columns:
        prices = df["price"].dropna()
        if not prices.empty:
            q25, q50, q75 = prices.quantile([0.25, 0.5, 0.75]).tolist()
            if estimated_price < q25:
                insights.append("Positionnement global : dans le quartile bas des prix du dataset.")
            elif estimated_price < q50:
                insights.append("Positionnement global : entre le 25e et le 50e percentile des prix du dataset.")
            elif estimated_price < q75:
                insights.append("Positionnement global : entre le 50e et le 75e percentile des prix du dataset.")
            else:
                insights.append("Positionnement global : dans le quartile haut des prix du dataset.")
        else:
            insights.append("Positionnement global : indisponible (colonne price vide).")
    else:
        insights.append("Positionnement global : indisponible (colonne price absente).")

    # Message sur le modèle
    insights.append(f"Estimation obtenue via le modèle : {model_name}.")

    # Petit rappel sur les entrées
    if rooms is not None and area is not None and area > 0:
        insights.append(f"Configuration saisie : {area:,.0f} m², {rooms} pièces, quartier {citycode}.")
    else:
        insights.append(f"Quartier saisi : {citycode}.")

    return insights


def _safe_float(x: Any) -> float | None:
    try:
        v = float(x)
        if pd.isna(v):
            return None
        return v
    except Exception:
        return None


def _safe_int(x: Any) -> int | None:
    try:
        return int(x)
    except Exception:
        try:
            return int(str(x))
        except Exception:
            return None
