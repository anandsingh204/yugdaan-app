import streamlit as st
import requests
import random

st.set_page_config(page_title="Yugdaan - खेती सलाह", layout="centered")
st.title("🌾 Yugdaan - Bihar Smart Farming Assistant")
st.markdown("आपके जिले और ज़रूरत के अनुसार फ़सल की सिफ़ारिश (Crop recommendation based on your district and needs)")

# --- District Selection ---
districts = {
    "Darbhanga": "Darbhanga,IN",
    "Vaishali": "Hajipur,IN",
    "Aara": "Arrah,IN",
    "Chapra": "Chhapra,IN",
    "Balia": "Ballia,IN"
}

district = st.selectbox("📍 Select your district (जिला चुनें)", list(districts.keys()))
city_name = districts[district]

# --- Real-Time Weather API ---
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

        st.markdown(f"🌤 **Today's Weather (आज का मौसम):**")
        st.markdown(f"- Temperature (तापमान): {temp}°C")
        st.markdown(f"- Humidity (नमी): {humidity}%")
        st.markdown(f"- Condition: {weather.capitalize()} ({'बारिश' if rain else 'कोई बारिश नहीं'})")
    else:
        st.error("⚠️ Weather data not available for your district right now.")
except:
    st.error("❌ Could not fetch live weather. Please check internet connection.")

# --- User Goal ---
goal = st.selectbox("🎯 What do you want from your crop? (आपकी प्राथमिकता)", [
    "High Profit (ज्यादा कमाई)",
    "Less Water Need (कम पानी वाली फ़सल)",
    "Quick Harvest (तेज़ी से तैयार होने वाली फ़सल)"
])

# --- Soil Moisture (Mock) ---
soil_moisture = random.choice(["Low", "Medium", "High"])
st.info(f"💧 Current Soil Moisture (मिट्टी में नमी): **{soil_moisture}**")

# --- Smart Crop Recommendation Logic ---
crop_db = {
    "Darbhanga": [
        {"name": "Paddy (धान)", "profit": "high", "water": "high", "speed": "medium"},
        {"name": "Maize (मक्का)", "profit": "medium", "water": "medium", "speed": "fast"},
        {"name": "Banana (केला)", "profit": "high", "water": "high", "speed": "slow"},
        {"name": "Marigold (गेंदा)", "profit": "medium", "water": "low", "speed": "fast"}
    ],
    "Vaishali": [
        {"name": "Wheat (गेहूं)", "profit": "medium", "water": "medium", "speed": "medium"},
        {"name": "Potato (आलू)", "profit": "high", "water": "medium", "speed": "fast"},
        {"name": "Litchi (लीची)", "profit": "high", "water": "high", "speed": "slow"},
        {"name": "Mustard (सरसों)", "profit": "medium", "water": "low", "speed": "fast"}
    ],
    "Aara": [
        {"name": "Sugarcane (गन्ना)", "profit": "high", "water": "high", "speed": "slow"},
        {"name": "Brinjal (बैंगन)", "profit": "medium", "water": "medium", "speed": "fast"},
        {"name": "Cauliflower (फूलगोभी)", "profit": "medium", "water": "low", "speed": "fast"}
    ],
    "Chapra": [
        {"name": "Paddy (धान)", "profit": "high", "water": "high", "speed": "medium"},
        {"name": "Tomato (टमाटर)", "profit": "medium", "water": "medium", "speed": "fast"},
        {"name": "Garlic (लहसुन)", "profit": "medium", "water": "low", "speed": "medium"}
    ],
    "Balia": [
        {"name": "Wheat (गेहूं)", "profit": "medium", "water": "medium", "speed": "medium"},
        {"name": "Onion (प्याज)", "profit": "high", "water": "medium", "speed": "fast"},
        {"name": "Pumpkin (कद्दू)", "profit": "medium", "water": "low", "speed": "fast"}
    ]
}

# --- Apply filter based on user goal ---
filter_key = {
    "High Profit (ज्यादा कमाई)": "profit",
    "Less Water Need (कम पानी वाली फ़सल)": "water",
    "Quick Harvest (तेज़ी से तैयार होने वाली फ़सल)": "speed"
}[goal]

desired_value = {
    "profit": "high",
    "water": "low",
    "speed": "fast"
}[filter_key]

matching_crops = [crop["name"] for crop in crop_db[district] if crop[filter_key] == desired_value]

# --- Output Recommendations ---
st.subheader("🌱 Recommended Crops (अनुशंसित फ़सलें):")
if matching_crops:
    for crop in matching_crops[:3]:
        st.markdown(f"- ✅ {crop}")
else:
    st.warning("⚠️ कोई उपयुक्त फ़सल नहीं मिली। कृपया अलग प्राथमिकता चुनें। (No ideal crop found for this goal.)")

# --- Soil Moisture Suggestion ---
if soil_moisture == "Low":
    st.warning("💧 मिट्टी में नमी कम है, सुबह सिंचाई करें (Low soil moist
