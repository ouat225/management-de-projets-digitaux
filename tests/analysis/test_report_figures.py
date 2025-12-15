import pandas as pd
import matplotlib

matplotlib.use("Agg")

from maison_estimateur.analysis.report_figures import fig_price_distribution_png


class TestFigPriceDistributionPng:

    def test_returns_png_bytes_when_price_exists(self):
        df = pd.DataFrame({
            "price": [100000, 150000, 200000, 250000, 300000],
            "cityCode": [101, 101, 202, 202, 303],
        })

        png_bytes = fig_price_distribution_png(df=df, estimated_price=210000.0)

        assert isinstance(png_bytes, (bytes, bytearray))
        # signature PNG
        assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"
        assert len(png_bytes) > 200

    def test_returns_none_if_price_missing(self):
        df = pd.DataFrame({"cityCode": [1, 2, 3]})
        assert fig_price_distribution_png(df=df, estimated_price=1000.0) is None

    def test_returns_none_if_price_empty(self):
        df = pd.DataFrame({"price": [None, None, None]})
        assert fig_price_distribution_png(df=df, estimated_price=1000.0) is None
