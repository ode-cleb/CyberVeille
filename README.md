# CyberVeille

Plateforme de veille cybersécurité souveraine — agrégation automatique de CVE, alertes CERT-FR, et actualités sécurité, avec dashboard React et notifications push.

> Stack 100% souveraine : hébergement européen, zéro dépendance US, WAF self-hosted, backups chiffrés RGPD.

---

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Stack technique](#stack-technique)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Lancer l'environnement de dev](#lancer-lenvironnement-de-dev)
- [Commandes utiles](#commandes-utiles)
- [Structure du projet](#structure-du-projet)
- [Variables d'environnement](#variables-denvironnement)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [Sécurité](#sécurité)

---

## Fonctionnalités

- Collecte automatique depuis NVD, CERT-FR, CISA KEV, The Hacker News et AlienVault OTX
- Dashboard React avec filtres CVE par sévérité CVSS, produit, date
- Alertes push (Web Push API, sans Firebase) pour les CVE critiques et alertes CERT-FR
- PWA installable sur mobile, mode offline
- Authentification JWT + 2FA TOTP
- Export PDF / CSV, flux RSS personnalisé par utilisateur
- Résumés IA à la demande (API Claude, cache en base)
- Recherche full-text PostgreSQL avec tolérance aux fautes de frappe

---

## Architecture

```
Sources externes (NVD, CERT-FR, CISA KEV, RSS...)
        │
        ▼
  Celery Beat (scheduler)
        │
        ▼
  Celery Workers (collecte, parsing, enrichissement)
        │
        ▼
  PostgreSQL 16 + Redis 7
        │
        ▼
  Django REST API (DRF + JWT)
        │
        ▼
  React SPA + PWA (Vite + Workbox)
```

---

## Stack technique

| Composant | Technologie |
|---|---|
| Backend API | Django 5 + Django REST Framework |
| Auth | JWT (simplejwt) + 2FA TOTP |
| Base de données | PostgreSQL 16 |
| Cache / Broker | Redis 7 |
| Tâches async | Celery + Celery Beat |
| Frontend | React 18 + TypeScript + Vite |
| UI | Tailwind CSS + shadcn/ui |
| PWA | Workbox + Web Push API |
| Conteneurisation | Docker + Docker Compose |
| Reverse Proxy | Nginx + ModSecurity (WAF OWASP) |
| TLS | Let's Encrypt (Certbot) |
| DNS | OVH |
| Protection réseau | fail2ban + iptables |
| Monitoring dispo | Uptime Kuma (self-hosted) |
| Monitoring erreurs | Sentry (self-hostable) |
| Backups | Scaleway Object Storage (Paris, RGPD) |
| CI/CD | GitHub Actions |
| Pool connexions | pgBouncer |

---

## Prérequis

- Docker >= 24
- Docker Compose v2 (`docker compose`)
- Git

Aucune installation locale de Python ou Node n'est requise — tout tourne dans Docker.

---

## Installation

```bash
# 1. Cloner le repo
git clone https://github.com/TON_USER/cyberveille.git
cd cyberveille

# 2. Créer le fichier d'environnement dev
cp docker/.env.example docker/.env.dev
# Éditer docker/.env.dev avec tes valeurs
```

---

## Lancer l'environnement de dev

```bash
# Démarrer toute la stack
docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml --env-file docker/.env.dev up --build

# Dans un second terminal — appliquer les migrations (premier démarrage uniquement)
docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml --env-file docker/.env.dev exec backend python manage.py migrate
```

L'application est disponible sur :

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API Django | http://localhost:8000 |
| API Health | http://localhost:8000/api/health/ |
| Django Admin | http://localhost:8000/admin/ |
| Debug Toolbar | http://localhost:8000/__debug__/ |
| Silk (profiler) | http://localhost:8000/silk/ |

---

## Commandes utiles

```bash
# Arrêter la stack
docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml --env-file docker/.env.dev down

# Arrêter et supprimer les volumes (reset complet de la base)
docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml --env-file docker/.env.dev down -v

# Créer un superuser Django
docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml --env-file docker/.env.dev exec backend python manage.py createsuperuser

# Lancer les tests
docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml --env-file docker/.env.dev exec backend pytest

# Accéder au shell Django
docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml --env-file docker/.env.dev exec backend python manage.py shell

# Voir les logs d'un service
docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml --env-file docker/.env.dev logs -f backend
```

---

## Structure du projet

```
cyberveille/
├── backend/
│   ├── apps/
│   │   └── core/               # App principale Django
│   ├── cyberveille/
│   │   ├── settings/
│   │   │   ├── base.py         # Settings communs
│   │   │   ├── dev.py          # Settings dev (DEBUG=True, Silk, Toolbar)
│   │   │   ├── prod.py         # Settings prod (sécurité renforcée)
│   │   │   └── staging.py      # Settings staging
│   │   ├── celery.py           # Config Celery
│   │   └── urls.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── dev.txt             # + debug-toolbar, silk, pytest
│   │   └── prod.txt            # + django-csp, sentry-sdk
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── tailwind.config.js
│   └── vite.config.ts
├── docker/
│   ├── docker-compose.base.yml
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   ├── Dockerfile.backend.dev
│   ├── Dockerfile.backend.prod
│   ├── Dockerfile.frontend.dev
│   ├── Dockerfile.nginx
│   ├── nginx/
│   ├── fail2ban/
│   ├── .env.example            # Template — copier en .env.dev / .env.prod
│   └── .env.dev                # Non versionné
├── docs/
│   └── threat-model.md         # Modèle de menaces STRIDE
├── scripts/
├── .github/workflows/
├── .gitignore
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
└── README.md
```

---

## Variables d'environnement

Copier `docker/.env.example` en `docker/.env.dev` et renseigner :

| Variable | Description | Exemple |
|---|---|---|
| `DB_NAME` | Nom de la base PostgreSQL | `cyberveille_dev` |
| `DB_USER` | Utilisateur PostgreSQL | `cyberveille` |
| `DB_PASSWORD` | Mot de passe PostgreSQL | |
| `DB_HOST` | Hôte DB (dev = `db`) | `db` |
| `DB_PORT` | Port DB | `5432` |
| `REDIS_PASSWORD` | Mot de passe Redis | |
| `REDIS_URL` | URL Redis complète | `redis://:password@redis:6379/0` |
| `SECRET_KEY` | Django secret key | Générer avec `python -c "import secrets; print(secrets.token_hex(50))"` |
| `ALLOWED_HOSTS` | Hosts autorisés Django | `localhost,127.0.0.1,backend` |
| `DJANGO_SETTINGS_MODULE` | Module settings à utiliser | `cyberveille.settings.dev` |
| `VITE_API_URL` | URL API pour le frontend | `http://localhost:8000/api` |

---

## Tests

```bash
# Backend — pytest
docker compose ... exec backend pytest

# Backend — avec coverage
docker compose ... exec backend pytest --cov=apps --cov-report=term-missing

# Frontend — vitest
docker compose ... exec frontend npm run test
```

---

## Déploiement

Le déploiement prod utilise `docker-compose.prod.yml` avec Nginx + ModSecurity + Certbot. Voir la documentation complète dans `docs/` et le plan de projet.

Hébergement recommandé : **Hetzner CX31** (prod) + **Hetzner CX11** (staging), ~15€/mois au total.

---

## Sécurité

Ce projet applique une politique de sécurité dès le départ :

- Modèle de menaces STRIDE documenté dans `docs/threat-model.md`
- Secrets exclusivement via variables d'environnement, jamais dans le code
- `detect-secrets` en pre-commit hook
- `DEBUG = False` par défaut dans `base.py`
- `django-debug-toolbar` et `django-silk` uniquement en dev, jamais en prod
- WAF ModSecurity + règles OWASP CRS en production
- Backups PostgreSQL chiffrés GPG → Scaleway Object Storage (Paris, RGPD)

Pour signaler une vulnérabilité, ouvrir une issue privée sur GitHub.

---