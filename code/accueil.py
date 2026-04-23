import streamlit as st
from dsfr import BLEU, ROUGE, VERT, GRIS_F, GRIS_B, TEXTE, metric_box
def render():

    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(180deg, #f6f7fb 0%, #ffffff 42%);
                color: #161616;
                font-family: "Marianne", "Segoe UI", sans-serif;
            }

            .page-shell {
                max-width: 1250px;
                margin: 0 auto;
                padding: 0 1.5rem 3.5rem;
            }

            .top-spacer {
                height: 105px;
            }

            .hero {
                text-align: center;
                margin: 1.5rem auto 0;
                max-width: 900px;
            }

            .hero-title {
                font-size: clamp(2rem, 4vw, 3.25rem);
                line-height: 1.15;
                font-weight: 700;
                color: #000091;
                margin-bottom: 1rem;
            }

            .hero-subtitle {
                font-size: 1.15rem;
                line-height: 1.7;
                color: #3a3a3a;
                max-width: 760px;
                margin: 0 auto;
            }

            .cards-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 1.25rem;
                margin-top: 3.4rem;
            }

            .info-card {
                background: #ffffff;
                border: 1px solid #e3e6f0;
                min-height: 330px;
                padding: 2rem 1.5rem 1.4rem;
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
                box-shadow: 0 16px 30px rgba(0, 0, 60, 0.04);
            }

            .card-icon {
                width: 68px;
                height: 68px;
                border-radius: 999px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1.2rem;
                border: 2px solid #d9dcf7;
                background: linear-gradient(135deg, #ffffff 0%, #f7f8ff 100%);
            }

            .card-icon svg {
                width: 34px;
                height: 34px;
                stroke: #000091;
            }

            .card-title {
                font-size: 1.6rem;
                line-height: 1.25;
                font-weight: 700;
                color: #000091;
                margin-bottom: 0.9rem;
            }

            .card-text {
                font-size: 1.03rem;
                line-height: 1.65;
                color: #3a3a3a;
                max-width: 220px;
                margin: 0 auto;
            }

            .card-bottom {
                margin-top: auto;
                width: 100%;
                padding-top: 1.4rem;
                border-bottom: 4px solid #e1000f;
            }

            .sources {
                margin: 3rem auto 0;
                max-width: 840px;
                background: rgba(255, 255, 255, 0.94);
                border: 1px solid #d6d6f0;
                border-radius: 18px;
                padding: 1.5rem 1.75rem;
                box-shadow: 0 16px 40px rgba(0, 0, 80, 0.05);
            }

            .sources p {
                font-size: 1rem;
                line-height: 1.7;
                color: #3a3a3a;
                margin-bottom: 1rem;
            }

            .sources-title {
                font-weight: 700;
                color: #000091;
                margin-bottom: 0.6rem;
            }

            .sources ul {
                margin: 0;
                padding-left: 1.2rem;
            }

            .sources li {
                margin: 0.45rem 0;
            }

            .sources a {
                color: #000091;
                text-decoration: none;
                font-weight: 600;
            }

            .sources a:hover {
                text-decoration: underline;
            }

            @media (max-width: 1100px) {
                .cards-grid {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }
            }

            @media (max-width: 700px) {
                .top-spacer {
                    height: 72px;
                }

                .cards-grid {
                    grid-template-columns: 1fr;
                }

                .info-card {
                    min-height: auto;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


    person_icon = """
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4Z"></path>
        <path d="M5.5 20a6.5 6.5 0 0 1 13 0"></path>
        <path d="M17.8 5.5a2.2 2.2 0 1 1 3.2 1.9c-.9.5-1.5 1-1.5 2"></path>
        <path d="M19.5 12h.01"></path>
    </svg>
    """

    city_icon = """
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 21h18"></path>
        <path d="M5 21V9l6-3v15"></path>
        <path d="M11 21V5l8 3v13"></path>
        <path d="M8 12h.01"></path>
        <path d="M8 15h.01"></path>
        <path d="M14 10h.01"></path>
        <path d="M14 13h.01"></path>
        <path d="M17 10h.01"></path>
        <path d="M17 13h.01"></path>
    </svg>
    """

    criteria_icon = """
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 6h10"></path>
        <path d="M4 12h16"></path>
        <path d="M4 18h12"></path>
        <circle cx="17" cy="6" r="2"></circle>
        <circle cx="9" cy="18" r="2"></circle>
    </svg>
    """

    happy_icon = """
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"></circle>
        <path d="M9 10h.01"></path>
        <path d="M15 10h.01"></path>
        <path d="M8.5 14.5a5 5 0 0 0 7 0"></path>
    </svg>
    """


    st.markdown('<div class="page-shell">', unsafe_allow_html=True)
    st.markdown('<div class="top-spacer"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <section class="hero">
            <div class="hero-title">
                <strong>Application de comparaison de villes françaises</strong>
            </div>
            <div class="hero-subtitle">
                En quelques clics, comparez les villes que vous souhaitez
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    cards_html = f"""
    <section class="cards-grid">
        <article class="info-card">
            <div class="card-icon">{person_icon}</div>
            <div class="card-title">Envie De S'installer Ailleurs ?</div>
            <div class="card-text">mais hésiter entre plusieurs villes</div>
            <div class="card-bottom"></div>
        </article>
        <article class="info-card">
            <div class="card-icon">{city_icon}</div>
            <div class="card-title">Plus De XXX Villes À Comparer</div>
            <div class="card-text">de plus 20 000 habitants</div>
            <div class="card-bottom"></div>
        </article>
        <article class="info-card">
            <div class="card-icon">{criteria_icon}</div>
            <div class="card-title">Plusieurs Critères Disponibles</div>
            <div class="card-text">Logement, emploi, météo, éducation, culture</div>
            <div class="card-bottom"></div>
        </article>
        <article class="info-card">
            <div class="card-icon">{happy_icon}</div>
            <div class="card-title">Trouver La Ville Idéale</div>
            <div class="card-text">pour choisir plus sereinement votre future destination</div>
            <div class="card-bottom"></div>
        </article>
    </section>
    """

    st.markdown(cards_html, unsafe_allow_html=True)

    st.markdown(
        """
        <section class="sources">
            <p>
                Les données proviennent majoritairement de sites officiels de la République française,
                toutes les données sont disponibles en libre accès.
            </p>
            <div class="sources-title">Lien vers les sites :</div>
            <ul>
                <li><a href="https://www.data.gouv.fr/" target="_blank">https://www.data.gouv.fr/</a></li>
                <li><a href="https://open-meteo.com/" target="_blank">https://open-meteo.com/</a></li>
                <li><a href="https://open.urssaf.fr/pages/home/" target="_blank">https://open.urssaf.fr/pages/home/</a></li>
            </ul>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
