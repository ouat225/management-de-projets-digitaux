# src/functions/app_controller.py
import streamlit as st
from functions.data_viz import (
    load_data,
    plot_price_distribution,
    plot_surface_vs_price,
    get_average_price_by_citycode
)

def run_app():
    """Contrôle l'application Streamlit."""
    st.title("🏠 Analyse du marché immobilier à Paris")

    #Chargement des données
    df = load_data("data/ParisHousing.csv")

    #Choix du graphique / fonctionnalité
    st.sidebar.header("Paramètres")
    choice = st.sidebar.selectbox(
        "Que souhaitez-vous afficher ?",
        ("Distribution des prix", "Surface vs Prix", "Prix moyen par quartier")
    )

    #Afficher l'aperçu
    if choice != "Prix moyen par quartier": # ne pas l'afficher sur "prix moyen par quartier"
        st.write("### Aperçu des données")
        st.dataframe(df.head(), use_container_width=True)

    #AFFICHAGE SELON LE CHOIX
    
    if choice == "Distribution des prix":
        st.plotly_chart(plot_price_distribution(df), use_container_width=True)

    elif choice == "Surface vs Prix":
        st.plotly_chart(plot_surface_vs_price(df), use_container_width=True)

    elif choice == "Prix moyen par quartier":
        st.subheader("💶 Quartiers")

        if "cityCode" not in df.columns:
            st.warning("La colonne 'cityCode' est absente du dataset.")
        else:
            counts = df["cityCode"].value_counts()

            #Top 5 des cityCodes les plus fréquents
            st.write("### Top 5 des cityCodes les plus fréquents")
            top5 = counts.head(5).rename_axis("cityCode").reset_index(name="occurrences")
            st.dataframe(top5, use_container_width=True)

            # cityCode le plus fréquent
            if not counts.empty:
                top_city = int(counts.index[0])
                top_count = int(counts.iloc[0])
                st.info(f"🏙️ le cityCode le plus fréquent : **{top_city}** avec **{top_count}** occurrences")

            # Sélecteur du quartier + prix moyen
            codes = sorted(df["cityCode"].unique().tolist())
            sel = st.selectbox("Choisissez un quartier (cityCode)", options=[int(c) for c in codes])

            mean_price = get_average_price_by_citycode(df, int(sel))
            if mean_price is None:
                st.warning("Impossible de calculer le prix moyen pour ce quartier.")
            else:
                st.success(f"💰 Prix moyen pour le quartier {int(sel)} : **{mean_price:,.0f} €**.")
