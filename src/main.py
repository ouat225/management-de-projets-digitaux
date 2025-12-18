# src/main.py
from __future__ import annotations

import os
import sys

from streamlit.web.cli import main as st_main


def main() -> None:
    # Cible : le fichier Streamlit (ton app)
    target = os.path.join(os.path.dirname(__file__), "maison_estimateur", "app.py")

    # On simule: streamlit run <target>
    sys.argv = ["streamlit", "run", target]
    st_main()


if __name__ == "__main__":
    main()
