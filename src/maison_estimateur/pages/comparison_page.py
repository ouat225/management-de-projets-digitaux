from __future__ import annotations

import streamlit as st
import pandas as pd

from maison_estimateur.components.layout import section_title, divider
from maison_estimateur.components.widgets import property_inputs
from maison_estimateur.data_processing.load_data import load_data
from maison_estimateur.analysis.pricing import (
    train_and_compare_models,
    train_random_forest_only,
)


@st.cache_resource
def get_trained_models(df: pd.DataFrame, feature_cols: list[str]):
    """Entraîne les modèles une seule fois et met le résultat en cache."""
    return train_and_compare_models(df, feature_cols)


def _predict_price(
    df: pd.DataFrame,
    feature_cols: list[str],
    models: dict[str, object],
    selected_model_name: str,
    input_df: pd.DataFrame,
) -> float:
    """Prédit le prix selon le modèle choisi (gestion RF comme sur estimation_page)."""
    if selected_model_name == "Random Forest":
        with st.spinner("Ré-entraînement du Random Forest..."):
            model = train_random_forest_only(df, feature_cols)
    else:
        model = models[selected_model_name]

    return float(model.predict(input_df)[0])


def render() -> None:
    st.title("⚖️ Comparaison de deux biens")

    # Chargement des données
    try:
        df = load_data()
    except Exception:
        st.error("Impossible de charger les données.")
        return

    st.subheader("📊 Modèles disponibles (référence)")

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

    divider()

    st.subheader("🎯 Choix du modèle")
    selected_model_name = st.selectbox(
        "Sélectionnez un modèle", list(models.keys()), key="compare_model_select"
    )

    divider()

    section_title("🏠 Saisir les deux biens à comparer")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### Bien A")
        # ✅ Ici : Je ne sais pas autorisé
        input_A, meta_A = property_inputs(df, prefix="A", allow_unknown=True)

    with colB:
        st.markdown("### Bien B")
        # ✅ Ici : Je ne sais pas autorisé
        input_B, meta_B = property_inputs(df, prefix="B", allow_unknown=True)

    divider()

    if st.button("⚖️ Comparer", key="compare_button"):
        try:
            price_A = _predict_price(df, feature_cols, models, selected_model_name, input_A)
            price_B = _predict_price(df, feature_cols, models, selected_model_name, input_B)

            # Dérivés
            area_A = float(meta_A.get("squareMeters", 0.0))
            area_B = float(meta_B.get("squareMeters", 0.0))
            eur_m2_A = price_A / area_A if area_A > 0 else float("nan")
            eur_m2_B = price_B / area_B if area_B > 0 else float("nan")

            diff = price_B - price_A
            pct = (diff / price_A * 100.0) if price_A != 0 else float("nan")

            st.subheader("📌 Résultats (comparaison directe)")
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Prix estimé — Bien A", f"{price_A:,.0f} €")
            r2.metric("Prix estimé — Bien B", f"{price_B:,.0f} €")
            r3.metric("Écart (B − A)", f"{diff:,.0f} €")
            r4.metric("Écart (%)", f"{pct:,.2f} %")

            st.markdown("")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Surface — A", f"{area_A:,.0f} m²")
            c2.metric("Surface — B", f"{area_B:,.0f} m²")
            c3.metric("€/m² — A", f"{eur_m2_A:,.0f} €")
            c4.metric("€/m² — B", f"{eur_m2_B:,.0f} €")

        except Exception:
            st.error("Erreur lors de la comparaison. Vérifiez les paramètres et réessayez.")

