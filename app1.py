import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Namaz Time Alarm",
    page_icon="🕌",
    layout="centered"
)

# ---------------- CUSTOM PROFESSIONAL STYLE ---------------- #
st.markdown("""
<style>
.stApp {
    background-color: #0f3d2e;
    color: #f5d776;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3 {
    color: #f5d776;
    text-align: center;
}

div.stButton > button {
    background-color: #d4af37;
    color: #0f3d2e;
    font-weight: bold;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    border: none;
}

div.stButton > button:hover {
    background-color: #f5d776;
    color: #0f3d2e;
}

.stTextInput>div>div>input {
    background-color: #145a42;
    color: white;
    border-radius: 8px;
}

.card {
    background-color: #145a42;
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    text-align: center;
}

.footer {
    text-align: center;
    font-size: 14px;
    margin-top: 30px;
    color: #f5d776;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.title("🕌 Namaz Time Alarm")
st.markdown("### Stay Connected With Your Daily Prayers")

# ---------------- USER INPUT ---------------- #
city = st.text_input("Enter Your City", "Mecca")
country = st.text_input("Enter Your Country", "Saudi Arabia")

# ---------------- FUNCTION TO FETCH PRAYER TIMES ---------------- #
def get_prayer_times(city, country):
    today = datetime.now().strftime("%d-%m-%Y")
    url = f"https://api.aladhan.com/v1/timingsByCity/{today}"
    params = {
        "city": city,
        "country": country,
        "method": 2
    }
    response = requests.get(url, params=params)
    return response.json()

# ---------------- FETCH BUTTON ---------------- #
if st.button("Get Prayer Times"):
    data = get_prayer_times(city, country)

    if data["code"] == 200:
        timings = data["data"]["timings"]

        st.markdown("## 📅 Today's Prayer Times")

        prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

        for prayer in prayers:
            st.markdown(
                f"<div class='card'><h3>{prayer}</h3><p style='font-size:22px;'>{timings[prayer]}</p></div>",
                unsafe_allow_html=True
            )

        # ---------------- NEXT PRAYER COUNTDOWN ---------------- #
        st.markdown("## ⏳ Next Prayer Countdown")

        now = datetime.now()
        next_prayer_time = None
        next_prayer_name = ""

        for prayer in prayers:
            prayer_time = datetime.strptime(timings[prayer], "%H:%M")
            prayer_time = prayer_time.replace(
                year=now.year,
                month=now.month,
                day=now.day
            )

            if prayer_time > now:
                next_prayer_time = prayer_time
                next_prayer_name = prayer
                break

        if next_prayer_time:
            remaining = next_prayer_time - now
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            st.markdown(
                f"<div class='card'><h3>Next Prayer: {next_prayer_name}</h3>"
                f"<p style='font-size:22px;'>{hours}h {minutes}m {seconds}s remaining</p></div>",
                unsafe_allow_html=True
            )
        else:
            st.info("All prayers for today are completed.")

    else:
        st.error("Unable to fetch prayer times. Please check city/country.")

# ---------------- REMINDER SLIDER ---------------- #
st.markdown("---")
st.subheader("⏰ Reminder Settings")
minutes_before = st.slider("Remind me before prayer (minutes)", 0, 30, 10)

st.info("⚠️ Note: Browser apps cannot trigger phone alarm when closed.")

# ---------------- FOOTER ---------------- #
st.markdown("<div class='footer'>© 2026 Namaz Time Alarm | Professional Islamic Web App</div>", unsafe_allow_html=True)
