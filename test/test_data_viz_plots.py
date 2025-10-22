import sys, os
import pandas as pd
import plotly.graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from functions.data_viz import plot_price_distribution, plot_surface_vs_price


#Jeu de données factice pour les tests
def fake_df():
    return pd.DataFrame({
        "price": [100000, 150000, 200000],
        "squareMeters": [40, 60, 80]
    })


# TESTS POUR plot_price_distribution
def test_plot_price_distribution_returns_figure():
    """Vérifie que la fonction retourne bien une Figure Plotly."""
    df = fake_df()
    fig = plot_price_distribution(df)
    assert isinstance(fig, go.Figure)


def test_plot_price_distribution_has_price_on_xaxis():
    """Vérifie que l’axe X correspond à 'price'."""
    df = fake_df()
    fig = plot_price_distribution(df)
    layout = fig.to_dict()["layout"]

    # Vérifie le titre de l'axe X
    assert "xaxis" in layout
    assert "title" in layout["xaxis"]
    assert "text" in layout["xaxis"]["title"]
    assert layout["xaxis"]["title"]["text"].lower() in ["price", "prix"]



# TESTS POUR plot_surface_vs_price
def test_plot_surface_vs_price_returns_figure():
    """Vérifie que la fonction retourne bien une Figure Plotly."""
    df = fake_df()
    fig = plot_surface_vs_price(df)
    assert isinstance(fig, go.Figure)


def test_plot_surface_vs_price_axes_are_correct():
    """Vérifie que les bons champs sont utilisés sur les axes."""
    df = fake_df()
    fig = plot_surface_vs_price(df)
    layout = fig.to_dict()["layout"]
    assert layout["xaxis"]["title"]["text"] == "squareMeters"
    assert layout["yaxis"]["title"]["text"] == "price"

