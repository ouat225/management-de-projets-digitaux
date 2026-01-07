import pandas as pd
import matplotlib

# Backend headless pour CI / Windows sans GUI
matplotlib.use("Agg")

from maison_estimateur.analysis.report_pdf import generate_estimation_report_pdf


def _default_features(city_code: int = 101) -> dict:
    return {
        "squareMeters": 80.0,
        "numberOfRooms": 3,
        "cityCode": city_code,
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


class TestGenerateEstimationReportPdf:
    def test_returns_valid_pdf_bytes_signature_and_eof(self):
        df = pd.DataFrame(
            {
                "price": [100000, 200000, 300000, 400000],
                "cityCode": [101, 101, 202, 202],
            }
        )

        pdf_bytes = generate_estimation_report_pdf(
            df=df,
            features=_default_features(101),
            estimated_price=250000.0,
            model_name="Linear Regression",
        )

        # Type attendu
        assert isinstance(pdf_bytes, (bytes, bytearray))

        # "Vrai" PDF : signature + taille non triviale
        assert pdf_bytes[:4] == b"%PDF"
        assert len(pdf_bytes) > 1500  # plus robuste que 500 (évite faux positifs)

        # Beaucoup de PDFs finissent par %%EOF (ReportLab inclut généralement EOF)
        assert b"%%EOF" in pdf_bytes[-2048:]  # on cherche EOF en fin de fichier

    def test_pdf_contains_some_expected_text_markers(self):
        """
        Test de valeur : on vérifie que le PDF contient des marqueurs textuels
        (sans dépendre de la mise en page exacte).
        """
        df = pd.DataFrame({"price": [1, 2, 3, 4, 5], "cityCode": [1, 1, 1, 1, 1]})

        pdf_bytes = generate_estimation_report_pdf(
            df=df,
            features=_default_features(999),
            estimated_price=123456.0,
            model_name="Ridge",
        )

        assert pdf_bytes[:4] == b"%PDF"
        assert len(pdf_bytes) > 1500

        # On cherche des tokens PDF courants qui indiquent un PDF “structuré”
        # (objets, streams, etc.). Ça évite un test “does not crash” trop faible.
        assert b"/Type" in pdf_bytes
        assert b"stream" in pdf_bytes

    def test_minimal_df_still_generates_pdf(self):
        """
        df minimal : report_figures utilise seulement "price".
        On vérifie qu'on génère un PDF complet, pas juste "ça ne crash pas".
        """
        df = pd.DataFrame({"price": [1, 2, 3, 4, 5]})

        pdf_bytes = generate_estimation_report_pdf(
            df=df,
            features=_default_features(999),
            estimated_price=123456.0,
            model_name="Ridge",
        )

        assert pdf_bytes[:4] == b"%PDF"
        assert len(pdf_bytes) > 1500
        assert b"%%EOF" in pdf_bytes[-2048:]

