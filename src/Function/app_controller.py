# src/functions/app_controller.py
import streamlit as st

from Function.data_viz import (
    load_data,
    plot_price_distribution,
    plot_surface_vs_price,
    get_average_price_by_citycode
)

def run_app():
    """Contrôle l'application Streamlit."""
    st.title("🏠 Analyse du marché immobilier à Paris")

    # Chargement des données
    df = load_data("data/ParisHousing.csv")

    st.write("### Aperçu des données")
    st.dataframe(df.head())

    # Choix du graphique / fonctionnalité
    st.sidebar.header("Paramètres")
    choice = st.sidebar.selectbox(
        "Que souhaitez-vous afficher ?",
        ("Distribution des prix", "Surface vs Prix", "Prix moyen par quartier")
    )

    # Affichage
    if choice == "Distribution des prix":
        st.plotly_chart(plot_price_distribution(df))

    elif choice == "Surface vs Prix":
        st.plotly_chart(plot_surface_vs_price(df))

    elif choice == "Prix moyen par quartier":
        st.subheader("💶 Calcul du prix moyen par quartier")

        # Champ de saisie du cityCode
        city_code = st.number_input("Entrez le code du quartier (cityCode)", min_value=0, step=1)

        if city_code:
            mean_price = get_average_price_by_citycode(df, city_code)
            if mean_price is None:
                st.warning("⚠️ Ce code de quartier n'existe pas dans la base de données.")
            else:
                st.success(f"💰 Le prix moyen des logements pour le quartier {int(city_code)} est de **{mean_price:,.0f} €**.")
