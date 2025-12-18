from __future__ import annotations

from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd


def _fig_to_png_bytes(fig) -> bytes:
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()


def fig_price_distribution_png(df: pd.DataFrame, estimated_price: float) -> bytes | None:
    """Histogramme des prix du dataset + ligne verticale pour le bien estimé."""
    if "price" not in df.columns:
        return None

    prices = df["price"].dropna()
    if prices.empty:
        return None

    fig = plt.figure(figsize=(7.8, 2.8))
    ax = fig.add_subplot(111)
    ax.hist(prices.values, bins=30)

    ax.axvline(float(estimated_price), linewidth=2)
    ax.set_title("Distribution des prix (dataset) + position du bien")
    ax.set_xlabel("Prix (€)")
    ax.set_ylabel("Nombre de biens")
    ax.ticklabel_format(style="plain", axis="x")

    return _fig_to_png_bytes(fig)
