# Déployer l'application sur Render (guide pas à pas)

Ce guide suit la documentation officielle Render pour les **Web Services** et les **commandes de build/deploy**.

Références officielles :
- [Web Services (Render Docs)](https://render.com/docs/web-services)
- [Deploys: Build Command / Start Command (Render Docs)](https://render.com/docs/deploys)
- [Deploy a Flask App (exemple Python avec Gunicorn)](https://render.com/docs/deploy-flask)

---

## 1) Préparer le dépôt Git

Render déploie depuis un dépôt Git (GitHub/GitLab/Bitbucket ou URL publique).

Vérifie que ton dossier `TP6_deploiement_partage` contient au minimum :
- `app.py`
- `requirements.txt` (avec `gunicorn`)

Dans ce projet, la commande de démarrage production est :
- `gunicorn app:server --bind 0.0.0.0:$PORT`

> Pourquoi `app:server` ?  
> Parce que dans `app.py`, Dash expose `server = app.server` pour Gunicorn.

---

## 2) Créer le service sur Render

1. Ouvre le dashboard Render.
2. Clique sur **New > Web Service**.
3. Connecte ton repo Git.
4. Sélectionne la branche à déployer (souvent `main`).

---

## 3) Remplir les paramètres de déploiement

Dans le formulaire de création du service, renseigne :

- **Language**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:server --bind 0.0.0.0:$PORT`

Ces valeurs correspondent aux recommandations officielles Render pour Python (`pip install ...` + `gunicorn ...`).

---

## 4) Vérifier le port réseau (important)

D'après Render, un Web Service doit écouter sur `0.0.0.0` et utiliser le port attendu par la variable d'environnement `PORT` (par défaut `10000`).

Dans ce projet, c'est déjà géré via :
- `--bind 0.0.0.0:$PORT`

---

## 5) Lancer le premier déploiement

1. Choisis l'instance (Free/Starter/etc.).
2. Clique sur **Create Web Service**.
3. Suis les logs dans l'onglet **Events**.

Quand le build est terminé, Render fournit une URL :
- `https://<nom-service>.onrender.com`

---

## 6) Vérifier que l'application fonctionne

Checklist rapide :
- La page s'ouvre via l'URL Render.
- Les graphiques se chargent.
- Les callbacks Dash répondent (filtres, interactions).
- Le téléchargement CSV fonctionne.

---

## 7) Déploiements suivants (CI/CD automatique)

Selon la doc Render, après le premier déploiement :
- chaque `git push` sur la branche liée déclenche un nouveau build/deploy automatique ;
- si un build échoue, la version précédente reste en ligne.

---

## 8) Dépannage rapide

- **Erreur `ModuleNotFoundError`**  
  Vérifie que le package est dans `requirements.txt`.

- **Erreur de démarrage Gunicorn**  
  Vérifie que `server = app.server` existe dans `app.py` et que la commande est bien `gunicorn app:server ...`.

- **Service "healthy" mais page inaccessible**  
  Vérifie le bind `0.0.0.0:$PORT` (exigence Render pour le trafic HTTP entrant).

---

## Option recommandée : `render.yaml` (Infrastructure as Code)

Render supporte aussi la configuration par Blueprint. Tu peux ensuite versionner la configuration Render dans le repo (utile pour standardiser plusieurs déploiements).

Doc officielle : [Blueprints](https://render.com/docs/blueprint-spec)
