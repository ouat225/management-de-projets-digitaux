# src/functions/app_controller.py
import streamlit as st
import pandas as pd
from functions.data_viz import (
    load_data,
    plot_price_distribution,
    plot_surface_vs_price,
    get_average_price_by_citycode,
    generate_univariate_analysis
)

# --------- Configuration globale ----------
st.set_page_config(page_title="MAISONESTIMATEUR", page_icon="🏠", layout="wide")


def display_univariate_analysis(df: pd.DataFrame):
    """Affiche l'analyse univariée pour une variable sélectionnée."""
    st.header("🔍 Analyse univariée")
    
    # Sélection de la variable à analyser
    selected_var = st.selectbox(
        "Sélectionnez une variable à analyser",
        options=sorted(df.columns),
        index=0
    )
    
    # Génération de l'analyse
    try:
        analysis = generate_univariate_analysis(df, selected_var)
    except Exception as e:
        st.error(f"Erreur pendant l'analyse univariée : {e}")
        return
    
    if not isinstance(analysis, dict):
        st.warning("Le format retourné par generate_univariate_analysis n'est pas un dict.")
        return
    
    # Affichage des statistiques descriptives
    st.subheader(f"Statistiques descriptives - {selected_var}")
    a_type = analysis.get("type")
    stats = analysis.get("stats", {})

    if a_type == 'numeric':
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Moyenne", f"{stats.get('mean', float('nan')):,.2f}")
            st.metric("Médiane", f"{stats.get('median', float('nan')):,.2f}")
            st.metric("Écart-type", f"{stats.get('std', float('nan')):,.2f}")
        with col2:
            st.metric("Minimum", f"{stats.get('min', float('nan')):,.2f}")
            st.metric("25%", f"{stats.get('25%', float('nan')):,.2f}")
            st.metric("75%", f"{stats.get('75%', float('nan')):,.2f}")
        with col3:
            st.metric("Maximum", f"{stats.get('max', float('nan')):,.2f}")
            st.metric("Valeurs uniques", f"{analysis.get('unique_values', 0):,}")
            st.metric("Valeurs manquantes", f"{analysis.get('missing', 0):,}")
    elif a_type == 'categorical':
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Valeurs uniques", analysis.get('unique_values', 0))
            st.metric("Valeur la plus fréquente", stats.get('top', '—'))
        with col2:
            st.metric("Fréquence de la valeur la plus fréquente", stats.get('freq', '—'))
            st.metric("Valeurs manquantes", analysis.get('missing', 0))
    else:
        st.info("Type de variable non reconnu (attendu: 'numeric' ou 'categorical').")

    # Graphique
    fig = analysis.get("fig")
    if fig is not None:
        try:
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning("Le graphique retourné n'est pas compatible avec plotly_chart.")
    else:
        st.info("Pas de figure fournie pour cette analyse.")

    # Détail des effectifs (catégoriel)
    if a_type == 'categorical' and "value_counts" in analysis:
        st.subheader("Détail des effectifs")
        vc = analysis["value_counts"]
        try:
            if isinstance(vc, pd.Series):
                vc_df = (
                    vc.sort_values(ascending=False)
                      .rename_axis("Valeur")
                      .reset_index(name="Nombre")
                )
            elif isinstance(vc, pd.DataFrame):
                if set(vc.columns) >= {"Valeur", "Nombre"}:
                    vc_df = vc.sort_values("Nombre", ascending=False)
                else:
                    cols = list(vc.columns)
                    if len(cols) >= 2:
                        vc_df = vc[[cols[0], cols[1]]].copy()
                        vc_df.columns = ["Valeur", "Nombre"]
                        vc_df = vc_df.sort_values("Nombre", ascending=False)
                    else:
                        vc_df = vc.copy()
            else:
                vc_df = pd.DataFrame({"Valeur": list(vc), "Nombre": 1})
            st.dataframe(vc_df, use_container_width=True)
        except Exception as e:
            st.warning(f"Impossible d'afficher les effectifs : {e}")


def _topbar():
    """Barre supérieure avec titre et bouton Quitter."""
    left, mid, right = st.columns([6, 2, 2])
    with left:
        st.markdown("### 🏠 **MAISONESTIMATEUR**")
    with right:
        if st.button("Quitter", type="primary"):
            st.info("Application arrêtée. Merci d'avoir utilisé MAISONESTIMATEUR.")
            st.stop()


def _page_home():
    """Page d'accueil."""
    st.title("Bienvenue sur **MAISONESTIMATEUR**")
    st.write(
        """
        **MAISONESTIMATEUR** est un outil simple et rapide pour **estimer le prix de votre maison**
        à partir de données du marché et de statistiques descriptives.  
        Grâce à ce site, vous pourrez :
        - Explorer la **distribution des prix** et la relation **surface ↔ prix**,
        - Visualiser des **statistiques détaillées** sur vos variables,
        - (Bientôt) Obtenir une **estimation personnalisée** de votre bien 🏡.
        """
    )
    st.success("Commencez en cliquant sur l'onglet **Estimation** ou **Statistiques** ci-dessus.")


def _page_estimation():
    """Page Estimation (placeholder pour l’instant)."""
    st.title("🧮 Estimation")
    st.info("La fonctionnalité d’estimation arrive bientôt. Restez à l’écoute !")


def _page_stats():
    """Page Statistiques (tableau de bord + analyses univariées)."""
    st.title("📊 Statistiques")
    # Chargement des données
    try:
        df = load_data("data/ParisHousing.csv")
    except Exception as e:
        st.error(f"Impossible de charger les données : {e}")
        return

    # Sous-onglets internes à la page Stats
    tab_dash, tab_uni = st.tabs(["Tableau de bord", "Statistiques détaillées"])

    with tab_dash:
        # Sélecteur de visualisation
        choice = st.radio(
            "Que souhaitez-vous afficher ?",
            ("Distribution des prix", "Surface vs Prix", "Prix moyen par quartier"),
            horizontal=True,
        )

        # Aperçu des données (sauf pour 'Prix moyen par quartier' pour alléger)
        if choice != "Prix moyen par quartier":
            st.write("### Aperçu des données")
            st.dataframe(df.head(), use_container_width=True)

        if choice == "Distribution des prix":
            try:
                st.plotly_chart(plot_price_distribution(df), use_container_width=True)
            except Exception as e:
                st.error(f"Erreur lors de l'affichage de la distribution des prix : {e}")

        elif choice == "Surface vs Prix":
            try:
                st.plotly_chart(plot_surface_vs_price(df), use_container_width=True)
            except Exception as e:
                st.error(f"Erreur lors de l'affichage Surface vs Prix : {e}")

        elif choice == "Prix moyen par quartier":
            st.subheader("💶 Quartiers")
            if "cityCode" not in df.columns:
                st.warning("La colonne 'cityCode' est absente du dataset.")
            else:
                counts = df["cityCode"].value_counts(dropna=False)

                st.write("### Top 5 des cityCodes les plus fréquents")
                top5 = (
                    counts.head(5)
                          .rename_axis("cityCode")
                          .reset_index(name="occurrences")
                )
                top5["cityCode"] = top5["cityCode"].astype(str)
                st.dataframe(top5, use_container_width=True)

    with tab_uni:
        display_univariate_analysis(df)

        # Infos latérales sur cityCode (dans la page au lieu de la sidebar)
        if "cityCode" in df.columns:
            counts = df["cityCode"].value_counts(dropna=False)
            if not counts.empty:
                top_city = str(counts.index[0])
                top_count = int(counts.iloc[0])
                st.info(f"🏙️ Le cityCode le plus fréquent : **{top_city}** avec **{top_count}** occurrences")

            # Sélecteur du quartier + prix moyen
            codes = (
                df["cityCode"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
            codes = sorted(codes)
            if codes:
                sel = st.selectbox("Choisissez un quartier (cityCode)", options=codes, index=0)
                # Conversion souple pour le calcul
                sel_num = sel
                try:
                    sel_num = int(sel)
                except Exception:
                    try:
                        sel_num = float(sel)
                    except Exception:
                        pass

                try:
                    mean_price = get_average_price_by_citycode(df, sel_num)
                except Exception as e:
                    mean_price = None
                    st.warning(f"Erreur lors du calcul du prix moyen pour {sel} : {e}")

                if mean_price is None:
                    st.warning("Impossible de calculer le prix moyen pour ce quartier.")
                else:
                    st.metric("Prix moyen dans ce quartier", f"{mean_price:,.2f} €")
                    st.success(f"💰 Prix moyen pour le quartier {sel} : **{mean_price:,.0f} €**.")


def run_app():
    """Point d’entrée de l’application Streamlit, avec barre d’onglets."""
    _topbar()
    tabs = st.tabs(["🏠 Accueil", "🧮 Estimation", "📊 Statistiques"])
    with tabs[0]:
        _page_home()
    with tabs[1]:
        _page_estimation()
    with tabs[2]:
        _page_stats()
