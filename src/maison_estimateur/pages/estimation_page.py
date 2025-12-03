# src/maison_estimateur/pages/estimation_page.py
from __future__ import annotations
import streamlit as st
import pandas as pd

from maison_estimateur.components.layout import section_title, divider
from maison_estimateur.data_processing.load_data import load_data
from maison_estimateur.analysis.pricing import train_and_compare_models


def render() -> None:
    st.title("🧮 Estimation du prix")

    # Chargement des données
    try:
        df = load_data()
    except Exception:
        st.error("Impossible de charger les données.")
        return

    # --- COMPARAISON DES MODELES ---
    st.subheader("📊 Comparaison des modèles")

    feature_cols = [
        "squareMeters",
        "numberOfRooms",
        "hasYard",
        "hasPool",
        "floors",
        "cityCode",
        "cityPartRange",
        "numPrevOwners",
        "made",
        "isNewBuilt",
        "hasStormProtector",
        "basement",
        "attic",
        "garage",
        "hasStorageRoom",
        "hasGuestRoom",
    ]

    with st.spinner("Entraînement des modèles..."):
        results_df, models = train_and_compare_models(df, feature_cols)

    st.dataframe(results_df, use_container_width=True)

    # Choix du modèle pour l'estimation
    st.subheader("🎯 Choix du modèle de prédiction")
    selected_model_name = st.selectbox(
        "Sélectionnez un modèle", list(models.keys())
    )
    selected_model = models[selected_model_name]

    # --- PARAMETRES UTILISATEUR ---
    st.subheader("📌 Paramètres")

    area = st.number_input("Surface (m²)", min_value=10.0, max_value=300.0, value=80.0)
    citypart = st.slider("Prestige du quartier (1–10)", 1, 10, 5)
    rooms = st.slider("Nombre de pièces", 1, 10, 3)

    citycodes = sorted(df["cityCode"].unique())
    citycode = st.selectbox("Code ville", citycodes)

    if st.button("💰 Estimer le prix"):
        # Construction de l'observation à prédire
        input_data = pd.DataFrame(
            [
                {
                    "squareMeters": area,
                    "numberOfRooms": rooms,
                    "hasYard": 0,
                    "hasPool": 0,
                    "floors": 1,
                    "cityCode": citycode,
                    "cityPartRange": citypart,
                    "numPrevOwners": 1,
                    "made": 2000,
                    "isNewBuilt": 0,
                    "hasStormProtector": 0,
                    "basement": 0,
                    "attic": 0,
                    "garage": 0,
                    "hasStorageRoom": 0,
                    "hasGuestRoom": 0,
                }
            ]
        )

        try:
            price = float(selected_model.predict(input_data)[0])
            st.success(
                f"🏠 Prix estimé avec **{selected_model_name}** : **{price:,.0f} €**"
            )
        except Exception:
            st.error("Erreur lors de l'estimation du prix.")
