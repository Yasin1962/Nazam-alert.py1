import streamlit as st
import requests
from datetime import datetime
import math

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Islamic Prayer Companion",
    page_icon="🕌",
    layout="centered"
)

# ---------------- THEME TOGGLE ---------------- #
mode = st.sidebar.radio("Theme Mode", ["🌙 Dark", "☀ Light"])

if mode == "🌙 Dark":
    background = "linear-gradient(135deg, #0f2027, #203a43, #2c5364)"
    text_color = "#ffffff"
    card_bg = "rgba(255,255,255,0.1)"
    accent = "#ffd700"
else:
    background = "linear-gradient(135deg, #ff9a9e, #fad0c4, #fad0c4)"
    text_color = "#222222"
    card_bg = "rgba(255,255,255,0.7)"
    accent = "#1e88e5"

# ---------------- CUSTOM STYLE ---------------- #
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">

<style>
.stApp {{
    background: {background};
    background-attachment: fixed;
    color: {text_color};
    font-family: 'Poppins', sans-serif;
}}

h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    text-align: center;
}}

h2, h3 {{
    text-align: center;
}}

.card {{
    background: {card_bg};
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 20px;
    margin: 15px 0;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    text-align: center;
    transition: 0.3s;
}}

.card:hover {{
    transform: scale(1.02);
}}

div.stButton > button {{
    background: {accent};
    color: white;
    border-radius: 25px;
    height: 3em;
    width: 100%;
    border: none;
    font-weight: 600;
    font-size: 16px;
}}

.footer {{
    text-align: center;
    font-size: 14px;
    margin-top: 40px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.title("🕌 Islamic Prayer Companion")
st.markdown("### A Beautiful Spiritual Experience")

# ---------------- LOCATION INPUT ---------------- #
if st.button("📍 Detect My Location"):
    loc = requests.get("https://ipapi.co/json/").json()
    st.session_state.city = loc.get("city", "Mecca")
    st.session_state.country = loc.get("country_name", "Saudi Arabia")

city = st.text_input("City", st.session_state.get("city", "Mecca"))
country = st.text_input("Country", st.session_state.get("country", "Saudi Arabia"))

# ---------------- GET PRAYER TIMES ---------------- #
def get_prayer_times(city, country):
    today = datetime.now().strftime("%d-%m-%Y")
    url = f"https://api.aladhan.com/v1/timingsByCity/{today}"
    params = {"city": city, "country": country, "method": 2}
    response = requests.get(url, params=params)
    return response.json()

if st.button("🕋 Get Prayer Times"):
    data = get_prayer_times(city, country)

    if data["code"] == 200:
        timings = data["data"]["timings"]
        prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

        st.markdown("## 📅 Today's Prayer Times")

        for prayer in prayers:
            st.markdown(
                f"<div class='card'><h3>{prayer}</h3><p style='font-size:22px'>{timings[prayer]}</p></div>",
                unsafe_allow_html=True
            )

        # -------- NEXT PRAYER -------- #
        now = datetime.now()
        for prayer in prayers:
            pt = datetime.strptime(timings[prayer], "%H:%M")
            pt = pt.replace(year=now.year, month=now.month, day=now.day)
            if pt > now:
                remaining = pt - now
                hours, remainder = divmod(remaining.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                st.markdown(
                    f"<div class='card'><h3>⏳ Next Prayer: {prayer}</h3>"
                    f"<p>{hours}h {minutes}m {seconds}s remaining</p></div>",
                    unsafe_allow_html=True
                )
                break

# ---------------- QIBLA ---------------- #
st.markdown("## 🧭 Qibla Direction")

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

        st.success(f"Qibla Direction: {round(direction,2)}° from North")

# ---------------- AZAN ---------------- #
st.markdown("## 🔔 Azan")
st.audio("https://download.quranicaudio.com/quran/azan/azan1.mp3")

# ---------------- FOOTER ---------------- #
st.markdown("<div class='footer'>© 2026 Islamic Prayer Companion | Premium Edition</div>", unsafe_allow_html=True)
