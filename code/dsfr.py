# dsfr.py — Charte graphique DSFR partagée
import streamlit as st

# ── Palette ────────────────────────────────────────────────────────────────────
BLEU    = "#000091"
ROUGE   = "#E1000F"
VERT    = "#008941"
GRIS_F  = "#f6f6f6"
GRIS_B  = "#dddddd"
TEXTE   = "#1e1e1e"
COLORS  = ["#000091", "#E1000F", "#008941", "#F28E2B", "#76B7B2", "#EDC948", "#B07AA1"]


def inject_css(active_page: str = "meteo"):
    """Injecte le CSS DSFR global + navbar."""
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Source Sans Pro', Arial, sans-serif;
        color: {TEXTE};
    }}
    .main .block-container {{
        padding: 0 2rem 2rem 2rem !important;
        max-width: 1200px;
    }}
    section[data-testid="stSidebar"] {{ display: none; }}
    header[data-testid="stHeader"]   {{ background: white; }}

    /* ── Bandeau tricolore ── */
    .bandeau {{
        background: linear-gradient(to right,
            {BLEU} 33.33%, #ffffff 33.33%, #ffffff 66.66%, {ROUGE} 66.66%);
        height: 8px; width: 100%; margin-bottom: 0;
    }}

    /* ── En-tête ── */
    .gov-header {{
        background: white;
        border-bottom: 1px solid {GRIS_B};
        padding: 14px 0 12px 0;
        display: flex; align-items: center; gap: 20px;
        margin-bottom: 0;
    }}
    .rf-logo {{
        font-size: 0.55rem; font-weight: 700; text-transform: uppercase;
        color: {BLEU}; text-align: center; line-height: 1.25;
        letter-spacing: 0.04em; border: 2px solid {BLEU};
        padding: 5px 7px; min-width: 56px; flex-shrink: 0;
    }}
    .app-block {{ border-left: 3px solid {ROUGE}; padding-left: 14px; }}
    .app-name  {{ font-size: 1.2rem; font-weight: 700; color: {BLEU}; line-height: 1.2; }}
    .app-tagline {{ font-size: 0.76rem; color: #666; margin-top: 2px; }}

    /* ── Navbar horizontale ── */
    .dsfr-nav {{
        background: {BLEU};
        display: flex; align-items: stretch;
        gap: 0; margin-bottom: 28px;
        border-bottom: 3px solid {ROUGE};
    }}
    .dsfr-nav a {{
        color: rgba(255,255,255,0.78) !important;
        text-decoration: none !important;
        padding: 12px 24px;
        font-size: 0.82rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.07em;
        display: flex; align-items: center; gap: 7px;
        border-bottom: 3px solid transparent;
        transition: background 0.15s, color 0.15s;
        margin-bottom: -3px;
    }}
    .dsfr-nav a:hover {{
        background: rgba(255,255,255,0.10) !important;
        color: white !important;
    }}
    .dsfr-nav a.active {{
        color: white !important;
        border-bottom: 3px solid {ROUGE};
        background: rgba(255,255,255,0.08);
    }}

    /* ── Titres de section ── */
    .section-title {{
        font-size: 0.82rem; font-weight: 700; color: {BLEU};
        text-transform: uppercase; letter-spacing: 0.09em;
        border-bottom: 2px solid {BLEU};
        padding-bottom: 7px; margin: 28px 0 16px;
    }}
    .section-sub {{
        font-weight: 400; color: #555; text-transform: none;
        letter-spacing: 0; font-size: 0.78rem; margin-left: 8px;
    }}

    /* ── Métriques ── */
    .metric-box {{
        background: white; border: 1px solid {GRIS_B};
        border-left: 4px solid {BLEU}; padding: 12px 14px;
    }}
    .metric-box.rouge  {{ border-left-color: {ROUGE}; }}
    .metric-box.vert   {{ border-left-color: {VERT};  }}
    .metric-label {{
        font-size: 0.67rem; font-weight: 700; color: #555;
        text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 4px;
    }}
    .metric-value      {{ font-size: 1.35rem; font-weight: 700; color: {BLEU}; }}
    .metric-box.rouge .metric-value {{ color: {ROUGE}; }}
    .metric-box.vert  .metric-value  {{ color: {VERT};  }}

    /* ── Cartes prévision météo ── */
    .fc-card {{
        background: white; border: 1px solid {GRIS_B};
        border-top: 3px solid {GRIS_B}; padding: 12px 6px; text-align: center;
    }}
    .fc-card.today {{ border-top: 3px solid {BLEU}; background: #f0f0fb; }}
    .fc-day  {{ font-size: 0.65rem; font-weight: 700; color: #666;
               text-transform: uppercase; letter-spacing: 0.08em; }}
    .fc-date {{ font-size: 0.8rem; color: {TEXTE}; margin: 3px 0 8px; }}
    .fc-icon {{ font-size: 1.5rem; line-height: 1; }}
    .fc-cond {{ font-size: 0.6rem; color: #999; margin: 4px 0 6px; }}
    .fc-val  {{ font-size: 1rem; font-weight: 700; color: {BLEU}; }}

    /* ── Badge statut établissement ── */
    .badge-public  {{
        background: #dbeafe; color: #1e40af;
        padding: 2px 9px; border-radius: 0; font-size: 11px; font-weight: 600;
    }}
    .badge-prive {{
        background: #fce7f3; color: #9d174d;
        padding: 2px 9px; border-radius: 0; font-size: 11px; font-weight: 600;
    }}

    /* ── Selectbox DSFR ── */
    .stSelectbox label {{
        font-size: 0.75rem !important; font-weight: 700 !important;
        color: {BLEU} !important; text-transform: uppercase; letter-spacing: 0.06em;
    }}
    div[data-baseweb="select"] > div {{
        border-radius: 0 !important; border-color: {GRIS_B} !important;
    }}
    div[data-baseweb="select"] > div:focus-within {{
        border-color: {BLEU} !important;
        box-shadow: inset 0 -2px 0 0 {BLEU} !important;
    }}
    /* ── Multiselect DSFR ── */
    .stMultiSelect label {{
        font-size: 0.75rem !important; font-weight: 700 !important;
        color: {BLEU} !important; text-transform: uppercase; letter-spacing: 0.06em;
    }}

    /* ── Tableau ── */
    .stDataFrame {{ border: 1px solid {GRIS_B}; }}

    /* ── Footer ── */
    .gov-footer {{
        margin-top: 48px; border-top: 1px solid {GRIS_B};
        padding: 14px 0; font-size: 0.7rem; color: #888; text-align: center;
    }}
</style>
""", unsafe_allow_html=True)


def render_header(tagline: str = "Comparateur de communes françaises"):
    """Bandeau tricolore + en-tête gouvernemental."""
    st.markdown('<div class="bandeau"></div>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="gov-header">
                
<!-- Logo République Française -->
    <div class="rf-logo">
        <img src="Republique-francaise-logo.svg.png" 
             alt="République Française" 
             style="height:70px; margin-right:20px;">
    </div>
        <div class="app-block">
        <div class="app-name">France Comparateur</div>
        <div class="app-tagline">{tagline}</div>
    </div>
</div>
""", unsafe_allow_html=True)


def render_navbar(active_page: str):
    """Navbar horizontale DSFR avec navigation Streamlit (sans nouvel onglet)."""

    pages = [
        ("accueil",     "Accueil"),
        ("donnees",   "Données générales"),
        ("meteo",     "Météo"),
        ("education", "Éducation"),
        ("sport", "Sport"),
        ("emploi", "Emploi"),
        ("culture", "Culture"),
        ("logement",  "Logement")
    ]

    cols = st.columns(len(pages))

    for i, (key, label) in enumerate(pages):
        with cols[i]:

            # Style actif
            if key == active_page:
                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        font-weight:bold;
                        border-bottom:3px solid #000091;
                        padding:8px;
                    ">
                        {label}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                if st.button(label, use_container_width=True):
                    st.query_params["page"] = key
                    st.rerun()



def render_footer(source: str = "Open-Meteo, INSEE, data.gouv.fr"):
    st.markdown(f"""
<div class="gov-footer">
    France Comparateur &nbsp;&bull;&nbsp; Sources : {source}
    &nbsp;&bull;&nbsp; Données publiques — Usage interne
</div>
""", unsafe_allow_html=True)


def metric_box(col, label: str, value, theme: str = "bleu"):
    """Affiche une metric-box DSFR dans une colonne Streamlit."""
    cls = f"metric-box {theme}" if theme != "bleu" else "metric-box"
    with col:
        st.markdown(f"""
<div class="{cls}">
    <div class="metric-label">{label}</div>
    <div class="metric-value">{value}</div>
</div>""", unsafe_allow_html=True)
