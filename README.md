# MAISONESTIMATEUR

An interactive tool for analyzing the Paris real estate market.

## Overview

MaisonEstimateur provides a Streamlit application to explore and visualize the Paris housing market using a dataset of 10,000 housing units.  
It allows you to:
- Visualize descriptive statistics for each variable
- Generate interactive plots (histograms, boxplots, bar charts)
- Analyze neighborhoods (`cityCode`) with average price by geographical area

## Features

- **Univariate analysis**: descriptive statistics for each variable
- **Interactive visualizations**: histograms, boxplots, bar charts
- **Neighborhood analysis**: average price by geographical area

## Requirements

- Python 3.13+
- Poetry (dependency manager based on `pyproject.toml`)
- Streamlit (installed automatically via Poetry)

## Installation and Usage

1. **Clone the repository**
   ```bash
   git clone https://gitlab-mi.univ-reims.fr/malh0033/management-de-projets-digitaux.git
   cd management-de-projets-digitaux
   ```

2. **Install poetry if not installed**
   ```bash
   pip install poetry
   ```

3. **Install dependencies and create the virtual environment**
   ```bash
   poetry install
   ```

4. **Run the Streamlit application**
   ```bash
   poetry run streamlit run src/maison_estimateur/app.py
   ```

5. **Use of the application**

The application will automatically open in your browser (http://localhost:8501)

Navigate through the tabs: Home, Estimation, Statistics, Comparison

Interactively explore Paris real estate market data

## Project structure

```

project_root/
├── data/
│   └── ParisHousing.csv            # Main dataset
│
├── src/
│   ├── maison_estimateur/          # Main application package
│   │   ├── app.py                  # Streamlit entrypoint
│   │
│   │   ├── pages/                  # Application pages
│   │   │   ├── home_page.py
│   │   │   ├── estimation_page.py
│   │   │   ├── statistics_page.py
│   │   │   └── comparison_page.py  # Property comparison (Sprint 5)
│   │
│   │   ├── components/             # Reusable UI components
│   │   │   ├── layout.py
│   │   │   └── widgets.py
│   │
│   │   ├── data_processing/        # Data loading & preprocessing
│   │   │   └── load_data.py
│   │
│   │   └── analysis/               # Statistical logic & modeling
│   │       ├── univariate_analysis.py
│   │       ├── multivariate_analysis.py
│   │       └── pricing.py           # Estimation logic
│
├── tests/                          # Unit tests
├── pyproject.toml                  # Poetry configuration
├── poetry.lock                     # Dependency lock file
├── Dockerfile
├── docker-compose.yml
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
