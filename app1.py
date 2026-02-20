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

# ---------------- DARK / LIGHT MODE TOGGLE ---------------- #
mode = st.sidebar.radio("Choose Theme", ["Dark Mode", "Light Mode"])

if mode == "Dark Mode":
    background = "#0f3d2e"
    card_bg = "#145a42"
    text_color = "#f5d776"
    accent = "#d4af37"
else:
    background = "#f4f9f4"
    card_bg = "#ffffff"
    text_color = "#0f3d2e"
    accent = "#1e88e5"

# ---------------- CUSTOM STYLE ---------------- #
st.markdown(f"""
<style>
.stApp {{
    background-color: {background};
    color: {text_color};
    font-family: 'Segoe UI', sans-serif;
}}

h1, h2, h3 {{
    text-align: center;
}}

.card {{
    background-color: {card_bg};
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    text-align: center;
}}

div.stButton > button {{
    background-color: {accent};
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    border: none;
    font-weight: bold;
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
st.markdown("### Your Daily Spiritual Assistant")

# ---------------- AUTO LOCATION ---------------- #
if st.button("📍 Detect My Location"):
    loc = requests.get("https://ipapi.co/json/").json()
    st.session_state.city = loc.get("city", "Mecca")
    st.session_state.country = loc.get("country_name", "Saudi Arabia")

city = st.text_input("City", st.session_state.get("city", "Mecca"))
country = st.text_input("Country", st.session_state.get("country", "Saudi Arabia"))

# ---------------- FETCH PRAYER TIMES ---------------- #
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
        next_prayer = None
        next_time = None

        for prayer in prayers:
            pt = datetime.strptime(timings[prayer], "%H:%M")
            pt = pt.replace(year=now.year, month=now.month, day=now.day)
            if pt > now:
                next_prayer = prayer
                next_time = pt
                break

        if next_time:
            remaining = next_time - now
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            st.markdown(
                f"<div class='card'><h3>⏳ Next Prayer: {next_prayer}</h3>"
                f"<p>{hours}h {minutes}m {seconds}s remaining</p></div>",
                unsafe_allow_html=True
            )

    else:
        st.error("Could not fetch prayer times.")

# ---------------- QIBLA DIRECTION ---------------- #
st.markdown("## 🧭 Qibla Direction")

def calculate_qibla(lat, lon):
    kaaba_lat = math.radians(21.4225)
    kaaba_lon = math.radians(39.8262)
    lat = math.radians(lat)
    lon = math.radians(lon)

    direction = math.atan2(
        math.sin(kaaba_lon - lon),
        math.cos(lat) * math.tan(kaaba_lat) - math.sin(lat) * math.cos(kaaba_lon - lon)
    )
    return (math.degrees(direction) + 360) % 360

if st.button("Find Qibla Direction"):
    loc = requests.get("https://ipapi.co/json/").json()
    lat = loc.get("latitude")
    lon = loc.get("longitude")

    if lat and lon:
        direction = calculate_qibla(lat, lon)
        st.success(f"Qibla Direction: {round(direction,2)}° from North")
    else:
        st.error("Location not detected.")

# ---------------- DAILY QURAN VERSE ---------------- #
st.markdown("## 📖 Daily Quran Verse")

try:
    verse = requests.get("https://api.alquran.cloud/v1/ayah/random/en.asad").json()
    text = verse["data"]["text"]
    reference = f"{verse['data']['surah']['englishName']} {verse['data']['numberInSurah']}"
    st.markdown(f"<div class='card'><p>{text}</p><small>{reference}</small></div>", unsafe_allow_html=True)
except:
    st.info("Unable to fetch verse.")

# ---------------- AZAN SOUND ---------------- #
st.markdown("## 🔔 Play Azan")
st.audio("https://download.quranicaudio.com/quran/azan/azan1.mp3")

# ---------------- FOOTER ---------------- #
st.markdown("<div class='footer'>© 2026 Islamic Prayer Companion | Professional Edition</div>", unsafe_allow_html=True)
