import streamlit as st
import requests
from datetime import datetime
import pytz
from openai import OpenAI
import os

# ----------------- Config --------------------
API_KEY = "AIzaSyCsfJgoE10pmFhxAKLN4EXRX4ESmbTpB7A"
WEATHER_API_KEY = "cce8745e8f0664cd77af8b135789fe54"
OPENAI_API_KEY = "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"  # <-- Replace this line with your valid key
client = OpenAI(api_key=OPENAI_API_KEY)

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
            return "⚠️ बारिश नहीं होने वाली है, और मिट्टी में नमी कम है। सुबह सिंचाई करें।"
        return "✅ बारिश होने की संभावना है, सिंचाई रोकी जा सकती है।"
    except:
        return "⚠️ मौसम जानकारी उपलब्ध नहीं है।"

def get_crop_recommendation(pincode, land_size, budget):
    prompt = f"""
    I am a farmer from Bihar. My pincode is {pincode}. I want to do farming on land size: {land_size} and my budget is {budget}.
    Please suggest the 2–3 best crops I should grow now based on season, soil, weather and income trends. 
    Also explain:
    1. Why these crops are suitable
    2. Estimated cost and expected profit per acre
    3. What I will need for best yield (like fertilizers, pesticides etc.)
    4. Best month to start cultivation
    Answer in simple Hinglish (mix of Hindi-English) that a rural farmer can understand.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        st.warning("⚠️ GPT-4 not available, using GPT-3.5 instead.")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
    return response.choices[0].message.content


def ask_crop_question(user_query):
    prompt = f"एक किसान ने पूछा है: '{user_query}'. कृपया इस सवाल का जवाब सरल हिंदी में दें ताकि वह समझ सके। फसल की उपयोगिता, लागत, मुनाफा और मौसम की जानकारी जोड़ें।"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# ----------------- App UI --------------------
st.set_page_config(page_title="Yugdaan", layout="centered")
st.title("🌾 Yugdaan – Smart Farming Guide")

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

        # Weather section
        st.markdown("### 🌤️ मौसम सलाह (Weather Advice)")
        st.info(get_weather_alert(pincode))

        # GPT-based crop advice
        st.markdown("## 🌱 फसल सुझाव (AI Based Recommendations)")
        with st.spinner("AI से सुझाव लिए जा रहे हैं..."):
            advice = get_crop_recommendation(pincode, land_size, budget)
            st.markdown(advice)

        # Q&A follow-up
        st.markdown("### ❓ कोई सवाल पूछें (Ask AI about a crop)")
        user_crop_query = st.text_input("जैसे पूछें: मूली क्यों? / dhaniya kyon?")
        if user_crop_query:
            response = ask_crop_question(user_crop_query)
            st.markdown(response)
