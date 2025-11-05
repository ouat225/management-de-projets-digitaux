# tests/unit/test_pricing.py
import pandas as pd
from MaisonEstimateur.analysis.pricing import (
    get_average_price_by_citycode,
    get_average_price_by_citypart,
)

def test_get_average_price_by_citycode_valid():
    df = pd.DataFrame({
        "cityCode": [101, 101, 202],
        "price": [100000, 200000, 300000],
    })
    assert get_average_price_by_citycode(df, 101) == 150000.0
    assert get_average_price_by_citycode(df, 202) == 300000.0


def test_get_average_price_by_citycode_not_found():
    df = pd.DataFrame({
        "cityCode": [101, 202],
        "price": [120000, 180000],
    })
    assert get_average_price_by_citycode(df, 999) is None


def test_get_average_price_by_citypart_valid():
    df = pd.DataFrame({
        "cityPartRange": [3, 3, 7, 7],
        "price": [100000, 200000, 300000, 500000],
    })
    assert get_average_price_by_citypart(df, 3) == 150000.0
    assert get_average_price_by_citypart(df, 7) == 400000.0


def test_get_average_price_by_citypart_not_found():
    df = pd.DataFrame({
        "cityPartRange": [1, 2],
        "price": [100000, 150000],
    })
    assert get_average_price_by_citypart(df, 9) is None
