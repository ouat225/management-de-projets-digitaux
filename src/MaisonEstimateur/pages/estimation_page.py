# src/MaisonEstimateur/pages/estimation_page.py
from __future__ import annotations
import streamlit as st
import pandas as pd
from MaisonEstimateur.components.layout import section_title, divider
from MaisonEstimateur.data_processing.load_data import load_data
from MaisonEstimateur.analysis.estimation import estimate_price_rule


def render() -> None:
    section_title("🧮 Estimation")

    st.info("Renseignez les caractéristiques de votre logement pour obtenir une estimation du prix moyen.")

    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Fichier de données introuvable. Veuillez vérifier data/ParisHousing.csv.")
        return

    # --- Sélecteurs utilisateur ---
    if "cityPartRange" not in df.columns:
        st.error("La colonne 'cityPartRange' est absente du dataset.")
        return

    citypart_values = sorted(df["cityPartRange"].dropna().astype(int).unique().tolist())
    selected_citypart = st.selectbox("Valeur de cityPartRange (1 à 10)", citypart_values)

    col1, col2, col3 = st.columns(3)
    with col1:
        area = st.number_input("Surface (m²)", min_value=10, max_value=500, value=60)
    with col2:
        rooms = st.number_input("Nombre de pièces", min_value=1, max_value=10, value=3)
    with col3:
        has_garden = st.selectbox("Jardin", ["Oui", "Non"]) == "Oui"

    divider()

    if st.button("💰 Estimer le prix", type="primary"):
        estimated_price = estimate_price_rule(
            df=df,
            citypart=selected_citypart,
            area=area,
            rooms=rooms,
            has_garden=has_garden
        )

        if estimated_price is None:
            st.warning("Impossible de calculer une estimation pour cette valeur de cityPartRange.")
        else:
            st.success(f"🏠 Prix estimé : **{estimated_price:,.0f} €**")

    st.caption("⚙️ Estimation simplifiée basée sur les données du dataset.")
