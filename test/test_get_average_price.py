import sys, os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from functions.data_viz import get_average_price_by_citycode


def test_get_average_price_by_citycode_valid():
    """Test avec un cityCode existant."""
    df = pd.DataFrame({
        "cityCode": [101, 101, 202],
        "price": [100000, 200000, 300000]
    })

    result = get_average_price_by_citycode(df, 101)
    result2 = get_average_price_by_citycode(df, 202)
    assert result == 150000.0
    assert result2 == 300000.0
    
    


def test_get_average_price_by_citycode_not_found():
    """Test avec un cityCode inexistant."""
    df = pd.DataFrame({
        "cityCode": [101, 202],
        "price": [120000, 180000]
    })

    result = get_average_price_by_citycode(df, 999)
    assert result is None


def test_get_average_price_by_citycode_type():
    """Vérifie que la fonction retourne bien un float pour un code valide."""
    df = pd.DataFrame({
        "cityCode": [1, 1, 2],
        "price": [100000, 200000, 150000]
    })

    result = get_average_price_by_citycode(df, 1)
    assert isinstance(result, float)
