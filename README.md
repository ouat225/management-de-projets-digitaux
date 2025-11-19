# MAISONESTIMATEUR

Your Paris Real Estate Market Analysis Tool

## Overview

This project offers an interactive application for analyzing the Paris real estate market using a dataset of 10,000 housing units.
The tool allows you to visualize market statistics, explore the dataset’s descriptive variables, and obtain information by neighborhood.

## Features

- **Univariate analysis** : descriptive statistics for each variable
- **Interactive visualizations** : histograms, boxplots, bar charts
- **Neighborhood analysis (cityCode)** : average price by geographical area

## Requirements

- Python 3.8+
- Python libraries listed in requirements.txt
- Streamlit (automatically installed through dependencies)

## Installation and usage

1. **Clone the repository**
   ```bash
   git clone https://gitlab-mi.univ-reims.fr/malh0033/management-de-projets-digitaux.git
   cd management-de-projets-digitaux
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application**
   Depuis la racine du projet, run:
   ```bash
   streamlit run src/main.py
   ```

5. **Use of the application**
   - The application will automatically open in your browser
   - Navigate through the tabs: Home, Estimation, Statistics
   - Interactively explore Paris real estate market data

## Project structure

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
