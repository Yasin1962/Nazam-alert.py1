import streamlit as st
import requests
from datetime import datetime
import math

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Noor Prayer Premium",
    page_icon="🕌",
    layout="wide"
)

# ---------------- PREMIUM COLORS ---------------- #
PRIMARY_GRADIENT = "linear-gradient(135deg, #0B1F1A, #0F3D3E, #102A43)"
GOLD_ACCENT = "#D4AF37"
CARD_BG = "rgba(255, 255, 255, 0.05)"
TEXT_LIGHT = "#F8FAFC"

# ---------------- PREMIUM GLOBAL STYLE ---------------- #
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
.stApp {{
    background: {PRIMARY_GRADIENT};
    background-attachment: fixed;
    font-family: 'Inter', sans-serif;
    color: {TEXT_LIGHT};
}}

.navbar {{
    padding: 20px 50px;
    font-size: 24px;
    font-weight: 600;
    color: white;
    background: rgba(0,0,0,0.2);
    backdrop-filter: blur(10px);
}}

.hero {{
    text-align: center;
    padding: 80px 20px;
    margin-bottom: 40px;
}}

.hero h1 {{
    font-size: 48px;
    font-weight: 700;
    background: linear-gradient(90deg, #ffffff, {GOLD_ACCENT});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.card {{
    background: {CARD_BG};
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.08);
}}

.prayer-card {{
    background: linear-gradient(135deg, #0F3D3E, #145A42);
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 5px 25px rgba(212,175,55,0.2);
}}

.big-time {{
    font-size: 30px;
    font-weight: 700;
    color: {GOLD_ACCENT};
}}

button[kind="primary"] {{
    background-color: {GOLD_ACCENT} !important;
    color: black !important;
    border-radius: 14px !important;
    height: 3em;
    font-weight: 600;
}}

.footer {{
    text-align: center;
    padding: 50px;
    font-size: 14px;
    opacity: 0.7;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ---------------- #
st.markdown("<div class='navbar'>🕌 Noor Prayer — Premium Edition</div>", unsafe_allow_html=True)

# ---------------- HERO ---------------- #
st.markdown("""
<div class='hero'>
    <h1>Experience Prayer with Elegance</h1>
    <p>Accurate Times • Qibla • Quran • Premium Design</p>
</div>
""", unsafe_allow_html=True)

# ---------------- CONTENT ---------------- #
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📍 Location")

    city = st.text_input("City", "Mecca")
    country = st.text_input("Country", "Saudi Arabia")

    if st.button("Get Prayer Times", type="primary"):
        today = datetime.now().strftime("%d-%m-%Y")
        url = f"https://api.aladhan.com/v1/timingsByCity/{today}"
        params = {"city": city, "country": country, "method": 2}
        response = requests.get(url, params=params)
        data = response.json()

        if data["code"] == 200:
            timings = data["data"]["timings"]
            prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

            for prayer in prayers:
                st.markdown(
                    f"<div class='prayer-card'>"
                    f"<div>{prayer}</div>"
                    f"<div class='big-time'>{timings[prayer]}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📖 Daily Quran Verse")

    try:
        verse = requests.get("https://api.alquran.cloud/v1/ayah/random/en.asad").json()
        text = verse["data"]["text"]
        st.write(text)
    except:
        st.write("Verse unavailable.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #
st.markdown("<div class='footer'>© 2026 Noor Prayer Premium | Luxury Islamic Web Experience</div>", unsafe_allow_html=True)
