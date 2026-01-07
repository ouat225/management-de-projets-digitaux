# tests/conftest.py
import sys
from pathlib import Path
import pandas as pd
import pytest

# Ajouter le dossier src au PYTHONPATH pour les imports (MaisonEstimateur.*)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture
def df_small() -> pd.DataFrame:
    """DataFrame minimal pour plusieurs tests (prix, code, prestige)."""
    return pd.DataFrame({
        "price": [100000, 200000, 300000, 400000],
        "cityCode": [101, 101, 202, 202],
        "cityPartRange": [3, 3, 7, 7],
        "squareMeters": [40, 60, 80, 100],
        "rooms": [2, 3, 4, 5]
    })
