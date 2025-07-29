
import streamlit as st
import requests

st.set_page_config(page_title="🌾 Yugdaan - Smart Farming Bihar", layout="centered")
st.title("🌾 Yugdaan - किसान की अपनी सलाहकार")
st.markdown("फसल, मौसम, मंडी भाव और ज़रूरत के अनुसार सुझाव • Crop, mandi and weather-based guidance")

districts = {
    "Darbhanga": "Darbhanga,IN",
    "Vaishali": "Hajipur,IN",
    "Aara": "Arrah,IN",
    "Chapra": "Chhapra,IN",
    "Balia": "Ballia,IN"
}
district = st.selectbox("📍 Select your district (जिला चुनें)", list(districts.keys()))
city_name = districts[district]

api_key = "cce8745e8f0664cd77af8b135789fe54"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

try:
    response = requests.get(url)
    weather_data = response.json()
    if weather_data["cod"] == 200:
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        weather = weather_data["weather"][0]["description"]
        rain = "rain" in weather.lower()
        st.markdown("### 🌦️ Weather Today (आज का मौसम)")
        st.write(f"- Temperature (तापमान): {temp}°C")
        st.write(f"- Humidity (नमी): {humidity}%")
        st.write(f"- Condition: {weather.capitalize()} ({'बारिश हो सकती है' if rain else 'बारिश नहीं होगी'})")
except:
    st.warning("Weather data unavailable at the moment.")

# Mocked mandi prices
mandi_prices = {
    "Darbhanga": [("धान (Paddy)", 1860), ("मक्का (Maize)", 1750)],
    "Vaishali": [("गेहूं (Wheat)", 2100), ("आलू (Potato)", 1600)],
    "Aara": [("सरसों (Mustard)", 5000), ("बैंगन (Brinjal)", 2500)],
    "Chapra": [("प्याज (Onion)", 1400), ("टमाटर (Tomato)", 1800)],
    "Balia": [("चना (Gram)", 4600), ("कद्दू (Pumpkin)", 1300)],
}
st.markdown("### 🏪 Mandi Prices Today (मंडी भाव)")
for crop, price in mandi_prices[district]:
    st.write(f"- {crop}: ₹{price} per quintal (क्विंटल)")

st.markdown("### 🛰️ Satellite Soil Moisture (Mock Data)")
soil_moisture_status = {
    "Darbhanga": "Low",
    "Vaishali": "Medium",
    "Aara": "Low",
    "Chapra": "Medium",
    "Balia": "High"
}
moisture = soil_moisture_status.get(district, "Medium")
st.info(f"🧪 मिट्टी की नमी: **{moisture}** (based on NASA/ISRO trend)")

st.markdown("### 🧠 Answer a few questions (कुछ सवालों के जवाब दें)")

land = st.radio("आपके पास कितनी ज़मीन है? (Land size)", ["1-2 acre", "2-5 acre", "More than 5 acre"])
irrigation = st.radio("क्या आपके पास सिंचाई की सुविधा है? (Do you have irrigation?)", ["Yes", "No"])
wait_time = st.radio("आप कितने समय तक इंतज़ार कर सकते हैं फ़सल के लिए?", ["Short (3 months)", "Medium (6 months)", "Long (9+ months)"])

crop_knowledge = {
    "Darbhanga": [
        {"name": "Paddy (धान) – Kharif", "water": "high", "wait": "Medium", "profit": "high"},
        {"name": "Banana (केला)", "water": "high", "wait": "Long", "profit": "high"},
        {"name": "Marigold (गेंदा)", "water": "low", "wait": "Short", "profit": "medium"},
        {"name": "Maize (मक्का) – Kharif", "water": "medium", "wait": "Medium", "profit": "medium"},
    ],
    "Vaishali": [
        {"name": "Litchi (लीची)", "water": "high", "wait": "Long", "profit": "high"},
        {"name": "Mustard (सरसों) – Rabi", "water": "low", "wait": "Short", "profit": "medium"},
        {"name": "Potato (आलू) – Rabi", "water": "medium", "wait": "Short", "profit": "high"},
        {"name": "Wheat (गेहूं) – Rabi", "water": "medium", "wait": "Medium", "profit": "medium"},
    ],
    "Aara": [
        {"name": "Sugarcane (गन्ना)", "water": "high", "wait": "Long", "profit": "high"},
        {"name": "Cauliflower (फूलगोभी)", "water": "low", "wait": "Short", "profit": "medium"},
        {"name": "Brinjal (बैंगन)", "water": "medium", "wait": "Medium", "profit": "medium"},
    ],
    "Chapra": [
        {"name": "Garlic (लहसुन)", "water": "low", "wait": "Medium", "profit": "medium"},
        {"name": "Tomato (टमाटर)", "water": "medium", "wait": "Short", "profit": "high"},
    ],
    "Balia": [
        {"name": "Onion (प्याज)", "water": "medium", "wait": "Short", "profit": "high"},
        {"name": "Pumpkin (कद्दू)", "water": "low", "wait": "Short", "profit": "medium"},
    ]
}

st.markdown("### ✅ Recommended Crops (अनुशंसित फ़सलें)")
filtered = []
for crop in crop_knowledge.get(district, []):
    if (irrigation == "No" and crop["water"] == "high"):
        continue
    if wait_time.startswith("Short") and crop["wait"] != "Short":
        continue
    if wait_time.startswith("Medium") and crop["wait"] == "Long":
        continue
    filtered.append(crop["name"])

if filtered:
    for crop in filtered:
        st.markdown(f"- 🌱 {crop}")
else:
    st.warning("कोई उपयुक्त फ़सल नहीं मिली (No suitable crop found for your selection).")

st.markdown("---")
st.info("ℹ️ Kharif: Monsoon crops (जैसे धान, मक्का) • Rabi: Winter crops (जैसे गेहूं, सरसों)")
st.caption("Prototype v3 • Real weather + mandi + soil + advisory")
