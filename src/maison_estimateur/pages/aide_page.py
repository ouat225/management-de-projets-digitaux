from __future__ import annotations

import pandas as pd
import streamlit as st


def render() -> None:
    st.markdown(
        """
        <div class="big-title">🆘 Aide & Documentation</div>
        <p class="subtitle">
            Cette page explique le fonctionnement des paramètres, les données utilisées,
            la logique d’estimation et les bons usages de l’application.
        </p>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["⚙️ Paramètres", "📦 Données", "🧠 Logique d’estimation", "✅ Bonnes pratiques"]
    )

    # =========================
    # TAB 1 — Paramètres
    # =========================
    with tab1:
        st.subheader("⚙️ Paramètres du bien")

        st.markdown(
            """
            Les informations saisies décrivent votre bien immobilier. Elles sont utilisées pour comparer votre bien
            à des biens similaires et produire une estimation cohérente avec les données disponibles.
            """
        )

        rows = [
            ("Surface (m²)", "Surface du bien en mètres carrés.", "Numérique"),
            ("Nombre de pièces", "Nombre total de pièces du logement.", "Numérique"),
            ("Arrondissement (1–20)", "Zone de Paris dans laquelle se situe le bien.", "Catégorie (1..20)"),
            ("Jardin", "Indique si le bien dispose d’un jardin.", "Oui / Non"),
            ("Piscine", "Indique si le bien dispose d’une piscine.", "Oui / Non"),
            ("Nombre d'étages", "Nombre d’étages associés au bien (selon la donnée).", "Numérique"),
            ("Propriétaires précédents", "Nombre de propriétaires précédents (historique).", "Numérique"),
            ("Année de construction", "Année de construction du bien.", "Numérique"),
            ("Neuf", "Indique si le bien est considéré comme neuf.", "Oui / Non"),
            ("Protection tempête", "Présence d’un dispositif de protection tempête.", "Oui / Non"),
            ("Sous-sol", "Présence d’un sous-sol.", "Oui / Non"),
            ("Grenier", "Présence d’un grenier.", "Oui / Non"),
            ("Garage", "Présence d’un garage.", "Oui / Non"),
            ("Cave / stockage", "Présence d’une pièce de stockage / cave.", "Oui / Non"),
            ("Chambre d'amis", "Présence d’une chambre d’amis.", "Oui / Non"),
        ]

        df_doc = pd.DataFrame(rows, columns=["Champ", "Description", "Type"])
        st.dataframe(df_doc, width="stretch")

        st.info(
            "💡 Conseil : pour une estimation plus fiable, utilise des valeurs réalistes et cohérentes "
            "(surface, pièces, année de construction, équipements)."
        )

    # =========================
    # TAB 2 — Données
    # =========================
    with tab2:
        st.subheader("📦 Sources de données & chargement")

        st.markdown(
            """
            L’application utilise le jeu de données public suivant :

            **Paris Housing Price Prediction (Kaggle)**  
            https://www.kaggle.com/datasets/mssmartypants/paris-housing-price-prediction

            Ce dataset regroupe des biens immobiliers situés à Paris, avec leur prix et leurs principales caractéristiques.
            """
        )

        with st.expander("🏘️ Que contiennent les données ?", expanded=False):
            st.markdown(
                """
                Les informations disponibles décrivent notamment :
                - le **prix du bien**,
                - la **surface**,
                - le **nombre de pièces**,
                - l’**arrondissement**,
                - l’**année de construction**,
                - la présence ou non de certains équipements (garage, jardin, cave, etc.).
                """
            )

        st.markdown("### 📊 À quoi servent ces données dans l’application ?")
        st.markdown(
            """
            Elles sont utilisées pour :
            - estimer le prix d’un bien à partir de biens similaires,
            - comparer plusieurs logements entre eux,
            - afficher des statistiques (répartition des prix, relations entre critères et prix).
            """
        )

        st.warning(
            "⚠️ Si les données ne se chargent pas correctement, l’estimation, la comparaison et certaines statistiques "
            "peuvent ne pas fonctionner."
        )

    # =========================
    # TAB 3 — Logique d’estimation
    # =========================
    with tab3:
        st.subheader("🧠 Comment le prix est estimé ?")

        st.markdown(
            """
            L’application estime le prix d’un bien immobilier à partir de biens similaires situés à Paris,
            en analysant leurs caractéristiques et leurs prix.

            Elle utilise des méthodes statistiques et d’apprentissage automatique pour identifier des tendances
            et proposer une estimation cohérente avec les données disponibles.
            """
        )

        st.markdown("### 🔍 Étapes de l’estimation (simplifiées)")
        st.markdown(
            """
            1. **Analyse des données immobilières parisiennes**  
               L’application s’appuie sur un ensemble de biens avec leurs caractéristiques et leurs prix.

            2. **Apprentissage des relations prix ↔ caractéristiques**  
               Elle étudie comment la surface, le nombre de pièces, l’arrondissement, l’année de construction
               et les équipements influencent le prix.

            3. **Sélection de la méthode la plus fiable**  
               Plusieurs approches sont évaluées automatiquement pour retenir celle qui donne les estimations
               les plus précises sur les données disponibles.

            4. **Estimation de votre bien**  
               Les informations que vous saisissez sont comparées aux biens existants afin de produire une estimation.
            """
        )

        st.info(
            "ℹ️ À savoir : cette estimation est un indicateur basé sur des tendances observées dans les données, "
            "et ne remplace pas une expertise notariale ou une estimation professionnelle."
        )

    # =========================
    # TAB 4 — Bonnes pratiques
    # =========================
    with tab4:
        st.subheader("✅ Bons usages & limites")

        st.markdown(
            """
            **Bonnes pratiques**
            - Saisir des valeurs réalistes (surface, année, pièces).
            - Tester plusieurs scénarios (avec/sans équipements) pour comprendre l’impact.
            - Utiliser les statistiques pour mieux interpréter le résultat.

            **Limites**
            - L’estimation dépend de la qualité et du contenu du dataset utilisé.
            - Les biens atypiques peuvent être moins bien estimés (très haut standing, caractéristiques rares, etc.).
            - Certains critères importants ne sont pas présents (état du bien, vue, travaux, étage exact, etc.).
            """
        )

        st.success("✅ Astuce : si le résultat semble incohérent, vérifie d’abord l’arrondissement et la surface.")
