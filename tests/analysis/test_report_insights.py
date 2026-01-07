from __future__ import annotations

import re

import pandas as pd

from maison_estimateur.analysis.report_insights import build_insights


def _join(insights) -> str:
    return " ".join(list(insights)).lower()


def _as_list(insights):
    return list(insights)


def _contains_number_rough(text: str, number: int) -> bool:
    """
    Vérifie qu'un nombre apparaît dans le texte, en tolérant les formats:
    - 3000
    - 3 000
    - 3,000
    - 3.000
    """
    s = str(int(number))
    # ex: 3000 -> motif qui accepte 3 000 / 3,000 / 3.000 / 3000
    if len(s) >= 4:
        head = s[:-3]
        tail = s[-3:]
        pattern = rf"{head}[\s,\.]?{tail}"
    else:
        pattern = rf"{s}"
    return re.search(pattern, text) is not None


class TestBuildInsights:
    def test_returns_non_empty_iterable_with_non_blank_sentences(self):
        df = pd.DataFrame(
            {
                "price": [100000, 200000, 300000, 400000],
                "cityCode": [101, 101, 202, 202],
            }
        )

        features = {"squareMeters": 80.0, "numberOfRooms": 3, "cityCode": 101}

        insights = build_insights(
            df=df,
            features=features,
            estimated_price=250000.0,
            model_name="Linear Regression",
        )

        insights_list = _as_list(insights)

        # Valeur / comportement : au moins 2 phrases et aucune vide
        assert len(insights_list) >= 2
        assert all(s.strip() != "" for s in insights_list)

        # Valeur : on veut du contenu utile (prix ou estimation doit apparaître quelque part)
        text = _join(insights_list)
        assert any(k in text for k in ["prix", "estimation", "estimé"])

    def test_mentions_model_name_and_estimated_price_via_price_per_m2(self):
        """
        Le code n'affiche pas forcément le PRIX TOTAL estimé,
        mais il affiche le PRIX AU M² qui dépend directement de estimated_price / surface.
        """
        df = pd.DataFrame(
            {"price": [100000, 200000, 300000, 400000], "cityCode": [101, 101, 202, 202]}
        )

        model_name = "Ridge"
        estimated_price = 180000.0
        area = 60.0
        expected_eur_m2 = int(estimated_price / area)  # 3000

        features = {"squareMeters": area, "numberOfRooms": 2, "cityCode": 202}

        insights = _as_list(
            build_insights(
                df=df,
                features=features,
                estimated_price=estimated_price,
                model_name=model_name,
            )
        )

        text = _join(insights)

        # Valeur : le modèle doit être mentionné
        assert model_name.lower() in text

        # Valeur : le prix au m² doit être présent
        assert "m²" in text or "m2" in text

        # Valeur : on retrouve un chiffre cohérent (3000) dérivé du prix estimé
        assert _contains_number_rough(text, expected_eur_m2)

    def test_citycode_missing_still_provides_market_context(self):
        df = pd.DataFrame({"price": [10, 20, 30, 40]})
        features = {"squareMeters": 40.0, "numberOfRooms": 1}

        insights = _as_list(
            build_insights(
                df=df,
                features=features,
                estimated_price=25.0,
                model_name="Linear Regression",
            )
        )

        assert len(insights) >= 1
        text = _join(insights)

        assert any(k in text for k in ["prix", "moyen", "moyenne", "quartile", "percentile", "estimation"])

    def test_high_estimate_is_flagged_as_high_positioning_in_dataset(self):
        df = pd.DataFrame({"price": [200, 250, 300, 250]})
        features = {"squareMeters": 80.0, "numberOfRooms": 3}

        insights = _as_list(
            build_insights(
                df=df,
                features=features,
                estimated_price=1000.0,
                model_name="Linear Regression",
            )
        )

        text = _join(insights)

        assert re.search(r"quartile\s+haut", text) is not None
