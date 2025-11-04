# src/MaisonEstimateur/pages/estimation_page.py
from __future__ import annotations
import streamlit as st
import pandas as pd
from MaisonEstimateur.components.layout import section_title, divider
from MaisonEstimateur.data_processing.load_data import load_data
from MaisonEstimateur.analysis.pricing import get_average_price_by_citycode

def render() -> None:
    """Page Estimation - saisie des caractéristiques du logement."""
    section_title("🧮 Estimation")

    st.info("Renseignez les caractéristiques de votre logement pour obtenir une estimation du prix moyen.")

    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Fichier de données introuvable. Veuillez vérifier data/ParisHousing.csv.")
        return

    # --- Sélecteurs utilisateur ---
    city_codes = sorted(df["cityCode"].dropna().astype(str).unique().tolist())
    selected_city = st.selectbox("🏙️ Choisissez un quartier (cityCode)", city_codes)

    col1, col2, col3 = st.columns(3)
    with col1:
        area = st.number_input("Surface (m²)", min_value=10, max_value=500, value=60)
    with col2:
        rooms = st.number_input("Nombre de pièces", min_value=1, max_value=10, value=3)
    with col3:
        garden = st.selectbox("Jardin", ["Oui", "Non"])

    divider()

    if st.button("💰 Estimer le prix", type="primary"):
        # Calcul du prix moyen selon le cityCode
        mean_price = get_average_price_by_citycode(df, selected_city)
        if mean_price is None:
            st.warning("Impossible de calculer une estimation pour cette zone.")
        else:
            # Ajustement simple selon quelques variables
            coeff_surface = 1 + (area - 60) / 400
            coeff_rooms = 1 + (rooms - 3) * 0.05
            coeff_garden = 1.10 if garden == "Oui" else 1.0
            estimated_price = mean_price * coeff_surface * coeff_rooms * coeff_garden

            st.success(
                f"🏠 Prix estimé : **{estimated_price:,.0f} €**\n\n"
                f"*(Prix moyen du quartier : {mean_price:,.0f} €)*"
            )

    st.caption("⚙️ Estimation simplifiée basée sur la moyenne par quartier (version prototype).")
