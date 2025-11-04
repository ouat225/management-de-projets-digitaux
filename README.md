# MAISONESTIMATEUR

Votre outil d’analyse du marché immobilier parisien

## Aperçu

Ce projet propose une application interactive permettant d’analyser le marché immobilier parisien à partir d’un jeu de données de 10 000 logements.
L’outil permet de visualiser les statistiques du marché, d’explorer les variables descriptives du dataset et d’obtenir des informations par quartier.

## Fonctionnalités

- **Analyse univariée** : statistiques descriptives pour chaque variable
- **Visualisations interactives** : histogrammes, boxplots, diagrammes en barres
- **Analyse par quartier (cityCode)** : prix moyen par zone géographique

## Prérequis

- Python 3.8+
- Bibliothèques Python listées dans requirements.txt
- Streamlit (installé automatiquement via les dépendances)

## Installation et utilisation

1. **Cloneer le dépot**
   ```bash
   git clone https://gitlab-mi.univ-reims.fr/malh0033/management-de-projets-digitaux.git
   cd management-de-projets-digitaux
   ```

2. **Créer et activer un environnement virtuel**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l’application Streamlit**
   Depuis la racine du projet, run:
   ```bash
   streamlit run src/main.py
   ```

5. **Utilisation de l'application**
   - L’application s’ouvre automatiquement dans votre navigateur
   - Naviguez via les onglets : Accueil, Estimation, Statistiques
   - Analysez les données immobilières parisiennes de façon interactive

## Structure du projet

```

project_root/
├── data/
│   └── ParisHousing.csv               # Dataset principal
│
├── src/
│   ├── main.py                        # Point d'entrée Streamlit
│   └── MaisonEstimateur/
│       ├── app.py                     # Assemble et gère les pages
│       ├── pages/                     # Pages de l'application
│       │   ├── home_page.py
│       │   ├── estimation_page.py
│       │   └── statistics_page.py
│       ├── components/                # Composants UI réutilisables
│       │   ├── layout.py
│       │   └── widgets.py
│       ├── data_processing/           # Chargement/gestion des données
│       │   └── load_data.py
│       └── analysis/                  # Logique métier & statistiques
│           ├── univariate_analysis.py
│           └── pricing.py
│
├── tests/                             # Tests unitaires
│
├── requirements.txt
└── README.md

```

## Dataset

### Source
Data is sourced from [Kaggle - Paris Housing Price Prediction](https://www.kaggle.com/datasets/mssmartypants/paris-housing-price-prediction)

### Variable Descriptions

| Variable | Type | Description |
|----------|------|-------------|
| squareMeters | int | Property size in m² |
| numberOfRooms | int | Number of rooms |
| hasYard | int | Has yard (0: no, 1: yes) |
| hasPool | int | Has swimming pool (0: no, 1: yes) |
| floors | int | Number of floors |
| cityCode | int | Postal code |
| cityPartRange | int | Neighborhood prestige level (0-10) |
| numPrevOwners | int | Number of previous owners |
| made | int | Year of construction |
| isNewBuilt | int | New or renovated (0: no, 1: yes) |
| hasStormProtector | int | Weather protection (0: no, 1: yes) |
| basement | int | Basement area in m² |
| attic | int | Attic area in m² |
| garage | int | Garage size in m² |
| hasStorageRoom | int | Has storage room (0: no, 1: yes) |
| hasGuestRoom | int | Number of guest rooms |
| price | float | Property price |

## Authors

- Oumar Abdramane ALLAWAN
- Dimitri DELPECH
- Minan Jean-Marc OUATTARA
- Simon MALHEY
- Dominique MUSITELLI
