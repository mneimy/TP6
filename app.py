"""
TP6 — Application prête pour le déploiement (fil rouge)
-------------------------------------------------------
Version "production-ready" du dashboard :
  - expose `server = app.server` (point d'entrée WSGI / Gunicorn)
  - bouton de TÉLÉCHARGEMENT des données filtrées (CSV)
  - bandeau "source / dernière mise à jour / données agrégées (RGPD)"
  - authentification basique en option (décommenter le bloc dash_auth)

Lancement en local :
    python app.py
Lancement en production :
    gunicorn app:server --bind 0.0.0.0:8050
"""

from datetime import date

from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

from data import charger_donnees

df = charger_donnees()
REGIONS = ["Toutes"] + sorted(df["region"].unique())
ACCENT = "#1F4E79"
TEMPLATE = "simple_white"

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "TP6 — Dashboard déployable"
server = app.server  # <-- indispensable pour Gunicorn / le déploiement

# --- Authentification basique (OPTIONNELLE, pour une démo interne) -----------
# Décommentez pour protéger l'accès :
# import dash_auth
# COMPTES = {"directeur": "motdepasse-fort"}
# dash_auth.BasicAuth(app, COMPTES)


app.layout = dbc.Container(fluid=True, children=[
    html.H2("Tableau de bord commercial — version diffusable", className="my-3"),

    dbc.Row([
        dbc.Col(dcc.Dropdown(id="region", options=REGIONS, value="Toutes",
                             clearable=False), md=4),
        dbc.Col(html.Div([
            dbc.Button("⬇️ Télécharger les données (CSV)", id="btn-dl",
                       color="primary", outline=True),
            dcc.Download(id="dl"),
        ]), md=4, className="d-flex align-items-center"),
    ], className="g-3 mb-2"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="g-evolution"), md=8),
        dbc.Col(dcc.Graph(id="g-produit"), md=4),
    ], className="g-3"),

    # Bandeau de gouvernance / conformité
    html.Footer(
        f"Source : données internes simulées · Dernière mise à jour : "
        f"{date.today():%d/%m/%Y} · Données agrégées (aucune donnée personnelle — RGPD).",
        className="text-muted small my-3 border-top pt-2",
    ),
])


@app.callback(
    Output("g-evolution", "figure"),
    Output("g-produit", "figure"),
    Input("region", "value"),
)
def maj(region):
    dff = df if region == "Toutes" else df[df["region"] == region]

    evo = dff.groupby("mois", as_index=False)["montant"].sum()
    fig_evo = px.line(evo, x="mois", y="montant", markers=True,
                      title="Évolution mensuelle du CA",
                      labels={"mois": "Mois", "montant": "CA (€)"},
                      template=TEMPLATE)
    fig_evo.update_traces(line_color=ACCENT)

    par_prod = (dff.groupby("produit", as_index=False)["montant"].sum()
                   .sort_values("montant"))
    fig_prod = px.bar(par_prod, x="montant", y="produit", orientation="h",
                      title="CA par produit",
                      labels={"montant": "CA (€)", "produit": ""},
                      template=TEMPLATE, color_discrete_sequence=[ACCENT])
    return fig_evo, fig_prod


@app.callback(
    Output("dl", "data"),
    Input("btn-dl", "n_clicks"),
    Input("region", "value"),
    prevent_initial_call=True,
)
def telecharger(n_clicks, region):
    # On ne déclenche le téléchargement que sur le clic du bouton
    from dash import ctx
    if ctx.triggered_id != "btn-dl":
        return None
    dff = df if region == "Toutes" else df[df["region"] == region]
    export = dff[["date", "region", "produit", "quantite", "montant"]]
    return dcc.send_data_frame(export.to_csv, "ventes_export.csv", index=False)


if __name__ == "__main__":
    app.run()
