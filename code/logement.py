# logement.py — Page "Logement" · France Comparateur
# Appelé depuis app.py via logement.render()

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from dsfr import BLEU, ROUGE, VERT, GRIS_F, GRIS_B, TEXTE, metric_box

from pathlib import Path
BASE_DIR = Path(__file__).parent          # dossier code/
DATA_DIR = BASE_DIR.parent / "data" / "processed"


# ── Couleurs propres à cette page ─────────────────────────────────────────────
Ville1 = "#000091"   # bleu DSFR
Ville2   = "#E1000F"   # rouge DSFR
BORDER   = GRIS_B


# ── Chargement des données ────────────────────────────────────────────────────
@st.cache_data
def load_logement():
    return pd.read_excel(DATA_DIR / "logement_filtrer.xlsx")


# ── CSS spécifique à la page ──────────────────────────────────────────────────
def _inject_page_css():
    st.markdown(f"""
<style>
/* ── Bandeau KPI ── */
.kpi-strip {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0;
    border: 1px solid {GRIS_B};
    margin-bottom: 28px;
}}
.kpi-item {{
    padding: 16px 20px;
    border-right: 1px solid {GRIS_B};
    background: white;
}}
.kpi-item:last-child {{ border-right: none; }}
.kpi-label {{
    font-size: 0.67rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #666;
    margin-bottom: 6px;
}}
.kpi-value {{
    font-size: 1.5rem;
    font-weight: 700;
    color: {TEXTE};
    line-height: 1.1;
}}
.kpi-sub {{
    font-size: 0.72rem;
    color: #888;
    margin-top: 4px;
}}

/* ── Synthèse ── */
.synth-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 20px;
}}
.synth-item {{
    background: white;
    border: 1px solid {GRIS_B};
    padding: 16px 20px;
}}
.synth-city {{
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid {GRIS_B};
}}
.synth-city.Ville1 {{ color: {Ville1}; border-bottom-color: {Ville1}; }}
.synth-city.Ville2   {{ color: {Ville2};   border-bottom-color: {Ville2};   }}
.synth-row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 5px 0;
    border-bottom: 1px solid {GRIS_F};
    font-size: 0.82rem;
}}
.synth-row:last-child {{ border-bottom: none; }}
.synth-row-label {{ color: #555; }}
.synth-row-value {{ font-weight: 700; color: {TEXTE}; }}

/* ── Bloc insight ── */
.insight {{
    background: {GRIS_F};
    border-left: 4px solid {BLEU};
    padding: 14px 18px;
    font-size: 0.86rem;
    line-height: 1.65;
    color: {TEXTE};
    margin-top: 4px;
}}

/* ── Séparateur ── */
.page-divider {{
    border: none;
    border-top: 2px solid {GRIS_B};
    margin: 28px 0;
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


# ── Layout commun pour les graphiques Plotly ──────────────────────────────────
def _base_layout(height=360, ytitle=""):
    return dict(
        barmode="group",
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        margin=dict(t=20, b=10, l=10, r=10),
        legend=dict(orientation="h", y=-0.18, x=0),
        yaxis=dict(title=ytitle, gridcolor="#f3f4f6", tickfont=dict(size=11)),
        xaxis=dict(gridcolor="#f3f4f6", linecolor=BORDER, linewidth=1),
        height=height,
        font=dict(family="'Source Sans Pro', Arial, sans-serif"),
        bargap=0.25,
        bargroupgap=0.08,
    )


def _bar_trace(name, x, y, color):
    return go.Bar(
        name=name, x=x, y=y,
        marker_color=color,
        text=[f"{int(v):,} €" if isinstance(v, float) else f"{int(v):,}" for v in y],
        textposition="outside",
        textfont=dict(size=11),
    )


# ── Onglet détail par type ────────────────────────────────────────────────────
def _make_tab(tab, nb_c, moy_c, med_c, nb_a, moy_a, med_a):
    with tab:
        labels = ["Nb ventes", "Prix moyen (€/m²)", "Prix médian (€/m²)"]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Ville1", x=labels, y=[nb_c, moy_c, med_c],
            marker_color=Ville1,
            text=[f"{int(nb_c):,}", f"{int(moy_c):,} €", f"{int(med_c):,} €"],
            textposition="outside",
        ))
        fig.add_trace(go.Bar(
            name="Ville2", x=labels, y=[nb_a, moy_a, med_a],
            marker_color=Ville2,
            text=[f"{int(nb_a):,}", f"{int(moy_a):,} €", f"{int(med_a):,} €"],
            textposition="outside",
        ))
        layout = _base_layout(height=320)
        layout["bargap"] = 0.3
        layout.pop("bargroupgap", None)
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)


# ── CSS sélecteurs de ville ───────────────────────────────────────────────────
def _inject_selector_css():
    st.markdown(f"""
<style>
.selector-label {{
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 4px;
}}
.selector-label.ville1 {{ color: {Ville1}; }}
.selector-label.ville2 {{ color: {Ville2}; }}
.selector-label.indic  {{ color: #444; }}
.warning-box {{
    background: #fefce8;
    border: 1px solid #fde68a;
    padding: 10px 16px;
    font-size: 0.82rem;
    color: #92400e;
    margin-bottom: 16px;
}}
</style>
""", unsafe_allow_html=True)


# ── Point d'entrée appelé par app.py ─────────────────────────────────────────
def render():
    _inject_page_css()
    _inject_selector_css()

    dl     = load_logement()
    villes = sorted(dl["libelle_geo"].dropna().unique().tolist())

    # ── Titre de section DSFR ─────────────────────────────────────────────────
    st.markdown(
        '<div class="section-title">Logement'
        '<span class="section-sub">Marché immobilier · DVF · data.gouv.fr</span></div>',
        unsafe_allow_html=True,
    )

    # ── Sélecteurs de villes ──────────────────────────────────────────────────
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div class="selector-label ville1">VILLE 1</div>', unsafe_allow_html=True)
        ville1 = st.selectbox(
            "Ville 1", villes,
            index=villes.index("Ville1") if "Ville1" in villes else 0,
            key="log_ville1", label_visibility="collapsed",
        )
    with s2:
        st.markdown('<div class="selector-label ville2">VILLE 2</div>', unsafe_allow_html=True)
        default2 = "Ville2" if "Ville2" in villes else (villes[1] if len(villes) > 1 else villes[0])
        ville2 = st.selectbox(
            "Ville 2", villes,
            index=villes.index(default2),
            key="log_ville2", label_visibility="collapsed",
        )
    with s3:
        st.markdown('<div class="selector-label indic">INDICATEUR</div>', unsafe_allow_html=True)
        st.selectbox(
            "Indicateur", ["Prix au m²"],
            key="log_indic", label_visibility="collapsed",
        )

    # ── Garde-fou : deux villes différentes ──────────────────────────────────
    if ville1 == ville2:
        st.markdown(
            '<div class="warning-box">⚠️ Veuillez choisir deux villes différentes.</div>',
            unsafe_allow_html=True,
        )
        return

    col_l = dl[dl["libelle_geo"] == ville1].iloc[0]
    ang_l = dl[dl["libelle_geo"] == ville2].iloc[0]

    diff_apt = int(col_l["moy_prix_m2_whole_appartement"] - ang_l["moy_prix_m2_whole_appartement"])
    diff_pct = round(diff_apt / ang_l["moy_prix_m2_whole_appartement"] * 100, 1)
    sign     = "+" if diff_pct >= 0 else ""

    # ── KPI synthétiques ──────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    metric_box(c1, f"Prix m² appt. — {ville1}",
               f"{int(col_l['moy_prix_m2_whole_appartement']):,} €")
    metric_box(c2, f"Prix m² appt. — {ville2}",
               f"{int(ang_l['moy_prix_m2_whole_appartement']):,} €", theme="rouge")
    metric_box(c3, f"Médiane appt. — {ville1}",
               f"{int(col_l['med_prix_m2_whole_appartement']):,} €/m²")
    metric_box(c4, "Écart appartements",
               f"{sign}{diff_pct} %", theme="vert")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bandeau KPI HTML ─────────────────────────────────────────────────────
    st.markdown(f"""
<div class="kpi-strip">
  <div class="kpi-item">
    <div class="kpi-label" style="color:{Ville1}">{ville1} · Prix m² appt.</div>
    <div class="kpi-value">{int(col_l['moy_prix_m2_whole_appartement']):,} €</div>
    <div class="kpi-sub">Médiane : {int(col_l['med_prix_m2_whole_appartement']):,} €/m²</div>
  </div>
  <div class="kpi-item">
    <div class="kpi-label" style="color:{Ville2}">{ville2} · Prix m² appt.</div>
    <div class="kpi-value">{int(ang_l['moy_prix_m2_whole_appartement']):,} €</div>
    <div class="kpi-sub">Médiane : {int(ang_l['med_prix_m2_whole_appartement']):,} €/m²</div>
  </div>
  <div class="kpi-item">
    <div class="kpi-label">Écart appartements</div>
    <div class="kpi-value">{sign}{diff_pct} %</div>
    <div class="kpi-sub">{ville1} est {sign}{diff_apt:,} €/m² {'plus chère' if diff_apt >= 0 else 'moins chère'}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Graphiques côte à côte ────────────────────────────────────────────────
    st.markdown(
        '<div class="section-title" style="font-size:0.75rem">Prix moyen au m² par type de bien</div>',
        unsafe_allow_html=True,
    )

    categories = ["Appartements", "Maisons", "Ensemble"]
    col_vals   = [
        col_l["moy_prix_m2_whole_appartement"],
        col_l["moy_prix_m2_whole_maison"],
        col_l["moy_prix_m2_whole_apt_maison"],
    ]
    ang_vals   = [
        ang_l["moy_prix_m2_whole_appartement"],
        ang_l["moy_prix_m2_whole_maison"],
        ang_l["moy_prix_m2_whole_apt_maison"],
    ]

    fig1 = go.Figure()
    fig1.add_trace(_bar_trace("Ville1", categories, col_vals, Ville1))
    fig1.add_trace(_bar_trace("Ville2",   categories, ang_vals, Ville2))
    fig1.update_layout(**_base_layout(ytitle="€/m²"))

    types  = ["Appartements", "Maisons", "Locaux"]
    col_nb = [col_l["nb_ventes_whole_appartement"], col_l["nb_ventes_whole_maison"], col_l["nb_ventes_whole_local"]]
    ang_nb = [ang_l["nb_ventes_whole_appartement"], ang_l["nb_ventes_whole_maison"], ang_l["nb_ventes_whole_local"]]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="Ville1", x=types, y=col_nb,
        marker_color=Ville1,
        text=[f"{int(v):,}" for v in col_nb],
        textposition="outside", textfont=dict(size=11),
    ))
    fig2.add_trace(go.Bar(
        name="Ville2", x=types, y=ang_nb,
        marker_color=Ville2,
        text=[f"{int(v):,}" for v in ang_nb],
        textposition="outside", textfont=dict(size=11),
    ))
    fig2.update_layout(**_base_layout(ytitle="Nb transactions"))

    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(fig1, use_container_width=True, key="prix_m2")
    with g2:
        st.markdown(
            '<div class="section-title" style="font-size:0.75rem">Volumes de transactions</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig2, use_container_width=True, key="volumes")

    # ── Onglets détail ────────────────────────────────────────────────────────
    st.markdown('<div class="page-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Détail par type de bien</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Appartements", "Maisons", "Locaux commerciaux"])

    _make_tab(
        tab1,
        col_l["nb_ventes_whole_appartement"], col_l["moy_prix_m2_whole_appartement"], col_l["med_prix_m2_whole_appartement"],
        ang_l["nb_ventes_whole_appartement"], ang_l["moy_prix_m2_whole_appartement"], ang_l["med_prix_m2_whole_appartement"],
    )
    _make_tab(
        tab2,
        col_l["nb_ventes_whole_maison"], col_l["moy_prix_m2_whole_maison"], col_l["med_prix_m2_whole_maison"],
        ang_l["nb_ventes_whole_maison"], ang_l["moy_prix_m2_whole_maison"], ang_l["med_prix_m2_whole_maison"],
    )
    _make_tab(
        tab3,
        col_l["nb_ventes_whole_local"], col_l["moy_prix_m2_whole_local"], col_l["med_prix_m2_whole_local"],
        ang_l["nb_ventes_whole_local"], ang_l["moy_prix_m2_whole_local"], ang_l["med_prix_m2_whole_local"],
    )

    # ── Synthèse ──────────────────────────────────────────────────────────────
    st.markdown('<div class="page-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Synthèse</div>',
        unsafe_allow_html=True,
    )

    ratio_apt   = round(col_l["moy_prix_m2_whole_appartement"] / ang_l["moy_prix_m2_whole_appartement"], 1)
    ratio_mais  = round(col_l["moy_prix_m2_whole_maison"]      / ang_l["moy_prix_m2_whole_maison"],      1)
    pct_apt_col = round(col_l["nb_ventes_whole_appartement"]    / col_l["nb_ventes_whole_apt_maison"] * 100, 0)
    pct_apt_ang = round(ang_l["nb_ventes_whole_appartement"]    / ang_l["nb_ventes_whole_apt_maison"] * 100, 0)
    ratio_vol   = round(ang_l["nb_ventes_whole_apt_maison"]     / col_l["nb_ventes_whole_apt_maison"],    1)

    st.markdown(f"""
<div class="synth-grid">
  <div class="synth-item">
    <div class="synth-city Ville1">{ville1}</div>
    <div class="synth-row">
      <span class="synth-row-label">Prix m² moyen appartements</span>
      <span class="synth-row-value">{int(col_l['moy_prix_m2_whole_appartement']):,} €</span>
    </div>
    <div class="synth-row">
      <span class="synth-row-label">Prix m² moyen maisons</span>
      <span class="synth-row-value">{int(col_l['moy_prix_m2_whole_maison']):,} €</span>
    </div>
    <div class="synth-row">
      <span class="synth-row-label">Transactions (appt + maisons)</span>
      <span class="synth-row-value">{int(col_l['nb_ventes_whole_apt_maison']):,}</span>
    </div>
    <div class="synth-row">
      <span class="synth-row-label">Part appartements</span>
      <span class="synth-row-value">{pct_apt_col:.0f} %</span>
    </div>
  </div>
  <div class="synth-item">
    <div class="synth-city Ville2">{ville2}</div>
    <div class="synth-row">
      <span class="synth-row-label">Prix m² moyen appartements</span>
      <span class="synth-row-value">{int(ang_l['moy_prix_m2_whole_appartement']):,} €</span>
    </div>
    <div class="synth-row">
      <span class="synth-row-label">Prix m² moyen maisons</span>
      <span class="synth-row-value">{int(ang_l['moy_prix_m2_whole_maison']):,} €</span>
    </div>
    <div class="synth-row">
      <span class="synth-row-label">Transactions (appt + maisons)</span>
      <span class="synth-row-value">{int(ang_l['nb_ventes_whole_apt_maison']):,}</span>
    </div>
    <div class="synth-row">
      <span class="synth-row-label">Part appartements</span>
      <span class="synth-row-value">{pct_apt_ang:.0f} %</span>
    </div>
  </div>
</div>
<div class="insight">
  Les appartements coûtent <strong>{ratio_apt}× {'plus cher' if ratio_apt >= 1 else 'moins cher'}</strong> à {ville1} qu'à {ville2},
  les maisons <strong>{ratio_mais}×</strong>. {ville2} enregistre un volume de transactions
  <strong>{ratio_vol}× {'supérieur' if ratio_vol >= 1 else 'inférieur'}</strong> à celui de {ville1}.
  Dans les deux villes, prix moyen et médian sont proches, signe de marchés homogènes.
</div>
""", unsafe_allow_html=True)

    # ── Source ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="pg-source">'
        "Source : DVF · Demandes de Valeurs Foncières · data.gouv.fr · Traitements France Compare · 2026"
        "</div>",
        unsafe_allow_html=True,
    )