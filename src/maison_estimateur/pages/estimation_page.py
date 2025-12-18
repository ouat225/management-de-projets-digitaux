from __future__ import annotations

import pandas as pd
import streamlit as st

from maison_estimateur.analysis.pricing import train_and_compare_models
from maison_estimateur.analysis.report_pdf import generate_estimation_report_pdf
from maison_estimateur.components.layout import divider, section_title
from maison_estimateur.components.widgets import property_inputs
from maison_estimateur.data_processing.load_data import load_data


@st.cache_data(show_spinner=False)
def get_model_comparison(df: pd.DataFrame, feature_cols: list[str]):
    """Compare les modèles (split + métriques) et cache les résultats."""
    return train_and_compare_models(df, feature_cols)


def _pick_best_model(
    results_df: pd.DataFrame, models: dict[str, object]
) -> tuple[str, object] | tuple[None, None]:
    """
    Sélection auto du meilleur modèle.

    Hypothèse (pricing.py) :
    - results_df est trié par RMSE croissant (le meilleur est en ligne 0)
    - results_df contient une colonne 'model'
    """
    if results_df is None or results_df.empty or not models:
        return None, None

    if "model" not in results_df.columns:
        return None, None

    best_name = str(results_df.iloc[0]["model"])
    best_model = models.get(best_name)

    if best_model is None:
        return None, None

    return best_name, best_model


def render() -> None:
    st.title("🧮 Estimation du prix")

    # Chargement des données
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Impossible de charger les données : {e}")
        return

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

    # =========================
    # Modèle auto
    # =========================
    st.subheader("🤖 Modèle de prédiction (auto)")

    with st.spinner("Préparation du modèle..."):
        results_df, models = get_model_comparison(df, feature_cols)

    if results_df is None or results_df.empty or not models:
        st.error("Impossible de comparer les modèles (résultats vides).")
        return

    best_name, best_model = _pick_best_model(results_df, models)
    if best_model is None:
        st.error("Impossible de sélectionner automatiquement un modèle.")
        return

    # Message user-friendly (sans “RMSE minimal”)
    st.info("Nous sélectionnons automatiquement le modèle le plus précis sur des données de test.")
    st.caption("*(critère : erreur moyenne la plus faible)*")
    st.caption(f"Modèle retenu : **{best_name}**")

    # Détails optionnels
    with st.expander("Voir les détails de comparaison (optionnel)", expanded=False):
        st.dataframe(results_df, width="stretch")

    divider()
    st.subheader("📌 Paramètres du bien")

    # Tous les champs, Oui/Non seulement
    input_data, _meta = property_inputs(df, prefix="EST", allow_unknown=False)

    # =========================
    # Estimation
    # =========================
    if st.button("💰 Estimer le prix", key="est_button"):
        try:
            price = float(best_model.predict(input_data)[0])

            st.session_state["last_estimation"] = {
                "price": price,
                "model_name": best_name,
                "features": input_data.iloc[0].to_dict(),
            }

            st.success(f"🏠 Prix estimé : **{price:,.0f} €**")
        except Exception as e:
            st.error(f"Erreur lors de l'estimation du prix : {e}")

    # =========================
    # Rapport PDF
    # =========================
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
                key="download_report_pdf",
            )
        except Exception as e:
            st.error(f"Impossible de générer le rapport PDF : {e}")
