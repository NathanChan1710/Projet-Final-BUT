# app.py — Point d'entrée France Comparateur
# Lancement : streamlit run app.py

import streamlit as st
import pandas as pd
from pathlib import Path

from dsfr import inject_css, render_header, render_navbar, render_footer

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data" / "processed"


@st.cache_data(show_spinner=False)
def load_villes_master():
    df = pd.read_excel(DATA_DIR / "donnees_generale_filtrer.xlsx", usecols=["nom_standard"])
    return sorted(df["nom_standard"].dropna().unique().tolist())


def _sync_global_ville1():
    st.session_state["global_ville1"] = st.session_state["ville1_selector"]


def _sync_global_ville2():
    st.session_state["global_ville2"] = st.session_state["ville2_selector"]


# ── Configuration (une seule fois, ici) ───────────────────────────────────────
st.set_page_config(
    page_title="France Comparateur",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS + En-tête gouvernemental ──────────────────────────────────────────────
inject_css()
render_header("Comparateur de communes françaises — données publiques")

# ── Routing via query param ?page=xxx ─────────────────────────────────────────
params       = st.query_params
active_page  = params.get("page", "accueil")
# Valider la page (évite les valeurs inconnues)
PAGES_VALIDES = {"accueil","donnees","meteo", "education", "logement","sport","emploi","culture"}
if active_page not in PAGES_VALIDES:
    active_page = "accueil"

# ── Navbar ────────────────────────────────────────────────────────────────────
render_navbar(active_page)

# ── Sélecteur de villes global (masqué sur l'accueil) ────────────────────────
if active_page != "accueil":
    villes_master = load_villes_master()
    _def1 = "Colombes" if "Colombes" in villes_master else villes_master[0]
    _def2 = "Angers"   if "Angers"   in villes_master else villes_master[1]

    if "global_ville1" not in st.session_state or st.session_state["global_ville1"] not in villes_master:
        st.session_state["global_ville1"] = _def1
    if "global_ville2" not in st.session_state or st.session_state["global_ville2"] not in villes_master:
        st.session_state["global_ville2"] = _def2
    if "ville1_selector" not in st.session_state or st.session_state["ville1_selector"] != st.session_state["global_ville1"]:
        st.session_state["ville1_selector"] = st.session_state["global_ville1"]
    if "ville2_selector" not in st.session_state or st.session_state["ville2_selector"] != st.session_state["global_ville2"]:
        st.session_state["ville2_selector"] = st.session_state["global_ville2"]

    st.markdown("""
<style>
.ville-label-1 { font-size:0.65rem; font-weight:700; color:#000091;
    text-transform:uppercase; letter-spacing:0.08em; margin-bottom:2px; }
.ville-label-2 { font-size:0.65rem; font-weight:700; color:#E1000F;
    text-transform:uppercase; letter-spacing:0.08em; margin-bottom:2px; }
</style>""", unsafe_allow_html=True)

    gc1, gc2 = st.columns(2)
    with gc1:
        st.markdown('<div class="ville-label-1">● VILLE 1</div>', unsafe_allow_html=True)
        st.selectbox("Ville 1", villes_master,
                     key="ville1_selector", on_change=_sync_global_ville1,
                     label_visibility="collapsed")
    with gc2:
        st.markdown('<div class="ville-label-2">● VILLE 2</div>', unsafe_allow_html=True)
        st.selectbox("Ville 2", villes_master,
                     key="ville2_selector", on_change=_sync_global_ville2,
                     label_visibility="collapsed")


# ── Rendu de la page active ───────────────────────────────────────────────────

if active_page == "accueil":
    import accueil
    accueil.render()

elif active_page == "donnees":
    import donnees_generales
    donnees_generales.render()

elif active_page == "meteo":
    import meteo
    meteo.render()

elif active_page == "education":
    import education
    education.render()
    
elif active_page == "logement":
    import logement
    logement.render()

elif active_page == "sport":
    import sport
    sport.render()

elif active_page == "emploi":
    import emploi
    emploi.render()

elif active_page == "culture":
    import culture
    culture.render()
# ── Footer ────────────────────────────────────────────────────────────────────
render_footer("Open-Meteo (archive &amp; prévisions), INSEE, data.gouv.fr")
