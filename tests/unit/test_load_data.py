# tests/unit/test_load_data.py
from pathlib import Path
import pandas as pd
from MaisonEstimateur.data_processing.load_data import load_data

def test_load_data_creates_dataframe(tmp_path: Path):
    csv_path = tmp_path / "sample.csv"
    df = pd.DataFrame({"price": [1, 2, 3], "squareMeters": [40, 50, 60]})
    df.to_csv(csv_path, index=False)

    loaded = load_data(csv_path)

    assert isinstance(loaded, pd.DataFrame)
    assert "price" in loaded.columns
    assert len(loaded) == 3


def test_load_data_missing_file_raises(tmp_path: Path):
    missing = tmp_path / "does_not_exist.csv"
    # load_data() doit lever un FileNotFoundError si le fichier n'existe pas
    try:
        load_data(missing)
        assert False, "FileNotFoundError attendu"
    except FileNotFoundError:
        assert True
