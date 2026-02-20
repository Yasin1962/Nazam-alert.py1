import streamlit as st
import requests
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Namaz Time Alarm", page_icon="🕌")

st.title("🕌 Namaz Time Alarm App")

city = st.text_input("Enter your City", "Mecca")
country = st.text_input("Enter your Country", "Saudi Arabia")

if st.button("Get Prayer Times"):
    today = datetime.now().strftime("%d-%m-%Y")
    
    url = f"http://api.aladhan.com/v1/timingsByCity/{today}"
    params = {
        "city": city,
        "country": country,
        "method": 2
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if data["code"] == 200:
        timings = data["data"]["timings"]
        
        st.subheader("📅 Today's Prayer Times")
        for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
            st.write(f"**{prayer}:** {timings[prayer]}")
    else:
        st.error("Could not fetch prayer times.")

st.markdown("---")

st.subheader("⏰ Reminder Settings")
minutes_before = st.slider("Remind me before prayer (minutes)", 0, 30, 10)

st.info("⚠️ Note: Browser apps cannot trigger real phone alarms when closed. Keep the app open for alerts.")