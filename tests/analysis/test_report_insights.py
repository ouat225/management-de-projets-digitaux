import pandas as pd

from maison_estimateur.analysis.report_insights import build_insights


class TestBuildInsights:

    def test_returns_list_of_strings_non_empty(self):
        df = pd.DataFrame({
            "price": [100000, 200000, 300000, 400000],
            "cityCode": [101, 101, 202, 202],
        })

        features = {
            "squareMeters": 80.0,
            "numberOfRooms": 3,
            "cityCode": 101,
        }

        insights = build_insights(
            df=df,
            features=features,
            estimated_price=250000.0,
            model_name="Linear Regression",
        )

        assert isinstance(insights, list)
        assert len(insights) >= 3
        assert all(isinstance(x, str) for x in insights)

    def test_mentions_model_name(self):
        df = pd.DataFrame({
            "price": [100000, 200000, 300000, 400000],
            "cityCode": [101, 101, 202, 202],
        })

        features = {"squareMeters": 60.0, "numberOfRooms": 2, "cityCode": 202}

        model_name = "Ridge"
        insights = build_insights(
            df=df,
            features=features,
            estimated_price=180000.0,
            model_name=model_name,
        )

        # On vérifie qu'au moins une phrase parle du modèle
        assert any(model_name in s for s in insights)

    def test_does_not_crash_if_citycode_missing(self):
        df = pd.DataFrame({"price": [10, 20, 30, 40]})

        features = {"squareMeters": 40.0, "numberOfRooms": 1}  # cityCode absent

        insights = build_insights(
            df=df,
            features=features,
            estimated_price=25.0,
            model_name="Linear Regression",
        )

        assert isinstance(insights, list)
        assert len(insights) > 0
