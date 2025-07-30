import streamlit as st
import json
import requests
from datetime import datetime
import pytz
import difflib
import openai

# ----------------- Load Static Data --------------------
with open("crop_recommendations.json", "r", encoding="utf-8") as f:
    crop_data = json.load(f)

# ----------------- Config --------------------
API_KEY = "AIzaSyCsfJgoE10pmFhxAKLN4EXRX4ESmbTpB7A"
WEATHER_API_KEY = "cce8745e8f0664cd77af8b135789fe54"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

roman_to_hindi = {
    "mooli": "मूली",
    "dhaniya": "धनिया",
    "baigan": "बैगन",
    "aloo": "आलू",
    "pyaz": "प्याज",
    "gobhi": "गोभी",
    "genda": "गेंदा",
    "tomato": "टमाटर",
    "tamatar": "टमाटर"
}

# ----------------- Helper Functions --------------------
def get_location_details_from_google(pincode):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={pincode}&key={API_KEY}"
    response = requests.get(geocode_url).json()
    if response["status"] == "OK":
        components = response["results"][0]["address_components"]
        district, village = None, None
        for comp in components:
            if "administrative_area_level_2" in comp["types"]:
                district = comp["long_name"]
            if "sublocality_level_1" in comp["types"] or "locality" in comp["types"]:
                village = comp["long_name"]
        return village or "Unknown", district or "Unknown"
    return "❌ Not Found", "❌ Not Found"

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

def get_crop_advice(query, crops):
    query = query.lower().replace("?", "").replace("kyon", "").replace("kyun", "").strip()
    if query in roman_to_hindi:
        query = roman_to_hindi[query]

    all_crop_names = [crop["name"] for cat in crops.values() for crop in cat]
    closest_match = difflib.get_close_matches(query, all_crop_names, n=1, cutoff=0.6)
    if closest_match:
        for cat in crops.values():
            for crop in cat:
                if crop["name"] == closest_match[0]:
                    return f"🌱 **{crop['name']}** इसलिए सुझाया गया है:", f"🔎 कारण: {crop['why']}\n\n💰 लागत: ₹{crop['cost_per_acre']} प्रति एकड़\n📈 अनुमानित मुनाफ़ा: {crop['expected_profit']} प्रति एकड़"

    # If not matched, ask GPT
    gpt_prompt = f"Why should a farmer in Bihar grow '{query}'? Explain in simple Hindi with cost and profit approximation if known."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": gpt_prompt}
        ]
    )
    return f"🌾 {query} के बारे में जानकारी:", response["choices"][0]["message"]["content"]

# ----------------- App Config --------------------
st.set_page_config(page_title="Yugdaan", layout="centered")
st.title("🌾 Yugdaan – Smart Farming Guide")

# ----------------- Input Section --------------------
st.markdown("### 📍 कृपया अपना विवरण भरें")

pincode = st.text_input("पिनकोड दर्ज करें (Enter Pincode)")
land_size = st.selectbox("कितनी ज़मीन में खेती करना है? (Land Size)", ["<1 acre", "1–2 acre", "2–5 acre", "5+ acre"])
budget = st.selectbox("आपका बजट कितना है? (Budget)", ["<₹10,000", "₹10,000–30,000", "₹30,000–50,000", "₹50,000+"])

if pincode:
    village, district = get_location_details_from_google(pincode)
    if district == "❌ Not Found":
        st.warning("⚠️ यह पिनकोड हमारे सिस्टम में नहीं मिला। कृपया पुनः जांचें।")
    else:
        st.success(f"📍 जिला: {district}, गाँव: {village}")
        img_url, address = get_satellite_image(pincode)
        if img_url:
            st.image(img_url, caption=f"🌍 {address}", use_column_width=True)

        # Weather Section
        st.markdown("### 🌤️ मौसम सलाह (Weather Advice)")
        st.info(get_weather_alert(pincode))

        # Crop Recommendation
        st.markdown("## 🌱 आपके लिए फसल सुझाव")
        for category, crops in crop_data.items():
            st.markdown(f"### 🔹 {category.replace('_', ' ').title()} Crops")
            for crop in crops:
                st.success(f"**{crop['name']}** ({crop['type']})")
                st.markdown(f"💰 **लागत (Cost/acre)**: ₹{crop['cost_per_acre']}  \n"
                            f"📈 **मुनाफ़ा (Profit/acre)**: {crop['expected_profit']}  \n"
                            f"📝 **क्यों उगाएं? (Why)**: {crop['why']}")
                st.markdown("---")

        # Conversational Q&A
        st.markdown("### ❓ कोई सवाल पूछें फसल पर (Ask about a crop)")
        user_crop_query = st.text_input("जैसे पूछें: मूली क्यों? / dhaniya kyon?")
        if user_crop_query:
            title, response = get_crop_advice(user_crop_query, crop_data)
            st.markdown(f"#### {title}")
            st.info(response)
