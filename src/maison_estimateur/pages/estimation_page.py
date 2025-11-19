# src/maison_estimateur/pages/estimation_page.py
from __future__ import annotations
import streamlit as st
import pandas as pd

from maison_estimateur.components.layout import section_title, divider
from maison_estimateur.data_processing.load_data import load_data
from maison_estimateur.analysis.estimation import estimate_price

def render():

    st.title("🧮 Estimation du prix")

    try:
        df = load_data()
    except:
        st.error("Impossible de charger les données.")
        return

    st.subheader("📌 Paramètres")

    area = st.number_input("Surface (m²)", min_value=10.0, max_value=300.0, value=80.0)
    citypart = st.slider("Prestige du quartier (1–10)", 1, 10, 5)
    rooms = st.slider("Nombre de pièces", 1, 10, 3)

    citycodes = sorted(df["cityCode"].unique())
    citycode = st.selectbox("Code ville", citycodes)

    if st.button("💰 Estimer le prix"):
        price = estimate_price(df, area, citypart, rooms, citycode)

        if price is None:
            st.error("Erreur dans l'estimation.")
        else:
            st.success(f"🏠 Prix estimé : **{price:,.0f} €**")
