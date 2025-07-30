
import streamlit as st
import json
import requests
from datetime import datetime
import pytz
import difflib

# ----------------- Load Static Data --------------------
with open("bihar_pincode_district_map.json", "r", encoding="utf-8") as f:
    district_map = json.load(f)

with open("crop_recommendations.json", "r", encoding="utf-8") as f:
    crop_data = json.load(f)

# ----------------- Config --------------------
API_KEY = "AIzaSyCsfJgoE10pmFhxAKLN4EXRX4ESmbTpB7A"
WEATHER_API_KEY = "cce8745e8f0664cd77af8b135789fe54"

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
        district_name = None
        for component in geocode_response["results"][0]["address_components"]:
            if "administrative_area_level_2" in component["types"]:
                district_name = component["long_name"]
                break
        return static_map_url, geocode_response["results"][0]["formatted_address"], district_name
    return None, None, None

def get_weather_alert(pincode):
    try:
        url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={pincode}&days=2&aqi=no&alerts=no"
        data = requests.get(url).json()
        rain = any(day["day"]["daily_chance_of_rain"] > 40 for day in data["forecast"]["forecastday"])
        if not rain:
            return "⚠️ No rain expected. Soil moisture is low. Irrigate in the morning."
        return "✅ Rain expected. Irrigation can be postponed."
    except:
        return "⚠️ Weather data not available."

def get_crop_advice(query, crops):
    query = query.lower()
    all_crop_names = [crop["name"].lower() for cat in crops.values() for crop in cat]
    closest_match = difflib.get_close_matches(query, all_crop_names, n=1, cutoff=0.6)
    if closest_match:
        for cat in crops.values():
            for crop in cat:
                if crop["name"].lower() == closest_match[0]:
                    return (
                        f"🌱 {crop['name']} is recommended because: {crop['why']}

"
                        f"💰 Cost: ₹{crop['cost_per_acre']} per acre
"
                        f"📈 Estimated Profit: {crop['expected_profit']} per acre"
                    )
    return "❓ Information not available for this crop."

# ----------------- App Config --------------------
st.set_page_config(page_title="Yugdaan", layout="centered")
st.title("🌾 Yugdaan – Smart Farming Guide")

# ----------------- Input Section --------------------
st.markdown("### 📍 Please fill in your details")

pincode = st.text_input("Enter Pincode")
land_size = st.selectbox("Land Size", ["<1 acre", "1–2 acre", "2–5 acre", "5+ acre"])
budget = st.selectbox("Budget", ["<₹10,000", "₹10,000–30,000", "₹30,000–50,000", "₹50,000+"])

if pincode:
    district = get_district_from_pincode(pincode)
    img_url, address, detected_district = get_satellite_image(pincode)
    display_district = district if district else detected_district
    if display_district:
        st.success(f"📍 District: {display_district}")
    elif not district:
        st.warning("⚠️ Pincode not found in system, but location was detected via satellite.")
    if img_url:
        st.image(img_url, caption=f"🌍 {address}", use_column_width=True)

    # ----------------- Weather Section --------------------
    st.markdown("### 🌤️ Weather Advice")
    weather_tip = get_weather_alert(pincode)
    st.info(weather_tip)

    # ----------------- Crop Recommendation Section --------------------
    st.markdown("## 🌱 Crop Recommendations for You")
    for category, crops in crop_data.items():
        st.markdown(f"### 🔹 {category.replace('_', ' ').title()} Crops")
        for crop in crops:
            st.success(f"**{crop['name']}** ({crop['type']})")
            st.markdown(f"💰 **Cost (per acre)**: ₹{crop['cost_per_acre']}  
"
                        f"📈 **Profit (per acre)**: {crop['expected_profit']}  
"
                        f"📝 **Why Grow?**: {crop['why']}")
            st.markdown("---")

    # ----------------- Conversational Crop Q&A --------------------
    st.markdown("### ❓ Ask About a Crop")
    user_crop_query = st.text_input("e.g., Why radish? / Why coriander?")
    if user_crop_query:
        cleaned_query = user_crop_query.replace("Why", "").replace("?", "").strip()
        response = get_crop_advice(cleaned_query, crop_data)
        st.info(response)
