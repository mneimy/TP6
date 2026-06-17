# TP6 — Déploiement, partage & gouvernance

**Module 5 — Diffusion et partage des visualisations**
⏱️ Durée : ~2 h · 🎓 Niveau : intermédiaire

---

## 🎯 Objectif

Rendre le dashboard **accessible et sûr** : le préparer pour la production, ajouter
un **export de données**, un **bandeau de conformité**, puis le **déployer** sur le web.

---

## 🧠 Le tutoriel

### 1. Du mode développement à la production

On ne lance **jamais** `app.run(debug=True)` en production. On utilise **Gunicorn**,
un serveur WSGI, qui a besoin de l'objet Flask exposé par Dash :

```python
app = Dash(__name__)
server = app.server          # <- point d'entrée WSGI (déjà présent dans app.py)
```

```bash
# Test local "comme en prod" :
gunicorn app:server --bind 0.0.0.0:8050 --workers 4
```

### 2. Fichiers fournis

| Fichier | Rôle |
|---|---|
| `app.py` | Dashboard + bouton d'export CSV + bandeau RGPD |
| `requirements.txt` | Dépendances figées (reproductibilité) |
| `Dockerfile` | Conteneuriser l'app (déploiement portable) |
| `Procfile` | Déploiement sur Render / Railway / Heroku-like |
| `data.py` | Génération des données |

### 3. Trois façons de déployer

| Plateforme | Pour qui | Commande / principe |
|---|---|---|
| **Render / Railway** | Démo, MVP | Connecter le dépôt Git ; le `Procfile` est détecté |
| **Docker + VPS** | Entreprise, contrôle total | `docker build -t dashboard . && docker run -p 8050:8050 dashboard` |
| **Dash Enterprise** | Grands comptes | Auth, scalabilité, support (payant) |

### 4. Sécurité & gouvernance (intégrées dans `app.py`)

- **Export contrôlé** : bouton de téléchargement CSV des données filtrées.
- **Bandeau** : source + date de mise à jour + mention « données agrégées (RGPD) ».
- **Authentification** : bloc `dash_auth.BasicAuth` prêt à décommenter pour une démo interne.

> ⚠️ `BasicAuth` convient à une démo, pas à des données sensibles (comptes en clair).
> Pour de vrais utilisateurs : mots de passe hachés en base + **HTTPS**.

### 5. Lancez et testez

```bash
# Local (développement)
python app.py

# Local (simulation production)
gunicorn app:server --bind 0.0.0.0:8050
```

Cliquez sur **« Télécharger les données (CSV) »** : un fichier `ventes_export.csv`
est généré à partir des filtres en cours.

---

## ✏️ À vous de jouer

1. **Décommentez** le bloc `dash_auth.BasicAuth` et protégez l'accès.
2. Construisez l'image Docker et lancez le conteneur.
3. Ajoutez un **export PNG** d'un graphique (`fig.write_image`, nécessite `pip install kaleido`).
4. **Bonus** : déployez sur Render à partir d'un dépôt Git et vérifiez l'accès en **HTTPS**.

---

## 📦 Livrable attendu

Le dashboard **lancé via Gunicorn** (et idéalement déployé en ligne), avec export de données
et bandeau de conformité.

✅ **Critère de réussite** : l'app répond via `gunicorn app:server`, l'export fonctionne,
et le bandeau source/date/RGPD est visible.

---

## ✅ Checklist qualité avant publication

- [ ] Chaque graphique a un titre qui énonce une conclusion
- [ ] Axes de barres à zéro, pas de double axe Y trompeur
- [ ] ≤ 5 couleurs, une seule couleur d'accent
- [ ] Données triées, annotations directes
- [ ] KPI accompagnés d'un point de comparaison
- [ ] Responsive (lisible sur mobile)
- [ ] Données agrégées avant envoi au navigateur
- [ ] HTTPS, secrets hors du code, accès maîtrisés
- [ ] Source et date de mise à jour affichées
