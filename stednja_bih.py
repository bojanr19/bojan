import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ─────────────────────────────────────────────
#  KONFIGURACIJA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Štednja u BiH | Poređenje banaka",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: #f5f0eb;
    color: #1a1a2e;
}
h1,h2,h3 { font-family: 'Playfair Display', serif; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #1a1a2e;
    border-right: none;
}
section[data-testid="stSidebar"] * { color: #f5f0eb !important; }
section[data-testid="stSidebar"] label {
    color: #a0a8c0 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* ── Number input — veći, čitljiviji broj ── */
section[data-testid="stSidebar"] input[type="number"] {
    background-color: #2a2a4e !important;
    color: #e0b355 !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    font-family: 'Playfair Display', serif !important;
    border: 2px solid #c8973a !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    text-align: right !important;
}
section[data-testid="stSidebar"] input[type="number"]:focus {
    border-color: #e0b355 !important;
    box-shadow: 0 0 0 2px rgba(224,179,85,0.3) !important;
}

/* ── Select / Radio ── */
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #2a2a4e !important;
    border: 1px solid #3a3a6e !important;
    color: #f5f0eb !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stRadio > div {
    gap: 6px;
}
section[data-testid="stSidebar"] .stRadio label span {
    color: #c9d1d9 !important;
    font-size: 0.9rem !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* ── Checkbox ── */
section[data-testid="stSidebar"] .stCheckbox label span {
    color: #c9d1d9 !important;
    font-size: 0.88rem !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* ── Metric kartice ── */
[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e0d8cf;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.7rem !important;
    color: #1a1a2e !important;
}
[data-testid="stMetricLabel"] {
    color: #7a7a8c !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stMetricDelta"] { font-size: 0.85rem !important; }

/* ── Dugme ── */
.stButton > button {
    background: linear-gradient(135deg, #c8973a, #e0b355);
    color: #1a1a2e; border: none; border-radius: 10px;
    padding: 11px 24px; font-family: 'Source Sans 3', sans-serif;
    font-weight: 700; font-size: 0.95rem; width: 100%;
    transition: all 0.2s; box-shadow: 0 3px 12px rgba(200,151,58,0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(200,151,58,0.45);
}

/* ── Tabovi ── */
.stTabs [data-baseweb="tab"] {
    background-color: #ede8e2; border-radius: 8px 8px 0 0;
    color: #7a7a8c; font-weight: 600; font-size: 0.88rem;
}
.stTabs [aria-selected="true"] {
    background-color: #1a1a2e !important;
    color: #e0b355 !important;
}

/* ── Kartice ── */
.card {
    background: white; border: 1px solid #e0d8cf; border-radius: 14px;
    padding: 20px 24px; margin-bottom: 14px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.card-gold {
    background: linear-gradient(135deg, #1a1a2e, #2a2a4e);
    border: 2px solid #c8973a; border-radius: 14px;
    padding: 20px 24px; margin-bottom: 14px; color: #f5f0eb;
}

/* ── Razred boxovi ── */
.razred-box {
    border-radius: 10px; padding: 10px 16px; margin: 6px 0;
    font-size: 0.85rem; font-weight: 600;
}
.razred-aktivan {
    background: linear-gradient(135deg, #1f2a4e, #2a3a6e);
    border: 2px solid #c8973a; color: #e0b355;
}
.razred-neaktivan {
    background: #2a2a40; border: 1px solid #3a3a5e; color: #6a6a8e;
}

/* ── Info / Warning boxovi ── */
.info-box {
    background: #eef4ff; border-left: 3px solid #3a6bc8;
    border-radius: 8px; padding: 12px 16px; margin: 10px 0;
    font-size: 0.88rem; color: #2a3a5e;
}
.warning-box {
    background: #fff8ee; border-left: 3px solid #c8973a;
    border-radius: 8px; padding: 12px 16px; margin: 10px 0;
    font-size: 0.88rem; color: #5e3a10;
}

/* ── Naslov ── */
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem; color: #1a1a2e; margin-bottom: 0;
}
.subtitle {
    color: #7a7a8c; font-size: 0.95rem;
    margin-top: 4px; margin-bottom: 28px;
}

hr { border-color: #e0d8cf; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  RAZREDI IZNOSA
# ─────────────────────────────────────────────
RAZREDI = [
    {"naziv": "do 10.000 KM",        "min": 0,     "max": 10000,        "kljuc": "do_10000"},
    {"naziv": "10.000 – 50.000 KM",  "min": 10000, "max": 50000,        "kljuc": "10000_50000"},
    {"naziv": "preko 50.000 KM",      "min": 50000, "max": float('inf'), "kljuc": "preko_50000"},
]

def odredi_razred(iznos):
    for r in RAZREDI:
        if iznos < r["max"]:
            return r
    return RAZREDI[-1]

# ─────────────────────────────────────────────
#  PODACI O BANKAMA — stvarne stope
# ─────────────────────────────────────────────
BANKE = {
    "UniCredit Bank": {
        "boja": "#e31e24",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "12 mjeseci": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "24 mjeseca": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "36 mjeseci": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
        "min_iznos": 0,
        "napomena": "Kamate iskazane na godišnjem nivou (p.a.)"
    },
    "Raiffeisen Bank": {
        "boja": "#f5c500",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "12 mjeseci": {"do_10000": 0.05, "10000_50000": 0.05, "preko_50000": 0.05},
            "24 mjeseca": {"do_10000": 0.50, "10000_50000": 0.50, "preko_50000": 0.50},
            "36 mjeseci": {"do_10000": 0.70, "10000_50000": 0.70, "preko_50000": 0.70},
        },
        "tekuca": {"do_10000": 0.00, "10000_50000": 0.00, "preko_50000": 0.00},
        "min_iznos": 500,
        "napomena": "Viša stopa dostupna za Premium klijente"
    },
    "NLB Banka": {
        "boja": "#00843d",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.00, "10000_50000": 0.00, "preko_50000": 0.00},
            "6 mjeseci":  {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "12 mjeseci": {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "24 mjeseca": {"do_10000": 2.00, "10000_50000": 2.00, "preko_50000": 2.00},
            "36 mjeseci": {"do_10000": 2.15, "10000_50000": 2.15, "preko_50000": 2.15},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.04},
        "min_iznos": 0,
        "napomena": "Posebne ponude za penzionere i mlade"
    },
    "Sparkasse Bank": {
        "boja": "#e2001a",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.25, "10000_50000": 0.25, "preko_50000": 0.25},
            "6 mjeseci":  {"do_10000": 0.45, "10000_50000": 0.45, "preko_50000": 0.45},
            "12 mjeseci": {"do_10000": 0.65, "10000_50000": 0.65, "preko_50000": 0.65},
            "24 mjeseca": {"do_10000": 0.85, "10000_50000": 0.85, "preko_50000": 0.85},
            "36 mjeseci": {"do_10000": 1.10, "10000_50000": 1.10, "preko_50000": 1.10},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min_iznos": 100,
        "napomena": "Minimalan iznos oročenja 100 KM ili 50 EUR"
    },
    "ASA Banka": {
        "boja": "#003da5",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.35, "10000_50000": 0.50, "preko_50000": 0.65},
            "6 mjeseci":  {"do_10000": 0.55, "10000_50000": 0.70, "preko_50000": 0.90},
            "12 mjeseci": {"do_10000": 0.85, "10000_50000": 1.00, "preko_50000": 1.25},
            "24 mjeseca": {"do_10000": 1.05, "10000_50000": 1.20, "preko_50000": 1.50},
            "36 mjeseci": {"do_10000": 1.15, "10000_50000": 1.40, "preko_50000": 1.70},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min_iznos": 200,
        "napomena": "Jedna od konkurentnijih stopa na tržištu BiH"
    },
    "Atos Bank": {
        "boja": "#005f8e",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.30, "10000_50000": 0.30, "preko_50000": 0.30},
            "12 mjeseci": {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "24 mjeseca": {"do_10000": 1.50, "10000_50000": 1.50, "preko_50000": 1.50},
            "36 mjeseci": {"do_10000": 1.80, "10000_50000": 1.80, "preko_50000": 1.80},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min_iznos": 1000,
        "napomena": "Minimalan iznos oročenja iznosi 1.000 KM, odnosno 500 EUR"
    },
    "Addiko Bank": {
        "boja": "#006ab3",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "12 mjeseci": {"do_10000": 2.00, "10000_50000": 2.00, "preko_50000": 2.00},
            "24 mjeseca": {"do_10000": 2.30, "10000_50000": 2.30, "preko_50000": 2.30},
            "36 mjeseci": {"do_10000": 2.40, "10000_50000": 2.40, "preko_50000": 2.40},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min_iznos": 500,
        "napomena": "Austrijska grupacija, prisutna u cijeloj regiji"
    },
}

PERIODI_OROCENE = ["3 mjeseca", "6 mjeseci", "12 mjeseci", "24 mjeseca", "36 mjeseci"]
PERIODI_MAPA   = {"3 mjeseca": 0.25, "6 mjeseci": 0.5, "12 mjeseci": 1.0, "24 mjeseca": 2.0, "36 mjeseci": 3.0}

# ─────────────────────────────────────────────
#  POMOĆNE FUNKCIJE
# ─────────────────────────────────────────────
def dohvati_stopu(banka_podaci, tip, period, razred_kljuc):
    if tip == "Oročena štednja":
        return banka_podaci["orocene"][period][razred_kljuc]
    return banka_podaci["tekuca"][razred_kljuc]

def format_km(iznos):
    if abs(iznos) >= 1_000_000:
        return f"{iznos/1_000_000:.3f}M KM"
    return f"{iznos:,.2f} KM"

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Parametri štednje")
    st.markdown("---")

    iznos = st.number_input(
        "Iznos štednje (KM)",
        min_value=100, max_value=500_000, value=10_000, step=500,
    )

    # Prikaz aktivnog razreda
    aktivan_razred = odredi_razred(iznos)
    st.markdown("**Razred iznosa:**")
    for r in RAZREDI:
        aktivan = r["kljuc"] == aktivan_razred["kljuc"]
        stil    = "razred-aktivan" if aktivan else "razred-neaktivan"
        ikona   = "✅" if aktivan else "○"
        st.markdown(
            f'<div class="razred-box {stil}">{ikona} {r["naziv"]}</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    tip_stednje = st.radio("Tip štednje", ["Oročena štednja", "Tekuća (po viđenju)"])

    if tip_stednje == "Oročena štednja":
        period = st.selectbox("Period oročenja", PERIODI_OROCENE, index=2)
    else:
        period = "12 mjeseci"
        st.info("Tekuća štednja — prosta kamata.")

    porezi = st.checkbox("Uračunaj porez na kamatu (10%)", value=False)
    st.markdown("---")
    izracunaj = st.button("🔍 Uporedi banke", type="primary")
    st.markdown("---")
    st.markdown(
        """
        <div style="background:#2a2a4e;border-radius:10px;padding:14px;
                    font-size:0.82rem;color:#a0a8c0;">
            ⚠️ <b style="color:#e0b355;">Napomena:</b><br>
            Kamatne stope su preuzete sa zvaničnih web stranica banaka.
            Preporučujemo provjeru aktuelnih podataka prije donošenja odluke.
        </div>
        """,
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
#  NASLOV
# ─────────────────────────────────────────────
st.markdown('<p class="main-title">🏦 Poređenje štednih proizvoda</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Banke u Bosni i Hercegovini · Finansijska matematika</p>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  POČETNI EKRAN
# ─────────────────────────────────────────────
if not izracunaj:
    st.markdown("#### 📊 Pregled kamatnih stopa po razredima (12 mj. oročenje)")
    hdr = st.columns([2, 1.5, 1.5, 1.5])
    hdr[0].markdown("**Banka**")
    hdr[1].markdown("**do 10.000 KM**")
    hdr[2].markdown("**10.000–50.000 KM**")
    hdr[3].markdown("**preko 50.000 KM**")
    st.markdown("---")
    for naziv, info in BANKE.items():
        cols = st.columns([2, 1.5, 1.5, 1.5])
        s = info["orocene"]["12 mjeseci"]
        with cols[0]:
            st.markdown(
                f"<span style='color:{info['boja']};font-weight:700;'>■</span> {naziv}",
                unsafe_allow_html=True
            )
        cols[1].markdown(f"`{s['do_10000']:.2f}%`")
        cols[2].markdown(f"`{s['10000_50000']:.2f}%`")
        cols[3].markdown(f"`{s['preko_50000']:.2f}%`")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-box">
            👈 <b>Unesite iznos i period štednje</b> u lijevoj koloni —
            aplikacija automatski određuje razred i prikazuje poređenje svih banaka.
        </div>
        """,
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
#  REZULTATI
# ─────────────────────────────────────────────
else:
    period_god   = PERIODI_MAPA.get(period, 1.0)
    razred       = odredi_razred(iznos)
    razred_kljuc = razred["kljuc"]

    # Banner aktivnog razreda
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#1a1a2e,#2a2a4e);
                    border:2px solid #c8973a;border-radius:12px;
                    padding:14px 22px;margin-bottom:20px;">
            <span style="font-size:0.72rem;color:#a0a8c0;
                         text-transform:uppercase;letter-spacing:0.1em;">
                Aktivan razred iznosa
            </span><br>
            <span style="font-size:1.3rem;font-weight:700;color:#e0b355;">
                💰 {razred['naziv']}
            </span>
            <span style="font-size:0.85rem;color:#c9cfe0;margin-left:16px;">
                Kamatne stope za ovaj razred se primjenjuju na vaš iznos od
                <b>{format_km(iznos)}</b>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Izračun
    rezultati = []
    for naziv, info in BANKE.items():
        stopa = dohvati_stopu(info, tip_stednje, period, razred_kljuc)
        if tip_stednje == "Oročena štednja":
            konacno = iznos * (1 + stopa / 100) ** period_god
            formula = "Složeni k.r."
        else:
            konacno = iznos * (1 + stopa / 100 * period_god)
            formula = "Prosta kamata"
        kamata       = konacno - iznos
        porez        = kamata * 0.10 if porezi else 0
        kamata_neto  = kamata - porez
        konacno_neto = iznos + kamata_neto
        rezultati.append({
            "naziv":     naziv,
            "boja":      info["boja"],
            "stopa":     stopa,
            "konacno":   konacno_neto,
            "kamata":    kamata_neto,
            "porez":     porez,
            "formula":   formula,
            "min_iznos": info["min_iznos"],
            "napomena":  info["napomena"],
            "sve_stope": {
                r["kljuc"]: dohvati_stopu(info, tip_stednje, period, r["kljuc"])
                for r in RAZREDI
            },
        })

    rezultati.sort(key=lambda x: x["konacno"], reverse=True)
    pobjednik = rezultati[0]

    # Metrike
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💰 Uloženi iznos", format_km(iznos))
    with c2:
        st.metric(
            "🥇 Najbolja banka",
            pobjednik["naziv"].replace(" Bank", "").replace(" Banka", ""),
            delta=f"{pobjednik['stopa']:.2f}% p.a."
        )
    with c3:
        st.metric(
            "📈 Maksimalna zarada",
            format_km(pobjednik["kamata"]),
            delta=f"+{pobjednik['kamata'] / iznos * 100:.3f}% ROI"
        )
    with c4:
        st.metric(
            "↕️ Razlika min/max",
            format_km(rezultati[0]["konacno"] - rezultati[-1]["konacno"]),
            delta="između banaka"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🥇 Preporuka",
        "📊 Graf rasta",
        "🎚️ Analiza razreda",
        "⚖️ Oročena vs. Tekuća",
        "📋 Detaljna tabela",
    ])

    # ══ TAB 1: PREPORUKA ══════════════════
    with tab1:
        col_p, col_r = st.columns(2)

        with col_p:
            porez_html = (
                f"<br>🧾 Porez (10%): <b style='color:#f0883e;'>-{format_km(pobjednik['porez'])}</b>"
                if porezi else ""
            )
            st.markdown(
                f"""
                <div class="card-gold">
                    <div style="font-size:0.72rem;letter-spacing:0.1em;
                                color:#c8973a;margin-bottom:8px;">
                        🥇 PREPORUČENA BANKA · RAZRED: {razred['naziv'].upper()}
                    </div>
                    <div style="font-family:'Playfair Display',serif;
                                font-size:1.8rem;margin-bottom:4px;">
                        {pobjednik['naziv']}
                    </div>
                    <div style="font-size:1.1rem;color:#e0b355;margin-bottom:16px;">
                        {pobjednik['stopa']:.2f}% godišnja kamatna stopa
                    </div>
                    <div style="font-size:0.9rem;line-height:1.9;color:#c9cfe0;">
                        💶 Konačna vrijednost:
                            <b style="color:#e0b355;">{format_km(pobjednik['konacno'])}</b><br>
                        💹 Zarada od kamate:
                            <b style="color:#3fb950;">{format_km(pobjednik['kamata'])}</b><br>
                        📅 Period:
                            <b>{period if tip_stednje == 'Oročena štednja' else 'Po viđenju'}</b><br>
                        🎚️ Razred iznosa: <b>{razred['naziv']}</b><br>
                        🧮 Formula: <b>{pobjednik['formula']}</b>
                        {porez_html}
                    </div>
                    <div style="margin-top:14px;font-size:0.8rem;
                                color:#8890a0;font-style:italic;">
                        ℹ️ {pobjednik['napomena']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if tip_stednje == "Oročena štednja":
                st.markdown(
                    f"""
                    <div class="info-box">
                        🧮 <b>Formula — Složeni kamatni račun:</b><br>
                        <code>Fn = P × (1 + r/100)<sup>n</sup></code><br>
                        P = {format_km(iznos)}, r = {pobjednik['stopa']:.2f}%,
                        n = {period_god} god.<br>
                        <b>Fn = {iznos:,.2f} ×
                        (1 + {pobjednik['stopa']/100:.4f})<sup>{period_god}</sup>
                        = {format_km(pobjednik['konacno'])}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="info-box">
                        🧮 <b>Formula — Prosta kamata:</b><br>
                        <code>Fn = P × (1 + r/100 × n)</code><br>
                        P = {format_km(iznos)}, r = {pobjednik['stopa']:.2f}%,
                        n = {period_god} god.<br>
                        <b>Fn = {iznos:,.2f} ×
                        (1 + {pobjednik['stopa']/100:.4f} × {period_god})
                        = {format_km(pobjednik['konacno'])}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col_r:
            st.markdown("#### 🏆 Rang lista banaka")
            medalje = ["🥇", "🥈", "🥉"] + ["   "] * 10
            for i, r in enumerate(rezultati):
                naziv    = r["naziv"]
                boja     = r["boja"]
                stopa    = f"{r['stopa']:.2f}%"
                konacno  = format_km(r["konacno"])
                kamata   = format_km(r["kamata"])
                medalja  = medalje[i]
                upozorenje = (
                    f"<span style='color:#f0883e;font-size:0.72rem;'>"
                    f" ⚠️ min. {r['min_iznos']:,} KM</span>"
                    if iznos < r["min_iznos"] else ""
                )
                html = (
                    f'<div class="card" style="padding:12px 18px;margin-bottom:8px;'
                    f'border-left:4px solid {boja};">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<div>'
                    f'<span>{medalja}</span>'
                    f'<b style="font-size:0.93rem;"> {naziv}</b>'
                    f'<span style="color:{boja};font-weight:700;margin-left:6px;">{stopa}</span>'
                    f'{upozorenje}'
                    f'</div>'
                    f'<div style="text-align:right;">'
                    f'<div style="font-weight:700;">{konacno}</div>'
                    f'<div style="font-size:0.78rem;color:#3a8c3a;">+{kamata}</div>'
                    f'</div>'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(html, unsafe_allow_html=True)

    # ══ TAB 2: GRAF RASTA ════════════════
    with tab2:
        fig, axes = plt.subplots(1, 2, figsize=(13, 5))
        fig.patch.set_facecolor('#fdf8f3')
        nazivi_k = [
            r["naziv"].replace(" Bank", "").replace(" Banka", "")
            for r in rezultati
        ]

        ax1 = axes[0]
        ax1.set_facecolor('#fdf8f3')
        bars = ax1.bar(
            nazivi_k,
            [r["konacno"] for r in rezultati],
            color=[r["boja"] for r in rezultati],
            alpha=0.85, edgecolor='white', zorder=3
        )
        ax1.axhline(
            iznos, color='#1a1a2e', linewidth=1.5, linestyle='--',
            alpha=0.5, label=f"Uloženo: {format_km(iznos)}", zorder=4
        )
        for bar, r in zip(bars, rezultati):
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + iznos * 0.002,
                f"+{format_km(r['kamata'])}",
                ha='center', va='bottom', fontsize=7.5,
                color='#2a6a2a', fontweight='bold'
            )
        ax1.set_title("Konačna vrijednost po banci", fontsize=12, color='#1a1a2e', pad=12)
        ax1.set_ylabel("Iznos (KM)", color='#7a7a8c', fontsize=9)
        ax1.tick_params(axis='x', rotation=30, labelsize=8, colors='#1a1a2e')
        ax1.tick_params(axis='y', labelsize=8, colors='#1a1a2e')
        ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax1.legend(fontsize=8, facecolor='#fdf8f3', edgecolor='#e0d8cf')
        ax1.grid(axis='y', color='#e0d8cf', linewidth=0.8, zorder=0)
        for sp in ax1.spines.values():
            sp.set_edgecolor('#e0d8cf')

        ax2 = axes[1]
        ax2.set_facecolor('#fdf8f3')
        rez_rev = list(reversed(rezultati))
        hbars = ax2.barh(
            [r["naziv"].replace(" Bank", "").replace(" Banka", "") for r in rez_rev],
            [r["stopa"] for r in rez_rev],
            color=[r["boja"] for r in rez_rev],
            alpha=0.85, edgecolor='white'
        )
        for bar, r in zip(hbars, rez_rev):
            ax2.text(
                bar.get_width() + 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{r['stopa']:.2f}%",
                va='center', fontsize=8.5, fontweight='bold', color='#1a1a2e'
            )
        ax2.set_title(
            f"Kamatna stopa — razred: {razred['naziv']}",
            fontsize=11, color='#1a1a2e', pad=12
        )
        ax2.set_xlabel("Kamatna stopa (% p.a.)", color='#7a7a8c', fontsize=9)
        ax2.tick_params(labelsize=8.5, colors='#1a1a2e')
        ax2.grid(axis='x', color='#e0d8cf', linewidth=0.8)
        for sp in ax2.spines.values():
            sp.set_edgecolor('#e0d8cf')

        fig.tight_layout(pad=2.5)
        st.pyplot(fig)
        plt.close()

        st.markdown("#### 📈 Rast štednje kroz vrijeme")
        fig2, ax = plt.subplots(figsize=(13, 4.5))
        fig2.patch.set_facecolor('#fdf8f3')
        ax.set_facecolor('#fdf8f3')
        max_god = max(3.0, period_god * 1.5) if tip_stednje == "Oročena štednja" else 3.0
        osi_x   = np.linspace(0, max_god, 100)
        for r in rezultati:
            if tip_stednje == "Oročena štednja":
                vr = [iznos * (1 + r["stopa"] / 100) ** g for g in osi_x]
            else:
                vr = [iznos * (1 + r["stopa"] / 100 * g) for g in osi_x]
            ax.plot(
                osi_x, vr,
                color=r["boja"],
                linewidth=2.8 if r["naziv"] == pobjednik["naziv"] else 1.4,
                alpha=1.0 if r["naziv"] == pobjednik["naziv"] else 0.5,
                label=r["naziv"].replace(" Bank", "").replace(" Banka", "")
            )
        ax.axhline(iznos, color='#1a1a2e', linewidth=1.2, linestyle=':', alpha=0.4, label="Polazni iznos")
        if tip_stednje == "Oročena štednja":
            ax.axvline(
                period_god, color='#c8973a', linewidth=1.5,
                linestyle='--', alpha=0.7, label=f"Kraj oročenja ({period})"
            )
        ax.set_xlabel("Godine", color='#7a7a8c', fontsize=10)
        ax.set_ylabel("Vrijednost (KM)", color='#7a7a8c', fontsize=10)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.legend(fontsize=8.5, facecolor='#fdf8f3', edgecolor='#e0d8cf', ncol=2)
        ax.grid(color='#e0d8cf', linewidth=0.7)
        for sp in ax.spines.values():
            sp.set_edgecolor('#e0d8cf')
        ax.tick_params(colors='#7a7a8c')
        ax.set_title("Rast štednje kroz vrijeme — sve banke", fontsize=12, color='#1a1a2e', pad=12)
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # ══ TAB 3: ANALIZA RAZREDA ════════════
    with tab3:
        st.markdown("#### 🎚️ Kako razred iznosa utiče na kamatnu stopu?")
        st.markdown(
            f"""
            <div class="info-box">
                Banke primjenjuju <b>tri razreda iznosa</b> — veći iznos donosi višu kamatnu stopu.
                Vaš iznos od <b>{format_km(iznos)}</b> spada u razred <b>{razred['naziv']}</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

        fig3, ax = plt.subplots(figsize=(13, 5))
        fig3.patch.set_facecolor('#fdf8f3')
        ax.set_facecolor('#fdf8f3')
        x = np.arange(len(rezultati))
        w = 0.25
        boje_raz = ["#b8cce0", "#5a8fd4", "#1a3a6e"]
        for i, (raz_i, boja_r) in enumerate(zip(RAZREDI, boje_raz)):
            stope_raz = [r["sve_stope"][raz_i["kljuc"]] for r in rezultati]
            je_aktivan = raz_i["kljuc"] == razred_kljuc
            bars3 = ax.bar(
                x + (i - 1) * w, stope_raz, w,
                label=raz_i["naziv"], color=boja_r, alpha=0.9,
                edgecolor='#c8973a' if je_aktivan else 'white',
                linewidth=2 if je_aktivan else 0
            )
            for bar, s in zip(bars3, stope_raz):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.005,
                    f"{s:.2f}",
                    ha='center', va='bottom', fontsize=6.5, color='#1a1a2e'
                )

        ax.set_xticks(x)
        ax.set_xticklabels(
            [r["naziv"].replace(" Bank", "").replace(" Banka", "") for r in rezultati],
            rotation=20, fontsize=8.5, color='#1a1a2e'
        )
        ax.set_ylabel("Kamatna stopa (% p.a.)", color='#7a7a8c', fontsize=9)
        ax.set_title(
            f"Kamatna stopa po razredu iznosa — {period}  "
            f"(aktivan razred: {razred['naziv']})",
            fontsize=11, color='#1a1a2e', pad=12
        )
        ax.legend(title="Razred iznosa", fontsize=9, facecolor='#fdf8f3', edgecolor='#e0d8cf')
        ax.grid(axis='y', color='#e0d8cf', linewidth=0.8)
        for sp in ax.spines.values():
            sp.set_edgecolor('#e0d8cf')
        ax.tick_params(axis='y', labelsize=8, colors='#7a7a8c')
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close()

        st.markdown(f"#### 💡 Efekt razreda na vašu štednju — **{pobjednik['naziv']}**")
        rows_raz = []
        for raz_i in RAZREDI:
            s = dohvati_stopu(BANKE[pobjednik["naziv"]], tip_stednje, period, raz_i["kljuc"])
            k = (
                iznos * (1 + s / 100) ** period_god - iznos
                if tip_stednje == "Oročena štednja"
                else iznos * s / 100 * period_god
            )
            aktivan_txt = " ✅ vaš razred" if raz_i["kljuc"] == razred_kljuc else ""
            rows_raz.append({
                "Razred iznosa":            raz_i["naziv"] + aktivan_txt,
                "Kamatna stopa":            f"{s:.2f}% p.a.",
                "Kamata na vaš iznos (KM)": f"{k:,.2f}",
                "Konačna vrijednost (KM)":  f"{iznos + k:,.2f}",
            })
        st.dataframe(
            pd.DataFrame(rows_raz).set_index("Razred iznosa"),
            use_container_width=True
        )

        st.markdown(
            """
            <div class="warning-box">
                💡 <b>Finansijski savjet:</b> Ako je vaš iznos blizu granice razreda
                (npr. 9.800 KM), razmotrite da dopunite do <b>10.000 KM</b> —
                prelaskom u viši razred dobijate bolju stopu na <i>cijeli</i> iznos.
            </div>
            """,
            unsafe_allow_html=True
        )

    # ══ TAB 4: OROČENA VS TEKUĆA ══════════
    with tab4:
        st.markdown("#### ⚖️ Poređenje: Oročena štednja vs. Štednja po viđenju")
        st.markdown(
            f"""
            <div class="info-box">
                Oročena štednja koristi <b>složeni kamatni račun</b> —
                kamata se pripisuje na kamatu.<br>
                Tekuća (po viđenju) koristi <b>prostu kamatu</b> —
                kamata se računa samo na glavnicu.<br>
                Analiza za: <b>{pobjednik['naziv']}</b> · Razred: <b>{razred['naziv']}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        sve_orocene, sve_tekuce, periodi_labele = [], [], []
        for p_naziv, p_god in PERIODI_MAPA.items():
            s_or  = BANKE[pobjednik["naziv"]]["orocene"][p_naziv][razred_kljuc]
            s_tek = BANKE[pobjednik["naziv"]]["tekuca"][razred_kljuc]
            sve_orocene.append(iznos * (1 + s_or  / 100) ** p_god)
            sve_tekuce.append( iznos * (1 + s_tek / 100 * p_god))
            periodi_labele.append(p_naziv)

        fig4, ax = plt.subplots(figsize=(10, 4.5))
        fig4.patch.set_facecolor('#fdf8f3')
        ax.set_facecolor('#fdf8f3')
        xp = np.arange(len(periodi_labele))
        w  = 0.35
        b1 = ax.bar(xp - w/2, sve_orocene, w, label="Oročena (složeni k.r.)",
                    color="#1a1a2e", alpha=0.85, edgecolor='white')
        b2 = ax.bar(xp + w/2, sve_tekuce,  w, label="Po viđenju (prosta kamata)",
                    color="#c8973a", alpha=0.85, edgecolor='white')
        ax.axhline(iznos, color='#e31e24', linewidth=1.2, linestyle='--',
                   alpha=0.5, label=f"Uloženo: {format_km(iznos)}")
        for bar in b1:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + iznos*0.002,
                    format_km(bar.get_height()), ha='center', va='bottom',
                    fontsize=7, fontweight='bold', color='#1a1a2e')
        for bar in b2:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + iznos*0.002,
                    format_km(bar.get_height()), ha='center', va='bottom',
                    fontsize=7, fontweight='bold', color='#8a5a00')
        ax.set_xticks(xp)
        ax.set_xticklabels(periodi_labele, fontsize=9)
        ax.set_ylabel("Iznos (KM)", color='#7a7a8c', fontsize=9)
        ax.set_title(
            f"Oročena vs. Tekuća — {pobjednik['naziv']} · {razred['naziv']}",
            fontsize=12, color='#1a1a2e', pad=12
        )
        ax.legend(fontsize=9, facecolor='#fdf8f3', edgecolor='#e0d8cf')
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.grid(axis='y', color='#e0d8cf', linewidth=0.8)
        for sp in ax.spines.values():
            sp.set_edgecolor('#e0d8cf')
        ax.tick_params(colors='#7a7a8c')
        fig4.tight_layout()
        st.pyplot(fig4)
        plt.close()

        st.dataframe(
            pd.DataFrame({
                "Period":                periodi_labele,
                "Oročena — konačno (KM)": [f"{v:,.2f}" for v in sve_orocene],
                "Tekuća — konačno (KM)":  [f"{v:,.2f}" for v in sve_tekuce],
                "Razlika (KM)":           [f"{o-t:,.2f}" for o, t in zip(sve_orocene, sve_tekuce)],
            }).set_index("Period"),
            use_container_width=True
        )

        st.markdown(
            """
            <div class="warning-box">
                💡 <b>Zaključak:</b> Oročena štednja uvijek donosi veći prinos zahvaljujući
                efektu složene kamate, ali novac je zaključan na dogovoreni period.
                Tekuća štednja je fleksibilnija, ali uz znatno niži prinos.
            </div>
            """,
            unsafe_allow_html=True
        )

    # ══ TAB 5: DETALJNA TABELA ════════════
    with tab5:
        st.markdown(f"#### 📋 Detaljna tabela · Razred: **{razred['naziv']}**")
        rows = []
        for r in rezultati:
            rows.append({
                "Banka":                    r["naziv"],
                "Razred iznosa":            razred["naziv"],
                "Kamatna stopa (% p.a.)":  f"{r['stopa']:.2f}%",
                "Uloženo (KM)":            f"{iznos:,.2f}",
                "Kamata (KM)":             f"{r['kamata']:,.2f}",
                "Porez (KM)":              f"{r['porez']:,.2f}" if porezi else "—",
                "Konačna vrijednost (KM)": f"{r['konacno']:,.2f}",
                "ROI (%)":                 f"{r['kamata'] / iznos * 100:.3f}%",
                "Formula":                 r["formula"],
            })
        df = pd.DataFrame(rows).set_index("Banka")
        st.dataframe(df, use_container_width=True, height=320)
        st.download_button(
            "⬇️ Preuzmi tabelu (CSV)",
            df.to_csv().encode("utf-8"),
            f"stednja_bih_{razred_kljuc}_{period.replace(' ', '_')}.csv",
            "text/csv"
        )
        st.markdown(
            """
            <div class="info-box">
                📌 <b>Legenda:</b> ROI = Return on Investment · p.a. = per annum ·
                Složeni k.r. = složeni kamatni račun ·
                Prosta kamata = jednostavni kamatni račun
            </div>
            """,
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center;color:#aaa;font-size:0.78rem;padding:10px 0;">
        📚 Seminarski rad · Finansijska matematika · Ekonomski fakultet<br>
        Kamatne stope su preuzete sa zvaničnih web stranica banaka —
        preporučujemo provjeru aktuelnih podataka.
    </div>
    """,
    unsafe_allow_html=True
)