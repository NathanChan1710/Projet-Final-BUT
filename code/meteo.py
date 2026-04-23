# meteo.py — Page Météo (charte DSFR)
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

from dsfr import BLEU, ROUGE, GRIS_F, GRIS_B, TEXTE, metric_box
from pathlib import Path
BASE_DIR = Path(__file__).parent          # dossier code/
DATA_DIR = BASE_DIR.parent / "data" / "processed"

# ── CHARGEMENT DES COORDONNÉES ───────────────────────────────────────────────
coordonnees_df = pd.read_excel(DATA_DIR/ "coordonnees_villes.xlsx")

VILLES = {
    row["ville"]: {"lat": row["latitude"], "lon": row["longitude"]}
    for _, row in coordonnees_df.iterrows()
}


VARIABLES_HISTORIQUE = {
    "Température (°C)":       "temperature_2m",
    "Humidité relative (%)":  "relativehumidity_2m",
    "Vitesse du vent (km/h)": "windspeed_10m",
    "Précipitations (mm)":    "precipitation",
}

WMO_CODES = {
    0: ("Clair", "☀️"),   1: ("Clair", "☀️"),
    2: ("Nuageux", "⛅"), 3: ("Couvert", "☁️"),
    45: ("Brouillard", "🌫️"), 48: ("Brouillard", "🌫️"),
    51: ("Bruine", "🌦️"), 53: ("Bruine", "🌦️"), 55: ("Bruine", "🌦️"),
    61: ("Pluie", "🌧️"), 63: ("Pluie", "🌧️"), 65: ("Forte pluie", "🌧️"),
    71: ("Neige", "❄️"),  73: ("Neige", "❄️"),  75: ("Neige", "❄️"),
    80: ("Averses", "🌦️"), 81: ("Averses", "🌦️"), 82: ("Averses", "🌦️"),
    95: ("Orage", "⛈️"),   96: ("Orage", "⛈️"),   99: ("Orage", "⛈️"),
}

JOURS_FR = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]


# ── API ───────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_historique(lat, lon, var_api):
    end   = date.today() - timedelta(days=1)
    start = end - timedelta(days=365)
    r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
        "latitude": lat, "longitude": lon,
        "start_date": start.isoformat(), "end_date": end.isoformat(),
        "hourly": var_api, "timezone": "Europe/Paris",
    }, timeout=20)
    r.raise_for_status()
    data = r.json()
    return pd.DataFrame({
        "datetime": pd.to_datetime(data["hourly"]["time"]),
        "value":    data["hourly"][var_api],
    })


@st.cache_data(ttl=3600)
def fetch_previsions(lat, lon):
    r = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": lat, "longitude": lon,
        "daily":  "temperature_2m_max,temperature_2m_min,precipitation_sum,"
                  "windspeed_10m_max,weathercode",
        "hourly": "relativehumidity_2m",
        "timezone": "Europe/Paris",
        "forecast_days": 7,
    }, timeout=20)
    r.raise_for_status()
    data  = r.json()
    daily = data["daily"]
    df_h  = pd.DataFrame({
        "dt": pd.to_datetime(data["hourly"]["time"]),
        "rh": data["hourly"]["relativehumidity_2m"],
    })
    df_h["date"] = df_h["dt"].dt.date
    daily["relativehumidity_2m_mean"] = (
        df_h.groupby("date")["rh"].mean().round(1).tolist()
    )
    return daily


def get_forecast_value(daily, var_label, i):
    if var_label == "Température (°C)":
        mx = daily.get("temperature_2m_max", [None] * 7)[i]
        mn = daily.get("temperature_2m_min", [None] * 7)[i]
        return f"{round(mx)}° / {round(mn)}°" if mx is not None else "—"
    if var_label == "Humidité relative (%)":
        v = daily.get("relativehumidity_2m_mean", [None] * 7)
        return f"{v[i]:.0f} %" if i < len(v) and v[i] is not None else "—"
    if var_label == "Vitesse du vent (km/h)":
        v = daily.get("windspeed_10m_max", [None] * 7)[i]
        return f"{round(v)} km/h" if v is not None else "—"
    if var_label == "Précipitations (mm)":
        v = daily.get("precipitation_sum", [None] * 7)[i]
        return f"{round(v, 1)} mm" if v is not None else "—"
    return "—"


def agreger(df):
    return df.set_index("datetime").resample("D")["value"].mean().reset_index()


# ── RENDU ──────────────────────────────────────────────────────────────────────
def render():

    # ── Sélecteurs ───────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        ville_1 = st.selectbox("Ville 1", sorted(VILLES.keys()))

    with col2:
        ville_2 = st.selectbox("Ville 2", sorted(VILLES.keys()))

    with col3:
        var_label = st.selectbox("Indicateur", list(VARIABLES_HISTORIQUE.keys()))

    if ville_1 == ville_2:
        st.warning("Veuillez choisir deux villes différentes")
        st.stop()

    lat1, lon1 = VILLES[ville_1]["lat"], VILLES[ville_1]["lon"]
    lat2, lon2 = VILLES[ville_2]["lat"], VILLES[ville_2]["lon"]
    var_api = VARIABLES_HISTORIQUE[var_label]

    # ── Prévisions ───────────────────────────────────────────────────────────
    st.markdown(f"### Prévisions 7 jours — {ville_1}")

    try:
        daily = fetch_previsions(lat1, lon1)
        cols  = st.columns(7)

        for i, col in enumerate(cols):
            d = date.today() + timedelta(days=i)
            wmo = daily.get("weathercode", [0]*7)[i]
            cond, ico = WMO_CODES.get(wmo, ("—", "?"))
            val = get_forecast_value(daily, var_label, i)

            with col:
                st.markdown(f"""
                **{ "Aujourd'hui" if i==0 else JOURS_FR[d.weekday()] }**  
                {d.day}/{d.month}  
                {ico} {cond}  
                **{val}**
                """)

    except Exception as e:
        st.error(f"Erreur prévisions : {e}")

    # ── Historique ───────────────────────────────────────────────────────────
    st.markdown(f"### Historique 12 mois — {ville_1} vs {ville_2}")

    try:
        df1 = fetch_historique(lat1, lon1, var_api)
        df2 = fetch_historique(lat2, lon2, var_api)

        df1_d = agreger(df1)
        df2_d = agreger(df2)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df1_d["datetime"], y=df1_d["value"],
            name=ville_1, mode="lines",
            line=dict(color=BLEU)
        ))

        fig.add_trace(go.Scatter(
            x=df2_d["datetime"], y=df2_d["value"],
            name=ville_2, mode="lines",
            line=dict(color=ROUGE, dash="dot")
        ))

        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur historique : {e}")