# emploi.py — Page "Emploi" · France Comparateur
# Appelé depuis app.py via emploi.render()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

from dsfr import BLEU, ROUGE, VERT, GRIS_F, GRIS_B, TEXTE, metric_box
from pathlib import Path
BASE_DIR = Path(__file__).parent          # dossier code/
DATA_DIR = BASE_DIR.parent / "data" / "processed"

# ── Constantes ────────────────────────────────────────────────────────────────
YEARS      = list(range(2006, 2025))
ETAB_COLS  = [f"Nombre d'établissements {y}" for y in YEARS]
SALA_COLS  = [f"Effectifs salariés {y}"       for y in YEARS]
BASE_COLS  = [
    "Région", "Département", "Zone d'emploi", "Nom commune",
    "Grand secteur d'activité", "Secteur NA17", "Secteur NA38",
    "Code commune",
]
# PARQUET_PATH = Path("../data/processed/emploi.parquet")

# ── Layout Plotly DSFR ────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    plot_bgcolor="#fff",
    paper_bgcolor="#fff",
    margin=dict(t=28, b=10, l=10, r=10),
    font=dict(family="'Source Sans Pro', Arial, sans-serif", size=11, color=TEXTE),
    legend=dict(orientation="h", y=-0.18, x=0),
    xaxis=dict(gridcolor=GRIS_F, linecolor=GRIS_B, linewidth=1),
    yaxis=dict(gridcolor=GRIS_F, linecolor=GRIS_B, linewidth=1),
    height=360,
)


# ── Chargement ────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Chargement des données emploi…")
def load_emploi():
    try:
        return pd.read_parquet(DATA_DIR / "emploi.parquet")    
    except FileNotFoundError:
        st.error(f"⚠️ Fichier `{"emploi"}` introuvable.")
        return None
    except Exception as e:
        st.error(f"Erreur de lecture du parquet : {e}")
        return None


# ── CSS spécifique à la page ──────────────────────────────────────────────────
def _inject_page_css():
    st.markdown(f"""
<style>
/* ── Grille KPI emploi ── */
.emploi-kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0;
    border: 1px solid {GRIS_B};
    margin-bottom: 8px;
}}
.emploi-kpi-item {{
    padding: 10px 14px;
    border-right: 1px solid {GRIS_B};
    border-bottom: 1px solid {GRIS_B};
    background: white;
}}
.emploi-kpi-label {{
    font-size: 0.62rem;
    font-weight: 700;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 4px;
}}
.emploi-kpi-value {{
    font-size: 1.05rem;
    font-weight: 700;
}}

/* ── Barre de similitude ── */
.score-bar-wrap {{
    margin: 4px 0 16px;
}}
.score-bar-label {{
    font-size: 0.72rem;
    color: #555;
    margin-bottom: 4px;
}}
.score-bar-track {{
    background: {GRIS_F};
    border: 1px solid {GRIS_B};
    height: 12px;
    width: 100%;
    position: relative;
}}
.score-bar-fill {{
    height: 100%;
    background: {BLEU};
}}
.score-bar-pct {{
    font-size: 0.72rem;
    font-weight: 700;
    color: {BLEU};
    margin-top: 3px;
}}

/* ── Podium ── */
.podium-item {{
    padding: .45rem .7rem;
    background: {GRIS_F};
    border-left: 3px solid {GRIS_B};
    margin-bottom: .3rem;
    font-size: .82rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.podium-value {{
    font-size: .75rem;
    color: #888;
    white-space: nowrap;
    margin-left: 8px;
}}

/* ── Label de comparaison ── */
.emploi-compare-label {{
    font-size: 0.75rem;
    color: #888;
    margin: 0.3rem 0 1rem 0;
    font-style: italic;
}}

/* ── Placeholder vide ── */
.emploi-placeholder {{
    text-align: center;
    padding: 3rem 0;
    color: #aaa;
    font-size: .9rem;
    border: 1px dashed {GRIS_B};
    background: {GRIS_F};
    margin-top: 12px;
}}

/* ── Séparateur ── */
.page-divider {{
    border: none;
    border-top: 2px solid {GRIS_B};
    margin: 24px 0;
}}
</style>
""", unsafe_allow_html=True)


# ── Composants DSFR ───────────────────────────────────────────────────────────
def _section(title: str):
    st.markdown(
        f'<div class="section-title" style="margin-top:24px">{title}</div>',
        unsafe_allow_html=True,
    )


def _kpi_grid(items: list, color: str):
    cells = "".join(
        f'<div class="emploi-kpi-item">'
        f'<div class="emploi-kpi-label">{label}</div>'
        f'<div class="emploi-kpi-value" style="color:{color}">{value}</div>'
        f'</div>'
        for label, value in items
    )
    st.markdown(f'<div class="emploi-kpi-grid">{cells}</div>', unsafe_allow_html=True)


def _score_bar(pct: float, label: str):
    st.markdown(f"""
<div class="score-bar-wrap">
  <div class="score-bar-label">{label}</div>
  <div class="score-bar-track">
    <div class="score-bar-fill" style="width:{min(pct, 100):.1f}%"></div>
  </div>
  <div class="score-bar-pct">{pct:.1f} % de similitude</div>
</div>
""", unsafe_allow_html=True)


def _ville_badge(ville: str, color: str):
    st.markdown(
        f'<div style="font-size:.78rem;font-weight:700;color:{color};'
        f'margin-bottom:.5rem;text-transform:uppercase;letter-spacing:.06em">'
        f'● {ville}</div>',
        unsafe_allow_html=True,
    )


# ── Calcul des indicateurs ────────────────────────────────────────────────────
def _compute(sub, ec, sc, secteur_niv):
    ne    = sub[ec[-1]].sum()  if ec else 0
    ns    = sub[sc[-1]].sum()  if sc else 0
    nb_s  = sub[secteur_niv].nunique() if secteur_niv in sub.columns else 0
    ratio = round(ns / ne, 1)  if ne > 0 else 0
    first = sub[ec[0]].sum()   if ec else 0
    last  = sub[ec[-1]].sum()  if ec else 0
    crois = round((last - first) / first * 100, 1) if first > 0 else 0
    return dict(ne=int(ne), ns=int(ns), nb_s=nb_s, ratio=ratio, crois=crois)


# ── Point d'entrée appelé par app.py ─────────────────────────────────────────
def render():
    _inject_page_css()

    df = load_emploi()
    if df is None:
        return

    etab_avail  = [c for c in ETAB_COLS if c in df.columns]
    sala_avail  = [c for c in SALA_COLS  if c in df.columns]
    years_avail = [int(c.split()[-1]) for c in etab_avail]
    villes      = sorted(df["Nom commune"].dropna().unique().tolist())

    # ── Titre DSFR ────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-title">Emploi'
        '<span class="section-sub">Établissements & effectifs salariés · INSEE · SIRENE</span></div>',
        unsafe_allow_html=True,
    )

    # ── Sélecteurs ────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        ville1 = st.selectbox("Ville 1", villes, index=0, key="e_v1")
    with col2:
        ville2 = st.selectbox("Ville 2", villes, index=min(1, len(villes) - 1), key="e_v2")
    with col3:
        st.markdown("<div style='height:1.85rem'></div>", unsafe_allow_html=True)
        comparer = st.button("Comparer ▶", key="e_btn", use_container_width=True)

    if ville1 == ville2:
        st.warning("Sélectionnez deux communes différentes.")
        return

    if not comparer and "e_compared" not in st.session_state:
        st.markdown(
            '<div class="emploi-placeholder">'
            'Sélectionnez deux communes et cliquez sur <strong>Comparer ▶</strong>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    if comparer:
        st.session_state["e_compared"] = (ville1, ville2)

    v1, v2 = st.session_state.get("e_compared", (ville1, ville2))

    mask = df["Nom commune"].isin([v1, v2])
    dff  = df[mask].copy()
    sub1 = dff[dff["Nom commune"] == v1]
    sub2 = dff[dff["Nom commune"] == v2]

    st.markdown(
        f'<div class="emploi-compare-label">Comparaison : {v1} — {v2}</div>',
        unsafe_allow_html=True,
    )

    # ── Filtres secondaires ───────────────────────────────────────────────────
    col_a, col_b, _ = st.columns([2, 2, 2])
    with col_a:
        secteur_niv = st.selectbox(
            "Niveau de secteur",
            ["Grand secteur d'activité", "Secteur NA17", "Secteur NA38"],
            key="e_sect",
        )
    with col_b:
        y_min, y_max = min(years_avail), max(years_avail)
        y_range = st.select_slider(
            "Période", options=years_avail, value=(y_min, y_max), key="e_yr",
        )

    y_start, y_end = y_range
    sel_etab  = [c for c in etab_avail if y_start <= int(c.split()[-1]) <= y_end]
    sel_sala  = [c for c in sala_avail  if y_start <= int(c.split()[-1]) <= y_end]
    sel_years = [int(c.split()[-1]) for c in sel_etab]

    last_year  = sel_years[-1] if sel_years else 2024
    first_year = sel_years[0]  if sel_years else 2006

    k1 = _compute(sub1, sel_etab, sel_sala, secteur_niv)
    k2 = _compute(sub2, sel_etab, sel_sala, secteur_niv)

    cmap = {v1: BLEU, v2: ROUGE}

    # ── Indicateurs clés ──────────────────────────────────────────────────────
    _section(f"Indicateurs clés — {v1} vs {v2}")

    kpi_cols = st.columns(2)
    for col_st, k, ville, color in [
        (kpi_cols[0], k1, v1, BLEU),
        (kpi_cols[1], k2, v2, ROUGE),
    ]:
        with col_st:
            _ville_badge(ville, color)
            _kpi_grid([
                (f"Établissements ({last_year})",              f"{k['ne']:,}"),
                (f"Effectifs salariés ({last_year})",          f"{k['ns']:,}"),
                ("Secteurs représentés",                       k["nb_s"]),
                ("Ratio salariés / établ.",                    k["ratio"]),
                (f"Croissance établ. ({first_year}→{last_year})", f"{k['crois']:+.1f} %"),
            ], color)

    # ── Comparaison directe ───────────────────────────────────────────────────
    _section("Comparaison directe")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric(f"Établ. {v1}", f"{k1['ne']:,}",
                  delta=f"{k1['ne'] - k2['ne']:+,} vs {v2}")
    with col_m2:
        st.metric(f"Établ. {v2}", f"{k2['ne']:,}")
    with col_m3:
        st.metric(f"Salariés {v1}", f"{k1['ns']:,}",
                  delta=f"{k1['ns'] - k2['ns']:+,} vs {v2}")
    with col_m4:
        st.metric(f"Salariés {v2}", f"{k2['ns']:,}")

    # ── Similitude sectorielle ────────────────────────────────────────────────
    if secteur_niv in sub1.columns and secteur_niv in sub2.columns:
        s1_set = set(sub1[secteur_niv].dropna().unique())
        s2_set = set(sub2[secteur_niv].dropna().unique())
        jacc   = len(s1_set & s2_set) / len(s1_set | s2_set) * 100 if s1_set | s2_set else 0

        st.markdown('<div class="page-divider"></div>', unsafe_allow_html=True)
        col_sc1, col_sc2, col_sc3 = st.columns([3, 1, 1])
        with col_sc1:
            _score_bar(jacc, f"Similitude sectorielle entre {v1} et {v2}")
        with col_sc2:
            st.metric("En commun", len(s1_set & s2_set))
        with col_sc3:
            st.metric("Secteurs exclusifs", len((s1_set | s2_set) - (s1_set & s2_set)))

    # ── Évolution temporelle ──────────────────────────────────────────────────
    _section("Évolution dans le temps")
    tab_e, tab_s, tab_r = st.tabs(["Établissements", "Effectifs salariés", "Ratio sal./établ."])

    def evo_df(cols, label):
        rows = []
        for c in cols:
            y = int(c.split()[-1])
            rows += [
                {"Année": y, "Ville": v1, label: sub1[c].sum()},
                {"Année": y, "Ville": v2, label: sub2[c].sum()},
            ]
        return pd.DataFrame(rows)

    with tab_e:
        ev  = evo_df(sel_etab, "Établissements")
        fig = px.line(ev, x="Année", y="Établissements", color="Ville",
                      color_discrete_map=cmap, markers=True)
        fig.update_layout(**{**CHART_LAYOUT, "hovermode": "x unified"},
                          legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with tab_s:
        ev  = evo_df(sel_sala, "Effectifs salariés")
        fig = px.line(ev, x="Année", y="Effectifs salariés", color="Ville",
                      color_discrete_map=cmap, markers=True)
        fig.update_layout(**{**CHART_LAYOUT, "hovermode": "x unified"},
                          legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with tab_r:
        rows = []
        for ec, sc in zip(sel_etab, sel_sala):
            y  = int(ec.split()[-1])
            e1, s1_ = sub1[ec].sum(), sub1[sc].sum()
            e2, s2_ = sub2[ec].sum(), sub2[sc].sum()
            rows += [
                {"Année": y, "Ville": v1, "Ratio": round(s1_ / e1, 2) if e1 > 0 else 0},
                {"Année": y, "Ville": v2, "Ratio": round(s2_ / e2, 2) if e2 > 0 else 0},
            ]
        fig = px.line(pd.DataFrame(rows), x="Année", y="Ratio", color="Ville",
                      color_discrete_map=cmap, markers=True)
        fig.update_layout(**{**CHART_LAYOUT, "hovermode": "x unified"},
                          legend_title_text="", yaxis_title="Sal./Établ.")
        st.plotly_chart(fig, use_container_width=True)

    # ── Répartition sectorielle ───────────────────────────────────────────────
    _section("Répartition par secteur d'activité")
    metric_s = st.radio(
        "Métrique", ["Établissements", "Effectifs salariés"],
        horizontal=True, key="e_met",
    )
    last_col = (sel_etab[-1] if metric_s == "Établissements" and sel_etab
                else (sel_sala[-1] if sel_sala else None))

    col_a, col_b = st.columns(2)
    for col_p, sub, ville, color in [
        (col_a, sub1, v1, BLEU),
        (col_b, sub2, v2, ROUGE),
    ]:
        with col_p:
            if secteur_niv in sub.columns and last_col:
                g = (sub.groupby(secteur_niv)[last_col].sum()
                        .sort_values(ascending=False).head(12).reset_index())
                g.columns = [secteur_niv, metric_s]
                fig = px.bar(g, x=metric_s, y=secteur_niv, orientation="h",
                             color_discrete_sequence=[color])
                fig.update_layout(
                    **{**CHART_LAYOUT, "hovermode": "closest"},
                    title=dict(text=ville, font=dict(size=11)),
                    showlegend=False,
                )
                fig.update_yaxes(autorange="reversed", gridcolor=GRIS_F)
                st.plotly_chart(fig, use_container_width=True)

    # ── Podium ────────────────────────────────────────────────────────────────
    _section("Top 3 secteurs dominants")
    col_p1, col_p2 = st.columns(2)
    medals = ["🥇", "🥈", "🥉"]

    for col_p, sub, ville, color in [
        (col_p1, sub1, v1, BLEU),
        (col_p2, sub2, v2, ROUGE),
    ]:
        with col_p:
            _ville_badge(ville, color)
            if secteur_niv in sub.columns and sel_etab:
                top3 = (sub.groupby(secteur_niv)[sel_etab].sum()
                           .sum(axis=1)
                           .sort_values(ascending=False)
                           .head(3))
                for i, (s, v) in enumerate(top3.items()):
                    st.markdown(
                        f'<div class="podium-item" style="border-left-color:{color}">'
                        f'<span>{medals[i]} <strong>{s}</strong></span>'
                        f'<span class="podium-value">{int(v):,} établ.</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

    # ── Heatmap ───────────────────────────────────────────────────────────────
    _section("Carte de chaleur — Secteur × Année")
    col_heat1, col_heat2 = st.columns([2, 2])
    with col_heat1:
        v_heat = st.selectbox("Commune", [v1, v2], key="e_heat")
    with col_heat2:
        metric_heat = st.radio(
            "Métrique", ["Établissements", "Effectifs salariés"],
            horizontal=True, key="e_heat_met",
        )

    sub_h      = sub1 if v_heat == v1 else sub2
    cols_heat  = sel_etab if metric_heat == "Établissements" else sel_sala

    if secteur_niv in sub_h.columns and cols_heat:
        hd = sub_h.groupby(secteur_niv)[cols_heat].sum()
        hd.index   = [s[:35] + "…" if len(str(s)) > 35 else s for s in hd.index]
        hd.columns = [int(c.split()[-1]) for c in cols_heat]
        hd         = hd.loc[hd.sum(axis=1).nlargest(10).index]
        fig = px.imshow(
            hd, aspect="auto",
            color_continuous_scale=["#eef2ff", BLEU],
            labels={"x": "Année", "y": "", "color": "Établ."},
        )
        fig.update_layout(**{**CHART_LAYOUT, "margin": dict(l=0, r=0, t=10, b=0)})
        st.plotly_chart(fig, use_container_width=True)

    # ── Tableau croisé ────────────────────────────────────────────────────────
    _section("Tableau croisé")
    if secteur_niv in dff.columns and sel_etab:
        p1  = sub1.groupby(secteur_niv)[sel_etab].sum().sum(axis=1).rename(f"Établ. {v1}")
        p2  = sub2.groupby(secteur_niv)[sel_etab].sum().sum(axis=1).rename(f"Établ. {v2}")
        s1_ = sub1.groupby(secteur_niv)[sel_sala].sum().sum(axis=1).rename(f"Sal. {v1}") if sel_sala else None
        s2_ = sub2.groupby(secteur_niv)[sel_sala].sum().sum(axis=1).rename(f"Sal. {v2}") if sel_sala else None
        to_c = [x for x in [p1, p2, s1_, s2_] if x is not None]
        tab  = pd.concat(to_c, axis=1).fillna(0).astype(int)
        tab.index.name = secteur_niv
        st.dataframe(
            tab.sort_values(f"Établ. {v1}", ascending=False),
            use_container_width=True,
            height=320,
        )

    # ── Source ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="margin-top:32px;font-size:0.7rem;color:#aaa;text-align:center;'
        'border-top:1px solid #ddd;padding-top:12px">'
        "Source : INSEE · SIRENE · Données emploi communales · Traitements France Compare · 2026"
        "</div>",
        unsafe_allow_html=True,
    )
