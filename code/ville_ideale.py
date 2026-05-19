from pathlib import Path
import math

import pandas as pd
import pydeck as pdk
import streamlit as st


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data" / "processed"

BLEU = "#000091"
ROUGE = "#E1000F"
GRIS_B = "#dddddd"
GRIS_F = "#f6f6f6"
TEXTE = "#1e1e1e"


@st.cache_data(show_spinner=False)
def load_city_compare_data():
    general = pd.read_excel(
        DATA_DIR / "donnees_generale_filtrer.xlsx",
        usecols=[
            "nom_standard",
            "code_postal",
            "score",
            "population",
            "superficie_km2",
            "densite",
            "dep_nom",
            "dep_code",
            "reg_nom",
            "academie_nom",
            "niveau_equipements_services_texte",
            "grille_densite_texte",
            "latitude_centre",
            "longitude_centre",
        ],
    ).drop_duplicates(subset=["nom_standard"]).copy()

    general["Ville"] = general["nom_standard"]
    general["Code postal"] = general["code_postal"].astype(str)
    general["Score ville de reve"] = general["score"].astype(str)
    general["score_num"] = pd.to_numeric(
        general["Score ville de reve"].str.replace("/100", "", regex=False),
        errors="coerce",
    )
    general["Population"] = pd.to_numeric(general["population"], errors="coerce").fillna(0).astype(int)
    general["Superficie"] = pd.to_numeric(general["superficie_km2"], errors="coerce")
    general["Densite"] = pd.to_numeric(general["densite"], errors="coerce")
    general["latitude"] = pd.to_numeric(general["latitude_centre"], errors="coerce")
    general["longitude"] = pd.to_numeric(general["longitude_centre"], errors="coerce")

    logement = pd.read_excel(
        DATA_DIR / "logement_filtrer.xlsx",
        usecols=[
            "libelle_geo",
            "moy_prix_m2_whole_appartement",
            "moy_prix_m2_whole_maison",
        ],
    ).drop_duplicates(subset=["libelle_geo"]).rename(
        columns={
            "libelle_geo": "Ville",
            "moy_prix_m2_whole_appartement": "prix_appartement",
            "moy_prix_m2_whole_maison": "prix_maison",
        }
    )

    education = pd.read_excel(
        DATA_DIR / "education_filtrer.xlsx",
        usecols=["Nom_commune", "Statut_public_prive"],
    )
    education_summary = (
        education.groupby("Nom_commune")
        .agg(
            etablissements=("Nom_commune", "size"),
            etablissements_publics=("Statut_public_prive", lambda s: (s == "Public").sum()),
        )
        .reset_index()
        .rename(columns={"Nom_commune": "Ville"})
    )

    sport = pd.read_excel(
        DATA_DIR / "sport.xlsx",
        usecols=["Commune nom", "Nom de l'installation sportive"],
    )
    sport_summary = (
        sport.dropna(subset=["Commune nom"])
        .groupby("Commune nom")
        .agg(installations_sportives=("Nom de l'installation sportive", "nunique"))
        .reset_index()
        .rename(columns={"Commune nom": "Ville"})
    )

    culture = pd.read_excel(
        DATA_DIR / "culture_filtrer.xlsx",
        usecols=["libelle_geographique"],
    )
    culture_summary = (
        culture.dropna(subset=["libelle_geographique"])
        .groupby("libelle_geographique")
        .size()
        .reset_index(name="lieux_culturels")
        .rename(columns={"libelle_geographique": "Ville"})
    )

    df = general.merge(logement, on="Ville", how="left")
    df = df.merge(education_summary, on="Ville", how="left")
    df = df.merge(sport_summary, on="Ville", how="left")
    df = df.merge(culture_summary, on="Ville", how="left")

    for col in [
        "prix_appartement",
        "prix_maison",
        "etablissements",
        "etablissements_publics",
        "installations_sportives",
        "lieux_culturels",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Population fmt"] = df["Population"].map(lambda v: f"{int(v):,}".replace(",", "\u202f"))
    df["Superficie fmt"] = df["Superficie"].map(lambda v: f"{v:.0f} km²" if pd.notna(v) else "n.d.")
    df["Densite fmt"] = df["Densite"].map(
        lambda v: f"{int(v):,} hab/km²".replace(",", "\u202f") if pd.notna(v) else "n.d."
    )
    df["prix_appartement fmt"] = df["prix_appartement"].map(
        lambda v: f"{int(v):,} €/m²".replace(",", "\u202f") if pd.notna(v) else "n.d."
    )
    df["prix_maison fmt"] = df["prix_maison"].map(
        lambda v: f"{int(v):,} €/m²".replace(",", "\u202f") if pd.notna(v) else "n.d."
    )
    df["etablissements fmt"] = df["etablissements"].map(
        lambda v: f"{int(v)}" if pd.notna(v) else "n.d."
    )
    df["etablissements_publics fmt"] = df["etablissements_publics"].map(
        lambda v: f"{int(v)}" if pd.notna(v) else "n.d."
    )
    df["installations_sportives fmt"] = df["installations_sportives"].map(
        lambda v: f"{int(v)}" if pd.notna(v) else "n.d."
    )
    df["lieux_culturels fmt"] = df["lieux_culturels"].map(
        lambda v: f"{int(v)}" if pd.notna(v) else "n.d."
    )
    df["resume_geo"] = df.apply(
        lambda row: f"{row['dep_nom']} ({row['dep_code']}) · {row['reg_nom']}",
        axis=1,
    )
    df["resume_equipements"] = df["niveau_equipements_services_texte"].fillna("n.d.")
    df["resume_densite"] = df["grille_densite_texte"].fillna("n.d.")

    return df.sort_values("score_num", ascending=False, na_position="last").reset_index(drop=True)


def _map_view_from_points(df: pd.DataFrame):
    coords = df[["latitude", "longitude"]].dropna()
    if coords.empty:
        return pdk.ViewState(latitude=46.5, longitude=2.2, zoom=4.5, pitch=0)

    lat_min, lat_max = coords["latitude"].min(), coords["latitude"].max()
    lon_min, lon_max = coords["longitude"].min(), coords["longitude"].max()

    lat_span = max(lat_max - lat_min, 0.4)
    lon_span = max(lon_max - lon_min, 0.4)
    zoom_lon = math.log2(360 / (lon_span * 2.6))
    zoom_lat = math.log2(170 / (lat_span * 2.6))
    zoom = min(zoom_lon, zoom_lat, 10)
    zoom = max(zoom, 4.2)

    return pdk.ViewState(
        latitude=(lat_min + lat_max) / 2,
        longitude=(lon_min + lon_max) / 2,
        zoom=zoom,
        pitch=0,
    )


def _build_tooltip_html(row: pd.Series) -> str:
    return f"""
    <div style="min-width:320px;max-width:360px;padding:14px 16px;background:#ffffff;color:#1e1e1e;">
      <div style="font-size:18px;font-weight:700;color:{BLEU};margin-bottom:2px;">{row['Ville']}</div>
      <div style="font-size:12px;color:#666;margin-bottom:12px;">{row['resume_geo']}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px 14px;font-size:13px;">
        <div><div style="color:#666;">Code postal</div><div style="font-weight:700;">{row['Code postal']}</div></div>
        <div><div style="color:#666;">Score</div><div style="font-weight:700;color:{ROUGE};">{row['Score ville de reve']}</div></div>
        <div><div style="color:#666;">Population</div><div style="font-weight:700;">{row['Population fmt']} hab.</div></div>
        <div><div style="color:#666;">Densité</div><div style="font-weight:700;">{row['Densite fmt']}</div></div>
        <div><div style="color:#666;">Superficie</div><div style="font-weight:700;">{row['Superficie fmt']}</div></div>
        <div><div style="color:#666;">Académie</div><div style="font-weight:700;">{row['academie_nom']}</div></div>
      </div>
      <div style="margin-top:12px;padding-top:10px;border-top:1px solid #dddddd;font-size:13px;line-height:1.45;">
        <div style="font-weight:700;margin-bottom:6px;">Indicateurs clés</div>
        <div>Logement : {row['prix_appartement fmt']} appt. · {row['prix_maison fmt']} maison</div>
        <div>Éducation : {row['etablissements fmt']} établissements · {row['etablissements_publics fmt']} publics</div>
        <div>Sport : {row['installations_sportives fmt']} installations</div>
        <div>Culture : {row['lieux_culturels fmt']} lieux</div>
      </div>
      <div style="margin-top:12px;padding-top:10px;border-top:1px solid #dddddd;font-size:12px;color:#444;">
        <div><span style="color:#666;">Densité urbaine :</span> {row['resume_densite']}</div>
        <div><span style="color:#666;">Équipements :</span> {row['resume_equipements']}</div>
      </div>
    </div>
    """


def _render_city_card(row: pd.Series, color: str):
    st.markdown(
        f"""
        <div style="background:#fff;border:1px solid {GRIS_B};border-top:4px solid {color};padding:16px 18px;height:100%;">
          <div style="font-size:1.1rem;font-weight:700;color:{color};margin-bottom:4px;">{row['Ville']}</div>
          <div style="font-size:0.8rem;color:#666;margin-bottom:14px;">{row['resume_geo']}</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px 14px;font-size:0.86rem;">
            <div><div style="color:#666;">Code postal</div><div style="font-weight:700;">{row['Code postal']}</div></div>
            <div><div style="color:#666;">Score</div><div style="font-weight:700;">{row['Score ville de reve']}</div></div>
            <div><div style="color:#666;">Population</div><div style="font-weight:700;">{row['Population fmt']} hab.</div></div>
            <div><div style="color:#666;">Densité</div><div style="font-weight:700;">{row['Densite fmt']}</div></div>
            <div><div style="color:#666;">Prix appt.</div><div style="font-weight:700;">{row['prix_appartement fmt']}</div></div>
            <div><div style="color:#666;">Prix maison</div><div style="font-weight:700;">{row['prix_maison fmt']}</div></div>
            <div><div style="color:#666;">Établissements</div><div style="font-weight:700;">{row['etablissements fmt']}</div></div>
            <div><div style="color:#666;">Sport</div><div style="font-weight:700;">{row['installations_sportives fmt']}</div></div>
            <div><div style="color:#666;">Culture</div><div style="font-weight:700;">{row['lieux_culturels fmt']}</div></div>
            <div><div style="color:#666;">Académie</div><div style="font-weight:700;">{row['academie_nom']}</div></div>
          </div>
          <div style="margin-top:14px;padding-top:10px;border-top:1px solid {GRIS_B};font-size:0.82rem;line-height:1.5;">
            <div><span style="color:#666;">Densité urbaine :</span> {row['resume_densite']}</div>
            <div><span style="color:#666;">Équipements :</span> {row['resume_equipements']}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render():
    df = load_city_compare_data()
    city_options = df["Ville"].tolist()

    default_1 = st.session_state.get("global_ville1", city_options[0])
    default_2 = st.session_state.get("global_ville2", city_options[1] if len(city_options) > 1 else city_options[0])
    if default_1 not in city_options:
        default_1 = city_options[0]
    if default_2 not in city_options:
        default_2 = city_options[1] if len(city_options) > 1 else city_options[0]

    st.markdown(
        '<div class="section-title">Trouver la ville ideale'
        f'<span class="section-sub">— {len(df)} villes classees par score</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin-bottom:16px;color:#555;font-size:0.98rem;">
            Sélectionnez deux villes dans le classement pour afficher leur position sur la carte et un résumé comparatif.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Retour a l'accueil", key="back_to_home_ideal"):
        st.query_params["page"] = "accueil"
        st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        ville_1 = st.selectbox("Ville 1", city_options, index=city_options.index(default_1), key="ideal_city_1")
    with c2:
        ville_2 = st.selectbox("Ville 2", city_options, index=city_options.index(default_2), key="ideal_city_2")

    st.session_state["global_ville1"] = ville_1
    st.session_state["global_ville2"] = ville_2

    recherche = st.text_input(
        "Rechercher dans le classement",
        placeholder="Nom de ville ou code postal",
        key="ideal_city_search",
    ).strip()

    display_df = df[["Ville", "Code postal", "Score ville de reve"]].copy()
    display_df["Sélection"] = display_df["Ville"].map(
        lambda v: "Ville 1" if v == ville_1 else ("Ville 2" if v == ville_2 else "")
    )
    display_df.index = display_df.index + 1

    if recherche:
        query = recherche.lower()
        mask = (
            display_df["Ville"].astype(str).str.lower().str.contains(query, na=False)
            | display_df["Code postal"].astype(str).str.contains(recherche, na=False)
        )
        display_df = display_df[mask].copy()

    st.dataframe(
        display_df,
        use_container_width=True,
        height=500,
        column_config={
            "Code postal": st.column_config.TextColumn("Code postal"),
            "Score ville de reve": st.column_config.TextColumn("Score ville de reve"),
            "Sélection": st.column_config.TextColumn("Sélection"),
        },
    )

    if ville_1 == ville_2:
        st.warning("Sélectionnez deux villes différentes pour afficher la carte comparative.")
        return

    selected = df[df["Ville"].isin([ville_1, ville_2])].copy()
    selected["color"] = selected["Ville"].map({ville_1: [0, 0, 145, 180], ville_2: [225, 0, 15, 180]})
    selected["radius"] = selected["Population"].clip(lower=1).pow(0.5) * 90
    selected["tooltip_html"] = selected.apply(_build_tooltip_html, axis=1)

    st.markdown(
        '<div class="section-title">Carte comparative'
        '<span class="section-sub">— survolez un point pour afficher le résumé</span></div>',
        unsafe_allow_html=True,
    )

    scatter = pdk.Layer(
        "ScatterplotLayer",
        data=selected,
        get_position="[longitude, latitude]",
        get_radius="radius",
        get_fill_color="color",
        get_line_color=[255, 255, 255, 220],
        line_width_min_pixels=2,
        pickable=True,
        stroked=True,
        filled=True,
    )
    labels = pdk.Layer(
        "TextLayer",
        data=selected,
        get_position="[longitude, latitude]",
        get_text="Ville",
        get_size=16,
        get_color=[30, 30, 30, 220],
        get_alignment_baseline="'top'",
        get_pixel_offset=[0, 16],
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style="light",
            initial_view_state=_map_view_from_points(selected),
            layers=[scatter, labels],
            tooltip={"html": "{tooltip_html}", "style": {"backgroundColor": "transparent", "color": "#1e1e1e"}},
        ),
        use_container_width=True,
    )

    st.markdown(
        '<div class="section-title">Résumé comparatif rapide</div>',
        unsafe_allow_html=True,
    )
    col_left, col_right = st.columns(2)
    with col_left:
        _render_city_card(selected[selected["Ville"] == ville_1].iloc[0], BLEU)
    with col_right:
        _render_city_card(selected[selected["Ville"] == ville_2].iloc[0], ROUGE)
