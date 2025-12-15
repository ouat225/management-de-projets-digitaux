import pandas as pd
import matplotlib

# Backend headless pour CI / Windows sans GUI
matplotlib.use("Agg")

from maison_estimateur.analysis.report_pdf import generate_estimation_report_pdf


class TestGenerateEstimationReportPdf:

    def test_returns_bytes_and_starts_with_pdf_header(self):
        df = pd.DataFrame({
            "price": [100000, 200000, 300000, 400000],
            "cityCode": [101, 101, 202, 202],
        })

        features = {
            "squareMeters": 80.0,
            "numberOfRooms": 3,
            "cityCode": 101,
            "floors": 1,
            "hasYard": 1,
            "hasPool": 0,
            "garage": 0,
            "basement": 0,
            "attic": 0,
            "hasStorageRoom": 1,
            "hasGuestRoom": 0,
            "made": 2000,
            "isNewBuilt": 0,
            "numPrevOwners": 1,
            "hasStormProtector": 0,
        }

        pdf_bytes = generate_estimation_report_pdf(
            df=df,
            features=features,
            estimated_price=250000.0,
            model_name="Linear Regression",
        )

        assert isinstance(pdf_bytes, (bytes, bytearray))
        assert len(pdf_bytes) > 500  # PDF non vide
        assert pdf_bytes[:4] == b"%PDF"

    def test_does_not_crash_with_minimal_df(self):
        # df minimal : report_figures utilise seulement "price"
        df = pd.DataFrame({"price": [1, 2, 3, 4, 5]})

        features = {
            "squareMeters": 50.0,
            "numberOfRooms": 2,
            "cityCode": 999,
            "floors": 1,
            "hasYard": 0,
            "hasPool": 0,
            "garage": 0,
            "basement": 0,
            "attic": 0,
            "hasStorageRoom": 0,
            "hasGuestRoom": 0,
            "made": 1995,
            "isNewBuilt": 0,
            "numPrevOwners": 0,
            "hasStormProtector": 0,
        }

        pdf_bytes = generate_estimation_report_pdf(
            df=df,
            features=features,
            estimated_price=123456.0,
            model_name="Ridge",
        )

        assert isinstance(pdf_bytes, (bytes, bytearray))
        assert pdf_bytes[:4] == b"%PDF"
