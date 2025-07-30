
import streamlit as st
import json
import requests
from datetime import datetime
import pytz

# ----------------- Load Static Data --------------------
with open("bihar_pincode_district_map.json", "r", encoding="utf-8") as f:
    district_map = json.load(f)

with open("crop_recommendations.json", "r", encoding="utf-8") as f:
    crop_data = json.load(f)

# ----------------- Helper Functions --------------------
def get_district_from_pincode(pincode):
    return district_map.get(pincode)

def get_satellite_image(pincode):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={pincode}&key={API_KEY}"
    geocode_response = requests.get(geocode_url).json()
    if geocode_response["status"] == "OK":
        location = geocode_response["results"][0]["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]
        static_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=13&size=600x300&maptype=satellite&key={API_KEY}"
        return static_map_url, geocode_response["results"][0]["formatted_address"]
    return None, None

def get_weather_alert(pincode):
    try:
        url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={pincode}&days=2&aqi=no&alerts=no"
        data = requests.get(url).json()
        rain = any(day["day"]["daily_chance_of_rain"] > 40 for day in data["forecast"]["forecastday"])
        if not rain:
            return "⚠️ बारिश नहीं होने वाली है, और मिट्टी में नमी कम है। सुबह सिंचाई करें। (Low soil moisture – irrigate in the morning)"
        return "✅ बारिश होने की संभावना है, सिंचाई रोकी जा सकती है।"
    except:
        return "⚠️ मौसम जानकारी उपलब्ध नहीं है।"

# ----------------- App Config --------------------
st.set_page_config(page_title="Yugdaan", layout="centered")
st.title("🌾 Yugdaan – Smart Farming Guide")

# ----------------- Input Section --------------------
st.markdown("### 📍 कृपया अपना विवरण भरें")

pincode = st.text_input("पिनकोड दर्ज करें (Enter Pincode)")
land_size = st.selectbox("कितनी ज़मीन में खेती करना है? (Land Size)", ["<1 acre", "1–2 acre", "2–5 acre", "5+ acre"])
budget = st.selectbox("आपका बजट कितना है? (Budget)", ["<₹10,000", "₹10,000–30,000", "₹30,000–50,000", "₹50,000+"])

if pincode:
    district = get_district_from_pincode(pincode)
    if not district:
        st.warning("⚠️ यह पिनकोड हमारे सिस्टम में नहीं मिला। कृपया पुनः जांचें।")
    else:
        st.success(f"📍 जिला: {district}")
        img_url, address = get_satellite_image(pincode)
        if img_url:
            st.image(img_url, caption=f"🌍 {address}", use_column_width=True)

        # ----------------- Weather Section --------------------
        st.markdown("### 🌤️ मौसम सलाह (Weather Advice)")
        weather_tip = get_weather_alert(pincode)
        st.info(weather_tip)

        # ----------------- Crop Recommendation Section --------------------
        st.markdown("## 🌱 आपके लिए फसल सुझाव")
        for category, crops in crop_data.items():
            st.markdown(f"### 🔹 {category.replace('_', ' ').title()} Crops")
            for crop in crops:
                st.success(f"**{crop['name']}** ({crop['type']})")
                st.markdown(f"💰 **लागत (Cost/acre)**: ₹{crop['cost_per_acre']}  
"
                            f"📈 **मुनाफ़ा (Profit/acre)**: {crop['expected_profit']}  
"
                            f"📝 **क्यों उगाएं? (Why)**: {crop['why']}")
                st.markdown("---")
