from __future__ import annotations

import pandas as pd
import streamlit as st


# =========================
# Helpers affichage
# =========================

def data_head(
    df: pd.DataFrame,
    rows: int = 5,
    expanded: bool = False,
    title: str = "Aperçu des données (head)",
) -> None:
    """Affiche un aperçu des premières lignes dans un expander."""
    with st.expander(title, expanded=expanded):
        st.dataframe(df.head(rows), width="stretch")


def plot_figure(fig) -> None:
    """Affiche une figure Plotly en pleine largeur avec gestion d'erreurs douce."""
    if fig is None:
        st.info("Pas de figure à afficher.")
        return
    try:
        st.plotly_chart(fig, width="stretch")
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
        st.metric("Valeurs uniques", analysis.get("unique_values", 0))
        st.metric("Valeur la plus fréquente", stats.get("top", "—"))
    with col2:
        st.metric("Fréquence (valeur la plus fréquente)", stats.get("freq", "—"))
        st.metric("Valeurs manquantes", analysis.get("missing", 0))


def value_counts_table(vc: pd.Series | pd.DataFrame | list | dict) -> None:
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
            vc_df = pd.DataFrame(vc)
            if list(vc_df.columns)[:2] != ["Valeur", "Nombre"]:
                vc_df.columns = ["Valeur", "Nombre"][: len(vc_df.columns)]

        st.dataframe(vc_df, width="stretch")
    except Exception as e:
        st.warning(f"Impossible d'afficher les effectifs : {e}")


# =========================
# Arrondissement selector (Stats page)
# =========================

def arrondissement_selector_and_metric(
    df: pd.DataFrame,
    get_mean_fn,
    select_label: str = "Arrondissement (1–20)",
) -> None:
    """
    Sélecteur d'arrondissement 1..20 + affichage prix moyen.

    Source métier officielle :
    - df["arrondissement"] (créé dans load_data)
    """
    if "arrondissement" not in df.columns:
        st.warning("La colonne 'arrondissement' est absente du dataset.")
        return

    s = df["arrondissement"].dropna().astype(int)
    s = s[(s >= 1) & (s <= 20)]
    if s.empty:
        st.warning("Aucun arrondissement valide (1–20) n'est disponible dans les données.")
        return

    counts = s.value_counts()
    top_arr = int(counts.idxmax())

    st.info(f"🏙️ Arrondissement le plus fréquent : **{top_arr}**")

    sel = st.selectbox(
        select_label,
        options=list(range(1, 21)),
        index=top_arr - 1,
        key="arrondissement_selector_stats",
    )

    try:
        mean_price = get_mean_fn(df, sel)
    except Exception as e:
        mean_price = None
        st.warning(f"Erreur lors du calcul du prix moyen pour l'arrondissement {sel} : {e}")

    if mean_price is None:
        st.warning("Impossible de calculer le prix moyen pour cet arrondissement.")
    else:
        st.metric("Prix moyen (proxy) dans cet arrondissement", f"{mean_price:,.2f} €")
        st.success(f"💰 Prix moyen pour l'arrondissement {sel} : **{mean_price:,.0f} €**.")


# =========================
# Inputs bien immobilier (Estimation & Comparaison)
# =========================

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
    """Renvoie le choix texte ("Oui"/"Non"/"Je ne sais pas")."""
    if allow_unknown:
        return st.selectbox(label, ["Je ne sais pas", "Non", "Oui"], index=0, key=key)

    idx = 1 if int(default) == 1 else 0
    return st.selectbox(label, ["Non", "Oui"], index=idx, key=key)


def _yn_to_value(choice: str, df: pd.DataFrame, col: str, allow_unknown: bool) -> int:
    """Convertit le choix texte en 0/1 (si inconnu -> mode dataset)."""
    if allow_unknown and choice == "Je ne sais pas":
        return _mode_binary(df, col, fallback=0)
    return 1 if choice == "Oui" else 0


def property_inputs(
    df: pd.DataFrame,
    prefix: str = "A",
    allow_unknown: bool = False,
) -> tuple[pd.DataFrame, dict]:
    """
    Bloc de saisie standardisé pour un bien immobilier.

    - UI : arrondissement 1..20
    - Feature modèle : cityCode = arrondissement
    """
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

    arrondissement = st.selectbox(
        "Arrondissement (1–20)",
        options=list(range(1, 21)),
        index=0,
        key=f"{prefix}_arrondissement",
    )

    with st.expander("Options avancées", expanded=False):
        default_yard = _mode_binary(df, "hasYard", 0)
        default_pool = _mode_binary(df, "hasPool", 0)
        default_storm = _mode_binary(df, "hasStormProtector", 0)
        default_basement = _mode_binary(df, "basement", 0)
        default_attic = _mode_binary(df, "attic", 0)
        default_garage = _mode_binary(df, "garage", 0)
        default_storage = _mode_binary(df, "hasStorageRoom", 0)
        default_guest = _mode_binary(df, "hasGuestRoom", 0)
        default_new = _mode_binary(df, "isNewBuilt", 0)

        ch_yard = _yn_selector(
            "Jardin",
            key=f"{prefix}_hasYard",
            allow_unknown=allow_unknown,
            default=default_yard,
        )
        ch_pool = _yn_selector(
            "Piscine",
            key=f"{prefix}_hasPool",
            allow_unknown=allow_unknown,
            default=default_pool,
        )

        floors = st.slider("Nombre d'étages", 1, 5, 1, key=f"{prefix}_floors")
        num_prev_owners = st.slider(
            "Nombre de propriétaires précédents",
            0,
            5,
            1,
            key=f"{prefix}_numPrevOwners",
        )
        made = st.slider("Année de construction", 1900, 2025, 2000, key=f"{prefix}_made")

        ch_new = _yn_selector(
            "Neuf",
            key=f"{prefix}_isNewBuilt",
            allow_unknown=allow_unknown,
            default=default_new,
        )
        ch_storm = _yn_selector(
            "Protection tempête",
            key=f"{prefix}_hasStormProtector",
            allow_unknown=allow_unknown,
            default=default_storm,
        )
        ch_basement = _yn_selector(
            "Sous-sol",
            key=f"{prefix}_basement",
            allow_unknown=allow_unknown,
            default=default_basement,
        )
        ch_attic = _yn_selector(
            "Grenier",
            key=f"{prefix}_attic",
            allow_unknown=allow_unknown,
            default=default_attic,
        )
        ch_garage = _yn_selector(
            "Garage",
            key=f"{prefix}_garage",
            allow_unknown=allow_unknown,
            default=default_garage,
        )
        ch_storage = _yn_selector(
            "Cave/Stockage",
            key=f"{prefix}_hasStorageRoom",
            allow_unknown=allow_unknown,
            default=default_storage,
        )
        ch_guest = _yn_selector(
            "Chambre d'amis",
            key=f"{prefix}_hasGuestRoom",
            allow_unknown=allow_unknown,
            default=default_guest,
        )

        has_yard = _yn_to_value(ch_yard, df, "hasYard", allow_unknown)
        has_pool = _yn_to_value(ch_pool, df, "hasPool", allow_unknown)
        is_new_built = _yn_to_value(ch_new, df, "isNewBuilt", allow_unknown)
        has_storm_protector = _yn_to_value(ch_storm, df, "hasStormProtector", allow_unknown)
        basement = _yn_to_value(ch_basement, df, "basement", allow_unknown)
        attic = _yn_to_value(ch_attic, df, "attic", allow_unknown)
        garage = _yn_to_value(ch_garage, df, "garage", allow_unknown)
        has_storage_room = _yn_to_value(ch_storage, df, "hasStorageRoom", allow_unknown)
        has_guest_room = _yn_to_value(ch_guest, df, "hasGuestRoom", allow_unknown)

    row = {
        "squareMeters": float(area),
        "numberOfRooms": int(rooms),
        "hasYard": int(has_yard),
        "hasPool": int(has_pool),
        "floors": int(floors),
        "cityCode": int(arrondissement),  # feature modèle
        "numPrevOwners": int(num_prev_owners),
        "made": int(made),
        "isNewBuilt": int(is_new_built),
        "hasStormProtector": int(has_storm_protector),
        "basement": int(basement),
        "attic": int(attic),
        "garage": int(garage),
        "hasStorageRoom": int(has_storage_room),
        "hasGuestRoom": int(has_guest_room),
    }

    return pd.DataFrame([row]), dict(row)










