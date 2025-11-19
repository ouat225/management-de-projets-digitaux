from pathlib import Path
import pandas as pd
import pytest

from maison_estimateur.data_processing.load_data import (
    load_data,
    default_data_path,
    _read_csv_cached,
)


class TestLoadData:
    def test_load_data_from_explicit_csv(self, tmp_path: Path):
        csv_path = tmp_path / "sample.csv"
        df = pd.DataFrame({"price": [1, 2, 3], "squareMeters": [40, 50, 60]})
        df.to_csv(csv_path, index=False)

        loaded = load_data(csv_path)

        assert isinstance(loaded, pd.DataFrame)
        assert list(loaded.columns) == ["price", "squareMeters"]
        assert len(loaded) == 3

    def test_load_data_missing_file_raises(self, tmp_path: Path):
        missing = tmp_path / "does_not_exist.csv"

        with pytest.raises(FileNotFoundError):
            load_data(missing)

    def test_default_path_is_a_path(self):
        path = default_data_path()
        assert isinstance(path, Path)
        assert path.name == "ParisHousing.csv"

    def test_cached_read_called_once(self, tmp_path: Path, monkeypatch):
        called = {"count": 0}

        def fake_read(path: str):
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

        assert called["count"] == 2  # cache est mocké → appelé 2 fois

    def test_load_data_uses_default_path_when_none(self, monkeypatch):
        fake_df = pd.DataFrame({"x": [1]})

        monkeypatch.setattr(
            "maison_estimateur.data_processing.load_data._read_csv_cached",
            lambda x: fake_df,
        )
        monkeypatch.setattr(
            "maison_estimateur.data_processing.load_data.default_data_path",
            lambda: Path("/fake/data/ParisHousing.csv"),
        )
        monkeypatch.setattr(
            Path, "exists", lambda self: True
        )

        df = load_data(None)

        assert isinstance(df, pd.DataFrame)
        assert df.equals(fake_df)
