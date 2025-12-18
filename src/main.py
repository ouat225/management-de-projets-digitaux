# src/main.py
from __future__ import annotations

import os
import runpy

def main() -> None:
    target = os.path.join(os.path.dirname(__file__), "maison_estimateur", "app.py")
    runpy.run_path(target, run_name="__main__")

if __name__ == "__main__":
    main()
