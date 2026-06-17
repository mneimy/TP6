"""
TP4 — Données de ventes (générées à la volée)
---------------------------------------------
Aucun fichier externe : on simule un jeu de ventes réaliste et REPRODUCTIBLE
(graine fixée). Colonnes : date, region, produit, quantite, prix_unitaire, montant.

Un "creux" volontaire est injecté dans une région au 3e trimestre : il servira
de fil narratif au TP5 (storytelling).
"""

import numpy as np
import pandas as pd

REGIONS = ["Nord", "Sud", "Est", "Ouest"]
PRODUITS = ["Clavier", "Souris", "Écran", "Casque", "Webcam"]
PRIX = {"Clavier": 45, "Souris": 25, "Écran": 180, "Casque": 70, "Webcam": 55}


def charger_donnees() -> pd.DataFrame:
    """Retourne un DataFrame de ventes quotidiennes propre et typé."""
    rng = np.random.default_rng(42)  # reproductible

    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    lignes = []

    for date in dates:
        # Saisonnalité douce (pic en fin d'année)
        saison = 1 + 0.3 * np.sin((date.dayofyear / 365) * 2 * np.pi - 1.5)

        for region in REGIONS:
            # Creux volontaire : région "Est", de juillet à septembre 2025
            creux = 0.45 if (region == "Est" and date.year == 2025
                             and date.month in (7, 8, 9)) else 1.0

            for produit in PRODUITS:
                base = rng.poisson(6) * saison * creux
                quantite = int(max(0, round(base)))
                if quantite == 0:
                    continue
                prix = PRIX[produit]
                lignes.append({
                    "date": date,
                    "region": region,
                    "produit": produit,
                    "quantite": quantite,
                    "prix_unitaire": prix,
                    "montant": quantite * prix,
                })

    df = pd.DataFrame(lignes)
    df["date"] = pd.to_datetime(df["date"])
    df["mois"] = df["date"].dt.to_period("M").dt.to_timestamp()
    return df


if __name__ == "__main__":
    # Petit aperçu en ligne de commande
    df = charger_donnees()
    print(df.head())
    print("\nLignes :", len(df))
    print("Période :", df["date"].min().date(), "→", df["date"].max().date())
    print("CA total : {:,.0f} €".format(df["montant"].sum()).replace(",", " "))
