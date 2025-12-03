# src/maison_estimateur/pages/estimation_page.py
from __future__ import annotations

import pandas as pd
import streamlit as st

from maison_estimateur.components.layout import section_title, divider
from maison_estimateur.data_processing.load_data import load_data
from maison_estimateur.analysis.estimation import estimate_price


def _build_insights(
    df: pd.DataFrame,
    price: float,
    area: float,
    citypart: int,
    rooms: int,
    citycode,
):
    """Construit quelques phrases d'insight 'à la MeilleursAgents'."""
    insights = []

    # Comparaison à la médiane de la ville
    if "price" in df.columns and "cityCode" in df.columns:
        city_df = df[df["cityCode"] == citycode]
        if not city_df.empty:
            median_city = city_df["price"].median()
            if median_city > 0:
                diff = (price - median_city) / median_city * 100
                direction = "plus cher" if diff > 0 else "moins cher"
                insights.append(
                    f"Le prix estimé est environ **{abs(diff):.1f}% {direction}** "
                    f"que la médiane des biens pour le code ville `{citycode}`."
                )

    # Position dans la distribution globale
    if "price" in df.columns:
        percentile = (df["price"] < price).mean() * 100
        insights.append(
            f"Ce bien se situe autour du **{percentile:.1f}ᵉ percentile** des prix du dataset."
        )

    # Taille du bien
    if "area" in df.columns:
        median_area = df["area"].median()
        if median_area > 0:
            diff_area = (area - median_area) / median_area * 100
            direction = "plus grand" if diff_area > 0 else "plus petit"
            insights.append(
                f"Avec **{area:.0f} m²**, le bien est environ **{abs(diff_area):.1f}% {direction}** "
                "que la surface médiane du dataset."
            )

    # Prestige du quartier
    insights.append(
        f"Le prestige de quartier choisi est **{citypart}/10**, "
        "ce qui impacte fortement l’estimation finale."
    )

    return insights


def render():

    st.markdown(
        """
        <div class="big-title">🧮 Estimation du prix</div>
        <p class="subtitle">
            Renseignez les caractéristiques principales de votre bien pour obtenir
            une estimation basée sur les données du marché parisien.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Chargement des données
    try:
        df = load_data()
    except Exception:
        st.error("Impossible de charger les données nécessaires à l'estimation.")
        return

    col_form, col_side = st.columns([2.0, 1.6])

    # ---------- COLONNE FORMULAIRE ----------
    with col_form:
        st.markdown('<div class="params-panel">', unsafe_allow_html=True)
        section_title("📌 Paramètres du bien")

        area = st.number_input(
            "Surface (m²)",
            min_value=10.0,
            max_value=300.0,
            value=80.0,
            help="Surface habitable approximative en mètres carrés.",
        )
        citypart = st.slider(
            "Prestige du quartier (1–10)",
            1,
            10,
            5,
            help="1 = quartier peu recherché, 10 = quartier très prestigieux.",
        )
        rooms = st.slider(
            "Nombre de pièces",
            1,
            10,
            3,
            help="Nombre de pièces principales (hors cuisine, salle de bain, etc.).",
        )

        citycodes = sorted(df["cityCode"].unique()) if "cityCode" in df.columns else []
        citycode = st.selectbox(
            "Code ville",
            citycodes,
            help="Code correspondant à la zone / commune dans le dataset.",
        )

        estimate_clicked = st.button("💰 Estimer le prix")
        st.markdown("</div>", unsafe_allow_html=True)

        if estimate_clicked:
            price = estimate_price(df, area, citypart, rooms, citycode)

            if price is None:
                st.error("Erreur dans l'estimation.")
            else:
                divider()
                st.markdown(
                    f"""
                    <div class="card">
                        <h4>Résultat de l’estimation</h4>
                        <p style="font-size:1.4rem; margin-top:0.4rem;">
                            🏠 Prix estimé : <strong>{price:,.0f} €</strong>
                        </p>
                        <p style="font-size:0.9rem; opacity:0.9;">
                            Cette estimation reste indicative et dépend des données disponibles dans le dataset.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Insights automatiques
                insights = _build_insights(df, price, area, citypart, rooms, citycode)
                if insights:
                    st.markdown(
                        """
                        <div class="card">
                            <h4>🔎 Comment lire ce résultat ?</h4>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    for txt in insights:
                        st.markdown(f"- {txt}")

    # ---------- COLONNE DROITE ----------
    with col_side:
        st.markdown(
            """
            <div class="card">
                <h4>💡 Conseils d’utilisation</h4>
                <ul>
                    <li>Renseignez des valeurs réalistes et cohérentes pour approcher au mieux le marché réel.</li>
                    <li>Testez plusieurs scénarios (surface, prestige, pièces) pour voir l’impact sur le prix.</li>
                    <li>Comparez ensuite avec les statistiques détaillées de l’onglet <strong>📊 Statistiques</strong>.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="card">
                <h4>📊 D’où viennent les données ?</h4>
                <p>
                    Les estimations sont basées sur un jeu de données de ventes immobilières parisiennes :
                    prix, surface, caractéristiques du logement, code ville, etc.
                </p>
                <p style="font-size:0.85rem; opacity:0.9;">
                    Ces données sont utilisées pour entraîner un modèle de régression qui sert à produire l’estimation ci-dessus.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
