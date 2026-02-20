import streamlit as st
import requests
from datetime import datetime
import math

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Noor Prayer",
    page_icon="🕌",
    layout="wide"
)

# ---------------- PROFESSIONAL COLOR SYSTEM ---------------- #
PRIMARY = "#0F3D3E"
SECONDARY = "#14B8A6"
ACCENT = "#FACC15"
LIGHT_BG = "#F8FAFC"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#1E293B"

# ---------------- GLOBAL STYLE ---------------- #
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
.stApp {{
    background-color: {LIGHT_BG};
    font-family: 'Inter', sans-serif;
}}

.navbar {{
    background-color: {PRIMARY};
    padding: 18px 40px;
    color: white;
    font-size: 22px;
    font-weight: 600;
}}

.hero {{
    background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
    padding: 60px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
}}

.card {{
    background-color: {CARD_BG};
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}}

.prayer-card {{
    background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
    color: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
}}

.big-number {{
    font-size: 28px;
    font-weight: 700;
}}

button[kind="primary"] {{
    background-color: {ACCENT} !important;
    color: black !important;
    border-radius: 12px !important;
    height: 3em;
}}

.footer {{
    text-align: center;
    padding: 40px;
    color: {TEXT_DARK};
    font-size: 14px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ---------------- #
st.markdown("<div class='navbar'>🕌 Noor Prayer — Islamic Companion</div>", unsafe_allow_html=True)

# ---------------- HERO SECTION ---------------- #
st.markdown("""
<div class='hero'>
    <h1>Stay Connected to Your Prayers</h1>
    <p>Accurate Prayer Times • Qibla Direction • Daily Quran Verse</p>
</div>
""", unsafe_allow_html=True)

# ---------------- MAIN GRID ---------------- #
col1, col2 = st.columns([2, 1])

# ---------------- LEFT SIDE (PRAYER TIMES) ---------------- #
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📍 Your Location")

    if st.button("Detect Location"):
        loc = requests.get("https://ipapi.co/json/").json()
        st.session_state.city = loc.get("city", "Mecca")
        st.session_state.country = loc.get("country_name", "Saudi Arabia")

    city = st.text_input("City", st.session_state.get("city", "Mecca"))
    country = st.text_input("Country", st.session_state.get("country", "Saudi Arabia"))

    if st.button("Get Prayer Times", type="primary"):
        today = datetime.now().strftime("%d-%m-%Y")
        url = f"https://api.aladhan.com/v1/timingsByCity/{today}"
        params = {"city": city, "country": country, "method": 2}
        response = requests.get(url, params=params)
        data = response.json()

        if data["code"] == 200:
            timings = data["data"]["timings"]
            prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

            st.markdown("### 🕋 Today's Prayer Schedule")

            for prayer in prayers:
                st.markdown(
                    f"<div class='prayer-card'><div>{prayer}</div>"
                    f"<div class='big-number'>{timings[prayer]}</div></div>",
                    unsafe_allow_html=True
                )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RIGHT SIDE (QIBLA + VERSE) ---------------- #
with col2:
    # Qibla Card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧭 Qibla Direction")

    if st.button("Find Qibla"):
        loc = requests.get("https://ipapi.co/json/").json()
        lat = loc.get("latitude")
        lon = loc.get("longitude")

        if lat and lon:
            kaaba_lat = math.radians(21.4225)
            kaaba_lon = math.radians(39.8262)
            lat = math.radians(lat)
            lon = math.radians(lon)

            direction = math.atan2(
                math.sin(kaaba_lon - lon),
                math.cos(lat) * math.tan(kaaba_lat) - math.sin(lat) * math.cos(kaaba_lon - lon)
            )
            direction = (math.degrees(direction) + 360) % 360

            st.success(f"{round(direction,2)}° from North")

    st.markdown("</div>", unsafe_allow_html=True)

    # Quran Verse Card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📖 Daily Quran Verse")

    try:
        verse = requests.get("https://api.alquran.cloud/v1/ayah/random/en.asad").json()
        text = verse["data"]["text"]
        reference = f"{verse['data']['surah']['englishName']} {verse['data']['numberInSurah']}"
        st.write(text)
        st.caption(reference)
    except:
        st.write("Unable to load verse.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #
st.markdown("<div class='footer'>© 2026 Noor Prayer | Designed as Real-Life Professional Islamic Application</div>", unsafe_allow_html=True)
