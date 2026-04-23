# education.py — Page Éducation (charte DSFR)
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go

from dsfr import BLEU, ROUGE, VERT, GRIS_F, GRIS_B, TEXTE, COLORS, metric_box

def render():
    # ── Titre de section ──────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-title">Établissements scolaires</div>',
        unsafe_allow_html=True,
    )

    # ── Chargement ─────────────────────────────────────────────────────────────
    try:
        @st.cache_data
        def load_data():
            return pd.read_excel("../data/processed/education_filtrer.xlsx")

        df = load_data()
    except FileNotFoundError:
        st.error("Fichier introuvable : `../data/processed/education_filtrer.xlsx`")
        return

    # Nettoyage coordonnées
    coords = df["position"].dropna().str.split(",", expand=True)
    coords.columns = ["lat", "lon"]
    df.loc[coords.index, "lat"] = pd.to_numeric(coords["lat"], errors="coerce")
    df.loc[coords.index, "lon"] = pd.to_numeric(coords["lon"], errors="coerce")

    # ───────────────────────────────────────────────
    # 🔵 Sélecteurs de villes (2 villes à comparer)
    # ───────────────────────────────────────────────
    st.markdown(
        '<div class="section-title" style="margin-top:0;font-size:0.72rem;">Sélection des villes</div>',
        unsafe_allow_html=True,
    )

    villes_dispo = sorted(df["Nom_commune"].dropna().unique().tolist())

    c1, c2 = st.columns(2)
    with c1:
        ville_1 = st.selectbox("Ville 1", villes_dispo, index=0)
    with c2:
        ville_2 = st.selectbox("Ville 2", villes_dispo, index=1)

    # Filtrage sur les deux villes
    df_villes = df[df["Nom_commune"].isin([ville_1, ville_2])]

    # Sous-titre dynamique
    st.markdown(
        f'<div class="section-sub" style="margin-bottom:18px;">— {ville_1} & {ville_2}</div>',
        unsafe_allow_html=True,
    )

    # ───────────────────────────────────────────────
    # 🔵 Filtres supplémentaires (type, statut, options)
    # ───────────────────────────────────────────────
    st.markdown(
        '<div class="section-title" style="margin-top:0;font-size:0.72rem;">Filtres</div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        types = ["Tous"] + sorted(df_villes["Type_etablissement"].dropna().unique().tolist())
        type_choisi = st.selectbox("Type d'établissement", types)

    with f2:
        statuts = ["Tous"] + sorted(df_villes["Statut_public_prive"].dropna().unique().tolist())
        statut_choisi = st.selectbox("Public / Privé", statuts)

    with f3:
        spec_options = {
            "Segpa": "Segpa",
            "Cinéma": "Section_cinema",
            "Théâtre": "Section_theatre",
            "Arts": "Section_arts",
            "Sport": "Section_sport",
            "Internationale": "Section_internationale",
            "Européenne": "Section_europeenne",
        }
        specs_choisies = st.multiselect("Spécialités", list(spec_options.keys()))

    # Filtrage final
    filtered = df_villes.copy()
    if type_choisi != "Tous":
        filtered = filtered[filtered["Type_etablissement"] == type_choisi]
    if statut_choisi != "Tous":
        filtered = filtered[filtered["Statut_public_prive"] == statut_choisi]
    for label in specs_choisies:
        col = spec_options[label]
        filtered = filtered[filtered[col] == 1]


    # ── KPIs DSFR ──────────────────────────────────────────────────────────────
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    kpi1, kpi2, kpi3 = st.columns(3)

    n_pub  = (filtered["Statut_public_prive"] == "Public").sum()
    n_priv = (filtered["Statut_public_prive"] == "Privé").sum()

    metric_box(kpi1, "Total établissements", len(filtered), "bleu")
    metric_box(kpi2, "Établissements publics", n_pub,  "vert")
    metric_box(kpi3, "Établissements privés",  n_priv, "rouge")

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    # ── Graphiques répartition ────────────────────────────────────────────────
    st.markdown(
        '<div class="section-title">Répartition</div>',
        unsafe_allow_html=True,
    )

    chart1, chart2 = st.columns(2)

    with chart1:
        type_counts = filtered["Type_etablissement"].value_counts()
        total_t = type_counts.sum()
        if total_t > 0:
            fig = go.Figure()
            for i, (t, cnt) in enumerate(type_counts.items()):
                pct = cnt / total_t * 100
                fig.add_trace(go.Bar(
                    name=str(t), x=[pct], y=["Types"], orientation="h",
                    text=f"{t}<br>{cnt} ({pct:.0f}%)", textposition="inside",
                    marker_color=COLORS[i % len(COLORS)],
                ))
            fig.update_layout(
                barmode="stack",
                title=dict(text="Par type d'établissement", font=dict(size=13, color=BLEU)),
                xaxis=dict(range=[0, 100], ticksuffix="%",
                           gridcolor=GRIS_B, tickfont=dict(size=11, color="#555")),
                yaxis=dict(tickfont=dict(size=11, color="#555")),
                height=140,
                margin=dict(l=0, r=0, t=44, b=0),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor=GRIS_F,
                font=dict(family="Source Sans Pro, sans-serif", color=TEXTE),
            )
            st.plotly_chart(fig, use_container_width=True)

    with chart2:
        n_total = len(filtered)
        if n_total > 0:
            fig2 = go.Figure()
            for statut, color in [("Public", BLEU), ("Privé", ROUGE)]:
                cnt = (filtered["Statut_public_prive"] == statut).sum()
                pct = cnt / n_total * 100
                fig2.add_trace(go.Bar(
                    name=statut, x=[pct], y=["Statut"], orientation="h",
                    text=f"{statut}<br>{cnt} ({pct:.0f}%)", textposition="inside",
                    marker_color=color,
                ))
            fig2.update_layout(
                barmode="stack",
                title=dict(text="Public / Privé", font=dict(size=13, color=BLEU)),
                xaxis=dict(range=[0, 100], ticksuffix="%",
                           gridcolor=GRIS_B, tickfont=dict(size=11, color="#555")),
                yaxis=dict(tickfont=dict(size=11, color="#555")),
                height=140,
                margin=dict(l=0, r=0, t=44, b=0),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor=GRIS_F,
                font=dict(family="Source Sans Pro, sans-serif", color=TEXTE),
            )
            st.plotly_chart(fig2, use_container_width=True)

    # ── Carte interactive ─────────────────────────────────────────────────────
    st.markdown(
        f'<div class="section-title">Carte des établissements'
        f'<span class="section-sub">— {len(filtered)} résultats</span></div>',
        unsafe_allow_html=True,
    )

    # On récupère uniquement les points géolocalisés
    map_data = filtered.dropna(subset=["lat", "lon"])

    # Si on a des points → centrage automatique
    if len(map_data) > 0:
        center_lat = map_data["lat"].mean()
        center_lon = map_data["lon"].mean()
        zoom = 12
    else:
        # fallback France entière
        center_lat, center_lon, zoom = 47.0, 2.0, 6

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="CartoDB positron",
    )

    # Ajout des marqueurs
    for _, row in map_data.iterrows():
        post_bac  = "Oui" if row.get("Post_BAC") == 1 else "Non"
        voie_gen  = "Oui" if row.get("Voie_generale") == 1 else "Non"
        nom       = row.get("Nom_etablissement", "–")
        statut    = row.get("Statut_public_prive", "–")
        type_etab = row.get("Type_etablissement", "–")
        web       = row.get("Web", "")
        mail      = str(row.get("Mail", "–"))
        date_ouv  = str(row.get("date_ouverture", "–"))

        web_html = (
            f'<a href="{web}" target="_blank" style="color:{BLEU};">{web}</a>'
            if pd.notna(web) and web else "–"
        )

        # Badge statut DSFR
        if statut == "Public":
            badge_bg, badge_color = "#dbeafe", "#1e40af"
            marker_color = "#000091"
        else:
            badge_bg, badge_color = "#fce7f3", "#9d174d"
            marker_color = "#E1000F"

        popup_html = f"""
        <div style="font-family:'Source Sans Pro',sans-serif;
                    min-width:260px;max-width:310px;padding:6px 4px;">
            <div style="font-size:13px;font-weight:700;margin-bottom:8px;color:{TEXTE};
                        border-bottom:2px solid {BLEU};padding-bottom:5px;">
                {nom}
            </div>
            <table style="width:100%;font-size:12px;border-collapse:collapse;">
                <tr>
                    <td style="color:#888;padding:4px 0;width:42%;">Statut</td>
                    <td>
                        <span style="background:{badge_bg};color:{badge_color};
                            padding:2px 9px;border-radius:0;
                            font-size:11px;font-weight:600;">
                            {statut}
                        </span>
                    </td>
                </tr>
                <tr>
                    <td style="color:#888;padding:4px 0;">Type</td>
                    <td style="font-weight:600;">{type_etab}</td>
                </tr>
                <tr>
                    <td style="color:#888;padding:4px 0;">Post-Bac</td>
                    <td style="font-weight:600;">{post_bac}</td>
                </tr>
                <tr>
                    <td style="color:#888;padding:4px 0;">Lycée général</td>
                    <td style="font-weight:600;">{voie_gen}</td>
                </tr>
                <tr>
                    <td style="color:#888;padding:4px 0;">Site web</td>
                    <td style="font-weight:600;word-break:break-all;">{web_html}</td>
                </tr>
                <tr>
                    <td style="color:#888;padding:4px 0;">Mail</td>
                    <td style="font-weight:600;word-break:break-all;">{mail}</td>
                </tr>
                <tr>
                    <td style="color:#888;padding:4px 0;">Ouverture</td>
                    <td style="font-weight:600;">{date_ouv}</td>
                </tr>
            </table>
        </div>
        """

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.85,
            weight=2,
            popup=folium.Popup(popup_html, max_width=330),
            tooltip=nom,
        ).add_to(m)

    st_folium(m, width="100%", height=520, returned_objects=[])

    # Légende carte
    st.markdown(f"""
<div style="display:flex;gap:20px;font-size:0.72rem;color:#555;
            margin-top:6px;font-family:'Source Sans Pro',sans-serif;">
    <span>
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;
                     background:{BLEU};margin-right:5px;vertical-align:middle;"></span>
        Public
    </span>
    <span>
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;
                     background:{ROUGE};margin-right:5px;vertical-align:middle;"></span>
        Privé
    </span>
</div>
""", unsafe_allow_html=True)

    # ── Tableau ───────────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="section-title">Liste des établissements'
        f'<span class="section-sub">— {len(filtered)} entrées</span></div>',
        unsafe_allow_html=True,
    )

    display_cols = [
        "Nom_etablissement", "Type_etablissement", "Statut_public_prive",
        "Nom_commune", "Libelle_departement", "Telephone", "date_ouverture",
    ]
    display_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(
        filtered[display_cols].reset_index(drop=True),
        use_container_width=True,
        height=340,
    )
