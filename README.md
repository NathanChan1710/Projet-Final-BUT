# 🏙️ CityCompare — Comparateur de Villes Françaises

> **SAE Outils Décisionnels** — IUT / BUT Science des Données

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io/)
[![Licence](https://img.shields.io/badge/Licence-MIT-green)](LICENSE)

---

## 👥 Équipe

| Nom | Prénom |
|-----|--------|
| CHANSINGMAN | Nathan |
| FRANCESCHIN | Camille |
| RATSIMBA | Manohy |

---

## 📌 Description du projet

**CityCompare** est une application web interactive permettant de **comparer deux villes françaises** (parmi celles de plus de 20 000 habitants) sur plusieurs dimensions clés : coût de la vie, emploi, logement, météo, culture, tourisme et bien plus encore.

L'application vise à aider les utilisateurs dans leur prise de décision lors d'un choix de ville (déménagement, études, emploi…) en centralisant des données issues de sources publiques fiables.

---

## 🌐 Accès à l'application

> 🔗 **URL de l'application déployée :** `https://<votre-app>.streamlit.app`  
> *(À mettre à jour après déploiement sur Streamlit Cloud ou shinyapps.io)*

---

## ✨ Fonctionnalités

- 🔍 **Sélection de deux villes** parmi toutes les communes françaises de +20 000 habitants
- 📊 **Données générales** : population, superficie, densité, catégorie urbaine
- 💼 **Emploi** : taux de chômage, secteurs d'activité, offres d'emploi (Pôle Emploi / France Travail)
- 🏠 **Logement** : prix au m², loyers médians, part de propriétaires/locataires
- 🌦️ **Météo** :
  - Données climatiques annuelles (températures, précipitations)
  - Météo des prochains jours en temps réel
- 🎭 **Culture & Tourisme** : musées, monuments, équipements culturels
- 🎓 **Formation** : établissements d'enseignement supérieur
- ⚽ **Sports** : clubs et infrastructures sportives
- 📰 **Informations générales** via Wikipedia

---

## 📂 Structure du projet

```
citycompare/
│
├── app.py                    # Point d'entrée de l'application Streamlit
├── requirements.txt          # Dépendances Python
├── README.md                 # Ce fichier
│
├── data/                     # Données statiques téléchargées
│   ├── communes_20k.csv      # Liste des communes +20 000 hab. (INSEE)
│   ├── logement.csv          # Données logement (INSEE / DVF)
│   ├── emploi.csv            # Données emploi (INSEE)
│   └── climat.csv            # Normales climatiques (Météo-France)
│
├── scripts/                  # Scripts d'import et de traitement des données
│   ├── fetch_communes.py     # Récupération et filtrage des communes INSEE
│   ├── fetch_logement.py     # Traitement des données DVF / INSEE logement
│   ├── fetch_emploi.py       # Import données emploi INSEE + API France Travail
│   ├── fetch_meteo.py        # Appels API météo (Open-Meteo)
│   └── fetch_wikipedia.py    # Résumés Wikipedia via API
│
├── pages/                    # Modules de l'interface (pages Streamlit)
│   ├── generales.py
│   ├── emploi.py
│   ├── logement.py
│   ├── meteo.py
│   └── culture_tourisme.py
│
└── utils/
    ├── charts.py             # Fonctions de visualisation (Plotly / Altair)
    └── helpers.py            # Fonctions utilitaires
```

---

## 📡 Sources de données

### Données statiques (fichiers téléchargés)

| Thème | Source | Format | Description |
|-------|--------|---------|-------------|
| Liste des communes | [INSEE — COG](https://www.insee.fr/fr/information/2560452) | CSV | Communes françaises avec population |
| Emploi | [INSEE — RP](https://www.insee.fr/fr/statistiques/7632870) | CSV | Taux de chômage, catégories socioprofessionnelles |
| Logement | [INSEE — RP Logement](https://www.insee.fr/fr/statistiques/7632867) | CSV | Statut d'occupation, parc immobilier |
| Prix immobilier | [DVF / data.gouv.fr](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/) | CSV | Transactions immobilières |
| Climatologie | [Météo-France Open Data](https://portail-api.meteofrance.fr/) | CSV | Normales climatiques par station |

### APIs (temps réel)

| Thème | API | Documentation |
|-------|-----|---------------|
| Météo actuelle & prévisions | [Open-Meteo](https://open-meteo.com/) | Gratuite, sans clé |
| Informations générales | [Wikipedia REST API](https://fr.wikipedia.org/api/rest_v1/) | Gratuite |
| Offres d'emploi | [API France Travail](https://francetravail.io/data/api) | Inscription requise |
| Géolocalisation | [API Adresse (gouv.fr)](https://adresse.data.gouv.fr/api-doc/adresse) | Gratuite, sans clé |

---

## 🚀 Installation et lancement en local

### Prérequis

- Python **3.10 ou supérieur**
- `pip` ou `conda`

### 1. Cloner le dépôt

```bash
git clone https://github.com/<votre-repo>/citycompare.git
cd citycompare
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
FRANCE_TRAVAIL_CLIENT_ID=votre_client_id
FRANCE_TRAVAIL_CLIENT_SECRET=votre_client_secret
```

> ⚠️ Ne commitez jamais ce fichier. Il est déjà listé dans le `.gitignore`.

### 5. Préparer les données locales

```bash
python scripts/fetch_communes.py
python scripts/fetch_logement.py
python scripts/fetch_emploi.py
```

### 6. Lancer l'application

```bash
streamlit run app.py
```

L'application est accessible à l'adresse : `http://localhost:8501`

---

## 🗺️ Mode d'emploi de l'interface

1. **Page d'accueil** : sélectionnez deux villes dans les menus déroulants filtrés (communes >20 000 hab.)
2. **Navigation par onglets** : parcourez les thèmes disponibles (Général, Emploi, Logement, Météo, Culture…)
3. **Visualisations** : chaque section affiche des graphiques comparatifs interactifs (Plotly)
4. **Météo** : la section météo affiche à la fois les données climatiques historiques et les prévisions des 7 prochains jours
5. **Export** : possibilité d'exporter les comparaisons en PDF ou CSV (si activé)

---

## 📦 Dépendances principales

```txt
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
requests>=2.31.0
python-dotenv>=1.0.0
altair>=5.0.0
numpy>=1.26.0
```

> Liste complète dans `requirements.txt`

---

## 🎬 Vidéo de démonstration

> 🎥 **Lien vers la vidéo :** `https://` *(à compléter)*  
> *(Hébergée en mode privé sur YouTube / Google Drive)*

---

## 📄 Rapport

Le rapport complet du projet (choix des sources, processus de récupération, présentation de l'interface) est disponible dans le fichier `rapport.pdf` à la racine du dépôt.

---

## 📝 Licence

Ce projet est réalisé dans le cadre d'une SAE universitaire. Tous droits réservés aux auteurs.
