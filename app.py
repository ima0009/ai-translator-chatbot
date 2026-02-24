import streamlit as st
import os
import time
import io
import json
import re
from datetime import datetime

st.set_page_config(page_title="MERCREDI-AI", page_icon="🌐", layout="wide")

# ── Clés API ────────────────────────────────────────────────────────
os.environ["OCR_API_KEY"] = st.secrets.get("OCR_API_KEY", "helloworld")

# ── Session clé utilisateur ─────────────────────────────────────────
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = st.secrets.get("GROQ_API_KEY", "")

if "language" not in st.session_state:
    st.session_state.language = "fr"

if "page" not in st.session_state:
    st.session_state.page = "accueil"

def _(fr, en, ar=None, ber=None):
    if st.session_state.language == "en": return en
    if st.session_state.language == "ar" and ar: return ar
    if st.session_state.language == "ber" and ber: return ber
    return fr

# ────────────────────────────────────────────────────────────────────
# ── CSS PROFESSIONNEL AVEC COULEURS STREAMLIT NATIVES ──────────────
# ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Sans+Pro:wght@400;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

:root {
    /* ════ PALETTE STREAMLIT NATIVE ════ */
    --st-primary: #FF4B4B;
    --st-primary-dark: #E03E3E;
    --st-primary-light: #FF6B6B;
    
    --st-secondary: #0068C9;
    --st-secondary-dark: #0054A3;
    --st-secondary-light: #1E88E5;
    
    --st-success: #09AB3B;
    --st-success-dark: #078A2F;
    --st-success-light: #21C55D;
    
    --st-warning: #FFA421;
    --st-info: #0068C9;
    --st-error: #FF4B4B;
    
    /* ════ ARRIÈRE-PLANS ════ */
    --bg-primary: #FFFFFF;
    --bg-secondary: #F8F9FA;
    --bg-tertiary: #F0F2F6;
    --bg-gradient: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 50%, #F0F2F6 100%);
    
    /* ════ TEXTE ════ */
    --text-primary: #262730;
    --text-secondary: #6C757D;
    --text-muted: #8E9297;
    --text-light: #FFFFFF;
    
    /* ════ BORDURES ════ */
    --border-color: #E6E9EF;
    --border-color-hover: #D4D8E1;
    
    /* ════ OMBRES MODERNES ════ */
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
    --shadow-xl: 0 16px 40px rgba(0, 0, 0, 0.15);
    
    /* ════ TRANSITIONS ════ */
    --transition-fast: 0.15s ease;
    --transition-normal: 0.3s ease;
    --transition-smooth: 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* ════ TYPOGRAPHIE ════ */
html, body, [class*="css"] {
    font-family: 'Inter', 'Source Sans Pro', sans-serif;
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

/* ════ PAGE ACCUEIL ════ */
.home-background {
    background: var(--bg-gradient);
    border-radius: 16px;
    padding: 3rem 2rem;
    margin: 2rem 0;
    border: 1px solid var(--border-color);
    animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

/* ════ CARTES PRINCIPALES ════ */
.card {
    background: var(--bg-primary);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-color);
    margin: 1.5rem 0;
    transition: all var(--transition-smooth);
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    border-color: var(--st-secondary);
}

/* ════ CARTES DE FEATURES ════ */
.feature-card {
    background: var(--bg-primary);
    border-radius: 12px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-smooth);
    height: 100%;
    border: 2px solid var(--border-color);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--st-primary) 0%, var(--st-secondary) 50%, var(--st-success) 100%);
    opacity: 0;
    transition: opacity var(--transition-normal);
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--st-secondary);
}

.feature-card:hover::before {
    opacity: 1;
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: inline-block;
    transition: transform var(--transition-normal);
}

.feature-card:hover .feature-icon {
    transform: scale(1.1);
    animation: bounce 1s ease-in-out;
}

.feature-card h3 {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
    font-weight: 600;
}

.feature-card p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.6;
}

/* ════ BOÎTES D'ÉTAPES ════ */
.step-box {
    background: var(--bg-primary);
    border-left: 4px solid var(--st-success);
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-normal);
    border-top: 1px solid var(--border-color);
    border-right: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
}

.step-box:hover {
    border-left-width: 6px;
    transform: translateX(4px);
    box-shadow: var(--shadow-md);
}

.step-box code {
    background: var(--st-secondary);
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.9em;
}

/* ════ BOÎTES RÉSULTATS ════ */
.result-box {
    background: var(--bg-primary);
    border-left: 4px solid var(--st-secondary);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    font-size: 1rem;
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-normal);
    min-height: 150px;
    line-height: 1.7;
    border: 1px solid var(--border-color);
}

.result-box:hover {
    box-shadow: var(--shadow-md);
    border-left-width: 6px;
}

/* ════ HISTORIQUE ════ */
.history-item {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-left: 4px solid var(--st-secondary);
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-normal);
}

.history-item:hover {
    border-left-width: 6px;
    transform: translateX(4px);
    box-shadow: var(--shadow-md);
    border-color: var(--st-secondary);
}

.history-meta {
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin-bottom: 0.8rem;
    font-weight: 500;
}

/* ════ BOUTONS - STREAMLIT NATIVE ════ */
button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    border: none !important;
    transition: all var(--transition-normal) !important;
    cursor: pointer !important;
    box-shadow: var(--shadow-sm) !important;
    letter-spacing: 0.01em !important;
}

button:hover {
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-md) !important;
}

/* Boutons principaux - Rouge Streamlit */
button:not([key*="btn_logout"]):not([key*="btn_clear"]):not([key*="btn_reset"]):not([key*="lang_"]):not([key*="nav_"]) {
    background-color: var(--st-primary) !important;
    color: white !important;
}

button:not([key*="btn_logout"]):not([key*="btn_clear"]):not([key*="btn_reset"]):not([key*="lang_"]):not([key*="nav_"]):hover {
    background-color: var(--st-primary-dark) !important;
}

/* Bouton Accéder à l'application */
button[key="btn_start"] {
    background: linear-gradient(135deg, var(--st-primary) 0%, var(--st-primary-light) 100%) !important;
    padding: 0.75rem 2rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
}

/* Boutons de déconnexion/réinitialisation */
button[key*="btn_logout"],
button[key*="btn_clear"],
button[key*="btn_reset"] {
    background-color: var(--st-error) !important;
    color: white !important;
}

button[key*="btn_logout"]:hover,
button[key*="btn_clear"]:hover,
button[key*="btn_reset"]:hover {
    background-color: var(--st-primary-dark) !important;
}

/* Boutons de langue */
button[key*="lang_"] {
    background-color: transparent !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--st-secondary) !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
}

button[key*="lang_"]:hover:not(:disabled) {
    background-color: var(--st-secondary) !important;
    color: white !important;
}

button[key*="lang_"]:disabled {
    background-color: var(--st-secondary) !important;
    color: white !important;
    border-color: var(--st-secondary) !important;
    opacity: 1 !important;
    cursor: not-allowed !important;
}

/* Bouton navigation */
button[key="nav_home"] {
    background-color: var(--st-secondary) !important;
    color: white !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
}

button[key="nav_home"]:hover {
    background-color: var(--st-secondary-dark) !important;
}

/* ════ FILE UPLOADERS ════ */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--border-color);
    border-radius: 8px;
    padding: 1rem;
    background: var(--bg-secondary);
    transition: all var(--transition-normal);
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--st-secondary);
    background: var(--bg-primary);
}

[data-testid="stFileUploader"] button {
    all: revert !important;
    background: var(--st-secondary) !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.4rem 1rem !important;
    font-family: inherit !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-sm) !important;
    cursor: pointer !important;
}

[data-testid="stFileUploader"] button:hover {
    background: var(--st-secondary-dark) !important;
    transform: none !important;
    box-shadow: var(--shadow-md) !important;
}

/* ════ FEEDBACK SECTION ════ */
.feedback-card {
    background: var(--bg-primary);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: var(--shadow-md);
    border: 2px solid var(--st-secondary);
    transition: all var(--transition-smooth);
    margin: 1.5rem 0;
}

.feedback-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.feedback-stats {
    background: var(--bg-primary);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    border-left: 4px solid var(--st-secondary);
    transition: all var(--transition-normal);
    border: 1px solid var(--border-color);
}

.feedback-stats:hover {
    border-left-width: 6px;
    transform: translateX(4px);
    box-shadow: var(--shadow-md);
}

.feedback-item {
    background: var(--bg-primary);
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-normal);
}

.feedback-item:hover {
    box-shadow: var(--shadow-md);
    transform: translateX(4px);
}

.feedback-score-high {
    border-left: 4px solid var(--st-success) !important;
}

.feedback-score-high:hover {
    border-left-width: 6px !important;
}

.feedback-score-medium {
    border-left: 4px solid var(--st-warning) !important;
}

.feedback-score-medium:hover {
    border-left-width: 6px !important;
}

.feedback-score-low {
    border-left: 4px solid var(--st-error) !important;
}

.feedback-score-low:hover {
    border-left-width: 6px !important;
}

/* ════ ALERTES ET MESSAGES ════ */
.stAlert {
    border-radius: 8px !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ════ MESSAGE LANGUE DÉTECTÉE ════ */
.detected-lang-box {
    max-width: 500px;
    margin: 0.8rem auto;
    padding: 0.8rem 1.2rem;
    background: linear-gradient(135deg, #FFF9E6 0%, #FFEAA7 100%);
    border: 2px solid var(--st-warning);
    border-radius: 8px;
    border-left: 4px solid var(--st-warning);
    box-shadow: var(--shadow-sm);
    font-weight: 500;
}

/* ════ ONGLETS ════ */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: transparent;
    border-bottom: 2px solid var(--border-color);
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: 0.75rem 1.5rem !important;
    transition: all var(--transition-fast) !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--st-secondary) !important;
    background: var(--bg-secondary) !important;
}

.stTabs [aria-selected="true"] {
    color: var(--st-secondary) !important;
    font-weight: 600 !important;
    border-bottom: 3px solid var(--st-secondary) !important;
}

/* ════ INPUTS ════ */
input, textarea, select {
    border-radius: 6px !important;
    border: 1px solid var(--border-color) !important;
    transition: all var(--transition-fast) !important;
}

input:focus, textarea:focus, select:focus {
    border-color: var(--st-secondary) !important;
    box-shadow: 0 0 0 3px rgba(0, 104, 201, 0.1) !important;
}

/* ════ FOOTER ════ */
.footer-home {
    text-align: center;
    color: var(--text-secondary);
    padding: 2rem 1rem;
    font-size: 0.9rem;
    margin-top: 3rem;
    font-weight: 500;
    animation: fadeIn 0.8s ease-out 0.3s backwards;
}

/* ════ SCROLLBAR ════ */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: var(--st-secondary);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--st-secondary-dark);
}

/* ════ METRICS ════ */
[data-testid="stMetric"] {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: var(--shadow-sm);
}

/* ════ RESPONSIVE DESIGN ════ */
@media (max-width: 768px) {
    .feature-card { padding: 1.5rem 1rem; }
    .card { padding: 1.5rem; }
    button { padding: 0.5rem 1rem !important; font-size: 0.9rem !important; }
    .feature-icon { font-size: 2.5rem; }
    .home-background { padding: 2rem 1rem; }
}

/* ════ ANIMATIONS SUBTILES ════ */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

.stSpinner > div {
    border-color: var(--st-secondary) !important;
    border-right-color: transparent !important;
}

/* ════ SUCCESS/ERROR STATES ════ */
.stSuccess {
    background-color: rgba(9, 171, 59, 0.1) !important;
    border-left: 4px solid var(--st-success) !important;
}

.stError {
    background-color: rgba(255, 75, 75, 0.1) !important;
    border-left: 4px solid var(--st-error) !important;
}

.stWarning {
    background-color: rgba(255, 164, 33, 0.1) !important;
    border-left: 4px solid var(--st-warning) !important;
}

.stInfo {
    background-color: rgba(0, 104, 201, 0.1) !important;
    border-left: 4px solid var(--st-info) !important;
}
</style>
""", unsafe_allow_html=True)

if st.session_state.language == "ar":
    st.markdown("""
    <style>
    body, .stApp, [class*="css"] { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# ── Header navigation ────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    if st.session_state.page != "accueil":
        if st.button("← " + _("Accueil", "Home", "الرئيسية", "ⴰⵙⵏⵓⴱⴳ"), key="nav_home"):
            st.session_state.page = "accueil"
            st.rerun()
with col2:
    st.markdown("<h1 style='text-align:center;margin:0;'>🌐 MERCREDI</h1>", unsafe_allow_html=True)
with col3:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🇫🇷", key="lang_fr", disabled=st.session_state.language=="fr", width="stretch"):
            st.session_state.language = "fr"; st.rerun()
    with c2:
        if st.button("🇬🇧", key="lang_en", disabled=st.session_state.language=="en", width="stretch"):
            st.session_state.language = "en"; st.rerun()
    with c3:
        if st.button("🇸🇦", key="lang_ar", disabled=st.session_state.language=="ar", width="stretch"):
            st.session_state.language = "ar"; st.rerun()
    with c4:
        if st.button("ⵣ", key="lang_ber", disabled=st.session_state.language=="ber", width="stretch"):
            st.session_state.language = "ber"; st.rerun()

st.markdown("<hr style='margin:1rem 0;border-color:var(--border-color);'>", unsafe_allow_html=True)

# ── Validation clé Groq ──────────────────────────────────────────────
def validate_groq_key(key: str) -> bool:
    try:
        from groq import Groq
        client = Groq(api_key=key)
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5)
        return True
    except Exception:
        return False

# ══════════════════════════════════════════════════════════════════════
# PAGE ACCUEIL
# ══════════════════════════════════════════════════════════════════════
if st.session_state.page == "accueil":
    welcome = _("Votre assistant de traduction intelligent basé sur l'IA",
                "Your intelligent AI-powered translation assistant",
                "مساعد الترجمة الذكي الخاص بك",
                "ⴰⵎⴰⵡⴰⵍ ⵏⵏⴽ ⴰⵎⴰⵙⵙⴰⵏ ⵏ ⵜⵙⵓⵖⵍⵜ")

    st.markdown(f"""
    <div class="home-background">
        <div style='text-align:center;padding:2rem 0;'>
            <p style='font-size:1.4rem;color:var(--text-primary);max-width:800px;margin:0 auto;font-weight:500;'>
                {welcome}<br><br>
                <span style='color:var(--st-secondary);font-weight:700;font-size:1.2rem;'>
                    Llama 3.3 · Whisper · OCR.space
                </span>
            </p>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3>{_("Traduction Multiformat","Multi-format Translation","ترجمة متعددة التنسيقات","ⵜⴰⵙⵓⵖⵍⵜ ⵜⴰⵎⴳⴳⴰⵔⵓⵜ")}</h3>
            <p>{_("Texte · Documents · Audio · Images","Text · Documents · Audio · Images","نص · مستندات · صوت · صور","ⴰⴹⵕⵉⵚ · ⵉⵙⵏⵟⴰⵟⵏ · ⴰⵎⴻⴷⵢⴰ · ⵜⵉⵡⵍⴰⴼⵉⵏ")}</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>{_("Chatbot Intelligent","Intelligent Chatbot","الدردشة الذكية","ⴰⵎⵙⴰⵡⴰⵍ ⴰⵎⴰⵙⵙⴰⵏ")}</h3>
            <p>{_("Assistant pédagogique multidomaines","Multidisciplinary assistant","مساعد تعليمي متعدد","ⴰⵎⴰⵡⴰⵍ ⴰⵙⵍⵎⴰⴷ ⴰⵎⴳⴳⴰⵔⵓ")}</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="feature-card">
            <div class="feature-icon">🌍</div>
            <h3>{_("10 Langues","10 Languages","10 لغات","10 ⵜⵓⵜⵍⴰⵢⵉⵏ")}</h3>
            <p>{_("Ar·Fr·En·De·Es·It·Ja·Zh·Ru·Tr","Ar·Fr·En·De·Es·It·Ja·Zh·Ru·Tr","عر·فر·إن·أل·إس·إي·ي·ص·ر·ت","ⵄⵔ·ⴼⵔ·ⵉⵏ·ⴷ·ⵉⵙ·ⵉⵜ·ⵊⴰ·ⵛⵀ·ⵔⵓ·ⵜⵔ")}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""<div class="card">
        <h2 style='margin-top:0;'>{_("Comment ça marche ?","How does it work?","كيف يعمل؟","ⵉⵙⵡⵓⵔⵉ ⴰⴽⴽⴰ?")}</h2>
        <div class="step-box"><b>{_("Étape 1","Step 1","الخطوة 1","ⴰⵙⵡⵉⵔ 1")}</b> — {_("Créez votre compte Groq gratuit","Create your free Groq account","انشئ حساب Groq المجاني","ⵙⵏⴼⵍⵓⵍ ⴰⵎⵉⴹⴰⵏ ⵏ Groq")}<br>
        <a href="https://console.groq.com" target="_blank" style="color:var(--st-secondary);font-weight:600;text-decoration:none;">https://console.groq.com</a></div>
        <div class="step-box"><b>{_("Étape 2","Step 2","الخطوة 2","ⴰⵙⵡⵉⵔ 2")}</b> — {_("Allez dans","Go to","اذهب الى","ⴷⴷⵓ ⵖⵔ")} <b>API Keys</b> → <b>Create API Key</b></div>
        <div class="step-box"><b>{_("Étape 3","Step 3","الخطوة 3","ⴰⵙⵡⵉⵔ 3")}</b> — {_("Copiez votre clé","Copy your key","انسخ مفتاحك","ⵙⵏⵖⵍ ⵜⴰⵙⴰⵔⵓⵜ ⵏⵏⴽ")} <code>gsk_...</code> {_("et collez-la ci-dessous","and paste it below","والصقه ادناه","ⵙⵏⴼⵍ ⴰⵜ ⴷⴷⴰⵡ")}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.groq_api_key:
        key_input = st.text_input(
            _("Votre clé Groq API", "Your Groq API Key", "مفتاح Groq API", "ⵜⴰⵙⴰⵔⵓⵜ ⵏ Groq API"),
            placeholder="gsk_...", type="password",
            help=_("Gratuit · 100,000 tokens/jour", "Free · 100,000 tokens/day", "مجاني · 100,000 رمز/يوم", "ⴱⴰⴱⴰⵙ · 100,000 ⵜⵓⴽⵏⵉⵏ/ⴰⵙⵙ"))

        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if st.button(_("Valider et commencer", "Validate and start", "تحقق وابدأ", "ⵙⴻⵏⵇⴷ ⵙⴻⵏⵜⵉ"), key="btn_validate", width="stretch"):
                if not key_input.strip():
                    st.error(_("Veuillez entrer votre clé API.", "Please enter your API key.", "الرجاء ادخال مفتاح API.", "ⵓⵔ ⵜⵛⴰⵔⴰⴷ ⵜⴰⵙⴰⵔⵓⵜ."))
                elif not key_input.strip().startswith("gsk_"):
                    st.error(_("Clé invalide — doit commencer par gsk_", "Invalid key — must start with gsk_", "مفتاح غير صالح - يجب ان يبدأ بـ gsk_", "ⵜⴰⵙⴰⵔⵓⵜ ⵓⵔ ⵜⴻⴼⵄⴻⵍ — ⵜⴻⴱⴷⵓ ⵙ gsk_"))
                else:
                    with st.spinner(_("Validation en cours...", "Validating...", "جاري التحقق...", "ⴰⵙⴻⵏⵇⴷ...")):
                        if validate_groq_key(key_input.strip()):
                            st.session_state.groq_api_key = key_input.strip()
                            st.success(_("Clé validée !", "Key validated!", "تم التحقق!", "ⵜⴻⵜⵡⴰⵙⴻⵏⵇⴷ!"))
                            st.rerun()
                        else:
                            st.error(_("Clé invalide ou expirée.", "Invalid or expired key.", "مفتاح غير صالح.", "ⵜⴰⵙⴰⵔⵓⵜ ⵓⵔ ⵜⴻⴼⵄⴻⵍ."))
    else:
        st.markdown(f"""
        <div style='text-align:center;padding:2rem;background:linear-gradient(135deg, rgba(9, 171, 59, 0.1) 0%, rgba(33, 197, 93, 0.1) 100%);
        border-radius:12px;margin:2rem 0;box-shadow:var(--shadow-md);border:2px solid var(--st-success);'>
            <p style='font-size:1.2rem;margin-bottom:1.5rem;color:var(--st-success-dark);font-weight:600;'>
                ✅ {_("Clé API valide détectée !","Valid API key detected!","تم اكتشاف مفتاح API صالح!","ⵜⴻⵜⵡⴰⵙⴻⵏⵇⴷ ⵜⴰⵙⴰⵔⵓⵜ!")}
            </p>
        </div>""", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if st.button(_("Accéder à l'application", "Access the app", "الوصول الى التطبيق", "ⴷⴷⵓ ⵖⵔ ⵓⵙⵏⴼⴰⵍ"), key="btn_start", width="stretch"):
                st.session_state.page = "main"; st.rerun()

    st.markdown(
    '<div class="footer-home">© 2026 Amina. All rights reserved.</div>',
    unsafe_allow_html=True
)
    
    st.stop()

# ══════════════════════════════════════════════════════════════════════
# PAGE PRINCIPALE
# ══════════════════════════════════════════════════════════════════════
if not st.session_state.groq_api_key:
    st.session_state.page = "accueil"; st.rerun()

os.environ["GROQ_API_KEY"] = st.session_state.groq_api_key

from text_translator import TextTranslator
from document_translator import DocumentTranslator
from audio_translator import AudioTranslator
from image_translator import ImageTranslator
from language_detector import LanguageDetector
from chatbot import Chatbot

@st.cache_resource
def load_modules():
    return {
        "text":     TextTranslator(),
        "document": DocumentTranslator(),
        "audio":    AudioTranslator(),
        "image":    ImageTranslator(),
        "detector": LanguageDetector(),
        "chatbot":  Chatbot(),
    }

modules = load_modules()

LANGUAGES = {
    "🇸🇦 العربية": "ar", "🇫🇷 Français": "fr", "🇬🇧 English": "en",
    "🇩🇪 Deutsch": "de", "🇪🇸 Español": "es", "🇮🇹 Italiano": "it",
    "🇯🇵 日本語": "ja", "🇨🇳 中文": "zh", "🇷🇺 Русский": "ru", "🇹🇷 Türkçe": "tr",
}

if "history" not in st.session_state:
    st.session_state.history = []

TYPE_LABELS = {"📝 Texte": "Texte", "📄 Document": "Document", "🎙️ Audio": "Audio", "🖼️ Image": "Image"}

def add_history(type_: str, src_lang: str, tgt_lang: str, original: str, translated: str):
    st.session_state.history.insert(0, {
        "type": type_, "type_clean": TYPE_LABELS.get(type_, type_),
        "src_lang": src_lang, "tgt_lang": tgt_lang,
        "original": original[:100] + "..." if len(original) > 100 else original,
        "translated": translated[:100] + "..." if len(translated) > 100 else translated,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    })
    st.session_state.history = st.session_state.history[:40]

def retry_call(fn, status_placeholder, *args, **kwargs):
    retries = 3
    for attempt in range(retries):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            err = str(e)
            is_rate_limit = "429" in err
            is_timeout    = "timeout" in err.lower() or "timed out" in err.lower()
            if (is_rate_limit or is_timeout) and attempt < retries - 1:
                wait = 5 if is_timeout else 3
                reason = _("Timeout réseau","Network timeout","انتهت مهلة الشبكة","ⵜⴰⵖⵓⵍⵜ ⵏ ⵓⵣⴷⴷⵓⵢ") if is_timeout else _("Limite Groq atteinte","Groq limit reached","تم الوصول الى حد Groq","ⵜⴰⵖⵓⵍⵜ ⵏ Groq")
                status_placeholder.warning(f"⏳ {reason} — {_('nouvelle tentative dans','retrying in','اعادة بعد','ⴰⵢⴰⵔⴰⵢ ⴷⵉ')} {wait}s... ({attempt+1}/{retries})")
                time.sleep(wait)
                status_placeholder.empty()
            else:
                raise e

def tts_audio(text: str, lang: str = "fr"):
    try:
        from gtts import gTTS
        clean = re.sub(r'\*+', '', text)
        clean = re.sub(r'#+\s', '', clean)
        clean = re.sub(r'`+', '', clean)
        clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
        clean = re.sub(r'[-•]\s', '', clean)
        clean = re.sub(r'\n+', ' ', clean).strip()
        chunks = []
        while len(clean) > 500:
            split = clean[:500].rfind(' ')
            if split == -1: split = 500
            chunks.append(clean[:split])
            clean = clean[split:].strip()
        if clean: chunks.append(clean)
        combined = io.BytesIO()
        for chunk in chunks:
            if not chunk.strip(): continue
            tts = gTTS(text=chunk, lang=lang, slow=False)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            combined.write(buf.read())
        combined.seek(0)
        st.audio(combined, format="audio/mp3")
    except Exception as e:
        st.warning(f"{_('Lecture audio non disponible','Audio unavailable','الصوت غير متوفر','ⵓⵔ ⵜⴻⵍⵍⵉ ⵜⵖⵓⵔⵉ')} : {e}")

def export_history_txt():
    lines = [
        f"MERCREDI - {_('Historique des traductions','Translation History','سجل الترجمات','ⴰⵎⵣⵔⵓⵢ ⵏ ⵜⵙⵓⵖⵍⵉⵏ')}",
        f"{_('Exporté le','Exported on','تم التصدير في','ⵜⴻⵜⵜⵡⴰⵙⵓⵖⴻⵍ ⴳ')} {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "=" * 50, ""
    ]
    for i, item in enumerate(st.session_state.history, 1):
        lines.append(f"#{i} [{item['date']}] {item.get('type_clean', '')} · {item['src_lang']} -> {item['tgt_lang']}")
        lines.append(f"{_('Original','Original','الأصلي','ⴰⵙⴰⴷⵙ')} : {item['original']}")
        lines.append(f"{_('Traduit','Translated','المترجم','ⵉⵜⵜⵡⴰⵙⵓⵖⵍ')} : {item['translated']}")
        lines.append("-" * 50)
    return "\n".join(lines).encode("utf-8")

# ── Supabase feedback ────────────────────────────────────────────────
def init_supabase():
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
        if url and key:
            return create_client(url, key)
    except Exception:
        pass
    return None

def save_feedback(feedback_data, supabase):
    if not supabase:
        return False
    try:
        def clean_str(s):
            return str(s).encode('utf-8', errors='replace').decode('utf-8') if s else ''
        data = {
            'type': clean_str(feedback_data.get('type', '')),
            'score': feedback_data.get('score'),
            'text': clean_str(feedback_data.get('text', '')),
            'user_name': clean_str(feedback_data.get('user_name', 'Anonyme')),
            'timestamp': datetime.now().isoformat()
        }
        supabase.table('feedbacks').insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Erreur sauvegarde : {e}")
        return False

def load_feedbacks(supabase):
    if not supabase:
        return []
    try:
        response = supabase.table('feedbacks').select('*').order('timestamp', desc=True).execute()
        return response.data
    except Exception:
        return []

# ── Header principal ─────────────────────────────────────────────────
col_l, col_r = st.columns([5, 1])
with col_r:
    if st.button("🔑 " + _("Changer de clé", "Change key", "تغيير المفتاح", "ⴱⴻⴷⴷⴻⵍ ⵜⴰⵙⴰⵔⵓⵜ"), key="btn_logout", width="stretch"):
        st.session_state.groq_api_key = ""
        st.session_state.page = "accueil"
        st.rerun()

# ── Tabs ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📝 " + _("Texte", "Text", "نص", "ⴰⴹⵕⵉⵚ"),
    "📄 " + _("Document", "Document", "مستند", "ⴰⵙⵏⵟⴰⵟ"),
    "🎙️ " + _("Audio", "Audio", "صوت", "ⴰⵎⴻⴷⵢⴰ"),
    "🖼️ " + _("Image", "Image", "صورة", "ⵜⴰⵡⵍⴰⴼⵜ"),
    "💬 " + _("Chat", "Chat", "محادثة", "ⴰⵎⵙⴰⵡⴰⵍ"),
    "📋 " + _("Historique", "History", "السجل", "ⴰⵎⵣⵔⵓⵢ"),
    "💡 " + _("Feedback", "Feedback", "تقييم", "ⴰⵙⵖⵔⵓ")
])

# ════════ ONGLET 1 — Texte ════════
with tab1:
    st.subheader(_("Traduction de texte", "Text translation", "ترجمة النص", "ⵜⴰⵙⵓⵖⵍⵜ ⵏ ⵓⴹⵕⵉⵚ"))
    st.caption("⚡ Groq Llama 3.3 70B")
    col1, col2 = st.columns(2)
    with col1:
        src_label = st.selectbox(_("Langue source","Source language","لغة المصدر","ⵜⵓⵜⵍⴰⵢⵜ ⵜⴰⵏⵙⴰⵡⵜ"),
            ["🔍 " + _("Détection auto","Auto detect","كشف تلقائي","ⴰⴽⵓⴷ ⴰⵡⵓⵔⵎⴰⵏ")] + list(LANGUAGES.keys()), key="txt_src")
    with col2:
        tgt_label = st.selectbox(_("Langue cible","Target language","اللغة الهدف","ⵜⵓⵜⵍⴰⵢⵜ ⵜⴰⵎⴰⴹⵍⴰⵏⵜ"),
            list(LANGUAGES.keys()), index=1, key="txt_tgt")
    col_left, col_right = st.columns(2)
    with col_left:
        # FIX 1: replaced "" with a real label + label_visibility="collapsed"
        text_input = st.text_area(
            _("Texte source", "Source text", "النص المصدر", "ⴰⴹⵕⵉⵚ ⴰⵏⵙⴰⵡ"),
            height=200,
            key="txt_input",
            placeholder=_("Entrez votre texte ici...","Enter your text here...","أدخل نصك هنا...","ⵙⵙⴽⴻⵎ ⴰⴹⵕⵉⵚ ⵏⵏⴽ ⴷⴰ..."),
            label_visibility="collapsed"
        )
        st.caption(f"✏️ {len(text_input)} " + _("caractères","characters","حرف","ⵉⵙⴽⴽⵉⵍⵏ"))
    with col_right:
        result_placeholder = st.empty()
        result_placeholder.markdown(f'<div class="result-box" style="color:var(--text-muted);min-height:200px">{_("La traduction apparaîtra ici...","Translation will appear here...","ستظهر الترجمة هنا...","ⴰⵜⵜⵢⴰⴼ ⵓⵙⵓⵖⵍ ⴷⴰ...")}</div>', unsafe_allow_html=True)
    if st.button("🔄 " + _("Traduire","Translate","ترجمة","ⵙⵓⵖⵍ"), key="btn_txt", width="stretch"):
        if not text_input.strip():
            st.warning(_("Veuillez entrer du texte.","Please enter some text.","الرجاء ادخال نص.","ⵓⵔ ⵜⵛⴰⵔⴰⴷ ⴰⴹⵕⵉⵚ."))
        else:
            status = st.empty()
            with st.spinner(_("Traduction en cours...","Translating...","جاري الترجمة...","ⴰⵙⵓⵖⵍ ⴷⴳ ⵓⴱⵔⵉⴷ...")):
                try:
                    auto_label = "🔍 " + _("Détection auto","Auto detect","كشف تلقائي","ⴰⴽⵓⴷ ⴰⵡⵓⵔⵎⴰⵏ")
                    if src_label == auto_label:
                        src_lang = modules["detector"].detect(text_input)
                        st.markdown(f'<div class="detected-lang-box">🌐 {_("Langue détectée","Detected language","اللغة المكتشفة","ⵜⵓⵜⵍⴰⵢⵜ ⵜⴻⵜⵜⵡⴰⴽⵛⵎⴻⵜ")} : <b>{src_lang}</b></div>', unsafe_allow_html=True)
                    else:
                        src_lang = LANGUAGES[src_label]
                    tgt_lang = LANGUAGES[tgt_label]
                    result = retry_call(modules["text"].translate, status, text_input, src_lang, tgt_lang)
                    status.empty()
                    result_placeholder.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                    tts_audio(result, LANGUAGES[tgt_label])
                    add_history("📝 Texte", src_lang, tgt_lang, text_input, result)
                except Exception as e:
                    status.empty()
                    st.error(_("Une erreur est survenue lors de la traduction.","An error occurred during translation.","حدث خطأ أثناء الترجمة.","ⵉⵍⵍⴰ ⵓⵣⴳⴰⵍ ⴷⵉ ⵜⵙⵓⵖⵍⵜ."))

# ════════ ONGLET 2 — Document ════════
with tab2:
    st.subheader(_("Traduction de document","Document translation","ترجمة المستند","ⵜⴰⵙⵓⵖⵍⵜ ⵏ ⵓⵙⵏⵟⴰⵟ"))
    st.caption("📄 .txt · .docx · .pdf · .pptx")
    col1, col2 = st.columns(2)
    with col1:
        doc_src = st.selectbox(_("Langue source","Source language","لغة المصدر","ⵜⵓⵜⵍⴰⵢⵜ ⵜⴰⵏⵙⴰⵡⵜ"),
            ["🔍 " + _("Détection auto","Auto detect","كشف تلقائي","ⴰⴽⵓⴷ ⴰⵡⵓⵔⵎⴰⵏ")] + list(LANGUAGES.keys()), key="doc_src")
    with col2:
        doc_tgt = st.selectbox(_("Langue cible","Target language","اللغة الهدف","ⵜⵓⵜⵍⴰⵢⵜ ⵜⴰⵎⴰⴹⵍⴰⵏⵜ"),
            list(LANGUAGES.keys()), index=1, key="doc_tgt")
    uploaded_doc = st.file_uploader(_("Choisir un document","Choose a document","اختر مستند","ⴼⵔⵏ ⴰⵙⵏⵟⴰⵟ"),
        type=["txt","docx","pdf","pptx"], key="doc_file")
    if st.button("📄 " + _("Traduire","Translate","ترجمة","ⵙⵓⵖⵍ"), key="btn_doc", width="stretch"):
        if uploaded_doc is None:
            st.warning(_("Veuillez uploader un document.","Please upload a document.","الرجاء تحميل مستند.","ⵓⵔ ⵜⵛⴰⵔⴰⴷ ⴰⵙⵏⵟⴰⵟ."))
        else:
            status = st.empty()
            with st.spinner(_("Traduction en cours...","Translating...","جاري الترجمة...","ⴰⵙⵓⵖⵍ ⴷⴳ ⵓⴱⵔⵉⴷ...")):
                try:
                    auto_label = "🔍 " + _("Détection auto","Auto detect","كشف تلقائي","ⴰⴽⵓⴷ ⴰⵡⵓⵔⵎⴰⵏ")
                    src = "fr" if doc_src == auto_label else LANGUAGES[doc_src]
                    tgt = LANGUAGES[doc_tgt]
                    content, ext, mime = retry_call(modules["document"].translate, status, uploaded_doc, tgt, src)
                    status.empty()
                    st.success(_("Traduction terminée !","Translation complete!","اكتملت الترجمة!","ⵜⴻⴼⵓⴽ ⵜⵙⵓⵖⵍⵜ!"))
                    st.download_button("📥 " + _("Télécharger","Download","تحميل","ⴰⴳⵎⴰⵜⵓⵔⵉⵏ"),
                        data=content, file_name=f"traduction{ext}", mime=mime, width="stretch")
                    if ext == ".txt":
                        decoded = content.decode("utf-8")
                        st.markdown(f'<div class="result-box">{decoded[:1000]}</div>', unsafe_allow_html=True)
                    else:
                        st.info(f"📄 {ext} {_('prêt avec mise en forme conservée','ready with preserved formatting','جاهز مع الحفاظ على التنسيق','ⵢⴻⵍⵍⴰ ⵙ ⵓⵃⵟⵟⵓ ⵏ ⵓⵎⵙⴰⵙⵙ')} !")
                    add_history("📄 Document", src, tgt, uploaded_doc.name, f"traduction{ext}")
                except Exception as e:
                    status.empty()
                    st.error(_("Une erreur est survenue lors de la traduction du document.","An error occurred during document translation.","حدث خطأ أثناء ترجمة المستند.","ⵉⵍⵍⴰ ⵓⵣⴳⴰⵍ ⴷⵉ ⵜⵙⵓⵖⵍⵜ ⵏ ⵓⵙⵏⵟⴰⵟ."))

# ════════ ONGLET 3 — Audio ════════
with tab3:
    st.subheader(_("Transcription & traduction audio","Audio transcription & translation","نسخ وترجمة الصوت","ⴰⵙⵙⵓⵖⵍ ⴷ ⵜⵙⵓⵖⵍⵜ ⵏ ⵓⵎⴻⴷⵢⴰ"))
    st.caption("🎤 Whisper Large v3 Turbo · Groq")

    audio_tgt = st.selectbox(_("Langue cible","Target language","اللغة الهدف","ⵜⵓⵜⵍⴰⵢⵜ ⵜⴰⵎⴰⴹⵍⴰⵏⵜ"),
        list(LANGUAGES.keys()), index=1, key="audio_tgt")

    # ── Deux options : fichier OU micro ──────────────────────────────
    audio_sub1, audio_sub2 = st.tabs([
        "📂 " + _("Fichier audio","Audio file","ملف صوتي","ⴰⵎⴻⴷⵢⴰ ⵏ ⵓⴼⴰⵢⵍ"),
        "🎙️ " + _("Enregistrer","Record","تسجيل","ⴰⵣⵏ ⵓⵙⴻⵏⴼⴰⵍ")
    ])

    def _process_audio(audio_source, tgt_lang_key):
        """Traite une source audio (fichier uploadé ou BytesIO du micro) et affiche les résultats."""
        status = st.empty()
        with st.spinner(_("Transcription en cours...","Transcribing...","جاري النسخ...","ⴰⵙⵙⵓⵖⵍ ⴷⴳ ⵓⴱⵔⵉⴷ...")):
            try:
                result = retry_call(modules["audio"].translate, status, audio_source, tgt_lang_key)
                status.empty()
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**" + _("Transcription","Transcription","النسخ","ⴰⵙⵙⵓⵖⵍ") + " :**")
                    st.markdown(f'<div class="result-box">{result["transcription"]}</div>', unsafe_allow_html=True)
                with col_b:
                    st.markdown("**" + _("Traduction","Translation","الترجمة","ⵜⴰⵙⵓⵖⵍⵜ") + " :**")
                    st.markdown(f'<div class="result-box">{result["translated_text"]}</div>', unsafe_allow_html=True)
                st.markdown("**🔊 " + _("Écouter","Listen","استمع","ⵙⵙⵍ") + "**")
                tts_audio(result["translated_text"], LANGUAGES[audio_tgt])
                add_history("🎙️ Audio", "auto", tgt_lang_key, result["transcription"], result["translated_text"])
            except Exception as e:
                status.empty()
                st.error(_("Une erreur est survenue lors de la transcription audio.","An error occurred during audio transcription.","حدث خطأ أثناء النسخ الصوتي.","ⵉⵍⵍⴰ ⵓⵣⴳⴰⵍ ⴷⵉ ⵓⵙⵙⵓⵖⵍ."))

    with audio_sub1:
        uploaded_audio = st.file_uploader(
            _("Choisir un fichier audio","Choose an audio file","اختر ملف صوت","ⴼⵔⵏ ⴰⵎⴻⴷⵢⴰ"),
            type=["mp3","wav","ogg","flac","m4a"], key="audio_file"
        )
        if st.button("🎙️ " + _("Transcrire & Traduire","Transcribe & Translate","نسخ وترجمة","ⵙⵙⵓⵖⵍ ⴷ ⵙⵓⵖⵍ"), key="btn_audio", width="stretch"):
            if uploaded_audio is None:
                st.warning(_("Veuillez uploader un fichier audio.","Please upload an audio file.","الرجاء تحميل ملف صوت.","ⵓⵔ ⵜⵛⴰⵔⴰⴷ ⴰⵎⴻⴷⵢⴰ."))
            else:
                _process_audio(uploaded_audio, LANGUAGES[audio_tgt])

    with audio_sub2:
        st.info("🎙️ " + _("Cliquez sur le micro pour démarrer, puis à nouveau pour arrêter.",
                            "Click the mic to start recording, then again to stop.",
                            "انقر على الميكروفون للبدء، ثم مرة أخرى للإيقاف.",
                            "ⵙⵏⵖⵍ ⴰⵎⵉⴽⵔⵓ ⴰⴷ ⵜⵙⵏⵜⵉⴷ, ⵓⵍⴰ ⵜⵉⵙⵙ ⵙⵏⴰⵜ ⴰⴷ ⵜⵓⴼⵓⴷ."))
        recorded_audio = st.audio_input(
            _("🎙️ Enregistrer ma voix", "🎙️ Record my voice", "🎙️ تسجيل صوتي", "🎙️ ⴰⵣⵏ ⵓⵎⵙⵙⵍⵖⵓ"),
            key="audio_mic"
        )
        if recorded_audio is not None:
            st.success("✅ " + _("Enregistrement prêt ! Cliquez sur Transcrire & Traduire.",
                                  "Recording ready! Click Transcribe & Translate.",
                                  "التسجيل جاهز! انقر على نسخ وترجمة.",
                                  "ⴰⵣⵏ ⵢⴻⵍⵍⴰ! ⵙⵙⵓⵖⵍ ⴷ ⵙⵓⵖⵍ."))
            if st.button("🔄 " + _("Transcrire & Traduire","Transcribe & Translate","نسخ وترجمة","ⵙⵙⵓⵖⵍ ⴷ ⵙⵓⵖⵍ"), key="btn_audio_mic", width="stretch"):
                buf = io.BytesIO(recorded_audio.getvalue())
                buf.name = "recording.wav"
                buf.seek(0)
                _process_audio(buf, LANGUAGES[audio_tgt])

# ════════ ONGLET 4 — Image ════════
with tab4:
    st.subheader(_("OCR & traduction d'image","OCR & image translation","OCR وترجمة الصور","OCR ⴷ ⵜⵙⵓⵖⵍⵜ ⵏ ⵜⵡⵍⴰⴼⵜ"))
    st.caption("🖼️ OCR.space API · Groq")

    img_tgt = st.selectbox(_("Langue cible","Target language","اللغة الهدف","ⵜⵓⵜⵍⴰⵢⵜ ⵜⴰⵎⴰⴹⵍⴰⵏⵜ"),
        list(LANGUAGES.keys()), index=1, key="img_tgt")

    def _process_image(img_source, tgt_lang_key):
        """Traite une source image (fichier uploadé ou photo caméra) et affiche les résultats."""
        if hasattr(img_source, "seek"):
            img_source.seek(0)
        status = st.empty()
        with st.spinner(_("OCR en cours...","OCR in progress...","جاري التعرف على النص...","OCR ⴷⴳ ⵓⴱⵔⵉⴷ...")):
            try:
                result = retry_call(modules["image"].translate, status, img_source, tgt_lang_key)
                status.empty()
                if not result.get("extracted_text"):
                    st.warning(_("Aucun texte détecté dans l'image. Essayez une image plus nette ou avec plus de contraste.",
                                  "No text detected in the image. Try a clearer image with more contrast.",
                                  "لم يتم اكتشاف نص في الصورة. جرب صورة أوضح.",
                                  "ⵓⵔ ⵉⵜⵜⵡⴰⴼ ⵓⴹⵕⵉⵚ. ⵙⵙⴽⵎ ⵜⴰⵡⵍⴰⴼⵜ ⵜⵓⴼⵔⴰⵔⵜ."))
                    return
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**" + _("Texte extrait","Extracted text","النص المستخرج","ⴰⴹⵕⵉⵚ ⵢⴻⵜⵜⵡⴰⴼⵙⴻⵔ") + " :**")
                    st.markdown(f'<div class="result-box">{result["extracted_text"]}</div>', unsafe_allow_html=True)
                with col_b:
                    st.markdown("**" + _("Traduction","Translation","الترجمة","ⵜⴰⵙⵓⵖⵍⵜ") + " :**")
                    st.markdown(f'<div class="result-box">{result["translated_text"]}</div>', unsafe_allow_html=True)
                st.markdown("**🔊 " + _("Écouter","Listen","استمع","ⵙⵙⵍ") + "**")
                tts_audio(result["translated_text"], LANGUAGES[img_tgt])
                add_history("🖼️ Image", "auto", tgt_lang_key, result["extracted_text"], result["translated_text"])
            except Exception as e:
                status.empty()
                st.error(_("Une erreur est survenue lors de l'extraction de texte.","An error occurred during text extraction.","حدث خطأ أثناء استخراج النص.","ⵉⵍⵍⴰ ⵓⵣⴳⴰⵍ ⴷⵉ ⵓⴼⵙⴰⵔ ⵏ ⵓⴹⵕⵉⵚ."))
                with st.expander("🔍 " + _("Détail de l'erreur","Error detail","تفاصيل الخطأ","ⴰⵎⵢⴰⵡⴰⵙ ⵏ ⵓⵣⴳⴰⵍ")):
                    st.exception(e)

    uploaded_img = st.file_uploader(
        _("Choisir une image","Choose an image","اختر صورة","ⴼⵔⵏ ⵜⴰⵡⵍⴰⴼⵜ"),
        type=["png","jpg","jpeg","bmp","tiff"], key="img_file"
    )
    if uploaded_img:
        st.image(uploaded_img, width=400)
    if st.button("🖼️ " + _("Extraire & Traduire","Extract & Translate","استخراج وترجمة","ⴼⵙⵙⵉ ⴷ ⵙⵓⵖⵍ"), key="btn_img", width="stretch"):
        if uploaded_img is None:
            st.warning(_("Veuillez uploader une image.","Please upload an image.","الرجاء تحميل صورة.","ⵓⵔ ⵜⵛⴰⵔⴰⴷ ⵜⴰⵡⵍⴰⴼⵜ."))
        else:
            _process_image(uploaded_img, LANGUAGES[img_tgt])

# ════════ ONGLET 5 — Chat ════════
with tab5:
    st.subheader(_("Chatbot IA — Llama 3.3 70B + Vision","AI Chatbot — Llama 3.3 70B + Vision","الدردشة الذكية","ⴰⵎⵙⴰⵡⴰⵍ ⴰⵎⴰⵙⵙⴰⵏ"))
    st.caption("🤖 Groq · " + _("Multidomaines · Images · Documents","Multidomain · Images · Documents","متعدد التخصصات","ⴰⵎⴳⴳⴰⵔⵓ ⵏ ⵉⴳⵔⴰⵏ"))
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for i, msg in enumerate(st.session_state.chat_history):
        with st.chat_message(msg["role"]):
            if msg.get("has_image"): st.caption("🖼️ " + _("Image envoyée","Image sent","تم ارسال صورة","ⵜⴻⵜⵜⵡⴰⵣⵏ ⵜⴰⵡⵍⴰⴼⵜ"))
            if msg.get("has_doc"): st.caption(f"📄 {msg.get('doc_name','')}")
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                if st.button("🔊 " + _("Écouter","Listen","استمع","ⵙⵙⵍ"), key=f"tts_chat_{i}"):
                    tts_audio(msg["content"], "fr")
    col_att1, col_att2 = st.columns(2)
    with col_att1:
        chat_img = st.file_uploader("🖼️ " + _("Joindre une image","Attach an image","ارفاق صورة","ⵙⵎⴰⵜⵜⵉ ⵜⴰⵡⵍⴰⴼⵜ"),
            type=["png","jpg","jpeg","bmp","tiff"], key="chat_img")
        if chat_img: st.image(chat_img, width=200)
    with col_att2:
        chat_doc = st.file_uploader("📄 " + _("Joindre un document","Attach a document","ارفاق مستند","ⵙⵎⴰⵜⵜⵉ ⴰⵙⵏⵟⴰⵟ"),
            type=["txt","pdf","docx","pptx"], key="chat_doc")
        if chat_doc: st.caption(f"✅ {chat_doc.name}")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        # FIX 2: replaced "" with a real label + label_visibility="collapsed"
        user_input = st.text_input(
            _("Message", "Message", "رسالة", "ⴰⵙⴻⵏⴼⴰⵍ"),
            key="chat_input",
            placeholder=_("Posez votre question...","Ask your question...","اطرح سؤالك...","ⵙⴰⵇⵙⴰ ⴰⵎⴻⵙⵜⵓⵔ ⵏⵏⴽ..."),
            label_visibility="collapsed"
        )
    with col_btn:
        send = st.button("➤", key="btn_send", width="stretch")
    if send and (user_input.strip() or chat_img or chat_doc):
        image_bytes = chat_img.read() if chat_img else None
        image_mime  = f"image/{chat_img.name.split('.')[-1].lower()}" if chat_img else "image/jpeg"
        doc_bytes   = chat_doc.read() if chat_doc else None
        doc_name    = chat_doc.name if chat_doc else None
        display_msg = user_input if user_input.strip() else (f"📄 {doc_name}" if chat_doc else "🖼️ Image")
        st.session_state.chat_history.append({"role":"user","content":display_msg,"has_image":bool(chat_img),"has_doc":bool(chat_doc),"doc_name":doc_name})
        status = st.empty()
        with st.spinner("🤖 MERCREDI " + _("réfléchit...","is thinking...","يفكر...","ⵉⵙⵎⴰⵙⴰⵢ...")):
            try:
                def on_retry(attempt, wait):
                    status.warning(f"⏳ {_('Limite atteinte, nouvelle tentative dans','Limit reached, retrying in','اعادة المحاولة بعد','ⴰⵢⴰⵔⴰⵢ ⴷⵉ')} {wait}s... ({attempt}/3)")
                response = modules["chatbot"].respond(user_input, image_bytes=image_bytes, image_mime=image_mime, doc_bytes=doc_bytes, doc_name=doc_name, on_retry=on_retry)
                status.empty()
                st.session_state.chat_history.append({"role":"assistant","content":response,"has_image":False,"has_doc":False})
            except Exception as e:
                status.empty()
                error_msg = _("Une erreur est survenue. Veuillez réessayer.","An error occurred. Please try again.","حدث خطأ. يرجى المحاولة مرة أخرى.","ⵉⵍⵍⴰ ⵓⵣⴳⴰⵍ. ⵄⴰⵡⴷ ⴰⵔⴰⵎ.")
                st.session_state.chat_history.append({"role":"assistant","content":f"❌ {error_msg}","has_image":False,"has_doc":False})
        st.rerun()
    if st.button("🗑️ " + _("Réinitialiser","Reset","اعادة ضبط","ⴰⵍⵙ"), key="btn_reset", width="stretch"):
        st.session_state.chat_history = []
        modules["chatbot"].reset_conversation()
        st.rerun()

# ════════ ONGLET 6 — Historique ════════
with tab6:
    st.subheader(_("Historique des traductions","Translation history","سجل الترجمات","ⴰⵎⵣⵔⵓⵢ ⵏ ⵜⵙⵓⵖⵍⵉⵏ"))
    if not st.session_state.history:
        st.info(_("Aucune traduction effectuée pour le moment.","No translations yet.","لا توجد ترجمات بعد.","ⵓⵔ ⵍⵍⵉⵏⵜ ⵜⵙⵓⵖⵍⵉⵏ ⵖⵉⵍⴰ."))
    else:
        col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
        with col_h2:
            st.download_button("📄 " + _("Exporter","Export","تصدير","ⴰⴳⵎⴰⵜⵓⵔⵉⵏ"),
                data=export_history_txt(), file_name="historique_mercredi.txt", mime="text/plain", width="stretch")
        with col_h3:
            if st.button("🗑️ " + _("Vider","Clear","مسح","ⵙⴼⴷ"), key="btn_clear_history", width="stretch"):
                st.session_state.history = []; st.rerun()
        for item in st.session_state.history:
            st.markdown(f"""
            <div class="history-item">
                <div class="history-meta">{item['type']} · {item['src_lang']} → {item['tgt_lang']} · {item['date']}</div>
                <div><b>{_('Original','Original','الأصلي','ⴰⵙⴰⴷⵙ')} :</b> {item['original']}</div>
                <div><b>{_('Traduit','Translated','المترجم','ⵉⵜⵜⵡⴰⵙⵓⵖⵍ')} :</b> {item['translated']}</div>
            </div>""", unsafe_allow_html=True)

# ════════ ONGLET 7 — Feedback ════════
with tab7:
    st.subheader("💡 " + _("Centre de feedback","Feedback Center","مركز التقييم","ⴰⴳⵔⴰⵡ ⵏ ⵓⵙⵖⵔⵓ"))
    supabase = init_supabase()

    FEEDBACK_TYPES = [
        ("app",      "🌐 " + _("Application globale","Overall app","التطبيق الكامل","ⵓⵙⵏⴼⴰⵍ")),
        ("text",     "📝 " + _("Traduction de texte","Text translation","ترجمة النص","ⵜⴰⵙⵓⵖⵍⵜ ⵏ ⵓⴹⵕⵉⵚ")),
        ("document", "📄 " + _("Traduction de document","Document translation","ترجمة المستند","ⵜⴰⵙⵓⵖⵍⵜ ⵏ ⵓⵙⵏⵟⴰⵟ")),
        ("audio",    "🎙️ " + _("Transcription audio","Audio transcription","نسخ الصوت","ⴰⵙⵙⵓⵖⵍ ⵏ ⵓⵎⴻⴷⵢⴰ")),
        ("image",    "🖼️ " + _("OCR & traduction d'image","OCR & image translation","OCR وترجمة الصور","OCR ⴷ ⵜⵙⵓⵖⵍⵜ ⵏ ⵜⵡⵍⴰⴼⵜ")),
        ("chat",     "💬 " + _("Chatbot IA","AI Chatbot","الدردشة الذكية","ⴰⵎⵙⴰⵡⴰⵍ ⴰⵎⴰⵙⵙⴰⵏ")),
    ]

    def translate_type_key(key):
        mapping = {k: v for k, v in FEEDBACK_TYPES}
        return mapping.get(key, key)

    if not supabase:
        st.warning(_("Le module feedback nécessite la configuration de Supabase dans secrets.toml",
                     "Feedback module requires Supabase configuration in secrets.toml",
                     "وحدة التقييم تتطلب تكوين Supabase",
                     "ⴰⵙⵖⵔⵓ ⵉⵙⵔⵙⴰ Supabase"))
    else:
        tab_new, tab_stats, tab_list = st.tabs([
            "✏️ " + _("Nouveau feedback","New feedback","تقييم جديد","ⴰⵙⵖⵔⵓ ⴰⵎⴰⵢⵏⵓ"),
            "📊 " + _("Statistiques","Statistics","الاحصائيات","ⵉⵙⵜⴰⵜⵉⵙⵜⵉⴽⵏ"),
            "📋 " + _("Liste des retours","Feedback list","قائمة التقييمات","ⵓⵎⵓⵖ ⵏ ⵉⵙⵖⵔⵉⵡⵏ")
        ])

        with tab_new:
            with st.container():
                st.markdown('<div class="feedback-card">', unsafe_allow_html=True)
                type_options = {label: key for key, label in FEEDBACK_TYPES}
                selected_label = st.radio(
                    _("Que souhaitez-vous évaluer ?","What do you want to rate?","ماذا تريد تقييمه؟","ⵎⴰ ⵜⵔⵉⴷ ⵙⵖⵔⵓ?"),
                    options=list(type_options.keys()),
                    horizontal=True,
                    key="feedback_category"
                )
                selected_key = type_options[selected_label]

                st.write(_("Votre évaluation :","Your rating:","تقييمك:","ⴰⵙⵖⵔⵓ ⵏⵏⴽ:"))
                cols = st.columns(5)
                emoji_score = {"😞": 0, "😕": 1, "😐": 2, "😊": 3, "😍": 4}
                for col, (emoji, score) in zip(cols, emoji_score.items()):
                    if col.button(emoji, key=f"fb_emoji_{score}"):
                        st.session_state["feedback_emoji"] = emoji
                        st.session_state["feedback_score"] = score
                if "feedback_emoji" in st.session_state:
                    st.success(f"{_('Sélectionné','Selected','المحدد','ⵉⵜⵜⵓⴼⵔⴰⵏ')} : {st.session_state['feedback_emoji']}")

                feedback_text = st.text_area(
                    _("Suggestions d'amélioration (optionnel)","Improvement suggestions (optional)","اقتراحات التحسين (اختياري)","ⵉⵎⵙⴳⵏⴰⵙⵏ (ⴰⵔ ⵉⵙⵔⴰ)"),
                    key="fb_comment"
                )

                user_name = st.text_input(
                    _("Votre nom (optionnel)","Your name (optional)","اسمك (اختياري)","ⵉⵙⵎⴽ (ⴰⵔ ⵉⵙⵔⴰ)"),
                    placeholder="Anonyme"
                )

                if st.button("📤 " + _("Envoyer","Send","ارسال","ⴰⵣⵏ"), width="stretch"):
                    if "feedback_score" not in st.session_state:
                        st.error(_("Veuillez sélectionner une évaluation.","Please select a rating.","الرجاء اختيار تقييم.","ⵓⵔ ⵜⵛⴰⵔⴰⴷ ⴰⵙⵖⵔⵓ."))
                    else:
                        data = {
                            'type': selected_key,
                            'score': st.session_state["feedback_score"],
                            'text': feedback_text or "",
                            'user_name': user_name or "Anonyme",
                            'timestamp': datetime.now().isoformat()
                        }
                        if save_feedback(data, supabase):
                            st.success(_("Merci pour votre retour !","Thank you for your feedback!","شكرا على تقييمك!","ⵜⴰⵏⵎⵉⵔⵜ!"))
                            st.balloons()
                            del st.session_state["feedback_emoji"]
                            del st.session_state["feedback_score"]
                st.markdown('</div>', unsafe_allow_html=True)

        with tab_stats:
            feedbacks = load_feedbacks(supabase)
            if feedbacks:
                for fb in feedbacks:
                    if isinstance(fb.get('score'), float):
                        fb['score'] = int(round(fb['score'] * 4))
                try:
                    import pandas as pd
                    import plotly.express as px
                    df = pd.DataFrame(feedbacks)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown('<div class="feedback-stats">', unsafe_allow_html=True)
                        st.metric(_("Total retours","Total feedback","اجمالي التقييمات","ⴰⴽⴽ ⵏ ⵉⵙⵖⵔⵉⵡⵏ"), len(df))
                        st.markdown('</div>', unsafe_allow_html=True)
                    with col2:
                        positive_count = len(df[df['score'] >= 3])
                        pct = positive_count / len(df) * 100
                        st.markdown('<div class="feedback-stats">', unsafe_allow_html=True)
                        st.metric(_("Retours positifs","Positive feedback","تقييمات ايجابية","ⵉⵙⵖⵔⵉⵡⵏ ⵉⴼⵓⵍⴽⵉⵏ"), f"{pct:.0f}%")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with col3:
                        st.markdown('<div class="feedback-stats">', unsafe_allow_html=True)
                        st.metric(_("Utilisateurs","Users","المستخدمون","ⵉⵙⵎⴷⴰⵏ"), df['user_name'].nunique())
                        st.markdown('</div>', unsafe_allow_html=True)

                    type_counts = df['type'].value_counts().reset_index()
                    type_counts.columns = ['type_key', 'count']
                    type_counts['type_label'] = type_counts['type_key'].apply(translate_type_key)
                    fig = px.pie(type_counts, values='count', names='type_label',
                                 title=_("Répartition par type","Distribution by type","التوزيع حسب النوع","ⴰⴱⵟⵟⵓ ⵙ ⵓⵏⴰⵡ"),
                                 hole=0.3)
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, width="stretch")

                    if 'timestamp' in df.columns:
                        df['date'] = pd.to_datetime(df['timestamp']).dt.date
                        daily = df.groupby('date').size().reset_index(name='count')
                        fig2 = px.line(daily, x='date', y='count',
                                       title=_("Évolution des retours","Feedback evolution","تطور التقييمات","ⴰⵏⴰⵡⴰⵢ ⵏ ⵉⵙⵖⵔⵉⵡⵏ"),
                                       markers=True, line_shape='linear')
                        fig2.update_traces(line_color='var(--st-secondary)')
                        st.plotly_chart(fig2, width="stretch")

                except ImportError:
                    st.info(_("Installez pandas et plotly pour les statistiques.","Install pandas and plotly for statistics.","قم بتثبيت pandas و plotly للاحصائيات.","ⵙⵙⵎⴷⵉ pandas ⴷ plotly."))
            else:
                st.info(_("Aucun feedback pour le moment.","No feedback yet.","لا يوجد تقييم بعد.","ⵓⵔ ⵍⵍⵉⵏ ⵉⵙⵖⵔⵉⵡⵏ ⵖⵉⵍⴰ."))

        with tab_list:
            feedbacks = load_feedbacks(supabase)
            if feedbacks:
                for fb in feedbacks:
                    if isinstance(fb.get('score'), float):
                        fb['score'] = int(round(fb['score'] * 4))
                st.markdown(f"**{len(feedbacks)}** " + _("retour(s)","feedback(s)","تقييم(ات)","ⵉⵙⵖⵔⵉⵡⵏ"))
                score_to_emoji = {4:"😍", 3:"😊", 2:"😐", 1:"😕", 0:"😞"}
                for fb in feedbacks[:20]:
                    score = fb.get('score', 2)
                    if score >= 3:
                        score_class = "feedback-score-high"
                    elif score >= 1:
                        score_class = "feedback-score-medium"
                    else:
                        score_class = "feedback-score-low"

                    type_display = translate_type_key(fb.get('type', 'app'))
                    emoji_display = score_to_emoji.get(score, "😐")

                    st.markdown(f"""
                    <div class="feedback-item {score_class}">
                        <div style="display:flex; justify-content:space-between;">
                            <span><b>{type_display}</b> · {fb.get('user_name', 'Anonyme')}</span>
                            <span style="color:var(--text-secondary);">{fb.get('timestamp', '')[:10]}</span>
                        </div>
                        <div style="margin: 0.5rem 0;">{fb.get('text', '')}</div>
                        <div style="font-size:1.2rem;">{emoji_display}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(_("Aucun feedback pour le moment.","No feedback yet.","لا يوجد تقييم بعد.","ⵓⵔ ⵍⵍⵉⵏ ⵉⵙⵖⵔⵉⵡⵏ ⵖⵉⵍⴰ."))