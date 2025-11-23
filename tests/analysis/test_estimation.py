import numpy as np
import pandas as pd
import pytest
from maison_estimateur.analysis.estimation import (
    estimate_price,
    train_simple_regression,
    FEATURES,
)


def _df_small():
    """Petit DataFrame réaliste pour entraîner une régression simple."""
    return pd.DataFrame({
        "squareMeters":  [60, 80, 120, 150],
        "cityPartRange": [3, 5, 7, 4],
        "numberOfRooms": [3, 4, 5, 6],
        "cityCode":      [100, 100, 200, 200],
        "price":         [200000, 260000, 400000, 550000],
    })


def _df_perfect_linear():
    """Données avec une relation linéaire parfaite : price = 1000 * squareMeters."""
    return pd.DataFrame({
        "squareMeters":  [50, 100, 150, 200],
        "cityPartRange": [1, 1, 1, 1],  # Valeur constante
        "numberOfRooms": [2, 2, 2, 2],  # Valeur constante
        "cityCode":      [100, 100, 100, 100],  # Valeur constante
        "price":         [50000, 100000, 150000, 200000],
    })


class TestTrainSimpleRegression:
    """Tests pour la fonction train_simple_regression."""

    def test_train_simple_regression_returns_model(self):
        """Vérifie que la fonction retourne un modèle OLS entraîné."""
        df = _df_perfect_linear()
        model = train_simple_regression(df)
        
        # Vérifie que le modèle a bien été entraîné
        assert hasattr(model, 'params'), "Le modèle doit avoir un attribut 'params'"
        assert len(model.params) == 5  # const + 4 features
        
        # Vérifie que le coefficient de squareMeters est proche de 1000
        # (car price = 1000 * squareMeters dans nos données de test)
        assert abs(model.params['squareMeters'] - 1000) < 1e-6
        
        # Vérifie que le R² est de 1.0 (relation linéaire parfaite)
        assert abs(model.rsquared - 1.0) < 1e-6

    def test_train_simple_regression_with_missing_data(self):
        """Vérifie que la fonction gère correctement les données manquantes."""
        df = _df_perfect_linear()
        # Ajoute une ligne avec des valeurs manquantes
        df = pd.concat([df, pd.DataFrame([{
            'squareMeters': None,
            'cityPartRange': 1,
            'numberOfRooms': 2,
            'cityCode': 100,
            'price': None
        }])], ignore_index=True)
        
        model = train_simple_regression(df)
        # Le modèle devrait être entraîné sur 4 observations (5 - 1 avec valeurs manquantes)
        assert model.nobs == 4

    def test_train_simple_regression_missing_columns(self):
        """Vérifie que la fonction lève une erreur si des colonnes sont manquantes."""
        df = pd.DataFrame({
            'squareMeters': [1, 2, 3],
            'price': [100, 200, 300]
        })
        
        with pytest.raises(KeyError):
            train_simple_regression(df)


class TestEstimatePrice:
    """Tests pour la fonction estimate_price."""

    def test_estimation_returns_float(self):
        """Vérifie que la fonction retourne un float."""
        df = _df_small()
        est = estimate_price(df, area=80, citypart=5, rooms=3, citycode=100)
        assert isinstance(est, float)

    def test_estimation_changes_with_area(self):
        """Vérifie que le prix estimé augmente avec la surface."""
        df = _df_small()
        small = estimate_price(df, 60, 5, 3, 100)
        big   = estimate_price(df, 150, 5, 3, 100)
        assert big > small

    def test_estimation_changes_with_citycode(self):
        """Vérifie que le code postal affecte le prix estimé."""
        df = _df_small()
        cheap = estimate_price(df, 80, 5, 4, 100)
        expensive = estimate_price(df, 80, 5, 4, 200)
        # On ne teste pas les valeurs exactes, juste une différence
        assert expensive != cheap

    def test_missing_columns_returns_none(self):
        """Vérifie que la fonction retourne None si des colonnes sont manquantes."""
        df = pd.DataFrame({
            "squareMeters": [60, 80],
            # cityPartRange manquant
            "price": [200000, 250000],
        })
        assert estimate_price(df, 80, 5, 3, 100) is None
