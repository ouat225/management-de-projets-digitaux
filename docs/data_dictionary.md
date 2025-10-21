# 📘 DATA DICTIONARY – Paris Housing Dataset   
**Team:** Digital Project Management – M2SEP 2025-2026  

---

## 1️⃣ General overview of the dataset

- **File name:** `ParisHousing.csv`  
- **Size:** 10 000 observations – 13 variables  
- **Source:** *Paris Housing Price Prediction* dataset (Kaggle, author : Yasser H)  
  <https://www.kaggle.com/datasets/yasserh/housing-prices-dataset>  
- **Purpose:** Analyze the factors influencing housing prices in Paris and build an interactive analytics application to explore the market  
- **Unit of observation:** Individual housing unit
- **Period:** Synthetic (simulated data — not linked to a real period)  
- **Use in the project:** Core dataset for descriptive analysis (price distribution, surface-price relationship, average price by district).

---

## 2️⃣ Variable descriptions

| Variable name | Type | Unit / Possible values | Description | Example |
|----------------|------|------------------------|--------------|----------|
| `squareMeters` | float | m² | Living area of the property | 200 |
| `numberOfRooms` | int | — | Total number of rooms | 5 |
| `hasYard` | bool (0/1) | 0 = No ; 1 = Yes | Presence of a yard or garden | 1 |
| `hasPool` | bool (0/1) | 0 = No ; 1 = Yes | Indicates whether a pool is available | 0 |
| `floors` | int | — | Number of floors in the building | 2 |
| `cityCode` | int | — | Numeric district identifier | 9374 |
| `cityPartRange` | int | 1 – 10 | Internal code representing district category | 3 |
| `numPrevOwners` | int | — | Number of previous owners | 2 |
| `made` | int | Year | Year of construction | 2011 |
| `isNewBuilt` | bool (0/1) | 0 = No ; 1 = Yes | Indicates if the property is newly built | 0 |
| `hasStormProtector` | bool (0/1) | 0 = No ; 1 = Yes | Storm or weather protection | 1 |
| `basement` | int | m² | Basement surface area | 50 |
| `attic` | int | m² | Attic surface area | 25 |
| `garage` | int | — | Number of garages | 1 |
| `hasStorageRoom` | bool (0/1) | 0 = No ; 1 = Yes | Storage room availability | 1 |
| `hasGuestRoom` | bool (0/1) | 0 = No ; 1 = Yes | Guest room availability | 0 |
| `price` | float | € | Total property price | 1 200 000 € |

> 💡 Boolean columns (0/1) can be converted to Python `bool` type (`True/False`) for easier analysis

---

## 3️⃣ Data quality

- ✅ No missing values (`isna().sum() == 0`)  
- ✅ Consistent numeric ranges (e.g. `price > 0`, `squareMeters` between 15 and 350)  
- ✅ Homogeneous encoding (0/1 for all binary features) 
- ✅ Dataset is **synthetic**, not collected from real observations — used for educational and prototyping purposes only.  

---

## 4️⃣ Analytical relevance and role in the product

This dataset serves as the **core analytical component** of the project  
- Variables such as **`squareMeters`**, **`numberOfRooms`**, **`cityCode`**, and **`price`** are the main market indicators  
- Boolean variables enrich descriptive insights and allow testing hypotheses on property value (impact of a pool, garage, or yard)  
- Temporal variables like **`made`** and **`isNewBuilt`** introduce a construction-age dimension useful for assessing depreciation or building quality.  

---

## 5️⃣ Conclusion

This data dictionary ensures:  
- full **traceability** and **clarity** of the dataset for all team members;  
- compliance with **Sprint 1 Definition of Done** : “A dataset is built and documented within the report. Its source and field definitions are clearly described.”  
- a **solid foundation** for the next phases : statistical exploration, supervised-learning model integration, and visualization development.  

---

📄**Authors:**
This project was developed by 5 students from the “Statistique pour l'Evaluation et la Prévision” (SEP) master's program at the University of Reims Champagne-Ardenne (class of 2025-2026).
The contributors to this project are identified below :

- Oumar ALLAWAN
- Dimitri DELPECH
- Jean-Marc OUATTARA
- Simon MALHEY
- Dominique MUSITELLI 

