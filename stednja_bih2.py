import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

# ═══════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="ŠtednjaBiH — Poređenje banaka",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════
#  DIZAJN SISTEM — zeleno/bijela profesionalna tema
# ═══════════════════════════════════════════════════════
G900 = "#0a3d1f"   # najdublja zelena
G800 = "#145a32"
G700 = "#1e7e45"
G600 = "#27ae60"   # primarna zelena
G500 = "#2ecc71"
G400 = "#58d68d"
G100 = "#eafaf1"   # jako svijetla zelena pozadina
G050 = "#f4fdf7"

WHITE  = "#ffffff"
GREY50 = "#f8fafb"
GREY100= "#f0f4f2"
GREY200= "#dde8e2"
GREY400= "#8aaa97"
GREY600= "#4a6659"
GREY800= "#1e2d26"

ACCENT  = "#0d6efd"   # plavi akcent za formule
WARN    = "#e67e22"
DANGER  = "#e74c3c"
SUCCESS = "#27ae60"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── RESET & BASE ── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {GREY50};
    color: {GREY800};
    font-size: 15px;
    line-height: 1.6;
}}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {G900} 0%, {G800} 100%);
    border-right: 3px solid {G600};
    padding-top: 0 !important;
}}
section[data-testid="stSidebar"] > div {{
    padding: 0 !important;
}}
section[data-testid="stSidebar"] * {{
    color: #e8f5ee !important;
}}
section[data-testid="stSidebar"] label {{
    color: {G400} !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}}
section[data-testid="stSidebar"] .stRadio label span,
section[data-testid="stSidebar"] .stCheckbox label span {{
    color: #d4edda !important;
    font-size: 0.88rem !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-weight: 400 !important;
}}

/* ── SIDEBAR NUMBER INPUT ── */
section[data-testid="stSidebar"] input[type="number"] {{
    background: rgba(255,255,255,0.08) !important;
    color: {G500} !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    border: 2px solid {G600} !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    text-align: right !important;
    letter-spacing: 0.02em !important;
}}
section[data-testid="stSidebar"] input[type="number"]:focus {{
    border-color: {G500} !important;
    box-shadow: 0 0 0 3px rgba(46,204,113,0.2) !important;
    outline: none !important;
}}

/* ── SIDEBAR SELECT ── */
section[data-testid="stSidebar"] .stSelectbox > div > div {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #e8f5ee !important;
    border-radius: 8px !important;
}}

/* ── GLAVNI DUGME ── */
.stButton > button {{
    background: linear-gradient(135deg, {G700}, {G600}) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 24px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    width: 100% !important;
    letter-spacing: 0.03em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(39,174,96,0.35) !important;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, {G800}, {G700}) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(39,174,96,0.45) !important;
}}

/* ── TABOVI ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {GREY100} !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 4px 4px 0 4px !important;
    gap: 4px !important;
    border-bottom: 2px solid {GREY200} !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    border-radius: 8px 8px 0 0 !important;
    color: {GREY400} !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 10px 18px !important;
    border: none !important;
}}
.stTabs [aria-selected="true"] {{
    background: {WHITE} !important;
    color: {G700} !important;
    font-weight: 700 !important;
    border-bottom: 2px solid {G600} !important;
}}

/* ── METRIKE ── */
[data-testid="metric-container"] {{
    background: {WHITE} !important;
    border: 1px solid {GREY200} !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05) !important;
    border-top: 3px solid {G600} !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Syne', sans-serif !important;
    font-size: 1.65rem !important;
    color: {G800} !important;
    font-weight: 700 !important;
}}
[data-testid="stMetricLabel"] {{
    color: {GREY400} !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
}}
[data-testid="stMetricDelta"] {{
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {{
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid {GREY200} !important;
}}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {GREY100}; border-radius: 10px; }}
::-webkit-scrollbar-thumb {{ background: {G400}; border-radius: 10px; }}

hr {{ border-color: {GREY200}; margin: 24px 0; }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  RAZREDI IZNOSA
# ═══════════════════════════════════════════════════════
RAZREDI = [
    {"naziv": "do 10.000 KM",        "min": 0,     "max": 10000,        "kljuc": "do_10000",     "ikona": "🥉"},
    {"naziv": "10.000 – 50.000 KM",  "min": 10000, "max": 50000,        "kljuc": "10000_50000",  "ikona": "🥈"},
    {"naziv": "preko 50.000 KM",      "min": 50000, "max": float('inf'), "kljuc": "preko_50000",  "ikona": "🥇"},
]

def odredi_razred(iznos):
    for r in RAZREDI:
        if iznos < r["max"]:
            return r
    return RAZREDI[-1]

# ═══════════════════════════════════════════════════════
#  PODACI O BANKAMA
# ═══════════════════════════════════════════════════════
BANKE = {
    "UniCredit Bank": {
        "boja": "#e31e24", "boja_sv": "#fdecea",
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
        "boja": "#d4a017", "boja_sv": "#fdf8e1",
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
        "boja": "#00843d", "boja_sv": "#e8f8ef",
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
        "boja": "#c0392b", "boja_sv": "#fdedec",
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
        "boja": "#1a56db", "boja_sv": "#ebf0fe",
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
        "boja": "#0e7490", "boja_sv": "#e0f5fa",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.30, "10000_50000": 0.30, "preko_50000": 0.30},
            "12 mjeseci": {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "24 mjeseca": {"do_10000": 1.50, "10000_50000": 1.50, "preko_50000": 1.50},
            "36 mjeseci": {"do_10000": 1.80, "10000_50000": 1.80, "preko_50000": 1.80},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min_iznos": 1000,
        "napomena": "Min. iznos oročenja 1.000 KM / 500 EUR"
    },
    "Addiko Bank": {
        "boja": "#6d28d9", "boja_sv": "#f0ebfe",
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

# ═══════════════════════════════════════════════════════
#  POMOĆNE FUNKCIJE
# ═══════════════════════════════════════════════════════
def dohvati_stopu(info, tip, period, kljuc):
    return info["orocene"][period][kljuc] if tip == "Oročena štednja" else info["tekuca"][kljuc]

def fmt(iznos):
    if abs(iznos) >= 1_000_000:
        return f"{iznos/1_000_000:.3f}M KM"
    return f"{iznos:,.2f} KM"

def card(sadrzaj, border_color=G600, bg=WHITE, padding="20px 24px"):
    return (
        f'<div style="background:{bg};border:1px solid {GREY200};border-left:4px solid {border_color};'
        f'border-radius:14px;padding:{padding};margin-bottom:12px;'
        f'box-shadow:0 2px 12px rgba(0,0,0,0.04);">{sadrzaj}</div>'
    )

# ═══════════════════════════════════════════════════════
#  MATPLOTLIB TEMA
# ═══════════════════════════════════════════════════════
def apply_chart_style(ax, fig):
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(GREY50)
    ax.tick_params(colors=GREY600, labelsize=8.5)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(axis='y', color=GREY200, linewidth=0.9, zorder=0)
    for sp in ax.spines.values():
        sp.set_edgecolor(GREY200)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# ═══════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    # Logo header
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{G900},{G700});
                padding:28px 24px 22px;margin:-1px -1px 0;
                border-bottom:1px solid rgba(255,255,255,0.1);">
        <div style="font-family:'Syne',sans-serif;font-size:1.4rem;
                    font-weight:800;color:white;letter-spacing:-0.02em;">
            🏦 ŠtednjaBiH
        </div>
        <div style="font-size:0.75rem;color:{G400};margin-top:4px;letter-spacing:0.05em;">
            KALKULATOR ŠTEDNJE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    with st.container():
        st.markdown(f"<div style='padding:0 16px;'>", unsafe_allow_html=True)

        iznos = st.number_input(
            "Iznos štednje (KM)",
            min_value=100, max_value=500_000, value=10_000, step=500,
        )

        # Razred indikator
        aktivan = odredi_razred(iznos)
        for r in RAZREDI:
            je_ak = r["kljuc"] == aktivan["kljuc"]
            bg   = f"rgba(46,204,113,0.15)" if je_ak else "rgba(255,255,255,0.04)"
            bord = f"2px solid {G500}"       if je_ak else f"1px solid rgba(255,255,255,0.08)"
            col  = G500 if je_ak else "rgba(255,255,255,0.3)"
            ck   = "✅ " if je_ak else "○ "
            fw   = "700" if je_ak else "400"
            st.markdown(
                f'<div style="background:{bg};border:{bord};border-radius:8px;'
                f'padding:7px 12px;margin:4px 0;font-size:0.82rem;'
                f'color:{col};font-weight:{fw};">{ck}{r["naziv"]}</div>',
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"<hr style='border-color:rgba(255,255,255,0.1);margin:8px 0 16px;'>", unsafe_allow_html=True)

        tip_stednje = st.radio("Tip štednje", ["Oročena štednja", "Tekuća (po viđenju)"])

        if tip_stednje == "Oročena štednja":
            period = st.selectbox("Period oročenja", PERIODI_OROCENE, index=2)
        else:
            period = "12 mjeseci"

        porezi = st.checkbox("Uračunaj porez na kamatu (10%)", value=False)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        izracunaj = st.button("🔍 Uporedi banke")

        st.markdown(f"""
        <div style="margin-top:20px;background:rgba(255,255,255,0.05);
                    border:1px solid rgba(255,255,255,0.1);border-radius:10px;
                    padding:12px 14px;font-size:0.78rem;color:rgba(255,255,255,0.5);
                    line-height:1.6;">
            ℹ️ Stope preuzete sa zvaničnih stranica banaka. Preporučujemo provjeru
            aktuelnih podataka prije donošenja odluke.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════
st.markdown(f"""
<div style="background:linear-gradient(135deg,{G900} 0%,{G700} 60%,{G600} 100%);
            border-radius:20px;padding:40px 48px;margin-bottom:32px;
            box-shadow:0 8px 32px rgba(10,61,31,0.2);">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
                        color:white;letter-spacing:-0.03em;line-height:1.15;">
                Poređenje štednih<br>proizvoda u BiH
            </div>
            <div style="color:rgba(255,255,255,0.65);font-size:0.95rem;margin-top:10px;">
                Finansijska matematika · Ekonomski fakultet · 2025/2026
            </div>
        </div>
        <div style="text-align:right;color:rgba(255,255,255,0.3);font-size:4rem;line-height:1;">
            🏦
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  POČETNI EKRAN
# ═══════════════════════════════════════════════════════
if not izracunaj:
    st.markdown(f"""
    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                color:{G800};margin-bottom:16px;letter-spacing:-0.01em;">
        📊 Pregled kamatnih stopa — oročena štednja (12 mj.)
    </div>
    """, unsafe_allow_html=True)

    # Header tabele
    h = st.columns([2.2, 1.2, 1.2, 1.2, 1])
    for col, txt in zip(h, ["Banka", "do 10K KM", "10K–50K KM", "preko 50K KM", "Min. iznos"]):
        col.markdown(
            f"<div style='font-size:0.72rem;font-weight:700;text-transform:uppercase;"
            f"letter-spacing:0.08em;color:{GREY400};padding:8px 0;border-bottom:2px solid {GREY200};'>"
            f"{txt}</div>",
            unsafe_allow_html=True
        )

    for naziv, info in BANKE.items():
        s   = info["orocene"]["12 mjeseci"]
        max_s = max(s.values())
        cols = st.columns([2.2, 1.2, 1.2, 1.2, 1])
        boja = info["boja"]
        with cols[0]:
            st.markdown(
                f"<div style='padding:10px 0;display:flex;align-items:center;gap:10px;'>"
                f"<span style='width:10px;height:10px;border-radius:50%;background:{boja};"
                f"display:inline-block;flex-shrink:0;'></span>"
                f"<span style='font-weight:600;font-size:0.9rem;color:{GREY800};'>{naziv}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        for col, k in zip(cols[1:4], ["do_10000","10000_50000","preko_50000"]):
            v = s[k]
            is_max = v == max_s and v > 0
            bg_pill = f"background:{G100};color:{G700};font-weight:700;" if is_max else f"color:{GREY600};"
            col.markdown(
                f"<div style='padding:10px 0;'>"
                f"<span style='{bg_pill}font-size:0.88rem;padding:3px 8px;"
                f"border-radius:6px;'>{v:.2f}%</span></div>",
                unsafe_allow_html=True
            )
        with cols[4]:
            mi = info["min_iznos"]
            st.markdown(
                f"<div style='padding:10px 0;font-size:0.82rem;color:{GREY400};'>"
                f"{'—' if mi == 0 else f'{mi:,} KM'}</div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:{G100};border:1px solid {G400};border-left:4px solid {G600};
                border-radius:12px;padding:16px 20px;color:{G800};font-size:0.9rem;">
        👈 <b>Unesite iznos i period u lijevoj koloni</b>, zatim kliknite
        <b>Uporedi banke</b> — aplikacija automatski odabira vaš razred i
        prikazuje detaljnu analizu svih banaka.
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  REZULTATI
# ═══════════════════════════════════════════════════════
else:
    period_god   = PERIODI_MAPA.get(period, 1.0)
    razred       = odredi_razred(iznos)
    rkljuc       = razred["kljuc"]

    # Izračun
    rezultati = []
    for naziv, info in BANKE.items():
        stopa = dohvati_stopu(info, tip_stednje, period, rkljuc)
        if tip_stednje == "Oročena štednja":
            konacno = iznos * (1 + stopa/100)**period_god
            formula = "Složeni kamatni račun"
        else:
            konacno = iznos * (1 + stopa/100 * period_god)
            formula = "Prosta kamata"
        kamata       = konacno - iznos
        porez        = kamata * 0.10 if porezi else 0
        kamata_neto  = kamata - porez
        konacno_neto = iznos + kamata_neto
        rezultati.append({
            "naziv": naziv, "boja": info["boja"], "boja_sv": info["boja_sv"],
            "stopa": stopa, "konacno": konacno_neto,
            "kamata": kamata_neto, "porez": porez,
            "formula": formula, "min_iznos": info["min_iznos"],
            "napomena": info["napomena"],
            "sve_stope": {r["kljuc"]: dohvati_stopu(info, tip_stednje, period, r["kljuc"]) for r in RAZREDI},
        })

    rezultati.sort(key=lambda x: x["konacno"], reverse=True)
    pob = rezultati[0]

    # ── RAZRED BANNER ──────────────────────────
    st.markdown(f"""
    <div style="background:{G100};border:1px solid {G400};border-radius:14px;
                padding:16px 24px;margin-bottom:24px;
                display:flex;align-items:center;gap:16px;">
        <div style="background:{G600};color:white;border-radius:10px;
                    padding:10px 14px;font-size:1.4rem;line-height:1;">💰</div>
        <div>
            <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.1em;color:{G600};">Aktivan razred iznosa</div>
            <div style="font-size:1.15rem;font-weight:700;color:{G800};">
                {razred['ikona']} {razred['naziv']}
            </div>
        </div>
        <div style="margin-left:auto;text-align:right;">
            <div style="font-size:0.7rem;color:{GREY400};text-transform:uppercase;
                        letter-spacing:0.08em;">Uloženi iznos</div>
            <div style="font-size:1.4rem;font-weight:700;color:{G700};font-family:'Syne',sans-serif;">
                {fmt(iznos)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 4 METRIKE ──────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💰 Uloženo", fmt(iznos))
    with c2:
        naziv_k = pob["naziv"].replace(" Bank","").replace(" Banka","")
        st.metric("🥇 Najbolja banka", naziv_k, delta=f"{pob['stopa']:.2f}% p.a.")
    with c3:
        st.metric("📈 Max. zarada", fmt(pob["kamata"]),
                  delta=f"+{pob['kamata']/iznos*100:.3f}% ROI")
    with c4:
        razl = rezultati[0]["konacno"] - rezultati[-1]["konacno"]
        st.metric("↕️ Razlika min/max", fmt(razl))

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── TABOVI ─────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🥇  Preporuka",
        "📊  Grafovi",
        "🎚️  Analiza razreda",
        "⚖️  Oročena vs. Tekuća",
        "📋  Tabela",
    ])

    # ════════════════════════════════════════════
    #  TAB 1 — PREPORUKA
    # ════════════════════════════════════════════
    with tab1:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        lc, rc = st.columns([1, 1], gap="large")

        with lc:
            # Pobjednička kartica
            porez_r = f"<br>🧾 Porez (10%): <b style='color:{WARN};'>−{fmt(pob['porez'])}</b>" if porezi else ""
            st.markdown(f"""
            <div style="background:linear-gradient(145deg,{G900},{G800});
                        border-radius:20px;padding:32px;
                        box-shadow:0 8px 32px rgba(10,61,31,0.25);">
                <div style="display:inline-block;background:{G600};color:white;
                            font-size:0.7rem;font-weight:700;letter-spacing:0.12em;
                            text-transform:uppercase;border-radius:20px;
                            padding:5px 14px;margin-bottom:20px;">
                    🥇 Preporučena banka
                </div>
                <div style="font-family:'Syne',sans-serif;font-size:1.9rem;
                            font-weight:800;color:white;margin-bottom:4px;
                            letter-spacing:-0.02em;">
                    {pob['naziv']}
                </div>
                <div style="font-size:2.4rem;font-weight:800;color:{G500};
                            font-family:'Syne',sans-serif;margin-bottom:24px;">
                    {pob['stopa']:.2f}%
                    <span style="font-size:0.9rem;color:{G400};font-weight:400;">
                        godišnje (p.a.)
                    </span>
                </div>
                <div style="background:rgba(255,255,255,0.06);border-radius:12px;
                            padding:18px 20px;font-size:0.9rem;line-height:2.1;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:rgba(255,255,255,0.55);">Konačna vrijednost</span>
                        <span style="color:{G400};font-weight:700;">{fmt(pob['konacno'])}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:rgba(255,255,255,0.55);">Zarada od kamate</span>
                        <span style="color:{G500};font-weight:700;">+{fmt(pob['kamata'])}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:rgba(255,255,255,0.55);">Period</span>
                        <span style="color:white;font-weight:600;">
                            {period if tip_stednje == 'Oročena štednja' else 'Po viđenju'}
                        </span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:rgba(255,255,255,0.55);">Razred iznosa</span>
                        <span style="color:white;font-weight:600;">{razred['naziv']}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:rgba(255,255,255,0.55);">Metoda</span>
                        <span style="color:white;font-weight:600;">{pob['formula']}</span>
                    </div>
                    {porez_r}
                </div>
                <div style="margin-top:16px;font-size:0.78rem;
                            color:rgba(255,255,255,0.3);font-style:italic;">
                    ℹ️ {pob['napomena']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Formula box
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            if tip_stednje == "Oročena štednja":
                st.markdown(f"""
                <div style="background:{G050};border:1px solid {G200 if False else GREY200};
                            border-left:4px solid {G600};border-radius:12px;padding:18px 20px;">
                    <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                                letter-spacing:0.1em;color:{G600};margin-bottom:10px;">
                        🧮 Primjenjena formula
                    </div>
                    <div style="font-family:monospace;font-size:1rem;color:{G800};
                                background:{GREY100};padding:10px 14px;border-radius:8px;
                                margin-bottom:10px;">
                        Fn = P × (1 + r/100)<sup>n</sup>
                    </div>
                    <div style="font-size:0.85rem;color:{GREY600};line-height:1.8;">
                        P = {fmt(iznos)} &nbsp;·&nbsp;
                        r = {pob['stopa']:.2f}% &nbsp;·&nbsp;
                        n = {period_god} god.<br>
                        <b style="color:{G700};">Fn = {iznos:,.2f} ×
                        (1 + {pob['stopa']/100:.4f})<sup>{period_god}</sup>
                        = {fmt(pob['konacno'])}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:{G050};border:1px solid {GREY200};
                            border-left:4px solid {G600};border-radius:12px;padding:18px 20px;">
                    <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                                letter-spacing:0.1em;color:{G600};margin-bottom:10px;">
                        🧮 Primjenjena formula
                    </div>
                    <div style="font-family:monospace;font-size:1rem;color:{G800};
                                background:{GREY100};padding:10px 14px;border-radius:8px;
                                margin-bottom:10px;">
                        Fn = P × (1 + r/100 × n)
                    </div>
                    <div style="font-size:0.85rem;color:{GREY600};line-height:1.8;">
                        P = {fmt(iznos)} &nbsp;·&nbsp;
                        r = {pob['stopa']:.2f}% &nbsp;·&nbsp;
                        n = {period_god} god.<br>
                        <b style="color:{G700};">Fn = {iznos:,.2f} ×
                        (1 + {pob['stopa']/100:.4f} × {period_god})
                        = {fmt(pob['konacno'])}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with rc:
            st.markdown(f"""
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;
                        color:{G800};margin-bottom:16px;">🏆 Rang lista banaka</div>
            """, unsafe_allow_html=True)

            medalje = ["🥇", "🥈", "🥉"] + ["   "] * 10
            for i, r in enumerate(rezultati):
                naziv   = r["naziv"]
                boja    = r["boja"]
                boja_sv = r["boja_sv"]
                stopa_t = f"{r['stopa']:.2f}%"
                konacno_t = fmt(r["konacno"])
                kamata_t  = fmt(r["kamata"])
                medalja = medalje[i]
                is_pob  = i == 0

                upoz = ""
                if iznos < r["min_iznos"]:
                    upoz = (f"<span style='background:#fff3cd;color:#856404;font-size:0.7rem;"
                            f"padding:2px 7px;border-radius:10px;margin-left:6px;font-weight:600;'>"
                            f"⚠️ min {r['min_iznos']:,} KM</span>")

                border_style = f"2px solid {boja}" if is_pob else f"1px solid {GREY200}"
                bg_style     = boja_sv if is_pob else WHITE
                shadow       = "box-shadow:0 4px 16px rgba(0,0,0,0.08);" if is_pob else ""

                html = (
                    f'<div style="background:{bg_style};border:{border_style};'
                    f'border-radius:12px;padding:14px 18px;margin-bottom:10px;{shadow}'
                    f'transition:all 0.2s;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<div style="display:flex;align-items:center;gap:8px;">'
                    f'<span style="font-size:1.1rem;">{medalja}</span>'
                    f'<div>'
                    f'<div style="font-weight:600;font-size:0.92rem;color:{GREY800};">'
                    f'{naziv}{upoz}</div>'
                    f'<div style="font-size:0.8rem;color:{GREY400};margin-top:1px;">'
                    f'Kamatna stopa: <b style="color:{boja};">{stopa_t} p.a.</b></div>'
                    f'</div></div>'
                    f'<div style="text-align:right;">'
                    f'<div style="font-weight:700;font-size:0.95rem;color:{G800};">{konacno_t}</div>'
                    f'<div style="font-size:0.78rem;color:{G600};font-weight:600;">+{kamata_t}</div>'
                    f'</div></div></div>'
                )
                st.markdown(html, unsafe_allow_html=True)

    # ════════════════════════════════════════════
    #  TAB 2 — GRAFOVI
    # ════════════════════════════════════════════
    with tab2:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ─ Graf 1: Bar + Horizontalni ─
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))
        apply_chart_style(ax1, fig)
        apply_chart_style(ax2, fig)

        nazivi_k = [r["naziv"].replace(" Bank","").replace(" Banka","") for r in rezultati]
        boje_plt = [r["boja"] for r in rezultati]

        # Bar chart konačnih vrijednosti
        bars = ax1.bar(nazivi_k, [r["konacno"] for r in rezultati],
                       color=boje_plt, alpha=0.85, edgecolor=WHITE,
                       linewidth=1.5, zorder=3, width=0.6)
        ax1.axhline(iznos, color=GREY600, linewidth=1.5, linestyle='--',
                    alpha=0.6, label=f"Uloženo: {fmt(iznos)}", zorder=4)
        for bar, r in zip(bars, rezultati):
            ax1.text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + iznos * 0.015,
                     f"+{fmt(r['kamata'])}", ha='center', va='bottom',
                     fontsize=7, color=GREY600, fontweight='600')
        ax1.set_title("Konačna vrijednost štednje po banci",
                      fontsize=11, color=GREY800, pad=14, fontweight='600')
        ax1.set_ylabel("Iznos (KM)", color=GREY400, fontsize=9)
        ax1.tick_params(axis='x', rotation=28, labelsize=8)
        ax1.legend(fontsize=8, facecolor=WHITE, edgecolor=GREY200,
                   framealpha=1, loc='upper right')

        # Horizontalni bar kamatnih stopa
        rez_rev = list(reversed(rezultati))
        hbars = ax2.barh(
            [r["naziv"].replace(" Bank","").replace(" Banka","") for r in rez_rev],
            [r["stopa"] for r in rez_rev],
            color=[r["boja"] for r in rez_rev],
            alpha=0.85, edgecolor=WHITE, linewidth=1.5, height=0.6
        )
        for bar, r in zip(hbars, rez_rev):
            ax2.text(bar.get_width() + 0.02,
                     bar.get_y() + bar.get_height()/2,
                     f"{r['stopa']:.2f}%", va='center',
                     fontsize=8.5, fontweight='700', color=GREY800)
        ax2.set_title(f"Kamatna stopa (% p.a.) — razred: {razred['naziv']}",
                      fontsize=11, color=GREY800, pad=14, fontweight='600')
        ax2.set_xlabel("Kamatna stopa (%)", color=GREY400, fontsize=9)
        ax2.grid(axis='x', color=GREY200, linewidth=0.9)
        ax2.grid(axis='y', visible=False)
        ax2.spines['left'].set_visible(False)

        fig.tight_layout(pad=3)
        st.pyplot(fig)
        plt.close()

        # ─ Graf 2: Linijski rast kroz vrijeme ─
        st.markdown(f"""
        <div style="font-size:0.95rem;font-weight:700;color:{G800};
                    margin:20px 0 12px;letter-spacing:-0.01em;">
            📈 Rast vrijednosti štednje kroz vrijeme — sve banke
        </div>
        """, unsafe_allow_html=True)

        fig2, ax = plt.subplots(figsize=(13, 4.5))
        apply_chart_style(ax, fig2)

        max_god = max(3.0, period_god * 1.5) if tip_stednje == "Oročena štednja" else 3.0
        osi_x   = np.linspace(0, max_god, 200)

        for r in rezultati:
            vr = ([iznos*(1+r["stopa"]/100)**g for g in osi_x]
                  if tip_stednje == "Oročena štednja"
                  else [iznos*(1+r["stopa"]/100*g) for g in osi_x])
            is_pob = r["naziv"] == pob["naziv"]
            ax.plot(osi_x, vr, color=r["boja"],
                    linewidth=3 if is_pob else 1.2,
                    alpha=1.0 if is_pob else 0.45,
                    zorder=5 if is_pob else 2,
                    label=r["naziv"].replace(" Bank","").replace(" Banka",""))

        ax.axhline(iznos, color=GREY400, linewidth=1.2, linestyle=':',
                   alpha=0.7, label="Polazni iznos")
        if tip_stednje == "Oročena štednja":
            ax.axvline(period_god, color=G600, linewidth=1.5, linestyle='--',
                       alpha=0.7, label=f"Kraj perioda ({period})")

        ax.set_xlabel("Godine", color=GREY400, fontsize=10)
        ax.set_ylabel("Vrijednost (KM)", color=GREY400, fontsize=10)
        ax.legend(fontsize=8.5, facecolor=WHITE, edgecolor=GREY200,
                  framealpha=1, ncol=2, loc='upper left')
        ax.set_title("", pad=0)

        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # ════════════════════════════════════════════
    #  TAB 3 — ANALIZA RAZREDA
    # ════════════════════════════════════════════
    with tab3:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{G100};border:1px solid {GREY200};border-left:4px solid {G600};
                    border-radius:12px;padding:16px 20px;margin-bottom:20px;font-size:0.9rem;color:{G800};">
            Banke primjenjuju <b>tri razreda iznosa</b> — veći iznos donosi višu kamatnu stopu.
            Vaš iznos <b>{fmt(iznos)}</b> spada u razred <b>{razred['naziv']}</b>.
            Grafikon ispod pokazuje stope za sva tri razreda kod svake banke.
        </div>
        """, unsafe_allow_html=True)

        fig3, ax = plt.subplots(figsize=(13, 5))
        apply_chart_style(ax, fig3)

        x = np.arange(len(rezultati))
        w = 0.26
        boje_raz   = [G400, G600, G800]
        labele_raz = [r["naziv"] for r in RAZREDI]

        for i, (raz_i, boja_r) in enumerate(zip(RAZREDI, boje_raz)):
            stope_r = [r["sve_stope"][raz_i["kljuc"]] for r in rezultati]
            je_ak   = raz_i["kljuc"] == rkljuc
            b3 = ax.bar(x+(i-1)*w, stope_r, w, label=raz_i["naziv"],
                        color=boja_r, alpha=0.9,
                        edgecolor=G900 if je_ak else WHITE,
                        linewidth=2 if je_ak else 0.5)
            for bar, s in zip(b3, stope_r):
                if s > 0:
                    ax.text(bar.get_x()+bar.get_width()/2,
                            bar.get_height()+0.01,
                            f"{s:.2f}", ha='center', va='bottom',
                            fontsize=6.5, color=GREY600, fontweight='600')

        ax.set_xticks(x)
        ax.set_xticklabels(
            [r["naziv"].replace(" Bank","").replace(" Banka","") for r in rezultati],
            rotation=18, fontsize=8.5
        )
        ax.set_ylabel("Kamatna stopa (% p.a.)", color=GREY400, fontsize=9)
        ax.set_title(
            f"Kamatna stopa po razredu iznosa — {period}   "
            f"(istaknuto: {razred['naziv']})",
            fontsize=11, color=GREY800, pad=14, fontweight='600'
        )
        ax.legend(title="Razred iznosa", fontsize=9,
                  facecolor=WHITE, edgecolor=GREY200, framealpha=1)
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close()

        # Tabela efekta razreda
        st.markdown(f"""
        <div style="font-size:0.88rem;font-weight:700;color:{G800};margin:20px 0 10px;">
            💡 Efekt razreda na vašu štednju — {pob['naziv']}
        </div>
        """, unsafe_allow_html=True)

        rows_r = []
        for raz_i in RAZREDI:
            s = dohvati_stopu(BANKE[pob["naziv"]], tip_stednje, period, raz_i["kljuc"])
            k = (iznos*(1+s/100)**period_god - iznos
                 if tip_stednje == "Oročena štednja"
                 else iznos*s/100*period_god)
            mark = " ✅" if raz_i["kljuc"] == rkljuc else ""
            rows_r.append({
                "Razred iznosa":            raz_i["naziv"] + mark,
                "Kamatna stopa":            f"{s:.2f}% p.a.",
                "Kamata na vaš iznos (KM)": f"{k:,.2f}",
                "Konačna vrijednost (KM)":  f"{iznos+k:,.2f}",
            })
        st.dataframe(pd.DataFrame(rows_r).set_index("Razred iznosa"),
                     use_container_width=True)

        st.markdown(f"""
        <div style="background:#fff8e1;border:1px solid #ffe082;border-left:4px solid {WARN};
                    border-radius:12px;padding:14px 18px;margin-top:12px;
                    font-size:0.88rem;color:#5d4037;">
            💡 <b>Savjet:</b> Ako je vaš iznos blizu gornje granice razreda (npr. 9.800 KM),
            razmotrite dopunu do <b>10.000 KM</b> — prelaskom u viši razred
            dobijate bolju stopu na <i>cijeli</i> iznos.
        </div>
        """, unsafe_allow_html=True)

    # ════════════════════════════════════════════
    #  TAB 4 — OROČENA VS TEKUĆA
    # ════════════════════════════════════════════
    with tab4:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{G100};border:1px solid {GREY200};border-left:4px solid {G600};
                    border-radius:12px;padding:16px 20px;margin-bottom:20px;font-size:0.9rem;color:{G800};">
            <b>Složeni kamatni račun</b> (oročena štednja) — kamata se pripisuje na kamatu.<br>
            <b>Prosta kamata</b> (po viđenju) — kamata se računa samo na glavnicu.<br>
            <span style="color:{GREY400};">Analiza za: <b>{pob['naziv']}</b> · Razred: <b>{razred['naziv']}</b></span>
        </div>
        """, unsafe_allow_html=True)

        sve_or, sve_tek, per_lab = [], [], []
        for p_naziv, p_god in PERIODI_MAPA.items():
            s_or  = BANKE[pob["naziv"]]["orocene"][p_naziv][rkljuc]
            s_tek = BANKE[pob["naziv"]]["tekuca"][rkljuc]
            sve_or.append(iznos*(1+s_or/100)**p_god)
            sve_tek.append(iznos*(1+s_tek/100*p_god))
            per_lab.append(p_naziv)

        fig4, ax = plt.subplots(figsize=(10, 4.5))
        apply_chart_style(ax, fig4)

        xp = np.arange(len(per_lab)); w = 0.35
        b1 = ax.bar(xp-w/2, sve_or,  w, label="Oročena (složeni k.r.)",
                    color=G600, alpha=0.88, edgecolor=WHITE, linewidth=1.5)
        b2 = ax.bar(xp+w/2, sve_tek, w, label="Po viđenju (prosta kamata)",
                    color=GREY400, alpha=0.88, edgecolor=WHITE, linewidth=1.5)
        ax.axhline(iznos, color=DANGER, linewidth=1.2, linestyle='--',
                   alpha=0.55, label=f"Uloženo: {fmt(iznos)}")

        for bar in b1:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+iznos*0.005,
                    fmt(bar.get_height()), ha='center', va='bottom',
                    fontsize=7, fontweight='600', color=G800)
        for bar in b2:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+iznos*0.005,
                    fmt(bar.get_height()), ha='center', va='bottom',
                    fontsize=7, fontweight='600', color=GREY600)

        ax.set_xticks(xp); ax.set_xticklabels(per_lab, fontsize=9)
        ax.set_ylabel("Iznos (KM)", color=GREY400, fontsize=9)
        ax.set_title(f"Oročena vs. Tekuća — {pob['naziv']} · {razred['naziv']}",
                     fontsize=11, color=GREY800, pad=14, fontweight='600')
        ax.legend(fontsize=9, facecolor=WHITE, edgecolor=GREY200, framealpha=1)
        fig4.tight_layout()
        st.pyplot(fig4)
        plt.close()

        st.dataframe(
            pd.DataFrame({
                "Period":                 per_lab,
                "Oročena — konačno (KM)": [f"{v:,.2f}" for v in sve_or],
                "Tekuća — konačno (KM)":  [f"{v:,.2f}" for v in sve_tek],
                "Razlika (KM)":           [f"{o-t:,.2f}" for o, t in zip(sve_or, sve_tek)],
            }).set_index("Period"),
            use_container_width=True
        )

        st.markdown(f"""
        <div style="background:#e8f8ef;border:1px solid {G400};border-left:4px solid {G600};
                    border-radius:12px;padding:14px 18px;margin-top:12px;
                    font-size:0.88rem;color:{G800};">
            💡 <b>Zaključak:</b> Oročena štednja uvijek donosi veći prinos zahvaljujući
            efektu složene kamate, ali novac je zaključan na ugovoreni period.
            Tekuća štednja je fleksibilna, ali uz znatno niži prinos.
        </div>
        """, unsafe_allow_html=True)

    # ════════════════════════════════════════════
    #  TAB 5 — DETALJNA TABELA
    # ════════════════════════════════════════════
    with tab5:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:0.88rem;color:{GREY400};margin-bottom:12px;">
            Razred: <b style="color:{G700};">{razred['naziv']}</b> &nbsp;·&nbsp;
            Period: <b style="color:{G700};">{period if tip_stednje == 'Oročena štednja' else 'Po viđenju'}</b> &nbsp;·&nbsp;
            Metoda: <b style="color:{G700};">{pob['formula']}</b>
        </div>
        """, unsafe_allow_html=True)

        rows = []
        for r in rezultati:
            rows.append({
                "Banka":                   r["naziv"],
                "Razred":                  razred["naziv"],
                "Stopa (% p.a.)":          f"{r['stopa']:.2f}%",
                "Uloženo (KM)":            f"{iznos:,.2f}",
                "Kamata (KM)":             f"{r['kamata']:,.2f}",
                "Porez (KM)":              f"{r['porez']:,.2f}" if porezi else "—",
                "Konačna vrijednost (KM)": f"{r['konacno']:,.2f}",
                "ROI (%)":                 f"{r['kamata']/iznos*100:.3f}%",
                "Formula":                 r["formula"],
            })

        df = pd.DataFrame(rows).set_index("Banka")
        st.dataframe(df, use_container_width=True, height=340)

        st.download_button(
            "⬇️ Preuzmi tabelu (CSV)",
            df.to_csv().encode("utf-8"),
            f"stednja_bih_{rkljuc}_{period.replace(' ','_')}.csv",
            "text/csv"
        )

        st.markdown(f"""
        <div style="background:{G050};border:1px solid {GREY200};border-radius:10px;
                    padding:12px 16px;margin-top:12px;font-size:0.82rem;color:{GREY400};">
            📌 <b>Legenda:</b> ROI = Return on Investment (povrat na investiciju) &nbsp;·&nbsp;
            p.a. = per annum (godišnje) &nbsp;·&nbsp;
            Složeni k.r. = složeni kamatni račun
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-top:48px;padding:24px 32px;background:{G100};
            border-radius:16px;border:1px solid {GREY200};
            display:flex;justify-content:space-between;align-items:center;">
    <div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;
                    color:{G800};font-size:0.95rem;">🏦 ŠtednjaBiH</div>
        <div style="font-size:0.78rem;color:{GREY400};margin-top:3px;">
            Seminarski rad · Finansijska matematika · Ekonomski fakultet
        </div>
    </div>
    <div style="font-size:0.78rem;color:{GREY400};text-align:right;">
        Kamatne stope preuzete sa zvaničnih web stranica banaka.<br>
        Preporučujemo provjeru aktuelnih podataka.
    </div>
</div>
""", unsafe_allow_html=True)
