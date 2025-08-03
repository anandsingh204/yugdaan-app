
import streamlit as st
import requests
import openai

# ----------------- Secure API Key Handling --------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]
API_KEY = st.secrets["GOOGLE_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]

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

def validate_farmer_crop(pincode, district, crop):
    prompt = f"""
    A farmer in {district} (pincode {pincode}) wants to grow {crop}. 
    Based on typical soil, season, and weather in this area, analyze if this is a good decision.
    If it's a good crop choice, say so clearly and provide:
    - Reasons it's suitable
    - Expected yield/profit
    - Timeline & what inputs (seeds, fertilizers) are needed
    - Suggest links for buying inputs (BigHaat, Amazon, etc.)
    - Recommend crop insurance: both government (like PMFBY) and private (IFFCO, HDFC Ergo)

    If it's NOT a good choice, explain why and suggest 2-3 better crops instead based on soil/weather/season.
    Respond in Hinglish with clear formatting and practical advice.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT issue: {str(e)}"

# ----------------- App UI --------------------
st.set_page_config(page_title="Yugdaan – FarmGPT", layout="centered")
st.title("🌾 Yugdaan – FarmGPT: Smart Crop Validator")

st.markdown("### 📍 Step 1: कृपया अपना पिनकोड और विवरण भरें")

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
            st.image(img_url, caption=f"🌍 {address}", use_container_width=True)

        # Weather section (placeholder)
        st.markdown("### ☁️ मौसम की जानकारी (coming soon...)")

        # Farmer crop input
        st.markdown("### 🌱 Step 2: किसान द्वारा चुनी गई फसल का चयन करें")
        farmer_crop = st.selectbox("आप कौन सी फसल उगाना चाहते हैं?", [
            "गेहूं (Wheat)", "धान (Paddy)", "मूली (Radish)", "टमाटर (Tomato)",
            "धनिया (Coriander)", "मक्का (Maize)", "गन्ना (Sugarcane)", 
            "बैंगन (Brinjal)", "सरसों (Mustard)", "चना (Chickpea)"
        ])

        if st.button("✅ सुझाव प्राप्त करें (Validate Crop Choice)"):
            with st.spinner("AI से सुझाव लिए जा रहे हैं..."):
                response = validate_farmer_crop(pincode, district, farmer_crop)
                st.markdown(response)
