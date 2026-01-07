from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from maison_estimateur.data_processing.load_data import (
    load_data,
    default_data_path,
)


class TestLoadData:
    def test_load_data_from_explicit_csv(self, tmp_path: Path):
        csv_path = tmp_path / "sample.csv"
        expected = pd.DataFrame({"price": [1, 2, 3], "squareMeters": [40, 50, 60]})
        expected.to_csv(csv_path, index=False)

        loaded = load_data(csv_path)

        # Tests de valeur (pas de isinstance)
        assert list(loaded.columns) == ["price", "squareMeters"]
        assert loaded.shape == (3, 2)
        pd.testing.assert_frame_equal(loaded.reset_index(drop=True), expected)

    def test_load_data_missing_file_raises(self, tmp_path: Path):
        missing = tmp_path / "does_not_exist.csv"
        with pytest.raises(FileNotFoundError):
            load_data(missing)

    def test_default_path_points_to_paris_housing_csv(self):
        path = default_data_path()

        # Tests de valeur / propriété
        assert path.name == "ParisHousing.csv"
        # optionnel mais utile : on vérifie que c'est bien un Path-like
        assert hasattr(path, "exists")

    def test_cached_read_called_once_per_load_call(self, tmp_path: Path, monkeypatch):
        """
        Ici on mock _read_csv_cached => donc on ne teste pas le cache Streamlit,
        on teste juste que load_data délègue bien la lecture à _read_csv_cached
        à chaque appel.
        """
        called = {"count": 0}

        def fake_read(_path: str | Path):
            called["count"] += 1
            return pd.DataFrame({"a": [1]})

        monkeypatch.setattr(
            "maison_estimateur.data_processing.load_data._read_csv_cached",
            fake_read,
        )

        csv_path = tmp_path / "x.csv"
        pd.DataFrame({"a": [1]}).to_csv(csv_path, index=False)

        _ = load_data(csv_path)
        _ = load_data(csv_path)

        assert called["count"] == 2  # mock => appelé à chaque load_data()

    def test_load_data_uses_default_path_when_none(self, monkeypatch):
        fake_df = pd.DataFrame({"x": [1]})

        monkeypatch.setattr(
            "maison_estimateur.data_processing.load_data._read_csv_cached",
            lambda _x: fake_df,
        )
        monkeypatch.setattr(
            "maison_estimateur.data_processing.load_data.default_data_path",
            lambda: Path("/fake/data/ParisHousing.csv"),
        )
        monkeypatch.setattr(Path, "exists", lambda self: True)

        df = load_data(None)

        # Test de valeur :SÛR : égalité de contenu
        pd.testing.assert_frame_equal(df, fake_df)
