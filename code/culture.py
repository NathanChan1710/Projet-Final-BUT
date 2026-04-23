# culture.py — Page Culture · France Comparateur
# Compatible avec app.py + dsfr.py (sans utils.py)

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from dsfr import BLEU, ROUGE, VERT, GRIS_B, TEXTE, COLORS, metric_box

from pathlib import Path
BASE_DIR = Path(__file__).parent          # dossier code/
DATA_DIR = BASE_DIR.parent / "data" / "processed"
# ── Palette locale (accès par clé string comme dans culture_page.py) ──────────
_COLORS = {"bleu": BLEU, "rouge": ROUGE, "vert": VERT}

# ── Layout Plotly partagé ─────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    font=dict(family="Source Sans Pro, Arial, sans-serif", size=11, color=TEXTE),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=10, r=10, t=30, b=10),
    height=280,
)

# ── Colonnes attendues dans le fichier Excel ──────────────────────────────────
CULTURE_COLS = [
    "Nom", "Type équipement ou lieu", "Label et appellation", "Région", "Domaine",
    "Département", "Fonction_1", "Fonction_2", "Fonction_3", "Fonction_4",
    "Nombre_fauteuils_de_cinema", "Nombre_ecrans", "Nombre_de_salles_de_theatre",
    "Jauge_du_theatre", "Surface_Bibliotheque", "Latitude", "Longitude",
    "libelle_geographique", "code_insee", "Demographie_AP"
]

COL = {
    "nom":           "Nom",
    "type":          "Type équipement ou lieu",
    "label":         "Label et appellation",
    "region":        "Région",
    "domaine":       "Domaine",
    "departement":   "Département",
    "fonction1":     "Fonction_1",
    "fonction2":     "Fonction_2",
    "fonction3":     "Fonction_3",
    "fonction4":     "Fonction_4",
    "fauteuils":     "Nombre_fauteuils_de_cinema",
    "ecrans":        "Nombre_ecrans",
    "salles_theatre":"Nombre_de_salles_de_theatre",
    "jauge":         "Jauge_du_theatre",
    "surface":       "Surface_Bibliotheque",
    "lat":           "Latitude",
    "lon":           "Longitude",
    "ville":         "libelle_geographique", 
    "code_insee":    "code_insee",
    "demographie":   "Demographie_AP"
}

HIGHLIGHT_TYPES = [
    "Centre chorégraphique national", "Librairie", "Monument historique",
    "Cinéma", "Théâtre", "Bibliothèque"
]
DOMAINES = ["Arts du spectacle", "Livre et presse", "Patrimoine", "Arts visuels", "Musique"]

# ── Helpers DSFR ──────────────────────────────────────────────────────────────

def _section(title: str, sub: str = ""):
    """Titre de section style DSFR."""
    sub_html = f'<span class="section-sub">{sub}</span>' if sub else ""
    st.markdown(
        f'<div class="section-title">{title}{sub_html}</div>',
        unsafe_allow_html=True
    )


def _kpi_row(items: list, cols_per_row: int = 3):
    """
    Affiche une liste de (label, value, theme) sous forme de metric-box DSFR.
    items : list of (label, value, theme)
    """
    for i in range(0, len(items), cols_per_row):
        chunk = items[i:i + cols_per_row]
        cols = st.columns(cols_per_row)
        for j, (label, value, theme) in enumerate(chunk):
            metric_box(cols[j], label, value, theme)
        st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)


def _score_bar(score: float, label: str):
    """Barre de similitude DSFR."""
    color = VERT if score >= 66 else (BLEU if score >= 33 else ROUGE)
    st.markdown(f"""
<div style="margin-bottom:6px">
    <div style="font-size:.72rem;font-weight:700;color:#555;text-transform:uppercase;
                letter-spacing:.06em;margin-bottom:4px;">{label}</div>
    <div style="background:{GRIS_B};height:10px;width:100%;position:relative;">
        <div style="background:{color};height:10px;width:{score:.1f}%;"></div>
    </div>
    <div style="font-size:.75rem;color:{color};font-weight:700;margin-top:3px;">{score:.1f} %</div>
</div>""", unsafe_allow_html=True)


# ── Chargement & nettoyage des données ───────────────────────────────────────

@st.cache_data(show_spinner="Chargement des données culturelles…")
def _load_culture():
    data_path = Path(DATA_DIR / "culture_filtrer.xlsx")
    if not data_path.exists():
        return None
    try:
        # On charge TOUTES les colonnes pour pouvoir détecter les noms réels
        return pd.read_excel(data_path)
    except Exception as e:
        st.error(f"⚠️ Erreur de chargement : {e}")
        return None


def _detect_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Retourne la première colonne du df qui correspond à l'un des candidats
    (comparaison insensible à la casse et aux espaces)."""
    normalized = {c.strip().lower(): c for c in df.columns}
    for candidate in candidates:
        hit = normalized.get(candidate.strip().lower())
        if hit:
            return hit
    return None


def _resolve_cols(df: pd.DataFrame) -> bool:
    """
    Met à jour COL avec les noms de colonnes réels trouvés dans df.
    Retourne False et affiche un message si une colonne critique est absente.
    """
    global COL

    ALIASES: dict[str, list[str]] = {
        "ville":         ["libelle_geographique", "libelle geographique", "commune",
                          "nom_commune", "nom commune", "ville", "city"],
        "nom":           ["Nom", "nom", "name", "libelle"],
        "type":          ["Type équipement ou lieu", "type equipement ou lieu",
                          "type", "type_equipement"],
        "label":         ["Label et appellation", "label et appellation",
                          "label", "appellation"],
        "region":        ["Région", "region"],
        "domaine":       ["Domaine", "domaine"],
        "departement":   ["Département", "departement"],
        "fonction1":     ["Fonction_1", "Fonction 1", "fonction1"],
        "fonction2":     ["Fonction_2", "Fonction 2", "fonction2"],
        "fonction3":     ["Fonction_3", "Fonction 3", "fonction3"],
        "fonction4":     ["Fonction_4", "Fonction 4", "fonction4"],
        "fauteuils":     ["Nombre_fauteuils_de_cinema", "nombre fauteuils de cinema",
                          "nb_fauteuils", "fauteuils"],
        "ecrans":        ["Nombre_ecrans", "nombre ecrans", "nb_ecrans", "ecrans"],
        "salles_theatre":["Nombre_de_salles_de_theatre", "nombre de salles de theatre",
                          "nb_salles_theatre"],
        "jauge":         ["Jauge_du_theatre", "jauge du theatre", "jauge"],
        "surface":       ["Surface_Bibliotheque", "surface bibliotheque", "surface"],
        "lat":           ["Latitude", "latitude", "lat"],
        "lon":           ["Longitude", "longitude", "lon", "lng"],
        "code_insee":    ["code_insee", "code insee", "insee"],
        "demographie":   ["Demographie_AP", "demographie", "population"],
    }

    resolved = {}
    missing_critical = []
    for key, candidates in ALIASES.items():
        found = _detect_col(df, candidates)
        if found:
            resolved[key] = found
        else:
            resolved[key] = candidates[0]       # valeur par défaut (peut manquer)
            if key in ("ville", "type", "nom"):  # colonnes indispensables
                missing_critical.append(candidates[0])

    COL = resolved

    if missing_critical:
        st.error(
            f"⚠️ Colonnes introuvables dans le fichier : **{', '.join(missing_critical)}**\n\n"
            f"Colonnes disponibles : `{', '.join(df.columns.tolist())}`"
        )
        return False
    return True


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    for col in [COL["fonction1"], COL["fonction2"], COL["fonction3"], COL["fonction4"]]:
        if col in df.columns:
            df[col] = df[col].astype(str)
    for col, default in {
        COL["fauteuils"]: 0, COL["ecrans"]: 0, COL["salles_theatre"]: 0,
        COL["jauge"]: 0, COL["surface"]: 0, COL["demographie"]: 0
    }.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(default)
    return df


# ── Statistiques ─────────────────────────────────────────────────────────────

def _compute_stats(sub: pd.DataFrame) -> dict:
    empty = dict(
        nb_equip=0, nb_types=0, nb_domaines=0, nb_labels=0,
        pct_labellise=0, cinemas=0, theatres=0, librairies=0,
        monuments=0, total_surface=0, creation=0, diffusion=0, preservation=0
    )
    if sub.empty:
        return empty

    func_cols = [COL["fonction1"], COL["fonction2"], COL["fonction3"], COL["fonction4"]]
    for c in func_cols:
        if c in sub.columns:
            sub[c] = sub[c].astype(str)

    def _cnt_type(keyword):
        return len(sub[sub[COL["type"]].str.contains(keyword, case=False, na=False)]) \
            if COL["type"] in sub.columns else 0

    def _cnt_func(keyword):
        mask = pd.Series([False] * len(sub), index=sub.index)
        for c in func_cols:
            if c in sub.columns:
                mask |= sub[c].str.contains(keyword, case=False, na=False)
        return int(mask.sum())

    return dict(
        nb_equip        = len(sub),
        nb_types        = sub[COL["type"]].nunique()  if COL["type"]   in sub.columns else 0,
        nb_domaines     = sub[COL["domaine"]].nunique() if COL["domaine"] in sub.columns else 0,
        nb_labels       = sub[COL["label"]].nunique() if COL["label"]  in sub.columns else 0,
        pct_labellise   = round(sub[COL["label"]].notna().mean() * 100, 1) if COL["label"] in sub.columns else 0,
        cinemas         = _cnt_type("Cinéma"),
        theatres        = _cnt_type("Théâtre"),
        librairies      = _cnt_type("Librairie"),
        monuments       = _cnt_type("Monument"),
        total_surface   = int(sub[COL["surface"]].sum()) if COL["surface"] in sub.columns else 0,
        creation        = _cnt_func("Création"),
        diffusion       = _cnt_func("Diffusion"),
        preservation    = _cnt_func("Préservation"),
    )


# ── Point d'entrée appelé par app.py ─────────────────────────────────────────

def render():
    # Titre de page
    _section("Culture", "Comparaison des équipements culturels")

    # Chargement
    df = _load_culture()
    if df is None:
        st.error("⚠️ Fichier introuvable : data/processed/culture_filtrer.xlsx")
        return
    df = _clean(df)
    if df.empty:
        st.error("⚠️ Aucune donnée disponible.")
        return

    villes = sorted(df[COL["ville"]].dropna().unique().tolist())

    # ── Sélecteurs de villes ──────────────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        ville1 = st.selectbox("Ville 1", villes, index=0, key="c_v1")
    with col2:
        ville2 = st.selectbox("Ville 2", villes,
                              index=min(1, len(villes) - 1), key="c_v2")
    with col3:
        st.markdown("<div style='height:1.85rem'></div>", unsafe_allow_html=True)
        comparer = st.button("Comparer ▶", key="c_btn", use_container_width=True)

    if ville1 == ville2:
        st.warning("⚠️ Sélectionnez deux communes différentes.")
        return

    if not comparer and "c_compared" not in st.session_state:
        st.markdown("""
        <div style="text-align:center;padding:3rem 0;color:#aaa;font-size:.9rem;">
            Sélectionnez deux communes et cliquez sur <strong>Comparer ▶</strong>
        </div>""", unsafe_allow_html=True)
        return

    if comparer:
        st.session_state["c_compared"] = (ville1, ville2)

    v1, v2 = st.session_state.get("c_compared", (ville1, ville2))

    # ── Filtrage principal ────────────────────────────────────────────────────
    dff  = df[df[COL["ville"]].isin([v1, v2])].copy()
    sub1 = dff[dff[COL["ville"]] == v1]
    sub2 = dff[dff[COL["ville"]] == v2]

    st.markdown(
        f'<p style="font-size:.78rem;color:#888;margin:.3rem 0 1rem 0;">'
        f'Comparaison culturelle — {v1} · {v2}</p>',
        unsafe_allow_html=True
    )

    # ── Filtres secondaires ───────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        domaine_sel  = st.selectbox("Domaine culturel",   ["Tous"] + DOMAINES,        key="c_dom")
    with col_f2:
        type_sel     = st.selectbox("Type d'équipement",  ["Tous"] + HIGHLIGHT_TYPES, key="c_type")
    with col_f3:
        fonction_sel = st.selectbox("Fonction principale",
                                    ["Tous", "Création", "Diffusion", "Préservation"], key="c_fonction")

    def _filt(sub):
        if domaine_sel != "Tous" and COL["domaine"] in sub.columns:
            sub = sub[sub[COL["domaine"]] == domaine_sel]
        if type_sel != "Tous" and COL["type"] in sub.columns:
            sub = sub[sub[COL["type"]].str.contains(type_sel, case=False, na=False)]
        if fonction_sel != "Tous":
            for f in [COL["fonction1"], COL["fonction2"], COL["fonction3"], COL["fonction4"]]:
                if f in sub.columns:
                    sub = sub[sub[f].str.contains(fonction_sel, case=False, na=False)]
        return sub

    sub1 = _filt(sub1)
    sub2 = _filt(sub2)

    stats1 = _compute_stats(sub1)
    stats2 = _compute_stats(sub2)

    # ── KPIs ─────────────────────────────────────────────────────────────────
    _section(f"Indicateurs clés culturels — {v1} vs {v2}")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown(
            f'<div style="font-size:.78rem;font-weight:700;color:{BLEU};margin-bottom:.4rem;">● {v1}</div>',
            unsafe_allow_html=True
        )
        _kpi_row([
            ("Équipements culturels",      f"{stats1['nb_equip']:,}",                           "bleu"),
            ("Types d'équipements",        stats1["nb_types"],                                  "bleu"),
            ("Domaines culturels",         stats1["nb_domaines"],                               "bleu"),
            ("Équipements labellisés",     f"{stats1['nb_labels']} ({stats1['pct_labellise']}%)", "bleu"),
            ("Cinémas",                    stats1["cinemas"],                                   "bleu"),
            ("Théâtres",                   stats1["theatres"],                                  "bleu"),
            ("Librairies",                 stats1["librairies"],                                "bleu"),
            ("Monuments historiques",      stats1["monuments"],                                 "bleu"),
            ("Surface bibliothèques",      f"{stats1['total_surface']:,} m²",                   "bleu"),
        ])

    with col_v2:
        st.markdown(
            f'<div style="font-size:.78rem;font-weight:700;color:{ROUGE};margin-bottom:.4rem;">● {v2}</div>',
            unsafe_allow_html=True
        )
        _kpi_row([
            ("Équipements culturels",      f"{stats2['nb_equip']:,}",                            "rouge"),
            ("Types d'équipements",        stats2["nb_types"],                                   "rouge"),
            ("Domaines culturels",         stats2["nb_domaines"],                                "rouge"),
            ("Équipements labellisés",     f"{stats2['nb_labels']} ({stats2['pct_labellise']}%)", "rouge"),
            ("Cinémas",                    stats2["cinemas"],                                    "rouge"),
            ("Théâtres",                   stats2["theatres"],                                   "rouge"),
            ("Librairies",                 stats2["librairies"],                                 "rouge"),
            ("Monuments historiques",      stats2["monuments"],                                  "rouge"),
            ("Surface bibliothèques",      f"{stats2['total_surface']:,} m²",                    "rouge"),
        ])

    # ── Comparaison directe ───────────────────────────────────────────────────
    _section("Comparaison directe")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric(f"Équipements {v1}", f"{stats1['nb_equip']:,}",
                  delta=f"{stats1['nb_equip'] - stats2['nb_equip']:+,} vs {v2}")
    with col_m2:
        st.metric(f"Équipements {v2}", f"{stats2['nb_equip']:,}")
    with col_m3:
        st.metric(f"Labellisés {v1}",
                  f"{stats1['nb_labels']} ({stats1['pct_labellise']}%)",
                  delta=f"{stats1['pct_labellise'] - stats2['pct_labellise']:+.1f}% vs {v2}")
    with col_m4:
        st.metric(f"Labellisés {v2}", f"{stats2['nb_labels']} ({stats2['pct_labellise']}%)")

    # ── Similitude des types ──────────────────────────────────────────────────
    t1  = set(sub1[COL["type"]].dropna().unique()) if COL["type"] in sub1.columns else set()
    t2  = set(sub2[COL["type"]].dropna().unique()) if COL["type"] in sub2.columns else set()
    jacc = len(t1 & t2) / len(t1 | t2) * 100 if t1 | t2 else 0
    col_sc1, col_sc2, col_sc3 = st.columns([3, 1, 1])
    with col_sc1:
        _score_bar(jacc, f"Similitude des types d'équipements entre {v1} et {v2}")
    with col_sc2:
        st.metric("En commun", len(t1 & t2))
    with col_sc3:
        st.metric("Exclusifs", len((t1 | t2) - (t1 & t2)))

    # ── Répartition par domaine culturel ─────────────────────────────────────
    _section("Répartition par domaine culturel")
    col_a, col_b = st.columns(2)
    for col_p, sub, ville, color in [
        (col_a, sub1, v1, BLEU),
        (col_b, sub2, v2, ROUGE)
    ]:
        with col_p:
            if COL["domaine"] in sub.columns and not sub.empty:
                g = sub[COL["domaine"]].value_counts().head(10).reset_index()
                g.columns = ["Domaine", "Nb"]
                fig = px.bar(g, x="Nb", y="Domaine", orientation="h",
                             color_discrete_sequence=[color])
                fig.update_layout(**CHART_LAYOUT,
                                  title=dict(text=ville, font=dict(size=11)),
                                  yaxis=dict(autorange="reversed"), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    # ── Répartition par type d'équipement ────────────────────────────────────
    _section("Répartition par type d'équipement")
    col_a, col_b = st.columns(2)
    for col_p, sub, ville, color in [
        (col_a, sub1, v1, BLEU),
        (col_b, sub2, v2, ROUGE)
    ]:
        with col_p:
            if COL["type"] in sub.columns and not sub.empty:
                type_counts = sub[COL["type"]].value_counts().reset_index()
                type_counts.columns = ["Type", "Nb"]
                HIGHLIGHT = ["Cinéma", "Théâtre", "Librairie", "Monument",
                             "Bibliothèque", "Centre chorégraphique"]
                other = type_counts[~type_counts["Type"].isin(HIGHLIGHT)]["Nb"].sum()
                highlighted = type_counts[type_counts["Type"].isin(HIGHLIGHT)]
                if other > 0:
                    highlighted = pd.concat([
                        highlighted,
                        pd.DataFrame({"Type": ["Autres"], "Nb": [other]})
                    ])
                fig = px.bar(
                    highlighted.sort_values("Nb", ascending=False).head(10),
                    x="Nb", y="Type", orientation="h",
                    color_discrete_sequence=[color]
                )
                fig.update_layout(**CHART_LAYOUT,
                                  title=dict(text=ville, font=dict(size=11)),
                                  yaxis=dict(autorange="reversed"), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    # ── Répartition par fonction principale ──────────────────────────────────
    _section("Répartition par fonction principale")
    col_a, col_b = st.columns(2)
    for col_p, sub, ville, color in [
        (col_a, sub1, v1, BLEU),
        (col_b, sub2, v2, ROUGE)
    ]:
        with col_p:
            functions = []
            for f in [COL["fonction1"], COL["fonction2"], COL["fonction3"], COL["fonction4"]]:
                if f in sub.columns:
                    functions.extend([
                        val for val in sub[f].dropna().tolist()
                        if str(val).strip().lower() not in ["nan", ""]
                    ])
            if functions:
                fc = pd.Series(functions).value_counts().reset_index()
                fc.columns = ["Fonction", "Nb"]
                fig = px.pie(fc, values="Nb", names="Fonction",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(**CHART_LAYOUT, title=dict(text=ville, font=dict(size=11)))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.caption("Aucune fonction renseignée.")

    # ── Capacité d'accueil spectacle ──────────────────────────────────────────
    _section("Capacité d'accueil spectacle")
    col_a, col_b = st.columns(2)
    for col_p, sub, ville, color in [
        (col_a, sub1, v1, BLEU),
        (col_b, sub2, v2, ROUGE)
    ]:
        with col_p:
            capacity_data = []
            if COL["fauteuils"] in sub.columns:
                cinema = sub[sub[COL["type"]].str.contains("Cinéma", case=False, na=False)]
                if not cinema.empty:
                    capacity_data.append(("Fauteuils cinéma", int(cinema[COL["fauteuils"]].sum())))
            if COL["jauge"] in sub.columns:
                theatre = sub[sub[COL["type"]].str.contains("Théâtre", case=False, na=False)]
                if not theatre.empty:
                    capacity_data.append(("Jauge théâtre", int(theatre[COL["jauge"]].sum())))
            if COL["surface"] in sub.columns:
                library = sub[sub[COL["type"]].str.contains("Bibliothèque", case=False, na=False)]
                if not library.empty:
                    capacity_data.append(("Surface bibliothèques", int(library[COL["surface"]].sum())))
            if capacity_data:
                cap_df = pd.DataFrame(capacity_data, columns=["Type", "Valeur"])
                fig = px.bar(cap_df, x="Valeur", y="Type", orientation="h",
                             color_discrete_sequence=[color])
                fig.update_layout(**CHART_LAYOUT,
                                  title=dict(text=ville, font=dict(size=11)),
                                  yaxis=dict(autorange="reversed"), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    # ── Carte géographique ────────────────────────────────────────────────────
    if COL["lat"] in dff.columns and COL["lon"] in dff.columns:
        _section("Carte des équipements culturels")
        map_df = dff[
            [COL["ville"], COL["lat"], COL["lon"], COL["type"], COL["nom"]]
        ].dropna(subset=[COL["lat"], COL["lon"]])
        if not map_df.empty:
            fig_map = px.scatter_mapbox(
                map_df,
                lat=COL["lat"], lon=COL["lon"],
                color=COL["ville"],
                color_discrete_map={v1: BLEU, v2: ROUGE},
                hover_name=COL["nom"],
                hover_data={COL["type"]: True, COL["lat"]: False, COL["lon"]: False},
                zoom=10,
                mapbox_style="open-street-map",
                height=450,
            )
            fig_map.update_layout(**{**CHART_LAYOUT, "margin": dict(l=0, r=0, t=10, b=0)})
            st.plotly_chart(fig_map, use_container_width=True)

    # ── Analyse des fonctions culturelles (onglets) ───────────────────────────
    _section("Analyse des fonctions culturelles")
    tab_creation, tab_diffusion, tab_preservation = st.tabs(
        ["🎨 Création", "📡 Diffusion", "🏛️ Préservation"]
    )

    def _func_tab(tab, keyword):
        with tab:
            col_a, col_b = st.columns(2)
            for col_p, sub, ville, color in [
                (col_a, sub1, v1, BLEU),
                (col_b, sub2, v2, ROUGE)
            ]:
                with col_p:
                    mask = pd.Series([False] * len(sub), index=sub.index)
                    for f in [COL["fonction1"], COL["fonction2"], COL["fonction3"], COL["fonction4"]]:
                        if f in sub.columns:
                            mask |= sub[f].str.contains(keyword, case=False, na=False)
                    filtered = sub[mask]
                    if not filtered.empty and COL["type"] in filtered.columns:
                        g = filtered[COL["type"]].value_counts().head(10).reset_index()
                        g.columns = ["Type", "Nb"]
                        fig = px.bar(g, x="Nb", y="Type", orientation="h",
                                     color_discrete_sequence=[color])
                        fig.update_layout(
                            **CHART_LAYOUT,
                            title=dict(text=f"Équipements — {ville}", font=dict(size=11)),
                            yaxis=dict(autorange="reversed"), showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.caption(f"Aucun équipement de {keyword.lower()} pour {ville}.")

    _func_tab(tab_creation,    "Création")
    _func_tab(tab_diffusion,   "Diffusion")
    _func_tab(tab_preservation,"Préservation")

    # ── Données brutes ────────────────────────────────────────────────────────
    with st.expander("📋 Données brutes"):
        tab_a, tab_b = st.tabs([f"● {v1}", f"● {v2}"])
        with tab_a:
            st.dataframe(sub1.reset_index(drop=True), use_container_width=True, height=280)
        with tab_b:
            st.dataframe(sub2.reset_index(drop=True), use_container_width=True, height=280)