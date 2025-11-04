from __future__ import annotations
import streamlit as st
from contextlib import contextmanager
from typing import Iterator, Optional

def topbar(title: str = "MAISONESTIMATEUR", show_quit: bool = True) -> None:
    """Barre supérieure avec titre et bouton Quitter."""
    left, _, right = st.columns([6, 2, 2])
    with left:
        st.markdown(f"### 🏠 **{title}**")
    if show_quit:
        with right:
            if st.button("Quitter", type="primary"):
                st.info("Application arrêtée. Merci d'avoir utilisé MAISONESTIMATEUR.")
                st.stop()

def section_title(text: str) -> None:
    """Titre de section uniforme."""
    st.markdown(f"#### {text}")

@contextmanager
def page_container(padding: int = 0) -> Iterator[None]:
    """
    Contexte pour homogénéiser la mise en page.
    Exemple:
        with page_container():
            ... contenu ...
    """
    css = f"""
        <style>
            .main .block-container {{
                padding-top: {padding}px;
            }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    yield

def divider(label: Optional[str] = None) -> None:
    """Séparateur visuel optionnel avec label."""
    st.markdown("---")
    if label:
        st.caption(label)
