import streamlit as st


def render():
    """Page d'accueil."""

    # Bandeau haut (optionnel, juste visuel)
    st.markdown('<div class="banner"></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2.2, 1.8])

    # --------- COLONNE GAUCHE : HERO ---------
    with col_left:
        st.markdown(
            """
            <div class="pill">Estimation immobilière à Paris</div>
            <h1 class="big-title">MAISONESTIMATEUR 🏠</h1>
            <p class="subtitle">
                MAISONESTIMATEUR vous aide à estimer rapidement le <strong>prix de votre maison à Paris</strong>
                à partir de données du marché parisien et d’analyses statistiques.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="card">
                <ul>
                    <li>Obtenez une <strong>estimation personnalisée</strong> en renseignant quelques caractéristiques de votre bien.</li>
                    <li>Explorez des <strong>statistiques descriptives</strong> sur les variables du dataset.</li>
                    <li>Visualisez les relations entre les variables et le <code>price</code>.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="info-band">
                🧭 <strong>Commencez par l’onglet</strong> <em>🧮 Estimation</em> pour simuler le prix de votre bien,
                ou rendez-vous dans <em>📊 Statistiques</em> pour explorer les données.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------- COLONNE DROITE : IMAGE + TEXTE ---------
    with col_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        # Image externe (pas besoin de fichier local)
        st.image(
            "https://images.unsplash.com/photo-1499856871958-5b9627545d1a"
            "?auto=format&fit=crop&w=1200&q=80",
            caption="Immeubles résidentiels à Paris",
            use_container_width=True,
        )

        st.markdown(
            """
            <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.6rem;">
                Les estimations sont calculées à partir d’un jeu de données de biens immobiliers
                parisiens (surface, quartier, nombre de pièces, etc.), puis modélisées statistiquement.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)
