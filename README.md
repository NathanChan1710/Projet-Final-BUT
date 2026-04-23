# France Comparateur — Outils Décisionnels

Application web interactive de comparaison de communes françaises, développée dans le cadre de la SAE Outils Décisionnels (BUT Science des Données).

**Application déployée :** [projet-final-but3-camille-manohy-nathan.streamlit.app](https://projet-final-but3-camille-manohy-nathan.streamlit.app)

---

## Equipe

| Nom | Prénom |
|-----|--------|
| CHANSINGMAN | Nathan |
| FRANCESCHIN | Camille |
| RATSIMBA | Manohy |

---

## Description

France Comparateur permet de comparer deux communes françaises sur plusieurs dimensions : météo, éducation, logement, emploi et données générales. L'interface s'appuie sur la charte graphique du Système de Design de l'Etat (DSFR) et mobilise des données publiques issues de sources officielles.

---

## Structure du projet

```
.
├── app.py                  # Point d'entrée — routing et layout global
├── dsfr.py                 # Charte graphique DSFR partagée (CSS, palette, composants)
├── meteo.py                # Page Météo
├── education.py            # Page Education
├── requirements.txt
├── data/
│   └── processed/          # Fichiers de données prétraités (.xlsx)
└── notebooks/              # Notebooks d'exploration et de préparation des données
```

---

## Sources de données

| Thème | Source |
|-------|--------|
| Etablissements scolaires | [data.gouv.fr — Annuaire de l'éducation](https://www.data.gouv.fr/fr/datasets/annuaire-de-leducation/) |
| Météo historique | [Open-Meteo Archive API](https://archive-api.open-meteo.com/) |
| Prévisions météo | [Open-Meteo Forecast API](https://api.open-meteo.com/) |
| Logement / transactions | [DVF — data.gouv.fr](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/) |
| Emploi | [API France Travail](https://francetravail.io/data/api) |

---

## Installation et lancement en local

### Prérequis

- Python 3.10 ou supérieur
- `pip`

### 1. Cloner le dépôt

```bash
git clone https://github.com/NathanChan1710/Projet-Final-BUT.git
cd Projet-Final-BUT
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales sont :

```
streamlit
pandas
plotly
folium
streamlit-folium
requests
openpyxl
```

### 4. Vérifier la présence des données

Les fichiers de données prétraitées doivent être présents dans `data/processed/` avant de lancer l'application. Si ce dossier est vide, exécutez d'abord les notebooks de préparation situés dans `notebooks/`.

### 5. Lancer l'application

```bash
streamlit run app.py
```

L'application est accessible à l'adresse `http://localhost:8501`.

La navigation entre pages se fait via la barre en haut de l'interface (`Meteo` / `Education`).

---

## Remarques

- Les appels à l'API Open-Meteo ne nécessitent pas de clé. Les données sont mises en cache 1 heure (`@st.cache_data(ttl=3600)`).
- L'API France Travail requiert une inscription sur [francetravail.io](https://francetravail.io) pour obtenir un `client_id` et un `client_secret`. Ces identifiants doivent être renseignés dans les notebooks de collecte ou dans un fichier `.env` (non versionné).
- Le fichier `.env` ne doit pas être commité. Il est déjà référencé dans `.gitignore`.
