from __future__ import annotations

from datetime import datetime
from io import BytesIO
from typing import Any

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from maison_estimateur.analysis.report_figures import fig_price_distribution_png
from maison_estimateur.analysis.report_insights import build_insights


# ==========================================================
# Helpers format
# ==========================================================

def _fmt_eur(x: float | None) -> str:
    try:
        return f"{float(x):,.0f} €"
    except Exception:
        return "—"


def _yn_str(x: Any) -> str:
    """Convertit 0/1 en 'Oui'/'Non' pour l'affichage PDF."""
    try:
        if int(x) == 1:
            return "Oui"
        if int(x) == 0:
            return "Non"
    except Exception:
        pass
    return "—"


def _safe_float(x: Any) -> float | None:
    try:
        v = float(x)
        if pd.isna(v):
            return None
        return v
    except Exception:
        return None


def _safe_int(x: Any) -> int | None:
    try:
        return int(x)
    except Exception:
        try:
            return int(str(x))
        except Exception:
            return None


# ==========================================================
# Génération du rapport PDF
# ==========================================================

def generate_estimation_report_pdf(
    df: pd.DataFrame,
    features: dict[str, Any],
    estimated_price: float,
    model_name: str,
) -> bytes:
    """
    Génère un rapport PDF récapitulatif :
    - Informations du bien
    - Estimation
    - Graphique principal (distribution des prix)
    - Insights automatiques
    """
    # Pré-calculs
    area = _safe_float(features.get("squareMeters"))
    rooms = _safe_int(features.get("numberOfRooms"))
    citycode = features.get("cityCode")
    price_per_m2 = (estimated_price / area) if area and area > 0 else None

    # Figure principale (PNG bytes)
    img_dist = fig_price_distribution_png(df=df, estimated_price=estimated_price)

    # Insights
    insights = build_insights(
        df=df,
        features=features,
        estimated_price=estimated_price,
        model_name=model_name,
    )

    # ======================================================
    # PDF
    # ======================================================
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x0 = 2.0 * cm
    y = height - 2.0 * cm

    # Titre
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x0, y, "Rapport d’estimation — MAISONESTIMATEUR")
    y -= 0.7 * cm

    c.setFont("Helvetica", 10)
    c.drawString(
        x0,
        y,
        f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
    )
    y -= 1.0 * cm

    # ------------------------------------------------------
    # 1) Résumé estimation
    # ------------------------------------------------------
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x0, y, "1) Résumé de l’estimation")
    y -= 0.6 * cm

    c.setFont("Helvetica", 11)
    c.drawString(x0, y, f"Modèle utilisé : {model_name}")
    y -= 0.5 * cm
    c.drawString(x0, y, f"Prix estimé : {_fmt_eur(estimated_price)}")
    y -= 0.5 * cm
    c.drawString(x0, y, f"Surface : {area:,.0f} m²" if area else "Surface : —")
    y -= 0.5 * cm
    c.drawString(
        x0,
        y,
        f"Nombre de pièces : {rooms}" if rooms is not None else "Nombre de pièces : —",
    )
    y -= 0.5 * cm
    c.drawString(x0, y, f"Code ville (cityCode) : {citycode}")
    y -= 0.5 * cm
    c.drawString(
        x0,
        y,
        f"Prix au m² : {_fmt_eur(price_per_m2)}" if price_per_m2 is not None else "Prix au m² : —",
    )
    y -= 0.8 * cm

    # ------------------------------------------------------
    # 2) Caractéristiques du bien
    # ------------------------------------------------------
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x0, y, "2) Caractéristiques du bien")
    y -= 0.6 * cm

    shown_keys = [
        "squareMeters",
        "numberOfRooms",
        "cityCode",
        "floors",
        "hasYard",
        "hasPool",
        "garage",
        "basement",
        "attic",
        "hasStorageRoom",
        "hasGuestRoom",
        "made",
        "isNewBuilt",
        "numPrevOwners",
        "hasStormProtector",
    ]

    boolean_keys = {
        "hasYard",
        "hasPool",
        "garage",
        "basement",
        "attic",
        "hasStorageRoom",
        "hasGuestRoom",
        "isNewBuilt",
        "hasStormProtector",
    }

    c.setFont("Helvetica", 10)
    col1 = x0
    col2 = x0 + 8.2 * cm
    row_h = 0.45 * cm

    for k in shown_keys:
        if y < 4.0 * cm:
            c.showPage()
            y = height - 2.0 * cm
            c.setFont("Helvetica-Bold", 13)
            c.drawString(x0, y, "2) Caractéristiques du bien (suite)")
            y -= 0.8 * cm
            c.setFont("Helvetica", 10)

        v = features.get(k, "—")
        v_display = _yn_str(v) if k in boolean_keys else str(v)

        c.drawString(col1, y, k)
        c.drawString(col2, y, v_display)
        y -= row_h

    y -= 0.6 * cm

    # ------------------------------------------------------
    # 3) Distribution des prix
    # ------------------------------------------------------
    if img_dist is not None:
        if y < 10.5 * cm:
            c.showPage()
            y = height - 2.0 * cm

        c.setFont("Helvetica-Bold", 13)
        c.drawString(x0, y, "3) Distribution des prix du dataset")
        y -= 0.5 * cm

        c.setFont("Helvetica", 11)
        c.drawString(x0, y, "Position du bien estimé par rapport au marché.")
        y -= 0.4 * cm

        _draw_image(
            c,
            img_dist,
            x=x0,
            y=y - 6.2 * cm,
            w=16.5 * cm,
            h=6.2 * cm,
        )
        y -= 7.0 * cm

    # ------------------------------------------------------
    # 4) Insights automatiques
    # ------------------------------------------------------
    if y < 4.5 * cm:
        c.showPage()
        y = height - 2.0 * cm

    c.setFont("Helvetica-Bold", 13)
    c.drawString(x0, y, "4) Insights automatiques")
    y -= 0.6 * cm

    c.setFont("Helvetica", 11)
    for line in insights:
        if y < 2.5 * cm:
            c.showPage()
            y = height - 2.0 * cm
            c.setFont("Helvetica-Bold", 13)
            c.drawString(x0, y, "4) Insights automatiques (suite)")
            y -= 0.8 * cm
            c.setFont("Helvetica", 11)

        c.drawString(x0, y, f"• {line}")
        y -= 0.5 * cm

    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        x0,
        1.5 * cm,
        "MAISONESTIMATEUR — Rapport généré automatiquement à titre indicatif.",
    )

    c.save()
    return buffer.getvalue()


def _draw_image(
    c: canvas.Canvas,
    png_bytes: bytes,
    x: float,
    y: float,
    w: float,
    h: float,
) -> None:
    """Dessine une image PNG (bytes) dans le PDF."""
    img = ImageReader(BytesIO(png_bytes))
    c.drawImage(img, x, y, width=w, height=h, preserveAspectRatio=True, mask="auto")
