from __future__ import annotations

import streamlit as st
import pandas as pd

from maison_estimateur.components.layout import section_title, divider
from maison_estimateur.data_processing.load_data import load_data
from maison_estimateur.analysis.pricing import (
    train_and_compare_models,
    train_random_forest_only,
)
from maison_estimateur.analysis.report_pdf import generate_estimation_report_pdf


@st.cache_resource
def get_trained_models(df: pd.DataFrame, feature_cols: list[str]):
    """
    Entraîne les modèles une seule fois et met le résultat en cache.

    Le cache est invalidé automatiquement si :
    - le DataFrame `df` change (contenu différent),
    - ou la liste `feature_cols` change.
    """
    return train_and_compare_models(df, feature_cols)


def render() -> None:
    st.title("🧮 Estimation du prix")

    # Chargement des données
    try:
        df = load_data()
    except Exception:
        st.error("Impossible de charger les données.")
        return

    # COMPARAISON DES MODÈLES
    st.subheader("📊 Comparaison des modèles")

    feature_cols = [
        "squareMeters",
        "numberOfRooms",
        "hasYard",
        "hasPool",
        "floors",
        "cityCode",
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
        results_df, models = get_trained_models(df, feature_cols)

    st.dataframe(results_df, use_container_width=True)

    # CHOIX DU MODÈLE
    st.subheader("🎯 Choix du modèle de prédiction")
    selected_model_name = st.selectbox(
        "Sélectionnez un modèle", list(models.keys())
    )

    # PARAMÈTRES UTILISATEUR
    st.subheader("📌 Paramètres")

    area = st.number_input(
        "Surface (m²)", min_value=10.0, max_value=300.0, value=80.0
    )
    rooms = st.slider("Nombre de pièces", 1, 10, 3)

    citycodes = sorted(df["cityCode"].dropna().unique())
    citycode = st.selectbox("Code ville", citycodes)

    # --- Estimation ---
    if st.button("💰 Estimer le prix"):
        input_data = pd.DataFrame(
            [
                {
                    "squareMeters": float(area),
                    "numberOfRooms": int(rooms),
                    "hasYard": 0,
                    "hasPool": 0,
                    "floors": 1,
                    "cityCode": citycode,
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
            if selected_model_name == "Random Forest":
                with st.spinner("Ré-entraînement du Random Forest..."):
                    selected_model = train_random_forest_only(df, feature_cols)
            else:
                selected_model = models[selected_model_name]

            price = float(selected_model.predict(input_data)[0])

            st.session_state["last_estimation"] = {
                "price": price,
                "model_name": selected_model_name,
                "features": input_data.iloc[0].to_dict(),
            }

            st.success(
                f"🏠 Prix estimé avec **{selected_model_name}** : **{price:,.0f} €**"
            )
        except Exception:
            st.error("Erreur lors de l'estimation du prix.")

    # --- Bouton PDF (affiché après une estimation) ---
    est = st.session_state.get("last_estimation")
    if est is not None:
        divider()
        section_title("📄 Rapport d’estimation")

        try:
            pdf_bytes = generate_estimation_report_pdf(
                df=df,
                features=est["features"],
                estimated_price=float(est["price"]),
                model_name=str(est["model_name"]),
            )

            st.download_button(
                label="📄 Télécharger le rapport (PDF)",
                data=pdf_bytes,
                file_name="rapport_estimation.pdf",
                mime="application/pdf",
                use_container_width=False,
            )
        except Exception:
            st.error("Impossible de générer le rapport PDF.")







