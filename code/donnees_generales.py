# donnees_generales.py — Page "Données générales" · France Comparateur
# Appelé depuis app.py via donnees_generales.render()

import streamlit as st
import pandas as pd
import ast

from dsfr import BLEU, ROUGE, VERT, GRIS_F, GRIS_B, TEXTE, metric_box

# ── Couleurs propres à cette page ─────────────────────────────────────────────
COLOMBES = "#000091"   # bleu DSFR
ANGERS   = "#E1000F"   # rouge DSFR


# ── Chargement des données ────────────────────────────────────────────────────
@st.cache_data
def load_general():
    return pd.read_excel("../data/processed/donnees_generale_filtrer.xlsx")


def parse_pres(val):
    """Parse une colonne 'presentation' qui peut contenir une liste Python sérialisée."""
    try:
        items = ast.literal_eval(str(val))
        return items if isinstance(items, list) else [str(val)]
    except Exception:
        return [str(val)]


# ── Carte d'identité ──────────────────────────────────────────────────────────
def render_id_card(row, city_key: str) -> str:
    """
    Génère le HTML d'une carte d'identité communale en suivant la charte DSFR.
    city_key : 'colombes' | 'angers'
    """
    color  = COLOMBES if city_key == "colombes" else ANGERS
    nom    = row["nom_standard"]
    dep    = f"{row['dep_nom']} ({row['dep_code']}) · {row['reg_nom']}"
    insee  = str(row["code_insee"])
    cp     = str(row["code_postal"])
    pop    = f"{int(row['population']):,}".replace(",", "\u202f")
    sup    = f"{row['superficie_km2']} km²"
    dens   = f"{int(row['densite']):,} hab/km²".replace(",", "\u202f")
    alt_m  = int(row["altitude_moyenne"])
    alt_min = int(row["altitude_minimale"])
    alt_max = int(row["altitude_maximale"])
    lat    = f"{round(row['latitude_mairie'], 3)}° N"
    lon    = f"{round(row['longitude_mairie'], 3)}° E"
    epci   = row["epci_nom"]
    acad   = row["academie_nom"]
    equip  = row["niveau_equipements_services_texte"]
    gentil = f"Les {row['gentile']}"
    score  = str(row["score"])
    unite  = row["nom_unite_urbaine"]
    grille = row["grille_densite_texte"]
    url_w  = row["url_wikipedia"]
    url_v  = row["url_villedereve"]

    def field(label, value, sub=None, full=False, colored=False):
        col_cls = "id-field full" if full else "id-field"
        val_style = f' style="color:{color};font-weight:700"' if colored else ""
        sub_html = f'<div class="id-field-sub">{sub}</div>' if sub else ""
        return (
            f'<div class="{col_cls}">'
            f'<div class="id-field-label">{label}</div>'
            f'<div class="id-field-value"{val_style}>{value}</div>'
            f'{sub_html}'
            f'</div>'
        )

    html = f"""
<div class="dsfr-id-card" style="border-top:4px solid {color}">
  <div class="dsfr-id-header">
    <div class="dsfr-id-dot" style="background:{color}"></div>
    <div>
      <div class="dsfr-id-city">{nom}</div>
      <div class="dsfr-id-dep">{dep}</div>
    </div>
  </div>
  <div class="dsfr-id-body">
    {field("Code INSEE",            insee,          colored=True)}
    {field("Code postal",           cp)}
    {field("Gentilé",               gentil)}
    {field("Score VilleDeRêve",     score,          colored=True)}
    {field("Population",            f"{pop} hab.",   colored=True)}
    {field("Superficie",            sup)}
    {field("Densité",               dens)}
    {field("Altitude",              f"{alt_m} m",   sub=f"min {alt_min} m · max {alt_max} m")}
    {field("Coordonnées",           lat,            sub=lon)}
    {field("Unité urbaine",         unite,          sub=grille)}
    {field("EPCI",                  epci,           full=True)}
    {field("Académie",              acad)}
    {field("Niveau d'équipements",  equip,          full=True)}
    <div class="id-field full">
      <div class="id-field-label">Liens</div>
      <div class="id-field-value" style="font-size:0.82rem;font-weight:400">
        <a href="{url_w}" target="_blank"
           style="color:{color};margin-right:16px;text-decoration:underline">
          Wikipédia →
        </a>
        <a href="{url_v}" target="_blank"
           style="color:{color};text-decoration:underline">
          VilleDeRêve →
        </a>
      </div>
    </div>
  </div>
</div>
"""
    return html


# ── CSS spécifique à la page ──────────────────────────────────────────────────
def _inject_page_css():
    st.markdown(f"""
<style>
/* ── Carte d'identité ── */
.dsfr-id-card {{
    background: white;
    border: 1px solid {GRIS_B};
    margin-bottom: 24px;
}}
.dsfr-id-header {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 20px 14px;
    border-bottom: 1px solid {GRIS_B};
    background: {GRIS_F};
}}
.dsfr-id-dot {{
    width: 12px; height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
}}
.dsfr-id-city {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {TEXTE};
    line-height: 1.2;
}}
.dsfr-id-dep {{
    font-size: 0.75rem;
    color: #666;
    margin-top: 2px;
}}
.dsfr-id-body {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0;
    padding: 0;
}}

/* ── Champs ── */
.id-field {{
    padding: 12px 18px;
    border-right: 1px solid {GRIS_B};
    border-bottom: 1px solid {GRIS_B};
}}
.id-field.full {{
    grid-column: 1 / -1;
    border-right: none;
}}
.id-field-label {{
    font-size: 0.65rem;
    font-weight: 700;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}}
.id-field-value {{
    font-size: 0.88rem;
    font-weight: 600;
    color: {TEXTE};
    line-height: 1.4;
}}
.id-field-sub {{
    font-size: 0.75rem;
    color: #888;
    margin-top: 2px;
}}

/* ── Texte de présentation ── */
.presentation-block {{
    background: {GRIS_F};
    border-left: 4px solid {GRIS_B};
    padding: 16px 20px;
    margin-bottom: 28px;
    font-size: 0.88rem;
    line-height: 1.7;
    color: {TEXTE};
}}
.presentation-block p {{
    margin: 0 0 10px;
}}
.presentation-block p:last-child {{
    margin-bottom: 0;
}}

/* ── Séparateur ── */
.page-divider {{
    border: none;
    border-top: 2px solid {GRIS_B};
    margin: 32px 0;
}}

/* ── Titres ── */
.pg-title {{
    font-size: 1.35rem;
    font-weight: 700;
    color: {BLEU};
    margin-bottom: 4px;
}}
.pg-subtitle {{
    font-size: 0.78rem;
    color: #666;
    margin-bottom: 24px;
}}

/* ── Source ── */
.pg-source {{
    margin-top: 32px;
    font-size: 0.7rem;
    color: #aaa;
    text-align: center;
    border-top: 1px solid {GRIS_B};
    padding-top: 12px;
}}
</style>
""", unsafe_allow_html=True)

def render():
    _inject_page_css()

    dg = load_general()

    # ───────────────────────────────────────────────
    # 🔵 Sélecteurs de villes (toutes les villes FR)
    # ───────────────────────────────────────────────
    st.markdown(
        '<div class="section-title">Données générales</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        ville_1 = st.selectbox(
            "Ville 1",
            sorted(dg["nom_standard"].unique()),
            index=sorted(dg["nom_standard"].unique()).index("Colombes") 
            if "Colombes" in dg["nom_standard"].values else 0
        )

    with col2:
        ville_2 = st.selectbox(
            "Ville 2",
            sorted(dg["nom_standard"].unique()),
            index=sorted(dg["nom_standard"].unique()).index("Angers")
            if "Angers" in dg["nom_standard"].values else 1
        )

    # Récupération des lignes
    row1 = dg[dg["nom_standard"] == ville_1].iloc[0]
    row2 = dg[dg["nom_standard"] == ville_2].iloc[0]

    # Couleurs dynamiques
    color1 = COLOMBES
    color2 = ANGERS

    # Sous-titre dynamique
    st.markdown(
        f'<div class="pg-subtitle">Comparaison : {ville_1} · {ville_2}</div>',
        unsafe_allow_html=True,
    )

    # ───────────────────────────────────────────────
    # 🔵 Métriques synthétiques
    # ───────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    metric_box(c1, f"Population — {ville_1}",
               f"{int(row1['population']):,}".replace(",", "\u202f") + " hab.")
    metric_box(c2, f"Population — {ville_2}",
               f"{int(row2['population']):,}".replace(",", "\u202f") + " hab.", theme="rouge")
    metric_box(c3, f"Superficie — {ville_1}",
               f"{row1['superficie_km2']} km²")
    metric_box(c4, f"Superficie — {ville_2}",
               f"{row2['superficie_km2']} km²", theme="rouge")

    st.markdown("<br>", unsafe_allow_html=True)

    # ───────────────────────────────────────────────
    # 🔵 Carte Ville 1
    # ───────────────────────────────────────────────
    st.markdown(render_id_card(row1, "colombes"), unsafe_allow_html=True)
    pres_1 = parse_pres(row1["presentation"])
    st.markdown(
        f'<div class="presentation-block">{"".join(f"<p>{p}</p>" for p in pres_1)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="page-divider"></div>', unsafe_allow_html=True)

    # ───────────────────────────────────────────────
    # 🔵 Carte Ville 2
    # ───────────────────────────────────────────────
    st.markdown(render_id_card(row2, "angers"), unsafe_allow_html=True)
    pres_2 = parse_pres(row2["presentation"])
    st.markdown(
        f'<div class="presentation-block">{"".join(f"<p>{p}</p>" for p in pres_2)}</div>',
        unsafe_allow_html=True,
    )

    # ───────────────────────────────────────────────
    # 🔵 Source
    # ───────────────────────────────────────────────
    st.markdown(
        '<div class="pg-source">'
        "Source : data.gouv.fr · villedereve.fr · Traitements France Compare · 2026"
        "</div>",
        unsafe_allow_html=True,
    )
