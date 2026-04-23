# sport.py — Page "Sport" · France Comparateur
# Appelé depuis app.py via sport.render()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast

from dsfr import BLEU, ROUGE, VERT, GRIS_F, GRIS_B, TEXTE, COLORS, metric_box

from pathlib import Path
BASE_DIR = Path(__file__).parent          # dossier code/
DATA_DIR = BASE_DIR.parent / "data" / "processed"


# ── Colonnes RES à charger ────────────────────────────────────────────────────
SPORT_COLS = [
    "Commune nom", "Commune INSEE", "Département Nom", "Région Nom",
    "Type d'équipement sportif", "Famille d'équipement sportif",
    "Nom de l'équipement sportif", "Nom de l'installation sportive",
    "Activités", "Type de particularité de l'installation",
    "Année de mise en service", "Surface de l'aire d'évolution",
    "Eclairage de l'aire d'évolution",
    "Accessibilité aux personnes à mobilité réduite",
    "Equipement d'accès libre", "Type de propriétaire",
    "Nombre de places assises en tribune",
    "Nombre de vestiaires sportifs",
    "Nature de l'équipement sportif",
    "Type d'utilisation", "QPV",
    "Accessibilité de l'installation en faveur des personnes en situation de handicap",
    "Accessibilité de l'installation en transport en commun",
    "Latitude", "Longitude",
]

COL = {
    "commune":    "Commune nom",
    "type_equip": "Type d'équipement sportif",
    "famille":    "Famille d'équipement sportif",
    "install":    "Nom de l'installation sportive",
    "activites":  "Activités",
    "particul":   "Type de particularité de l'installation",
    "annee":      "Année de mise en service",
    "surface":    "Surface de l'aire d'évolution",
    "eclairage":  "Eclairage de l'aire d'évolution",
    "pmr":        "Accessibilité aux personnes à mobilité réduite",
    "acces":      "Equipement d'accès libre",
    "proprio":    "Type de propriétaire",
    "tribunes":   "Nombre de places assises en tribune",
    "vestiaires": "Nombre de vestiaires sportifs",
    "nature":     "Nature de l'équipement sportif",
    "utilisation":"Type d'utilisation",
    "qpv":        "QPV",
    "pmr_install":"Accessibilité de l'installation en faveur des personnes en situation de handicap",
    "tc":         "Accessibilité de l'installation en transport en commun",
    "lat":        "Latitude",
    "lon":        "Longitude",
}

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
@st.cache_data(show_spinner="Chargement des données sportives…")
def load_sport():
    try:
        return pd.read_excel(DATA_DIR / "sport.xlsx", usecols=lambda c: c in SPORT_COLS)
    except FileNotFoundError:
        st.error("⚠️ Fichier `sport` introuvable.")
        return None
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return None


# ── Utilitaires ───────────────────────────────────────────────────────────────
def parse_list(v):
    if pd.isna(v):
        return []
    try:
        r = ast.literal_eval(str(v))
        return r if isinstance(r, list) else [r]
    except Exception:
        return [str(v)]


def explode_col(df, col):
    d = df.copy()
    d[col] = d[col].apply(parse_list)
    return d.explode(col)


def pct_bool(sub, col):
    if col not in sub.columns or len(sub) == 0:
        return 0.0
    s = sub[col]
    count = (s.eq(True) | s.astype(str).str.upper().isin(["VRAI", "TRUE", "OUI"])).sum()
    return round(count / len(sub) * 100, 1)


def pct_bool_install(sub, col):
    """Pourcentage d'installations (dédupliquées) avec col == True."""
    install_col = COL["install"]
    if col not in sub.columns or install_col not in sub.columns or len(sub) == 0:
        return 0.0
    deduped = sub.drop_duplicates(subset=[install_col])
    s = deduped[col]
    count = (s.eq(True) | s.astype(str).str.upper().isin(["VRAI", "TRUE", "OUI"])).sum()
    return round(count / len(deduped) * 100, 1) if len(deduped) > 0 else 0.0


# ── CSS spécifique à la page ──────────────────────────────────────────────────
def _inject_page_css():
    st.markdown(f"""
<style>
/* ── Bandeau de comparaison ── */
.sport-compare-label {{
    font-size: 0.75rem;
    color: #888;
    margin: 0.3rem 0 1rem 0;
    font-style: italic;
}}

/* ── Grille KPI sport ── */
.sport-kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 0;
    border: 1px solid {GRIS_B};
    margin-bottom: 8px;
}}
.sport-kpi-item {{
    padding: 10px 14px;
    border-right: 1px solid {GRIS_B};
    border-bottom: 1px solid {GRIS_B};
    background: white;
}}
.sport-kpi-label {{
    font-size: 0.62rem;
    font-weight: 700;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 4px;
}}
.sport-kpi-value {{
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
    transition: width 0.4s;
}}
.score-bar-pct {{
    font-size: 0.72rem;
    font-weight: 700;
    color: {BLEU};
    margin-top: 3px;
}}

/* ── Placeholder vide ── */
.sport-placeholder {{
    text-align: center;
    padding: 3rem 0;
    color: #aaa;
    font-size: 0.9rem;
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
    """Titre de sous-section DSFR."""
    st.markdown(
        f'<div class="section-title" style="margin-top:24px">{title}</div>',
        unsafe_allow_html=True,
    )


def _kpi_grid(items: list, color: str):
    """
    Affiche une grille de KPIs.
    items : liste de tuples (label, value)
    """
    cells = ""
    for label, value in items:
        cells += (
            f'<div class="sport-kpi-item">'
            f'<div class="sport-kpi-label">{label}</div>'
            f'<div class="sport-kpi-value" style="color:{color}">{value}</div>'
            f'</div>'
        )
    st.markdown(f'<div class="sport-kpi-grid">{cells}</div>', unsafe_allow_html=True)


def _score_bar(pct: float, label: str):
    """Barre de progression DSFR."""
    st.markdown(f"""
<div class="score-bar-wrap">
  <div class="score-bar-label">{label}</div>
  <div class="score-bar-track">
    <div class="score-bar-fill" style="width:{min(pct,100):.1f}%"></div>
  </div>
  <div class="score-bar-pct">{pct:.1f} % de similitude</div>
</div>
""", unsafe_allow_html=True)


def _chart_bar_h(sub, col_name, ville, color, title=None):
    """Graphique en barres horizontales DSFR."""
    if col_name not in sub.columns:
        return None
    g = sub[col_name].value_counts().head(12).reset_index()
    g.columns = ["Libellé", "Nb"]
    fig = px.bar(g, x="Nb", y="Libellé", orientation="h",
                 color_discrete_sequence=[color])
    layout = {**CHART_LAYOUT,
              "title": dict(text=title or ville, font=dict(size=11)),
              "yaxis": dict(autorange="reversed", gridcolor=GRIS_F),
              "showlegend": False,
              "height": 340}
    fig.update_layout(**layout)
    return fig


# ── Calcul des indicateurs ────────────────────────────────────────────────────
def _compute(sub):
    return dict(
        nb_equip   = len(sub),
        nb_install = sub[COL["install"]].nunique()   if COL["install"]   in sub.columns else 0,
        nb_types   = sub[COL["type_equip"]].nunique() if COL["type_equip"] in sub.columns else 0,
        nb_fam     = sub[COL["famille"]].nunique()    if COL["famille"]   in sub.columns else 0,
        surf_tot   = int(sub[COL["surface"]].sum())   if COL["surface"]   in sub.columns else 0,
        surf_moy   = round(sub[COL["surface"]].mean(), 0) if COL["surface"] in sub.columns else 0,
        pct_eclaire= pct_bool(sub, COL["eclairage"]),
        pct_pmr    = pct_bool_install(sub, COL["pmr_install"]),
        pct_tc     = pct_bool_install(sub, COL["tc"]),
        pct_acces  = pct_bool(sub, COL["acces"]),
        tribunes   = int(sub[COL["tribunes"]].sum())  if COL["tribunes"]  in sub.columns else 0,
        vestiaires = int(sub[COL["vestiaires"]].sum()) if COL["vestiaires"] in sub.columns else 0,
        en_qpv     = int(sub[COL["qpv"]].notna().sum()) if COL["qpv"]    in sub.columns else 0,
    )


# ── Point d'entrée appelé par app.py ─────────────────────────────────────────
def render():
    _inject_page_css()

    df = load_sport()
    if df is None:
        return

    villes = sorted(df[COL["commune"]].dropna().unique().tolist())

    # ── Titre DSFR ────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-title">Sport'
        '<span class="section-sub">Équipements sportifs · Recensement des équipements sportifs (RES)</span></div>',
        unsafe_allow_html=True,
    )

    # ── Sélecteurs ────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        ville1 = st.selectbox("Ville 1", villes, index=0, key="s_v1")
    with col2:
        ville2 = st.selectbox("Ville 2", villes, index=min(1, len(villes) - 1), key="s_v2")
    with col3:
        st.markdown("<div style='height:1.85rem'></div>", unsafe_allow_html=True)
        comparer = st.button("Comparer ▶", key="s_btn", use_container_width=True)

    if ville1 == ville2:
        st.warning("Sélectionnez deux communes différentes.")
        return

    if not comparer and "s_compared" not in st.session_state:
        st.markdown(
            '<div class="sport-placeholder">'
            'Sélectionnez deux communes et cliquez sur <strong>Comparer ▶</strong>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    if comparer:
        st.session_state["s_compared"] = (ville1, ville2)

    v1, v2 = st.session_state.get("s_compared", (ville1, ville2))

    # Filtrage
    mask = df[COL["commune"]].isin([v1, v2])
    dff  = df[mask].copy()
    sub1 = dff[dff[COL["commune"]] == v1]
    sub2 = dff[dff[COL["commune"]] == v2]

    st.markdown(
        f'<div class="sport-compare-label">Comparaison : {v1} — {v2}</div>',
        unsafe_allow_html=True,
    )

    # ── Filtres secondaires ───────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        fams    = ["Tous"] + sorted(dff[COL["famille"]].dropna().unique()) if COL["famille"] in dff.columns else ["Tous"]
        fam_sel = st.selectbox("Famille d'équipement", fams, key="s_fam")
    with col_f2:
        parts    = ["Tous"] + sorted(dff[COL["particul"]].dropna().unique()) if COL["particul"] in dff.columns else ["Tous"]
        part_sel = st.selectbox("Particularité", parts, key="s_part")
    with col_f3:
        nat_sel = st.selectbox("Nature", ["Tous", "Intérieur", "Découvert"], key="s_nat")

    def filt(sub):
        if fam_sel != "Tous" and COL["famille"] in sub.columns:
            sub = sub[sub[COL["famille"]] == fam_sel]
        if part_sel != "Tous" and COL["particul"] in sub.columns:
            sub = sub[sub[COL["particul"]] == part_sel]
        if nat_sel != "Tous" and COL["nature"] in sub.columns:
            sub = sub[sub[COL["nature"]] == nat_sel]
        return sub

    sub1, sub2 = filt(sub1), filt(sub2)

    # ── Indicateurs clés ──────────────────────────────────────────────────────
    k1, k2 = _compute(sub1), _compute(sub2)

    _section(f"Indicateurs clés — {v1} vs {v2}")

    kpi_cols = st.columns(2)
    for col_st, k, ville, color in [
        (kpi_cols[0], k1, v1, BLEU),
        (kpi_cols[1], k2, v2, ROUGE),
    ]:
        with col_st:
            st.markdown(
                f'<div style="font-size:.78rem;font-weight:700;color:{color};'
                f'margin-bottom:.5rem;text-transform:uppercase;letter-spacing:.06em">'
                f'● {ville}</div>',
                unsafe_allow_html=True,
            )
            _kpi_grid([
                ("Équipements sportifs",          f"{k['nb_equip']:,}"),
                ("Installations distinctes",       f"{k['nb_install']:,}"),
                ("Types d'équipements",            k["nb_types"]),
                ("Familles",                       k["nb_fam"]),
                ("Surface totale m²",              f"{k['surf_tot']:,}"),
                ("Surface moyenne m²",             int(k["surf_moy"])),
                ("Accessibilité handicap (inst.)", f"{k['pct_pmr']} %"),
                ("Transport en commun (inst.)",    f"{k['pct_tc']} %"),
                ("Accès libre",                    f"{k['pct_acces']} %"),
                ("Éclairé",                        f"{k['pct_eclaire']} %"),
                ("Places en tribune",              f"{k['tribunes']:,}"),
                ("Vestiaires",                     k["vestiaires"]),
                ("En QPV",                         k["en_qpv"]),
            ], color)

    # ── Similitude types ─────────────────────────────────────────────────────
    st.markdown('<div class="page-divider"></div>', unsafe_allow_html=True)
    t1 = set(sub1[COL["type_equip"]].dropna().unique()) if COL["type_equip"] in sub1.columns else set()
    t2 = set(sub2[COL["type_equip"]].dropna().unique()) if COL["type_equip"] in sub2.columns else set()
    jacc = len(t1 & t2) / len(t1 | t2) * 100 if t1 | t2 else 0

    col_sc1, col_sc2, col_sc3 = st.columns([3, 1, 1])
    with col_sc1:
        _score_bar(jacc, f"Similitude en types d'équipements entre {v1} et {v2}")
    with col_sc2:
        st.metric("En commun", len(t1 & t2))
    with col_sc3:
        st.metric("Exclusifs", len((t1 | t2) - (t1 & t2)))

    # ── Répartition par famille ───────────────────────────────────────────────
    _section("Répartition par famille d'équipement")
    col_a, col_b = st.columns(2)
    for col_p, sub, ville, color in [
        (col_a, sub1, v1, BLEU),
        (col_b, sub2, v2, ROUGE),
    ]:
        with col_p:
            fig = _chart_bar_h(sub, COL["famille"], ville, color)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

    # ── Activités sportives ───────────────────────────────────────────────────
    _section("Activités sportives pratiquées")
    if COL["activites"] in df.columns:
        col_a, col_b = st.columns(2)
        for col_p, sub, ville, color in [
            (col_a, sub1, v1, BLEU),
            (col_b, sub2, v2, ROUGE),
        ]:
            with col_p:
                exp = explode_col(sub, COL["activites"])
                exp = exp[exp[COL["activites"]].astype(str).str.strip().ne("")]
                vc  = exp[COL["activites"]].value_counts().head(15).reset_index()
                vc.columns = ["Activité", "Nb"]
                fig = px.bar(vc, x="Nb", y="Activité", orientation="h",
                             color_discrete_sequence=[color])
                fig.update_layout(**{**CHART_LAYOUT,
                                     "title": dict(text=ville, font=dict(size=11)),
                                     "yaxis": dict(autorange="reversed", gridcolor=GRIS_F),
                                     "showlegend": False, "height": 400})
                st.plotly_chart(fig, use_container_width=True)

        a1 = set(explode_col(sub1, COL["activites"])[COL["activites"]].dropna().astype(str).unique()) - {"", "nan"}
        a2 = set(explode_col(sub2, COL["activites"])[COL["activites"]].dropna().astype(str).unique()) - {"", "nan"}
        jacc_a = len(a1 & a2) / len(a1 | a2) * 100 if a1 | a2 else 0
        _score_bar(jacc_a, f"Similitude en activités déclarées entre {v1} et {v2}")

    # ── Historique mise en service ────────────────────────────────────────────
    _section("Historique — Mise en service des équipements")
    if COL["annee"] in df.columns:
        rows = []
        for sub, ville in [(sub1, v1), (sub2, v2)]:
            g = sub[COL["annee"]].dropna().astype(int)
            g = g[(g >= 1900) & (g <= 2030)].value_counts().sort_index().reset_index()
            g.columns = ["Année", "Nb"]
            g["Cumulé"] = g["Nb"].cumsum()
            g["Ville"]  = ville
            rows.append(g)
        if rows:
            ev   = pd.concat(rows)
            cmap = {v1: BLEU, v2: ROUGE}
            tab_h1, tab_h2 = st.tabs(["Par année", "Parc cumulatif"])
            with tab_h1:
                fig = px.bar(ev, x="Année", y="Nb", color="Ville",
                             barmode="group", color_discrete_map=cmap)
                fig.update_layout(**{**CHART_LAYOUT,
                                     "hovermode": "x unified",
                                     "legend_title_text": "",
                                     "yaxis_title": "Équipements"})
                st.plotly_chart(fig, use_container_width=True)
            with tab_h2:
                fig = px.line(ev, x="Année", y="Cumulé", color="Ville",
                              color_discrete_map=cmap)
                fig.update_layout(**{**CHART_LAYOUT,
                                     "hovermode": "x unified",
                                     "legend_title_text": "",
                                     "yaxis_title": "Stock cumulatif"})
                st.plotly_chart(fig, use_container_width=True)

    # ── Intérieur / Découvert ─────────────────────────────────────────────────
    if COL["nature"] in df.columns:
        _section("Intérieur vs Découvert")
        col_a, col_b = st.columns(2)
        for col_p, sub, ville, color in [
            (col_a, sub1, v1, BLEU),
            (col_b, sub2, v2, ROUGE),
        ]:
            with col_p:
                vc = sub[COL["nature"]].value_counts()
                fig = px.pie(vc, values=vc.values, names=vc.index, hole=0.5,
                             color_discrete_sequence=[color, "#aab8d8", "#e8a0a6"])
                fig.update_layout(**{**CHART_LAYOUT,
                                     "title": dict(text=ville, font=dict(size=11))})
                st.plotly_chart(fig, use_container_width=True)

    # ── Accessibilité ─────────────────────────────────────────────────────────
    _section("Accessibilité")
    acc_items = [
        ("PMR (installation)",   COL["pmr_install"], True),
        ("Transport en commun",  COL["tc"],           True),
        ("Accès libre",          COL["acces"],        False),
        ("Éclairage",            COL["eclairage"],    False),
    ]
    rows_acc = []
    for label, c, is_install in acc_items:
        fn = pct_bool_install if is_install else pct_bool
        if c in sub1.columns and c in sub2.columns:
            rows_acc.append({"Critère": label, v1: fn(sub1, c), v2: fn(sub2, c)})
    if rows_acc:
        rdf = pd.DataFrame(rows_acc)
        fig = go.Figure()
        for ville, color in [(v1, BLEU), (v2, ROUGE)]:
            fig.add_trace(go.Bar(name=ville, x=rdf["Critère"], y=rdf[ville],
                                 marker_color=color))
        fig.update_layout(**{**CHART_LAYOUT,
                              "barmode": "group",
                              "yaxis_title": "% équipements",
                              "legend_title_text": ""})
        st.plotly_chart(fig, use_container_width=True)

    # ── Propriétaires ─────────────────────────────────────────────────────────
    if COL["proprio"] in df.columns:
        _section("Type de propriétaire")
        col_a, col_b = st.columns(2)
        for col_p, sub, ville, color in [
            (col_a, sub1, v1, BLEU),
            (col_b, sub2, v2, ROUGE),
        ]:
            with col_p:
                fig = _chart_bar_h(sub, COL["proprio"], ville, color)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

    # ── Tableau croisé ────────────────────────────────────────────────────────
    _section("Tableau croisé — Par type d'équipement")
    if COL["type_equip"] in dff.columns:
        p1   = sub1[COL["type_equip"]].value_counts().rename(f"Nb {v1}")
        p2   = sub2[COL["type_equip"]].value_counts().rename(f"Nb {v2}")
        to_c = [p1, p2]
        if COL["surface"] in sub1.columns:
            to_c.append(sub1.groupby(COL["type_equip"])[COL["surface"]].sum().rename(f"Surf. m² {v1}"))
        if COL["surface"] in sub2.columns:
            to_c.append(sub2.groupby(COL["type_equip"])[COL["surface"]].sum().rename(f"Surf. m² {v2}"))
        tab = pd.concat(to_c, axis=1).fillna(0).astype(int)
        tab.index.name = "Type d'équipement"
        st.dataframe(
            tab.sort_values(f"Nb {v1}", ascending=False),
            use_container_width=True,
            height=320,
        )

    # ── Carte géographique ────────────────────────────────────────────────────
    if COL["lat"] in dff.columns and COL["lon"] in dff.columns:
        _section("Carte des équipements")
        map_df = dff[
            [COL["commune"], COL["lat"], COL["lon"], COL["type_equip"], COL["install"]]
        ].dropna(subset=[COL["lat"], COL["lon"]])
        if not map_df.empty:
            fig_map = px.scatter_mapbox(
                map_df,
                lat=COL["lat"],
                lon=COL["lon"],
                color=COL["commune"],
                color_discrete_map={v1: BLEU, v2: ROUGE},
                hover_name=COL["install"],
                hover_data={COL["type_equip"]: True, COL["lat"]: False, COL["lon"]: False},
                zoom=10,
                mapbox_style="open-street-map",
                height=450,
            )
            fig_map.update_layout(**{**CHART_LAYOUT, "margin": dict(l=0, r=0, t=10, b=0)})
            st.plotly_chart(fig_map, use_container_width=True)

    # ── Données brutes ────────────────────────────────────────────────────────
    with st.expander("Données brutes"):
        tab_a, tab_b = st.tabs([f"● {v1}", f"● {v2}"])
        with tab_a:
            st.dataframe(sub1.reset_index(drop=True), use_container_width=True, height=280)
        with tab_b:
            st.dataframe(sub2.reset_index(drop=True), use_container_width=True, height=280)

    # ── Source ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="margin-top:32px;font-size:0.7rem;color:#aaa;text-align:center;'
        'border-top:1px solid #ddd;padding-top:12px">'
        "Source : Recensement des Équipements Sportifs (RES) · data.gouv.fr · Traitements France Compare · 2026"
        "</div>",
        unsafe_allow_html=True,
    )
