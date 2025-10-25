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

def display_univariate_analysis(df):
    """Affiche l'analyse univariée pour une variable sélectionnée."""
    st.header("🔍 Analyse univariée")
    
    # Sélection de la variable à analyser
    selected_var = st.selectbox(
        "Sélectionnez une variable à analyser",
        options=sorted(df.columns),
        index=0
    )
    
    # Génération de l'analyse
    analysis = generate_univariate_analysis(df, selected_var)
    
    # Affichage des statistiques descriptives
    st.subheader(f"Statistiques descriptives - {selected_var}")
    
    if analysis["type"] == 'numeric':
        stats = analysis["stats"]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Moyenne", f"{stats['mean']:,.2f}")
            st.metric("Médiane", f"{stats['median']:,.2f}")
            st.metric("Écart-type", f"{stats['std']:,.2f}")
            
        with col2:
            st.metric("Minimum", f"{stats['min']:,.2f}")
            st.metric("25%", f"{stats['25%']:,.2f}")
            st.metric("75%", f"{stats['75%']:,.2f}")
            
        with col3:
            st.metric("Maximum", f"{stats['max']:,.2f}")
            st.metric("Valeurs uniques", f"{analysis['unique_values']:,}")
            st.metric("Valeurs manquantes", f"{analysis['missing']:,}")
    else:
        stats = analysis["stats"]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Valeurs uniques", analysis['unique_values'])
            st.metric("Valeur la plus fréquente", stats['top'])
            
        with col2:
            st.metric("Fréquence de la valeur la plus fréquente", stats['freq'])
            st.metric("Valeurs manquantes", analysis['missing'])
    
    # Affichage des graphiques
    st.plotly_chart(analysis["fig"], use_container_width=True)
    
    # Affichage du tableau des effectifs pour les variables catégorielles
    if analysis["type"] == 'categorical' and "value_counts" in analysis:
        st.subheader("Détail des effectifs")
        st.dataframe(
            pd.DataFrame(analysis["value_counts"]).sort_values("Nombre", ascending=False),
            use_container_width=True
        )

def run_app():
    """Contrôle l'application Streamlit."""
    st.title("🏠 Analyse du marché immobilier à Paris")

    # Chargement des données
    df = load_data("data/ParisHousing.csv")

    # Choix du graphique / fonctionnalité
    st.sidebar.header("Navigation")
    choice = st.sidebar.radio(
        "Que souhaitez-vous afficher ?",
        ("📊 Tableau de bord", "📈 Statistiques détaillées")
    )
    
    if choice == "📊 Tableau de bord":
        # Sous-menu pour les visualisations du tableau de bord
        dashboard_choice = st.sidebar.selectbox(
            "Visualisation",
            ("Distribution des prix", "Surface vs Prix", "Prix moyen par quartier")
        )
        
        # Afficher l'aperçu
        if dashboard_choice != "Prix moyen par quartier":  # ne pas l'afficher sur "prix moyen par quartier"
            st.write("### Aperçu des données")
            st.dataframe(df.head(), use_container_width=True)
        
        # AFFICHAGE SELON LE CHOIX
        if dashboard_choice == "Distribution des prix":
            st.plotly_chart(plot_price_distribution(df), use_container_width=True)
            
        elif dashboard_choice == "Surface vs Prix":
            st.plotly_chart(plot_surface_vs_price(df), use_container_width=True)
            
        elif dashboard_choice == "Prix moyen par quartier":
            st.subheader("💶 Quartiers")
            
            if "cityCode" not in df.columns:
                st.warning("La colonne 'cityCode' est absente du dataset.")
            else:
                counts = df["cityCode"].value_counts()
                
                # Top 5 des cityCodes les plus fréquents
                st.write("### Top 5 des cityCodes les plus fréquents")
                top5 = counts.head(5).rename_axis("cityCode").reset_index(name="occurrences")
                st.dataframe(top5, use_container_width=True)
    
    elif choice == "📈 Statistiques détaillées":
        display_univariate_analysis(df)
        
        # Afficher les informations sur le cityCode si la colonne existe
        if "cityCode" in df.columns:
            counts = df["cityCode"].value_counts()
            if not counts.empty:
                top_city = int(counts.index[0])
                top_count = int(counts.iloc[0])
                st.sidebar.info(f"🏙️ Le cityCode le plus fréquent : **{top_city}** avec **{top_count}** occurrences")

            # Sélecteur du quartier + prix moyen
            codes = sorted(df["cityCode"].unique().tolist())
            sel = st.sidebar.selectbox(
                "Choisissez un quartier (cityCode)", 
                options=[int(c) for c in codes],
                index=0
            )
            
            mean_price = get_average_price_by_citycode(df, int(sel))
            if mean_price is not None:
                st.sidebar.metric("Prix moyen dans ce quartier", f"{mean_price:,.2f} €")
            if mean_price is None:
                st.warning("Impossible de calculer le prix moyen pour ce quartier.")
            else:
                st.success(f"💰 Prix moyen pour le quartier {int(sel)} : **{mean_price:,.0f} €**.")
