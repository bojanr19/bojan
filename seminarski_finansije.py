import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import io

# ============================================================
# PODEŠAVANJE STRANICE
# ============================================================
st.set_page_config(
    page_title="Analiza krive prinosa",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PRILAGOĐENI CSS STILOVI — profesionalan plavo-bijeli dizajn
# ============================================================
st.markdown(
    """
    <style>
    /* Glavna pozadina */
    .stApp {
        background-color: #F0F4F8;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1B3A5C;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFFFFF !important;
    }

    /* Naslov */
    .main-title {
        text-align: center;
        color: #1B3A5C;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0;
        padding-top: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #4A7FB5;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }

    /* Metrika kartice */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #EBF2FA 100%);
        border-left: 5px solid #1B3A5C;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(27, 58, 92, 0.08);
        display: flex;           /* aktivira flexbox */
        flex-direction: column;  /* elementi idu jedan ispod drugog */
        justify-content: center; /* vertikalno centriranje */
        align-items: center;     /* horizontalno centriranje */
        text-align: center;      /* dodatno centrira tekst */
        min-height: 150px;
    }
    .metric-card h4 {
        color: #4A7FB5;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0 0 0.3rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card p {
        color: #1B3A5C;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
    }

    /* Tabovi */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #1B3A5C;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #EBF2FA 100%);
        color: #1B3A5C !important;
        border: 2px solid rgba(27, 58, 92, 0.7);
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #1B3A5C !important;
    }

    /* Info blokovi */
    .info-box {
        background-color: #FFFFFF;
        border: 1px solid #D0DCE8;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 4px rgba(27, 58, 92, 0.06);
    }
    .info-box h4 {
        color: #1B3A5C;
        margin-top: 0;
    }
    .info-box p {
        color: #3A5A7C;
        line-height: 1.7;
    }

    /* Razdvajač */
    hr {
        border: none;
        border-top: 2px solid #D0DCE8;
        margin: 1.5rem 0;
    }

    /* Dugmad */
    div[data-testid="stFileUploader"] label {
    display: none !important;
}

div[data-testid="stFileUploader"] section {
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
}
div[data-testid="stFileUploader"] section > div {
    display: none !important;
}
div[data-testid="stFileUploader"] section > div:has(button) {
    display: flex !important;
}

/* Cijeli uploader wrapper — pilula */
div[data-testid="stFileUploader"] {
    width: fit-content !important;
}

/* Dugme u obliku pilule — plavo */
div[data-testid="stFileUploader"] button {
    background-color: #3A5A7C !important;
    color: #FFFFFF !important;
    border: 3px solid #FFFFFF !important;
    border-radius: 50px !important;
    padding: 0.5rem 1.6rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    cursor: pointer;
    white-space: nowrap !important;
}

/* Zamijeni tekst dugmeta sa "Odaberi datoteku" */
div[data-testid="stFileUploader"] button span {
    visibility: hidden;
    position: relative;
    font-size: 0;
}
div[data-testid="stFileUploader"] button span::after {
    content: "Odaberi datoteku";
    visibility: visible;
    font-size: 0.95rem;
    color: #FFFFFF;
    font-weight: 600;
}

/* Kada je fajl učitan — prikaži naziv fajla pored dugmeta */
div[data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"] {
    color: #FFFFFF !important;
}
div[data-testid="stFileUploader"] small {
    color: #AACCEE !important;
    font-size: 0.8rem !important;
}

</style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# BOČNA TRAKA (SIDEBAR)
# ============================================================
with st.sidebar:
    st.markdown("## 📂 Učitavanje podataka")
    st.markdown(
        "Učitajte CSV ili XLSX fajl sa kolonama:\n"
        "- **Datum** (datumi)\n"
        "- **Dugoročne** (10-godišnje stope)\n"
        "- **Kratkorčne** (3-mjesečne stope)"
    )

    ucitani_fajl = st.file_uploader(
        "Izaberite fajl",
        type=["csv", "xlsx"],
        help="Podržani formati: CSV i XLSX",
    )

    st.markdown("---")
    st.markdown("## ⚙️ Podešavanja")
    prikazi_inverziju = st.toggle(
        "Prikaži zone inverzije",
        value=True,
        help="Uključite ili isključite prikaz perioda kada je spread manji od nule (inverzija krive prinosa).",
    )

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; font-size:0.75rem; opacity:0.7;'>"
        "Seminarski rad<br>Finansijska matematika<br><br>Radojević Bojan, 41/24<br>Ćurguz Aleksandar, 151/24<br>© 2026"
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# FUNKCIJE ZA UČITAVANJE I OBRADU PODATAKA
# ============================================================
@st.cache_data
def ucitaj_podatke(fajl) -> pd.DataFrame:
    """Učitava CSV ili XLSX fajl i vraća DataFrame sa standardizovanim kolonama."""
    ime = fajl.name.lower()
    if ime.endswith(".csv"):
        df = pd.read_csv(fajl)
    elif ime.endswith(".xlsx"):
        df = pd.read_excel(fajl)
    else:
        st.error("Nepodržan format fajla.")
        return pd.DataFrame()

    # Standardizacija naziva kolona (mala slova, bez razmaka)
    df.columns = df.columns.str.strip().str.lower()

    # Mapiranje mogućih naziva kolona
    mapiranje = {
        "date": "datum",
        "dates": "datum",
        "long": "dugorocne",
        "long_rate": "dugorocne",
        "dugoročne": "dugorocne",
        "dugorocne_stope": "dugorocne",
        "10y": "dugorocne",
        "10yr": "dugorocne",
        "short": "kratkorocne",
        "short_rate": "kratkorocne",
        "kratkoročne": "kratkorocne",
        "kratkorocne_stope": "kratkorocne",
        "3m": "kratkorocne",
        "3mo": "kratkorocne",
    }
    df.rename(columns=mapiranje, inplace=True)

    # Provera obaveznih kolona
    obavezne = {"datum", "dugorocne", "kratkorocne"}
    if not obavezne.issubset(set(df.columns)):
        nedostaju = obavezne - set(df.columns)
        st.error(f"Nedostaju kolone: {', '.join(nedostaju)}")
        return pd.DataFrame()

    df["datum"] = pd.to_datetime(df["datum"], dayfirst=False, errors="coerce")
    df.dropna(subset=["datum"], inplace=True)
    df.sort_values("datum", inplace=True)
    df.reset_index(drop=True, inplace=True)

    df["dugorocne"] = pd.to_numeric(df["dugorocne"], errors="coerce") * 100
    df["kratkorocne"] = pd.to_numeric(df["kratkorocne"], errors="coerce") * 100
    df.dropna(subset=["dugorocne", "kratkorocne"], inplace=True)


    # Izračunavanje spreada
    df["spread"] = df["dugorocne"] - df["kratkorocne"]

    return df


def kreiraj_primer_podataka() -> pd.DataFrame:
    """Kreira primer podataka za demonstraciju."""
    datumi = pd.date_range(start="2000-01-01", end="2025-12-01", freq="MS")
    np.random.seed(42)

    # Simulacija realistične krive prinosa
    n = len(datumi)
    t = np.linspace(0, 1, n)

    # 10-godišnje obveznice — bazni trend
    bazni_10y = 4.5 - 2.0 * t + 1.5 * np.sin(2 * np.pi * t * 3)
    sum_10y = np.cumsum(np.random.normal(0, 0.03, n))
    dugorocne = bazni_10y + sum_10y
    dugorocne = np.clip(dugorocne, 0.5, 7.0)

    # 3-mjesečne obveznice — prate ali sa većom volatilnošću
    bazni_3m = 3.5 - 2.5 * t + 2.0 * np.sin(2 * np.pi * t * 3 + 0.5)
    sum_3m = np.cumsum(np.random.normal(0, 0.04, n))
    kratkorocne = bazni_3m + sum_3m
    kratkorocne = np.clip(kratkorocne, 0.0, 6.5)

    df = pd.DataFrame(
        {
            "datum": datumi,
            "dugorocne": np.round(dugorocne, 2),
            "kratkorocne": np.round(kratkorocne, 2),
        }
    )
    df["spread"] = np.round(df["dugorocne"] - df["kratkorocne"], 2)
    return df


# ============================================================
# ZAJEDNIČKI STIL ZA GRAFIKONE
# ============================================================
BOJA_10G = "#1B3A5C"       # Tamno plava — 10-godišnje
BOJA_3M = "#4A9BD9"        # Svijetlo plava — 3-mesečne
BOJA_SPREAD = "#2E7D32"    # Zelena — spread
BOJA_INVERZIJA = "rgba(220, 53, 69, 0.15)"  # Crvena providna — inverzija
BOJA_POZADINA = "#FAFCFE"
BOJA_MREZA = "#E8EEF4"


def stilizuj_grafikon(fig, naslov="", visina=500):
    """Primenjuje zajednički stil na Plotly grafikon."""
    fig.update_layout(
    title=dict(
        text=naslov,
        font=dict(size=22, color="#1B3A5C", family="Arial"),
        x=0.5,
        xanchor="center",
        y=0.92  # pomjera naslov više prema vrhu
    ),
    plot_bgcolor=BOJA_POZADINA,
    paper_bgcolor="#FFFFFF",
    font=dict(family="Arial", size=13, color="#3A5A7C"),
    height=visina,
    margin=dict(l=60, r=30, t=100, b=50),  # t=100 povećava prostor iznad grafikona
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.011,  # pomjeri legendu malo više iznad plot-a
        xanchor="center",
        x=0.5,
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#D0DCE8",
        borderwidth=1,
        font=dict(size=12),
        ),
        xaxis=dict(
            gridcolor=BOJA_MREZA,
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor=BOJA_MREZA,
            showgrid=True,
            zeroline=True,
            zerolinecolor="#B0BEC5",
            zerolinewidth=1,
            title="Stopa prinosa (%)",
        ),
        hovermode="x unified",
    )
    # Interaktivne funkcije: zoom, pan, autoscale
    fig.update_layout(
        dragmode="zoom",
        xaxis_rangeslider_visible=False,
    )
    config = {
        "displayModeBar": True,
        "modeBarButtonsToInclude": [
            "zoom2d", "pan2d", "zoomIn2d", "zoomOut2d",
            "autoScale2d", "resetScale2d", "toImage",
        ],
        "displaylogo": False,
        "locale": "sr",
    }
    return fig, config


def dodaj_zone_inverzije(fig, df):
    """Dodaje crvene pravougaonike za periode inverzije."""
    inverzija = df["spread"] < 0
    if not inverzija.any():
        return fig

    # Pronalaženje početaka i krajeva inverzije
    promene = inverzija.astype(int).diff().fillna(0)
    poceci = df.loc[promene == 1, "datum"].tolist()
    krajevi = df.loc[promene == -1, "datum"].tolist()

    # Ako počinje u inverziji
    if inverzija.iloc[0]:
        poceci.insert(0, df["datum"].iloc[0])
    # Ako se završava u inverziji
    if inverzija.iloc[-1]:
        krajevi.append(df["datum"].iloc[-1])

    for pocetak, kraj in zip(poceci, krajevi):
        fig.add_vrect(
            x0=pocetak,
            x1=kraj,
            fillcolor=BOJA_INVERZIJA,
            layer="below",
            line_width=0,
            annotation_text="",
        )

    # Dodaj jednu legendu za inverziju
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=12, color=BOJA_INVERZIJA, symbol="square"),
            name="🔴 Zona inverzije (spread < 0)",
            showlegend=True,
        )
    )

    return fig


# ============================================================
# NASLOV STRANICE
# ============================================================
st.markdown('<h1 class="main-title">📈 Analiza krive prinosa</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Trezorski zapisi — 10-godišnji vs 3-mjesečni · Yield Spread Analysis</p>',
    unsafe_allow_html=True,
)

# ============================================================
# UČITAVANJE PODATAKA
# ============================================================
if ucitani_fajl is not None:
    df = ucitaj_podatke(ucitani_fajl)
else:
    df = kreiraj_primer_podataka()
    st.info(
        "ℹ️ Prikazani su demonstracioni podaci. "
        "Učitajte sopstveni CSV ili XLSX fajl putem bočne trake za analizu stvarnih podataka."
    )

if df.empty:
    st.error("Nema podataka za prikaz. Proverite format učitanog fajla.")
    st.stop()

# ============================================================
# OSNOVNE METRIKE
# ============================================================
poslednji = df.iloc[-1]
poslednji_10g = poslednji["dugorocne"]
poslednji_3m = poslednji["kratkorocne"]
poslednji_spread = poslednji["spread"]
ukupno_redova = len(df)
inverzija_redova = (df["spread"] < 0).sum()
procenat_inverzije = (inverzija_redova / ukupno_redova) * 100 if ukupno_redova > 0 else 0
datum_od = df["datum"].min().strftime("%d.%m.%Y.")
datum_do = df["datum"].max().strftime("%d.%m.%Y.")

# Prikaz metrika u karticama
kol1, kol2, kol3, kol4, kol5 = st.columns(5)

with kol1:
    st.markdown(
        f'<div class="metric-card"><h4>10Y Prinos (zadnji)</h4><p>{poslednji_10g:.2f}%</p></div>',
        unsafe_allow_html=True,
    )

with kol2:
    st.markdown(
        f'<div class="metric-card"><h4>3M Prinos (zadnji)</h4><p>{poslednji_3m:.2f}%</p></div>',
        unsafe_allow_html=True,
    )

with kol3:
    boja_spread = "#2E7D32" if poslednji_spread > 0 else "#DC3545"
    st.markdown(
        f'<div class="metric-card"><h4>Poslednji spread</h4>'
        f'<p style="color:{boja_spread}">{poslednji_spread:+.2f}%</p></div>',
        unsafe_allow_html=True,
    )

with kol4:
    boja_inv = "#DC3545"
    st.markdown(
        f'<div class="metric-card"><h4>Trajanje inverzije</h4>'
        f'<p style="color:{boja_inv}">{procenat_inverzije:.1f}%</p></div>',
        unsafe_allow_html=True,
    )

with kol5:
    st.markdown(
        f'<div class="metric-card"><h4>Period podataka</h4>'
        f'<p style="font-size:1rem">{datum_od}— {datum_do}</p></div>',
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================
# TABOVI
# ============================================================
tab1, tab2, tab3 = st.tabs([
    "📊 Kretanje obveznica",
    "📉 Yield Spread analiza",
    "📋 Tabela podataka",
])

# ============================================================
# TAB 1: KRETANJE OBVEZNICA
# ============================================================
with tab1:
    st.markdown("### Uporedni prikaz prinosa obveznica")

    # --- Zajednički grafikon ---
    fig_zajednicki = go.Figure()

    fig_zajednicki.add_trace(
        go.Scatter(
            x=df["datum"],
            y=df["dugorocne"],
            mode="lines",
            name="📘 10-godišnje obveznice",
            line=dict(color=BOJA_10G, width=2.5),
            hovertemplate="Datum: %{x|%d.%m.%Y.}<br>Prinos: %{y:.2f}%<extra></extra>",
        )
    )

    fig_zajednicki.add_trace(
        go.Scatter(
            x=df["datum"],
            y=df["kratkorocne"],
            mode="lines",
            name="📗 3-mjesečne obveznice",
            line=dict(color=BOJA_3M, width=2.5),
            hovertemplate="Datum: %{x|%d.%m.%Y.}<br>Prinos: %{y:.2f}%<extra></extra>",
        )
    )

    if prikazi_inverziju:
        fig_zajednicki = dodaj_zone_inverzije(fig_zajednicki, df)

    fig_zajednicki, config_z = stilizuj_grafikon(
        fig_zajednicki,
        naslov="Kretanje prinosa — 10-godišnje i 3-mjesečne obveznice",
        visina=520,
    )
    st.plotly_chart(fig_zajednicki, use_container_width=True, config=config_z)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Odvojeni prikazi")

    kol_levo, kol_desno = st.columns(2)

    # --- Grafikon 10-godišnjih ---
    with kol_levo:
        fig_10g = go.Figure()
        fig_10g.add_trace(
            go.Scatter(
                x=df["datum"],
                y=df["dugorocne"],
                mode="lines",
                name="📘 10-godišnje obveznice",
                line=dict(color=BOJA_10G, width=2),
                fill="tozeroy",
                fillcolor="rgba(27, 58, 92, 0.08)",
                hovertemplate="Datum: %{x|%d.%m.%Y.}<br>Prinos: %{y:.2f}%<extra></extra>",
            )
        )
        fig_10g, config_10g = stilizuj_grafikon(
            fig_10g, naslov="Prinos 10-godišnjih obveznica", visina=380
        )
        st.plotly_chart(fig_10g, use_container_width=True, config=config_10g)

    # --- Grafikon 3-mjesečnih ---
    with kol_desno:
        fig_3m = go.Figure()
        fig_3m.add_trace(
            go.Scatter(
                x=df["datum"],
                y=df["kratkorocne"],
                mode="lines",
                name="📗 3-mjesečne obveznice",
                line=dict(color=BOJA_3M, width=2),
                fill="tozeroy",
                fillcolor="rgba(74, 155, 217, 0.08)",
                hovertemplate="Datum: %{x|%d.%m.%Y.}<br>Prinos: %{y:.2f}%<extra></extra>",
            )
        )
        fig_3m, config_3m = stilizuj_grafikon(
            fig_3m, naslov="Prinos 3-mjesečnih obveznica", visina=380
        )
        st.plotly_chart(fig_3m, use_container_width=True, config=config_3m)

    # --- Objašnjenja ---
    st.markdown("<hr>", unsafe_allow_html=True)

    kol_obj1, kol_obj2 = st.columns(2)

    with kol_obj1:
        st.markdown(
            """
            <div class="info-box">
            <h4>📘 10-godišnje državne obveznice</h4>
            <p>
            Desetogodišnje trezorske obveznice (10Y Treasury) predstavljaju dugoročne hartije od vrednosti
            koje izdaje država. Njihov prinos se smatra jednim od najvažnijih pokazatelja u finansijskom
            svijetu jer odražava očekivanja tržišta u pogledu budućeg ekonomskog rasta, inflacije i monetarne
            politike. Viši prinos obično ukazuje na očekivanje jačeg ekonomskog rasta ili veće inflacije,
            dok niži prinos može signalizirati usporavanje ekonomije ili povećanu potražnju za sigurnim
            ulaganjima (flight to safety).
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kol_obj2:
        st.markdown(
            """
            <div class="info-box">
            <h4>📗 3-mjesečne državne obveznice</h4>
            <p>
            Tromjesečni trezorski zapisi (3M Treasury Bill) su kratkoročne hartije od vrednosti sa rokom
            dospeća od 91 dan. Njihov prinos je usko povezan sa trenutnom kamatnom stopom centralne banke
            i odražava kratkoročne uslove na tržištu novca. Ovi instrumenti se smatraju praktično
            bezrizičnim ulaganjem i služe kao referentna tačka (benchmark) za kratkoročne kamatne stope
            u cjelokupnom finansijskom sistemu. Promjene u njihovom prinosu često prethode promjenama u
            monetarnoj politici.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# TAB 2: YIELD SPREAD ANALIZA
# ============================================================
with tab2:
    st.markdown("### Analiza razlike prinosa (Yield Spread)")

    # --- Grafikon spreada ---
    fig_spread = go.Figure()

    # Spread linija
    boje_spread = [
        "#2E7D32" if s > 0 else "#DC3545" for s in df["spread"]
    ]

    fig_spread.add_trace(
        go.Scatter(
            x=df["datum"],
            y=df["spread"],
            mode="lines",
            name="📊 Spread (10G − 3M)",
            line=dict(color=BOJA_SPREAD, width=2.5),
            hovertemplate="Datum: %{x|%d.%m.%Y.}<br>Spread: %{y:.2f}%<extra></extra>",
        )
    )

    # Nulta linija
    fig_spread.add_hline(
        y=0,
        line_dash="dash",
        line_color="#B71C1C",
        line_width=1.5,
        annotation_text="Nulta linija — granica inverzije",
        annotation_position="bottom right",
        annotation_font=dict(size=11, color="#B71C1C"),
    )

    # Zone inverzije
    if prikazi_inverziju:
        fig_spread = dodaj_zone_inverzije(fig_spread, df)

    # Anotacije na grafikonu
    fig_spread.add_annotation(
        x=0.02,
        y=0.6,
        xref="paper",
        yref="paper",
        text="<b>Pozitivan spread</b>: Normalna kriva prinosa<br>"
             "<i>Dugoročne stope veće od kratkoročnih</i>",
        showarrow=False,
        font=dict(size=11, color="#2E7D32"),
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="#2E7D32",
        borderwidth=1,
        borderpad=8,
        align="left",
    )

    fig_spread.add_annotation(
        x=0.02,
        y=0.35,
        xref="paper",
        yref="paper",
        text="<b>Negativan spread</b>: Invertovana kriva prinosa<br>"
             "<i>Kratkoročne stope veće od dugoročnih — signal recesije</i>",
        showarrow=False,
        font=dict(size=11, color="#DC3545"),
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="#DC3545",
        borderwidth=1,
        borderpad=8,
        align="left",
    )

    fig_spread, config_sp = stilizuj_grafikon(
        fig_spread,
        naslov="Yield Spread: 10-godišnje minus 3-mjesečne obveznice",
        visina=520,
    )
    fig_spread.update_layout(
        yaxis_title="Spread (%)",
    )
    st.plotly_chart(fig_spread, use_container_width=True, config=config_sp)

    # --- Osnovne informacije o spreadu ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Ključne statistike spreada")

    maks_spread = df["spread"].max()
    maks_datum = df.loc[df["spread"].idxmax(), "datum"].strftime("%d.%m.%Y.")
    min_spread = df["spread"].min()
    min_datum = df.loc[df["spread"].idxmin(), "datum"].strftime("%d.%m.%Y.")
    prosjecni_spread = df["spread"].mean()

    # Trajanje inverzije u mjesecima
    inverzija_mjeseci = inverzija_redova  # svaki red ≈ 1 mjesec (mjesečni podaci)
    pozitivan_mjeseci = ukupno_redova - inverzija_redova

    kol_s1, kol_s2, kol_s3 = st.columns(3)

    with kol_s1:
        st.markdown(
            f'<div class="metric-card"><h4>📈 Maksimalni spread</h4>'
            f'<p style="color:#2E7D32">{maks_spread:+.2f}%</p>'
            f'<p style="font-size:0.85rem; color:#4A7FB5">{maks_datum}</p></div>',
            unsafe_allow_html=True,
        )

    with kol_s2:
        st.markdown(
            f'<div class="metric-card"><h4>📉 Minimalni spread</h4>'
            f'<p style="color:#DC3545">{min_spread:+.2f}%</p>'
            f'<p style="font-size:0.85rem; color:#4A7FB5">{min_datum}</p></div>',
            unsafe_allow_html=True,
        )

    with kol_s3:
        boja_pros = "#2E7D32" if prosjecni_spread > 0 else "#DC3545"
        st.markdown(
            f'<div class="metric-card"><h4>📊 Prosječni spread</h4>'
            f'<p style="color:{boja_pros}">{prosjecni_spread:+.2f}%</p></div>',
            unsafe_allow_html=True,
        )

    kol_s4, kol_s5 = st.columns(2)

    with kol_s4:
        st.markdown(
            f'<div class="metric-card"><h4>🔴 Ukupno trajanje inverzije</h4>'
            f'<p style="color:#DC3545">{inverzija_mjeseci} mjeseci ({procenat_inverzije:.1f}%)</p></div>',
            unsafe_allow_html=True,
        )

    with kol_s5:
        st.markdown(
            f'<div class="metric-card"><h4>🟢 Pozitivan spread</h4>'
            f'<p style="color:#2E7D32">{pozitivan_mjeseci} mjeseci ({100 - procenat_inverzije:.1f}%)</p></div>',
            unsafe_allow_html=True,
        )

    # --- Godišnji prosjek spreada ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Godišnji prosjek spreada")

    df["godina"] = df["datum"].dt.year
    godisnji_prosjek = df.groupby("godina")["spread"].mean().reset_index()
    godisnji_prosjek.columns = ["Godina", "Prosječni spread"]

    boje_stupci = [
        "#2E7D32" if s > 0 else "#DC3545" for s in godisnji_prosjek["Prosječni spread"]
    ]

    fig_godisnji = go.Figure()
    fig_godisnji.add_trace(
        go.Bar(
            x=godisnji_prosjek["Godina"],
            y=godisnji_prosjek["Prosječni spread"],
            marker_color=boje_stupci,
            name="Godišnji prosjek",
            hovertemplate="Godina: %{x}<br>Prosjek: %{y:.2f}%<extra></extra>",
        )
    )

    fig_godisnji.add_hline(
        y=0,
        line_dash="dash",
        line_color="#B71C1C",
        line_width=1,
    )

    fig_godisnji, config_god = stilizuj_grafikon(
        fig_godisnji,
        naslov="Godišnji prosjek yield spreada",
        visina=420,
    )
    fig_godisnji.update_layout(
        yaxis_title="Prosječni spread (%)",
        xaxis_title="Godina",
        xaxis=dict(dtick=1),
    )
    st.plotly_chart(fig_godisnji, use_container_width=True, config=config_god)

    # --- Objašnjenja ---
    st.markdown("<hr>", unsafe_allow_html=True)

    kol_tekst1, kol_tekst2 = st.columns(2)

    with kol_tekst1:
        st.markdown(
            """
            <div class="info-box">
            <h4>📊 Šta je Yield Spread?</h4>
            <p>
            Yield spread (razlika prinosa) predstavlja razliku između prinosa na dugoročne i kratkoročne
            državne obveznice. U ovom slučaju, to je razlika između prinosa na 10-godišnje trezorske
            obveznice i 3-mjesečne trezorske zapise. Ova razlika je jedan od najvažnijih makroekonomskih
            pokazatelja jer odražava očekivanja tržišta u pogledu budućeg ekonomskog rasta, inflacije i
            kamatnih stopa.
            <br><br>
            <b>Pozitivan spread</b> (normalna kriva prinosa) ukazuje na to da investitori očekuju
            ekonomski rast i zahtevaju veći prinos za dugoročno zaključavanje kapitala.
            <br><br>
            <b>Ravan spread</b> (blizu nule) signalizira neizvesnost na tržištu i moguću tranziciju
            između ekonomskih ciklusa.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kol_tekst2:
        st.markdown(
            """
            <div class="info-box">
            <h4>⚠️ Zašto je inverzija krive važna?</h4>
            <p>
            Inverzija krive prinosa nastaje kada kratkoročne kamatne stope premaše dugoročne, što
            rezultira negativnim spreadom. Ovaj fenomen se istorijski pokazao kao jedan od najpouzdanijih
            indikatora za predviđanje ekonomske recesije.
            <br><br>
            <b>Svaka recesija u SAD-u od 1955. godine</b> bila je predvođena inverzijom krive prinosa,
            sa samo jednim lažnim signalom u tom periodu. Prosječno vreme od inverzije do početka
            recesije iznosi 12-18 meseci.
            <br><br>
            Inverzija nastaje jer investitori očekuju da će centralna banka u budućnosti snižavati
            kamatne stope kao odgovor na ekonomsko usporavanje, što obara dugoročne prinose ispod
            kratkoročnih. To je signal da tržište „predviđa" slabljenje ekonomije.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown(
        """
        <div class="info-box">
        <h4>📉 Zašto je kriva prinosa bila invertovana u drugom kvartalu 2023?</h4>

        <ol>
            <li>
            <b>Globalni kontekst: ECB agresivno podiže kamate</b><br>
            Najvažniji faktor je monetarna politika ECB-a. Bosna i Hercegovina koristi valutni odbor vezan za euro, što znači da kamatne stope na eurozone direktno utiču na domaće tržište.
            ECB je u periodu od jula 2022. do septembra 2023. povisio kamatne stope za rekordnih 450 baznih bodova — historijsko pooštravanje monetarne politike.
            Početkom 2023. ukupna inflacija u eurozoni i dalje je bila visoka (8,6% u januaru), pa su kamate dodatno povećavane.
            Ovo je direktno podiglo kratkoročne stope zaduživanja.
            </li>
            <li>
            <b>Lokalni faktor: RS i pritisak duga</b><br>
            U junu 2023. Vlada RS emitovala je obveznice od 210 miliona KM uz kamatu od 6,1% — najvišu u istoriji RS.
            Istovremeno, Federacija BiH se zaduživala po oko 3,8%.
            Razlog je veliki dug (preko 5 milijardi KM) i potreba refinansiranja više od milijardu KM obaveza u 2023.
            </li>
            <li>
            <b>Sankcije i otežan pristup tržištima</b><br>
            Sankcije SAD iz 2022. otežale su pristup međunarodnim tržištima kapitala.
            RS se više oslanjala na domaće i regionalne berze, gdje su uslovi nepovoljniji.
            Investitori su zato tražili veće kamate zbog većeg rizika.
            </li>
        </ol>

        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TAB 3: TABELA PODATAKA
# ============================================================
with tab3:
    st.markdown("### Pregled podataka")

    # Filter po godini
    godine = sorted(df["datum"].dt.year.unique())
    opcije_godina = ["Sve godine"] + [str(g) for g in godine]

    izabrana_godina = st.selectbox(
        "Filtrirajte po godini:",
        opcije_godina,
        index=0,
        help="Izaberite godinu za filtriranje ili 'Sve godine' za kompletne podatke.",
    )

    if izabrana_godina == "Sve godine":
        df_filtrirano = df.copy()
    else:
        df_filtrirano = df[df["datum"].dt.year == int(izabrana_godina)].copy()

    st.markdown(
        f"**Prikazano redova:** {len(df_filtrirano)} od ukupno {len(df)}"
    )

    # Priprema za prikaz
    df_prikaz = df_filtrirano[["datum", "dugorocne", "kratkorocne", "spread"]].copy()
    df_prikaz["datum"] = df_prikaz["datum"].dt.strftime("%d.%m.%Y.")

    # Formatiranje brojeva na 4 decimale sa % znakom (bez zaokruživanja)
    for kol in ["dugorocne", "kratkorocne", "spread"]:
        df_prikaz[kol] = df_prikaz[kol].apply(
            lambda x: f"{x:.4f}%" if pd.notnull(x) else ""
        )

    df_prikaz.columns = ["Datum", "10-godišnje (%)", "3-mjesečne (%)", "Spread (%)"]

    # Funkcija za bojenje spreada
    def oboji_spread(val):
        """Vraća CSS stil za ćeliju spreada."""
        try:
            v = float(str(val).replace("%", "").strip())
        except (ValueError, TypeError):
            return ""
        if v <= 0:
            return "background-color: rgba(220, 53, 69, 0.15); color: #B71C1C; font-weight: 600;"
        elif v > 1:
            return "background-color: rgba(46, 125, 50, 0.12); color: #2E7D32; font-weight: 600;"
        else:
            return "background-color: rgba(27, 58, 92, 0.08); color: #1B3A5C; font-weight: 600;"

    # Stilizovana tabela
    styled_df = df_prikaz.style.applymap(
        oboji_spread, subset=["Spread (%)"]
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        height=500,
    )

    # Legenda boja
    st.markdown(
        """
        <div style="display:flex; gap:2rem; margin:1rem 0; flex-wrap:wrap;">
            <div style="display:flex; align-items:center; gap:0.5rem;">
                <div style="width:20px; height:20px; background:rgba(27,58,92,0.15); border-radius:4px; border:1px solid #1B3A5C;"></div>
                <span style="color:#1B3A5C; font-size:0.9rem;"><b>Plava</b> — Spread od 0% do 1%</span>
            </div>
            <div style="display:flex; align-items:center; gap:0.5rem;">
                <div style="width:20px; height:20px; background:rgba(46,125,50,0.15); border-radius:4px; border:1px solid #2E7D32;"></div>
                <span style="color:#2E7D32; font-size:0.9rem;"><b>Zelena</b> — Spread veći od 1%</span>
            </div>
            <div style="display:flex; align-items:center; gap:0.5rem;">
                <div style="width:20px; height:20px; background:rgba(220,53,69,0.15); border-radius:4px; border:1px solid #DC3545;"></div>
                <span style="color:#DC3545; font-size:0.9rem;"><b>Crvena</b> — Spread 0% ili manji (inverzija)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Preuzimanje filtriranih podataka
    csv_bafer = io.StringIO()
    df_za_preuzimanje = df_filtrirano[["datum", "dugorocne", "kratkorocne", "spread"]].copy()
    df_za_preuzimanje.columns = ["Datum", "Dugorocne_10G", "Kratkorocne_3M", "Spread"]
    df_za_preuzimanje.to_csv(csv_bafer, index=False, encoding="utf-8-sig")

    naziv_fajla = (
        f"yield_spread_podaci_{izabrana_godina}.csv"
        if izabrana_godina != "Sve godine"
        else "yield_spread_podaci_svi.csv"
    )

    st.download_button(
        label="⬇️ Preuzmi filtrirane podatke (CSV)",
        data=csv_bafer.getvalue(),
        file_name=naziv_fajla,
        mime="text/csv",
        help="Preuzmite trenutno prikazane podatke u CSV formatu.",
    )

# ============================================================
# PODNOŽJE
# ============================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align:center; color:#7A8FA6; font-size:0.8rem; padding:1rem 0;">
        Seminarski rad iz finansijske matematike · Analiza krive prinosa · 2026<br>
        Podaci: Trezorski zapisi — 10-godišnji vs 3-mesečni<br><br>Radojević Bojan, 41/24<br>Ćurguz Aleksandar, 151/24
    </div>
    """,
    unsafe_allow_html=True,
)
