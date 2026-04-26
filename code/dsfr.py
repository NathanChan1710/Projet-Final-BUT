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


def inject_css():
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

    /* ── Bouton primaire (CTA accueil) ── */
    .stButton > button[kind="primary"] {{
        background: {BLEU} !important; color: white !important;
        border-bottom: none !important; font-size: 1rem !important;
        padding: 14px 32px !important; letter-spacing: 0.04em !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: #0000c8 !important; color: white !important;
        border-bottom: none !important;
    }}

    /* ── Footer ── */
    .gov-footer {{
        margin-top: 48px; border-top: 1px solid {GRIS_B};
        padding: 20px 0 14px; font-size: 0.7rem; color: #888; text-align: center;
    }}
    .footer-cards {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
        margin-bottom: 18px;
        text-align: left;
    }}
    .footer-card {{
        background: white;
        border: 1px solid {GRIS_B};
        border-top: 3px solid {BLEU};
        padding: 14px 16px;
        min-height: 140px;
    }}
    .footer-card-title {{
        font-size: 0.85rem;
        font-weight: 700;
        color: {BLEU};
        margin-bottom: 10px;
    }}
    .footer-card-links {{
        display: flex;
        flex-direction: column;
        gap: 8px;
    }}
    .footer-card-link {{
        color: {TEXTE} !important;
        text-decoration: none !important;
        font-size: 0.8rem;
        border-bottom: 1px solid {GRIS_B};
        padding-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .footer-card-link:hover {{
        color: {BLEU} !important;
        border-bottom-color: {BLEU};
    }}
    .footer-link-icon {{
        width: 16px;
        height: 16px;
        flex: 0 0 16px;
        display: inline-block;
    }}
    .footer-link-icon svg {{
        width: 16px;
        height: 16px;
        fill: currentColor;
    }}
    .footer-project-box {{
        margin: 0 auto 18px;
        max-width: 420px;
        background: white;
        border: 1px solid {GRIS_B};
        border-top: 3px solid {ROUGE};
        padding: 14px 16px;
        text-align: center;
    }}
    .footer-project-title {{
        font-size: 0.78rem;
        font-weight: 700;
        color: {BLEU};
        text-transform: uppercase;
        margin-bottom: 6px;
    }}
    .footer-project-text {{
        font-size: 0.78rem;
        color: #666;
        margin-bottom: 12px;
    }}
    .footer-project-link {{
        display: inline-block;
        min-width: 220px;
        padding: 10px 16px;
        background: {BLEU};
        color: white !important;
        text-decoration: none !important;
        text-align: center;
        font-size: 0.8rem;
        font-weight: 700;
    }}
    .footer-project-link:hover {{
        background: #0000c8;
    }}
    @media (max-width: 900px) {{
        .footer-cards {{
            grid-template-columns: 1fr;
        }}
    }}
</style>
""", unsafe_allow_html=True)


def render_header(tagline: str = "Comparateur de communes françaises"):
    """Bandeau tricolore + en-tête gouvernemental."""
    st.markdown('<div class="bandeau"></div>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="gov-header">
    <div class="rf-logo">République<br>Française</div>
    <div class="app-block">
        <div class="app-name">France Comparateur</div>
        <div class="app-tagline">{tagline}</div>
    </div>
</div>
""", unsafe_allow_html=True)


def render_navbar(active_page: str):
    """Navbar horizontale DSFR — boutons stylisés fond blanc / texte bleu."""
    pages = [
        ("accueil",   "Accueil"),
        ("donnees",   "Données générales"),
        ("meteo",     "Météo"),
        ("education", "Éducation"),
        ("sport",     "Sport"),
        ("emploi",    "Emploi"),
        ("culture",   "Culture"),
        ("logement",  "Logement"),
    ]

    st.markdown("""<style>
    .stButton > button {
        background:#ffffff !important; color:#000091 !important;
        border:none !important; border-radius:0 !important;
        border-bottom:3px solid transparent !important;
        font-size:0.72rem !important; font-weight:700 !important;
        text-transform:uppercase !important; letter-spacing:0.06em !important;
        padding:12px 4px !important; width:100% !important;
        transition:border-bottom 0.15s !important;
    }
    .stButton > button:hover {
        background:#f0f0f8 !important; color:#000091 !important;
        border-bottom:3px solid #000091 !important;
    }
    .nav-active-tab {
        background:#f0f0f8; color:#000091;
        font-size:0.72rem; font-weight:700;
        text-transform:uppercase; letter-spacing:0.06em;
        padding:12px 4px; border-bottom:3px solid #E1000F;
        text-align:center; display:flex;
        align-items:center; justify-content:center; min-height:44px;
    }
    </style>""", unsafe_allow_html=True)

    cols = st.columns(len(pages))
    for i, (key, label) in enumerate(pages):
        with cols[i]:
            if key == active_page:
                st.markdown(
                    f'<div class="nav-active-tab">{label}</div>',
                    unsafe_allow_html=True,
                )
            else:
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    st.query_params["page"] = key
                    st.rerun()



def render_footer(source: str = "Open-Meteo, INSEE, data.gouv.fr"):
    st.markdown(f"""
<div class="gov-footer">
    <div class="footer-cards">
        <div class="footer-card">
            <div class="footer-card-title">Nathan Chan Sing Man</div>
            <div class="footer-card-links">
                <a class="footer-card-link" href="https://www.linkedin.com/in/nathan-chan-sing-man-560b10272/" target="_blank" rel="noopener noreferrer">
                    <span class="footer-link-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3A2 2 0 0 1 21 5V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19V5A2 2 0 0 1 5 3H19M8.34 17V10.66H6.23V17H8.34M7.29 9.8A1.23 1.23 0 1 0 7.29 7.34A1.23 1.23 0 0 0 7.29 9.8M17 17V13.5C17 11.63 16 10.42 14.16 10.42A2.5 2.5 0 0 0 11.9 11.66V10.66H9.79V17H11.9V13.79C11.9 12.94 12.06 12.11 13.12 12.11C14.16 12.11 14.17 13.08 14.17 13.84V17H17Z"/></svg>
                    </span>
                    <span>LinkedIn</span>
                </a>
                <a class="footer-card-link" href="https://github.com/NathanChan1710" target="_blank" rel="noopener noreferrer">
                    <span class="footer-link-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2A10 10 0 0 0 8.84 21.5C9.34 21.59 9.5 21.28 9.5 21V19.31C6.73 19.91 6.14 18 6.14 18C5.68 16.81 5 16.5 5 16.5C4.09 15.88 5.07 15.89 5.07 15.89C6.08 15.96 6.61 16.93 6.61 16.93C7.5 18.45 8.97 18 9.54 17.76C9.63 17.11 9.89 16.66 10.18 16.41C7.97 16.16 5.65 15.3 5.65 11.5C5.65 10.39 6.04 9.5 6.68 8.8C6.58 8.55 6.24 7.53 6.78 6.16C6.78 6.16 7.62 5.9 9.5 7.17C10.29 6.95 11.15 6.84 12 6.84C12.85 6.84 13.71 6.95 14.5 7.17C16.38 5.9 17.22 6.16 17.22 6.16C17.76 7.53 17.42 8.55 17.32 8.8C17.96 9.5 18.35 10.39 18.35 11.5C18.35 15.31 16.02 16.15 13.81 16.4C14.17 16.71 14.5 17.33 14.5 18.29V21C14.5 21.28 14.66 21.6 15.17 21.5A10 10 0 0 0 12 2Z"/></svg>
                    </span>
                    <span>GitHub</span>
                </a>
                <a class="footer-card-link" href="https://nathanchansingman.netlify.app/" target="_blank" rel="noopener noreferrer">
                    <span class="footer-link-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2A10 10 0 1 0 22 12A10 10 0 0 0 12 2M18.93 11H15.96A15.9 15.9 0 0 0 14.82 5.73A8.03 8.03 0 0 1 18.93 11M12 4.06C12.83 5.26 13.5 7.03 13.83 11H10.17C10.5 7.03 11.17 5.26 12 4.06M9.18 5.73A15.9 15.9 0 0 0 8.04 11H5.07A8.03 8.03 0 0 1 9.18 5.73M5.07 13H8.04A15.9 15.9 0 0 0 9.18 18.27A8.03 8.03 0 0 1 5.07 13M12 19.94C11.17 18.74 10.5 16.97 10.17 13H13.83C13.5 16.97 12.83 18.74 12 19.94M14.82 18.27A15.9 15.9 0 0 0 15.96 13H18.93A8.03 8.03 0 0 1 14.82 18.27Z"/></svg>
                    </span>
                    <span>Portfolio</span>
                </a>
            </div>
        </div>
        <div class="footer-card">
            <div class="footer-card-title">Manohy Ratsimba</div>
            <div class="footer-card-links">
                <a class="footer-card-link" href="https://www.linkedin.com/in/manohy-ratsimba-6a2b592b0/" target="_blank" rel="noopener noreferrer">
                    <span class="footer-link-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3A2 2 0 0 1 21 5V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19V5A2 2 0 0 1 5 3H19M8.34 17V10.66H6.23V17H8.34M7.29 9.8A1.23 1.23 0 1 0 7.29 7.34A1.23 1.23 0 0 0 7.29 9.8M17 17V13.5C17 11.63 16 10.42 14.16 10.42A2.5 2.5 0 0 0 11.9 11.66V10.66H9.79V17H11.9V13.79C11.9 12.94 12.06 12.11 13.12 12.11C14.16 12.11 14.17 13.08 14.17 13.84V17H17Z"/></svg>
                    </span>
                    <span>LinkedIn</span>
                </a>
                <a class="footer-card-link" href="https://github.com/manxhyrt" target="_blank" rel="noopener noreferrer">
                    <span class="footer-link-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2A10 10 0 0 0 8.84 21.5C9.34 21.59 9.5 21.28 9.5 21V19.31C6.73 19.91 6.14 18 6.14 18C5.68 16.81 5 16.5 5 16.5C4.09 15.88 5.07 15.89 5.07 15.89C6.08 15.96 6.61 16.93 6.61 16.93C7.5 18.45 8.97 18 9.54 17.76C9.63 17.11 9.89 16.66 10.18 16.41C7.97 16.16 5.65 15.3 5.65 11.5C5.65 10.39 6.04 9.5 6.68 8.8C6.58 8.55 6.24 7.53 6.78 6.16C6.78 6.16 7.62 5.9 9.5 7.17C10.29 6.95 11.15 6.84 12 6.84C12.85 6.84 13.71 6.95 14.5 7.17C16.38 5.9 17.22 6.16 17.22 6.16C17.76 7.53 17.42 8.55 17.32 8.8C17.96 9.5 18.35 10.39 18.35 11.5C18.35 15.31 16.02 16.15 13.81 16.4C14.17 16.71 14.5 17.33 14.5 18.29V21C14.5 21.28 14.66 21.6 15.17 21.5A10 10 0 0 0 12 2Z"/></svg>
                    </span>
                    <span>GitHub</span>
                </a>
                <a class="footer-card-link" href="https://portfolio-personne-2.fr" target="_blank" rel="noopener noreferrer">
                    <span class="footer-link-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2A10 10 0 1 0 22 12A10 10 0 0 0 12 2M18.93 11H15.96A15.9 15.9 0 0 0 14.82 5.73A8.03 8.03 0 0 1 18.93 11M12 4.06C12.83 5.26 13.5 7.03 13.83 11H10.17C10.5 7.03 11.17 5.26 12 4.06M9.18 5.73A15.9 15.9 0 0 0 8.04 11H5.07A8.03 8.03 0 0 1 9.18 5.73M5.07 13H8.04A15.9 15.9 0 0 0 9.18 18.27A8.03 8.03 0 0 1 5.07 13M12 19.94C11.17 18.74 10.5 16.97 10.17 13H13.83C13.5 16.97 12.83 18.74 12 19.94M14.82 18.27A15.9 15.9 0 0 0 15.96 13H18.93A8.03 8.03 0 0 1 14.82 18.27Z"/></svg>
                    </span>
                    <span>Portfolio</span>
                </a>
            </div>
        </div>
        <div class="footer-card">
            <div class="footer-card-title">Camille Franceschin</div>
            <div class="footer-card-links">
                <a class="footer-card-link" href="https://www.linkedin.com/in/camille-franceschin-674059357/" target="_blank" rel="noopener noreferrer">
                    <span class="footer-link-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3A2 2 0 0 1 21 5V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19V5A2 2 0 0 1 5 3H19M8.34 17V10.66H6.23V17H8.34M7.29 9.8A1.23 1.23 0 1 0 7.29 7.34A1.23 1.23 0 0 0 7.29 9.8M17 17V13.5C17 11.63 16 10.42 14.16 10.42A2.5 2.5 0 0 0 11.9 11.66V10.66H9.79V17H11.9V13.79C11.9 12.94 12.06 12.11 13.12 12.11C14.16 12.11 14.17 13.08 14.17 13.84V17H17Z"/></svg>
                    </span>
                    <span>LinkedIn</span>
                </a>
                <a class="footer-card-link" href="https://github.com/CamilleFrncn" target="_blank" rel="noopener noreferrer">
                    <span class="footer-link-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2A10 10 0 0 0 8.84 21.5C9.34 21.59 9.5 21.28 9.5 21V19.31C6.73 19.91 6.14 18 6.14 18C5.68 16.81 5 16.5 5 16.5C4.09 15.88 5.07 15.89 5.07 15.89C6.08 15.96 6.61 16.93 6.61 16.93C7.5 18.45 8.97 18 9.54 17.76C9.63 17.11 9.89 16.66 10.18 16.41C7.97 16.16 5.65 15.3 5.65 11.5C5.65 10.39 6.04 9.5 6.68 8.8C6.58 8.55 6.24 7.53 6.78 6.16C6.78 6.16 7.62 5.9 9.5 7.17C10.29 6.95 11.15 6.84 12 6.84C12.85 6.84 13.71 6.95 14.5 7.17C16.38 5.9 17.22 6.16 17.22 6.16C17.76 7.53 17.42 8.55 17.32 8.8C17.96 9.5 18.35 10.39 18.35 11.5C18.35 15.31 16.02 16.15 13.81 16.4C14.17 16.71 14.5 17.33 14.5 18.29V21C14.5 21.28 14.66 21.6 15.17 21.5A10 10 0 0 0 12 2Z"/></svg>
                    </span>
                    <span>GitHub</span>
                </a>
                <a class="footer-card-link" href="https://portfolio-personne-3.fr" target="_blank" rel="noopener noreferrer">
                    <span class="footer-link-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2A10 10 0 1 0 22 12A10 10 0 0 0 12 2M18.93 11H15.96A15.9 15.9 0 0 0 14.82 5.73A8.03 8.03 0 0 1 18.93 11M12 4.06C12.83 5.26 13.5 7.03 13.83 11H10.17C10.5 7.03 11.17 5.26 12 4.06M9.18 5.73A15.9 15.9 0 0 0 8.04 11H5.07A8.03 8.03 0 0 1 9.18 5.73M5.07 13H8.04A15.9 15.9 0 0 0 9.18 18.27A8.03 8.03 0 0 1 5.07 13M12 19.94C11.17 18.74 10.5 16.97 10.17 13H13.83C13.5 16.97 12.83 18.74 12 19.94M14.82 18.27A15.9 15.9 0 0 0 15.96 13H18.93A8.03 8.03 0 0 1 14.82 18.27Z"/></svg>
                    </span>
                    <span>Portfolio</span>
                </a>
            </div>
        </div>
    </div>
    <div class="footer-project-box">
        <div class="footer-project-title">Repo du projet</div>
        <div class="footer-project-text">Accéder au dépôt GitHub de France Comparateur</div>
        <a class="footer-project-link" href="https://github.com/organisation/repo-projet" target="_blank" rel="noopener noreferrer">Voir le repo GitHub</a>
    </div>
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
