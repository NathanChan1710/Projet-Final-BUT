from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data" / "processed"


@st.cache_data(show_spinner=False)
def load_villes_table():
    df = pd.read_excel(
        DATA_DIR / "donnees_generale_filtrer.xlsx",
        usecols=[
            "nom_standard",
            "population",
            "code_postal",
        ],
    )
    df = (
        df.dropna(subset=["nom_standard", "population"])
        .drop_duplicates(subset=["nom_standard"])
        .sort_values("population", ascending=False)
        .reset_index(drop=True)
    )

    df["Population"] = pd.to_numeric(df["population"], errors="coerce").fillna(0).astype(int)
    df["Code postal"] = df["code_postal"].astype(str)
    df["Ville"] = df["nom_standard"]

    table_df = df[["Ville", "Population", "Code postal"]].copy()
    table_df.index = table_df.index + 1
    return table_df


def render():
    villes_df = load_villes_table()

    st.markdown(
        '<div class="section-title">Toutes les villes disponibles'
        f'<span class="section-sub">— {len(villes_df)} villes</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin-bottom:16px;color:#555;font-size:0.98rem;">
            Liste des villes présentes dans la base de données générales, triées par nombre d'habitants.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Retour a l'accueil", key="back_to_home"):
        st.query_params["page"] = "accueil"
        st.rerun()

    recherche = st.text_input(
        "Rechercher une ville ou un code postal",
        placeholder="Ex. Paris ou 75000",
    ).strip()

    filtered_df = villes_df
    if recherche:
        query = recherche.lower()
        mask = (
            villes_df["Ville"].astype(str).str.lower().str.contains(query, na=False)
            | villes_df["Code postal"].astype(str).str.contains(recherche, na=False)
        )
        filtered_df = villes_df[mask].copy()

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=650,
        column_config={
            "Population": st.column_config.NumberColumn("Population", format="%d"),
            "Code postal": st.column_config.TextColumn("Code postal"),
        },
    )
