import sys, os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from functions.data_viz import load_data

def test_load_data_creates_dataframe(tmp_path):
    """Vérifie que load_data charge bien un CSV."""
    csv_path = tmp_path / "sample.csv"
    df = pd.DataFrame({"price": [1, 2, 3], "squareMeters": [40, 50, 60]})
    df.to_csv(csv_path, index=False)

    loaded = load_data(csv_path)

    assert isinstance(loaded, pd.DataFrame)
    assert "price" in loaded.columns
    assert len(loaded) == 3
