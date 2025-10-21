# PARIS HOUSING INSIGHTS 

Your Paris Real Estate Analysis Tool

## Overview

This project provides a comprehensive analysis of the Parisian real estate market using a dataset of 10,000 properties. The tool allows you to visualize and analyze market trends, and explore relationships between different property features.

## Features

- **Price Analysis**: Visualize price distribution by district
- **Feature Comparison**: Explore how different features influence prices
- **Advanced Filters**: Refine your search based on specific criteria
- **Interactive Visualizations**: Charts and maps for better data understanding

## Prerequisites

- Python 3.8+
- Python libraries listed in `requirements.txt`
- Streamlit (will be installed via dependencies)

## Installation and Usage

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

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit application**
   From the project root, run:
   ```bash
   streamlit run src/main.py
   ```

5. **Using the application**
   - The application will automatically open in your default browser
   - Use the sidebar to select different visualizations
   - Explore Parisian housing data interactively

## Project Structure

```
management-de-projets-digitaux/
├── data/
│   └── ParisHousing.csv         # Main Paris housing dataset
├── docs/                        # Additional documentation
├── src/
│   ├── functions/              
│   │   ├── app_controller.py   # Main application controller
│   │   └── data_viz.py         # Data visualization functions
│   └── main.py                 # Application entry point
├── test/                       # Unit and integration tests
├── .gitignore                  # Git ignore file
├── README.md                   # This file
└── requirements.txt            # Project dependencies
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
