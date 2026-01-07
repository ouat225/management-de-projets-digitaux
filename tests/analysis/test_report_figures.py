import pandas as pd
import matplotlib

# Backend headless pour CI / Windows sans GUI
matplotlib.use("Agg")

from maison_estimateur.analysis.report_figures import fig_price_distribution_png


class TestFigPriceDistributionPng:
    def test_returns_valid_png_bytes_when_price_exists(self):
        df = pd.DataFrame(
            {
                "price": [100000, 150000, 200000, 250000, 300000],
                "cityCode": [101, 101, 202, 202, 303],
            }
        )

        estimated_price = 210000.0
        png_bytes = fig_price_distribution_png(df=df, estimated_price=estimated_price)

        # Type et signature PNG
        assert isinstance(png_bytes, (bytes, bytearray))
        assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"

        # Taille minimale : évite faux positifs (image vide/corrompue)
        assert len(png_bytes) > 500

    def test_png_contains_expected_png_chunks(self):
        """
        Test de valeur : un PNG valide contient des chunks IHDR et IEND.
        On ne teste pas l'image visuellement, mais sa structure.
        """
        df = pd.DataFrame({"price": [10, 20, 30, 40, 50]})

        png_bytes = fig_price_distribution_png(df=df, estimated_price=25.0)

        assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"
        # Chunks PNG standards
        assert b"IHDR" in png_bytes
        assert b"IEND" in png_bytes

    def test_returns_none_if_price_column_missing(self):
        df = pd.DataFrame({"cityCode": [1, 2, 3]})

        result = fig_price_distribution_png(df=df, estimated_price=1000.0)

        assert result is None

    def test_returns_none_if_price_column_empty_or_all_nan(self):
        df = pd.DataFrame({"price": [None, None, None]})

        result = fig_price_distribution_png(df=df, estimated_price=1000.0)

        assert result is None
