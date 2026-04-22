# app.py — Point d'entrée France Comparateur
# Lancement : streamlit run app.py

import streamlit as st

from dsfr import inject_css, render_header, render_navbar, render_footer

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
active_page  = params.get("page", "meteo")

# Valider la page (évite les valeurs inconnues)
PAGES_VALIDES = {"meteo", "education", "donnees", "logement"}
if active_page not in PAGES_VALIDES:
    active_page = "meteo"

# ── Navbar ────────────────────────────────────────────────────────────────────
render_navbar(active_page)

# ── Rendu de la page active ───────────────────────────────────────────────────
if active_page == "meteo":
    import meteo
    meteo.render()

elif active_page == "education":
    import education
    education.render()

elif active_page == "donnees":
    import donnees_generales
    donnees_generales.render()
    
elif active_page == "logement":
    import logement
    logement.render()
# ── Footer ────────────────────────────────────────────────────────────────────
render_footer("Open-Meteo (archive &amp; prévisions), INSEE, data.gouv.fr")
