# France Comparateur — Outils Décisionnels

Application web interactive de comparaison de communes françaises, développée dans le cadre de la SAE Outils Décisionnels (BUT Science des Données).

**Application déployée :** [projet-final-but3-camille-manohy-nathan.streamlit.app](https://projet-final-but3-camille-manohy-nathan.streamlit.app)

---

## Equipe

| Nom | Prénom |
|-----|--------|
| FRANCESCHIN | Camille |
| RATSIMBA | Manohy |
| CHAN SING MAN | Nathan |

---

## Description

France Comparateur permet de comparer deux communes françaises sur plusieurs données tel que les données générales (population, taille, etc), la météo, l'éducation, les logements, l'emploi et la culture de chaque villes. L'interface s'appuie sur la charte graphique du Système de Design de l'Etat (DSFR) et mobilise des données publiques issues de sources officielles.

---

## Structure du projet


```
Projet-Final-BUT/
│
├── code/                              # Code source de l'application Streamlit
│   ├── app.py                         # Point d'entrée — configuration, routing, navbar et layout global
│   ├── dsfr.py                        # Charte graphique DSFR partagée (palette, CSS, composants réutilisables)
│   ├── accueil.py                     # Page d'accueil de l'application
│   ├── donnees_generales.py           # Page données générales sur les communes
│   ├── education.py                   # Page établissements scolaires (carte, filtres, KPIs)
│   ├── emploi.py                      # Page emploi (taux de chômage, secteurs d'activité)
│   ├── logement.py                    # Page logement (prix au m², transactions DVF)
│   ├── meteo.py                       # Page météo (prévisions 7 jours + historique 12 mois)
│   └── sport.py                       # Page équipements et clubs sportifs
│
├── data/
│   └── processed/                     # Données nettoyées et prêtes à l'emploi
│       ├── coordonnees_villes.xlsx    # Coordonnées géographiques des communes
│       ├── culture_filtrer.xlsx       # Equipements culturels filtrés
│       ├── donnees_generale_filtrer.xlsx  # Données générales INSEE filtrées
│       ├── education_filtrer.xlsx     # Annuaire des établissements scolaires filtré
│       ├── emploi.parquet             # Données emploi au format Parquet (lecture rapide)
│       ├── emploi.xlsx                # Données emploi au format Excel
│       ├── logement_filtrer.xlsx      # Données logement / transactions DVF filtrées
│       └── sport.xlsx                 # Données équipements sportifs
│
├── notebooks/                         # Exploration et préparation des données
│   ├── analyse rapide.ipynb           # Analyse exploratoire rapide des jeux de données
│   └── nettoyage des données.ipynb    # Pipeline de nettoyage et filtrage des données brutes
│
├── .gitignore
├── README.md
└── requirements.txt                   # Dépendances Python
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
Attention, les fichiers bruts ne sont pas commit sur ce repo, il faut les télécharger si on veut avoir les données brut.

### 5. Lancer l'application

```bash
streamlit run app.py
```

L'application est accessible à l'adresse `http://localhost:8501`.

La navigation entre pages se fait via la barre en haut de l'interface sur la navbar (données générales, météo, etc...).

---

## Remarques

- Les appels à l'API Open-Meteo ne nécessitent pas de clé. Les données sont mises en cache 1 heure (`@st.cache_data(ttl=3600)`).
- L'API France Travail requiert une inscription sur [francetravail.io](https://francetravail.io) pour obtenir un `client_id` et un `client_secret`.
