from __future__ import annotations
import pandas as pd
import statsmodels.api as sm
from typing import Optional


FEATURES = ["squareMeters", "cityPartRange", "numberOfRooms", "cityCode"]


def train_simple_regression(df: pd.DataFrame):
    data = df.copy()
    needed = FEATURES + ["price"]
    data = data[needed].dropna()

    X = sm.add_constant(data[FEATURES])
    y = data["price"]

    model = sm.OLS(y, X).fit()
    return model


def estimate_price(df: pd.DataFrame,
                   area: float,
                   citypart: int,
                   rooms: int,
                   citycode: int) -> Optional[float]:

    try:
        model = train_simple_regression(df)
    except Exception:
        return None

    x = pd.DataFrame([{
        "const": 1.0,
        "squareMeters": area,
        "cityPartRange": citypart,
        "numberOfRooms": rooms,
        "cityCode": citycode,
    }])

    price = float(model.predict(x)[0])
    return round(price, 2)

