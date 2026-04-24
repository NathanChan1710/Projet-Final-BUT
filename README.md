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
├── code/                              
│   ├── app.py                         
│   ├── dsfr.py                        
│   ├── accueil.py                     
│   ├── donnees_generales.py           
│   ├── education.py                   
│   ├── emploi.py                      
│   ├── logement.py                    
│   ├── meteo.py                       
│   └── sport.py                       
│
├── data/
│   └── processed/                     # Données nettoyées pour l'interface web
│       ├── coordonnees_villes.xlsx    # Coordonnées géographiques des communes (API météo)
│       ├── culture_filtrer.xlsx       
│       ├── donnees_generale_filtrer.xlsx  
│       ├── education_filtrer.xlsx     
│       ├── emploi.parquet             
│       ├── emploi.xlsx                
│       ├── logement_filtrer.xlsx      
│       └── sport.xlsx                 
│
├── notebooks/                         # Exploration et préparation des données
│   └── nettoyage des données.ipynb    # Nettoyage et filtrage des données brutes data/processed
│   ├── analyse rapide.ipynb           # Analyse exploratoire rapide des jeux de données pour le dashboard
│
├── .gitignore
├── README.md
└── requirements.txt                   # Dépendances Python
```

---

## Sources de données

| Thème | Source |
|-------|--------|
| Etablissements scolaires | [data.gouv.fr — Annuaire de l'éducation](https://data.sports.gouv.fr/explore/dataset/annuaire-de-l-education/table/?disjunctive.type_etablissement&disjunctive.libelle_academie&disjunctive.libelle_departement&disjunctive.libelle_region&disjunctive.ministere_tutelle&disjunctive.appartenance_education_prioritaire&disjunctive.nom_commune&disjunctive.code_postal&disjunctive.code_departement) |
| Météo historique | [Open-Meteo Archive API](https://archive-api.open-meteo.com/) |
| Prévisions météo | [Open-Meteo Forecast API](https://api.open-meteo.com/) |
| Logement / transactions | [DVF — data.gouv.fr](https://www.data.gouv.fr/datasets/logement-encadrement-des-loyers) |
| Emploi | [open.urssaf.fr](https://open.urssaf.fr/explore/dataset/etablissements-et-effectifs-salaries-au-niveau-commune-x-ape-last/table/) |
| Culture | [data.gouv.fr](https://www.data.gouv.fr/datasets/base-permanente-des-equipements-1) |
| Sport | [data.sports.gouv.fr](https://data.sports.gouv.fr/explore/dataset/equipements-sportifs/table/?sort=inst_numero) |

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

La navigation entre pages se fait via la barre en haut de l'interface (données générales, météo, etc...).
Il faut séléctionner 2 villes différentes dans chaque onglet, pour les comparer, 

---

## Difficutlé rencontré 
🔹 Données de transport
Nous avions prévu une page dédiée aux transports, mais les données disponibles étaient trop fragmentées (SNCF, IDF Mobilités, réseaux locaux…).
Les jeux de données étaient souvent régionaux, rarement communaux, et impossibles à harmoniser pour toutes les villes.
Nous avons donc abandonné cette fonctionnalité après plusieurs recherches non concluantes.

🔹 Harmonisation des pages
Chaque membre a développé ses pages séparément, puis nous les avons intégrées dans l’application.
Maque de cohésion dans les filtres, on aimerait améliorer cela en faisant 2 sélecteurs qui restent entre chaque onglet.
Toute la mise en forme (charte DSFR, composants, styles) est centralisée dans dsfr.py, ce qui garantit une interface cohérente et simplifie le développement des pages.