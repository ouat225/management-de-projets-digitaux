from __future__ import annotations

import streamlit as st
import pandas as pd
from typing import Optional, Union, Any, Dict, Tuple


def data_head(df: pd.DataFrame, rows: int = 5, expanded: bool = False, title: str = "Aperçu des données (head)") -> None:
    """Affiche un aperçu des premières lignes dans un expander."""
    with st.expander(title, expanded=expanded):
        st.dataframe(df.head(rows), use_container_width=True)


def plot_figure(fig) -> None:
    """Affiche une figure Plotly en pleine largeur avec gestion d'erreurs douce."""
    if fig is None:
        st.info("Pas de figure à afficher.")
        return
    try:
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.warning("Le graphique fourni n'est pas compatible avec plotly_chart.")


def stats_metrics_numeric(stats: dict, analysis: dict) -> None:
    """Affiche les métriques pour variable numérique (3 colonnes)."""
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


def stats_metrics_categorical(stats: dict, analysis: dict) -> None:
    """Affiche les métriques pour variable catégorielle (2 colonnes)."""
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Valeurs uniques", analysis.get('unique_values', 0))
        st.metric("Valeur la plus fréquente", stats.get('top', '—'))
    with col2:
        st.metric("Fréquence (valeur la plus fréquente)", stats.get('freq', '—'))
        st.metric("Valeurs manquantes", analysis.get('missing', 0))


def value_counts_table(vc: Union[pd.Series, pd.DataFrame, list, dict]) -> None:
    """Affiche le tableau des effectifs d'une variable catégorielle."""
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
            # list/dict → DataFrame par défaut
            vc_df = pd.DataFrame(vc)
            if list(vc_df.columns)[:2] != ["Valeur", "Nombre"]:
                vc_df.columns = ["Valeur", "Nombre"][: len(vc_df.columns)]
        st.dataframe(vc_df, use_container_width=True)
    except Exception as e:
        st.warning(f"Impossible d'afficher les effectifs : {e}")


def citycode_selector_and_metric(
    df: pd.DataFrame,
    get_mean_fn,
    select_label: str = "Choisissez un quartier (cityCode)"
) -> None:
    """
    Sélecteur de cityCode (en str) + affiche la métrique du prix moyen.
    get_mean_fn: fonction (df, city_code) -> float | None
    """
    if "cityCode" not in df.columns:
        return

    counts = df["cityCode"].value_counts(dropna=False)
    if not counts.empty:
        top_city = str(counts.index[0])
        top_count = int(counts.iloc[0])
        st.info(f"🏙️ Le cityCode le plus fréquent : **{top_city}** avec **{top_count}** occurrences")

    codes = sorted(df["cityCode"].dropna().astype(str).unique().tolist())
    if not codes:
        return

    sel = st.selectbox(select_label, options=codes, index=0, key="citycode_selector")

    try:
        mean_price = get_mean_fn(df, sel)
    except Exception as e:
        mean_price = None
        st.warning(f"Erreur lors du calcul du prix moyen pour {sel} : {e}")

    if mean_price is None:
        st.warning("Impossible de calculer le prix moyen pour ce quartier.")
    else:
        st.metric("Prix moyen dans ce quartier", f"{mean_price:,.2f} €")
        st.success(f"💰 Prix moyen pour le quartier {sel} : **{mean_price:,.0f} €**.")


# ==========================================================
# ✅ INPUTS BIEN IMMOBILIER (Estimation & Comparaison)
# - Estimation : allow_unknown=False  -> Oui/Non
# - Comparaison: allow_unknown=True   -> Oui/Non/Je ne sais pas
# ==========================================================

def _mode_binary(df: pd.DataFrame, col: str, fallback: int = 0) -> int:
    """Renvoie la valeur la plus fréquente (0/1) pour une colonne binaire."""
    try:
        if col not in df.columns:
            return fallback
        s = df[col].dropna()
        if s.empty:
            return fallback
        return int(s.mode().iloc[0])
    except Exception:
        return fallback


def _yn_selector(label: str, key: str, allow_unknown: bool, default: int = 0) -> str:
    """
    Renvoie le choix texte ("Oui"/"Non"/"Je ne sais pas").
    default: 0 -> Non, 1 -> Oui (sert uniquement à choisir l'index)
    """
    if allow_unknown:
        options = ["Je ne sais pas", "Non", "Oui"]
        return st.selectbox(label, options, index=0, key=key)
    else:
        options = ["Non", "Oui"]
        idx = 1 if int(default) == 1 else 0
        return st.selectbox(label, options, index=idx, key=key)


def _yn_to_value(choice: str, df: pd.DataFrame, col: str, allow_unknown: bool) -> int:
    """
    Convertit le choix texte en 0/1.
    Si 'Je ne sais pas', on remplace par la valeur la plus fréquente du dataset
    pour rester robuste (modèle sklearn ne gère pas NaN ici).
    """
    if allow_unknown and choice == "Je ne sais pas":
        return _mode_binary(df, col, fallback=0)
    return 1 if choice == "Oui" else 0


def property_inputs(
    df: pd.DataFrame,
    prefix: str = "A",
    allow_unknown: bool = False,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Bloc de saisie standardisé pour un bien immobilier.

    Retourne:
      - input_df: pd.DataFrame avec les colonnes attendues par le modèle
      - meta: dict (valeurs finales utilisées pour la prédiction)
    """
    # Champs principaux
    area = st.number_input(
        "Surface (m²)",
        min_value=10.0,
        max_value=300.0,
        value=80.0,
        key=f"{prefix}_area",
    )
    rooms = st.slider(
        "Nombre de pièces",
        min_value=1,
        max_value=10,
        value=3,
        key=f"{prefix}_rooms",
    )

    citycodes = sorted(df["cityCode"].dropna().unique()) if "cityCode" in df.columns else []
    citycode = st.selectbox(
        "Code ville",
        options=citycodes if citycodes else [0],
        index=0,
        key=f"{prefix}_citycode",
    )

    # Options avancées
    with st.expander("Options avancées", expanded=False):
        # Valeurs par défaut (pour Estimation) : mode dataset
        default_yard = _mode_binary(df, "hasYard", 0)
        default_pool = _mode_binary(df, "hasPool", 0)
        default_storm = _mode_binary(df, "hasStormProtector", 0)
        default_basement = _mode_binary(df, "basement", 0)
        default_attic = _mode_binary(df, "attic", 0)
        default_garage = _mode_binary(df, "garage", 0)
        default_storage = _mode_binary(df, "hasStorageRoom", 0)
        default_guest = _mode_binary(df, "hasGuestRoom", 0)
        default_new = _mode_binary(df, "isNewBuilt", 0)

        ch_yard = _yn_selector("Jardin", key=f"{prefix}_hasYard", allow_unknown=allow_unknown, default=default_yard)
        ch_pool = _yn_selector("Piscine", key=f"{prefix}_hasPool", allow_unknown=allow_unknown, default=default_pool)

        floors = st.slider("Nombre d'étages", 1, 5, 1, key=f"{prefix}_floors")
        numPrevOwners = st.slider("Nombre de propriétaires précédents", 0, 5, 1, key=f"{prefix}_numPrevOwners")
        made = st.slider("Année de construction", 1900, 2025, 2000, key=f"{prefix}_made")

        ch_new = _yn_selector("Neuf", key=f"{prefix}_isNewBuilt", allow_unknown=allow_unknown, default=default_new)
        ch_storm = _yn_selector("Protection tempête", key=f"{prefix}_hasStormProtector", allow_unknown=allow_unknown, default=default_storm)
        ch_basement = _yn_selector("Sous-sol", key=f"{prefix}_basement", allow_unknown=allow_unknown, default=default_basement)
        ch_attic = _yn_selector("Grenier", key=f"{prefix}_attic", allow_unknown=allow_unknown, default=default_attic)
        ch_garage = _yn_selector("Garage", key=f"{prefix}_garage", allow_unknown=allow_unknown, default=default_garage)
        ch_storage = _yn_selector("Cave/Stockage", key=f"{prefix}_hasStorageRoom", allow_unknown=allow_unknown, default=default_storage)
        ch_guest = _yn_selector("Chambre d'amis", key=f"{prefix}_hasGuestRoom", allow_unknown=allow_unknown, default=default_guest)

        hasYard = _yn_to_value(ch_yard, df, "hasYard", allow_unknown)
        hasPool = _yn_to_value(ch_pool, df, "hasPool", allow_unknown)
        isNewBuilt = _yn_to_value(ch_new, df, "isNewBuilt", allow_unknown)
        hasStormProtector = _yn_to_value(ch_storm, df, "hasStormProtector", allow_unknown)
        basement = _yn_to_value(ch_basement, df, "basement", allow_unknown)
        attic = _yn_to_value(ch_attic, df, "attic", allow_unknown)
        garage = _yn_to_value(ch_garage, df, "garage", allow_unknown)
        hasStorageRoom = _yn_to_value(ch_storage, df, "hasStorageRoom", allow_unknown)
        hasGuestRoom = _yn_to_value(ch_guest, df, "hasGuestRoom", allow_unknown)

    row = {
        "squareMeters": float(area),
        "numberOfRooms": int(rooms),
        "hasYard": int(hasYard),
        "hasPool": int(hasPool),
        "floors": int(floors),
        "cityCode": citycode,
        "numPrevOwners": int(numPrevOwners),
        "made": int(made),
        "isNewBuilt": int(isNewBuilt),
        "hasStormProtector": int(hasStormProtector),
        "basement": int(basement),
        "attic": int(attic),
        "garage": int(garage),
        "hasStorageRoom": int(hasStorageRoom),
        "hasGuestRoom": int(hasGuestRoom),
    }

    return pd.DataFrame([row]), dict(row)
