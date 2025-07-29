import streamlit as st
import json
from datetime import datetime
from geopy.geocoders import Nominatim

# --- Configurations ---
API_KEY = "AIzaSyCsfJgoE10pmFhxAKLN4EXRX4ESmbTpB7A"
st.set_page_config(page_title="Yugdaan – Personalized Farming Assistant", layout="centered")
st.title("🌾 Yugdaan – Personalized Farming Assistant for Bihar")

# --- Load Pincode-District Mapping ---
try:
    with open("bihar_pincode_district_map.json", "r", encoding="utf-8") as f:
        district_map = json.load(f)
except FileNotFoundError:
    district_map = {}

# --- Get District from Pincode ---
pincode = st.text_input("📮 Enter your pincode (पिनकोड दर्ज करें):")
district = district_map.get(pincode)

if pincode and not district:
    st.warning("⚠️ यह पिनकोड हमारे सिस्टम में नहीं मिला। कृपया पुनः जांचें।")

# --- Satellite Image Function ---
def get_satellite_image_url(pincode):
    geolocator = Nominatim(user_agent="yugdaan-live-app")
    location = geolocator.geocode({"postalcode": pincode, "country": "India"})
    if location:
        lat, lon = location.latitude, location.longitude
        return (
            f"https://maps.googleapis.com/maps/api/staticmap?"
            f"center={lat},{lon}&zoom=14&size=600x400&maptype=satellite"
            f"&markers=color:red%7Clabel:P%7C{lat},{lon}"
            f"&key={API_KEY}"
        )
    return None

# --- Show Satellite Image ---
if pincode:
    sat_url = get_satellite_image_url(pincode)
    if sat_url:
        st.image(sat_url, caption="📍 आपके खेत का सैटेलाइट दृश्य")

# --- Farm Questionnaire ---
if district:
    st.subheader("👨‍🌾 खेती की जानकारी दर्ज करें")
    land_size = st.selectbox("🧱 कितनी ज़मीन में खेती करना है?", ["<1 acre", "1–2 acres", "2–5 acres", "5+ acres"])
    budget = st.selectbox("💰 उपलब्ध बजट कितना है?", ["<₹10,000", "₹10,000–₹25,000", "₹25,000–₹50,000", "₹50,000+"])
    goal = st.selectbox("🎯 आपकी प्राथमिकता क्या है?", ["High Profit", "Short Duration", "Low Cost", "Less Effort"])

    st.markdown("---")
    st.subheader("📊 सुझाव और योजनाएं")

    # --- Sample AI Logic ---
    st.markdown(f"🗺️ जिला: **{district}**")
    st.markdown(f"📐 ज़मीन: **{land_size}** | 💸 बजट: **{budget}** | 🎯 लक्ष्य: **{goal}**")

    # Example recommendations (mock logic)
    if goal == "High Profit":
        st.success("🌱 आप **ड्रैगन फ्रूट**, **अवोकाडो**, या **ग्लैडियोलस फूल** उगा सकते हैं।")
        st.info("💡 शुरुआती लागत: ₹40,000–₹60,000 प्रति एकड़ | अनुमानित लाभ: ₹1.5–2 लाख प्रति एकड़")
        st.markdown("📅 **अगस्त-सितंबर** में शुरुआत करें, 12-14 महीने में फसल तैयार होती है।")

    elif goal == "Short Duration":
        st.success("🌿 आप **मूली**, **पालक**, या **धनिया** जैसे फसलें उगा सकते हैं।")
        st.info("🗓️ 30–60 दिनों में फसल तैयार | ₹5,000–₹15,000 लागत")

    elif goal == "Low Cost":
        st.success("🥔 **आलू**, **प्याज**, या **चना** जैसे पारंपरिक फसलें उगाइए।")
        st.info("💰 लागत: ₹8,000–₹20,000 प्रति एकड़ | लाभ: ₹30,000–₹60,000")

    else:
        st.success("🌾 आप **गेहूं**, **सरसों**, या **मक्का** जैसे आसान देखभाल वाली फसलें उगा सकते हैं।")

    st.markdown("📦 ज़रूरी सामग्री, उर्वरक और बीजों की सूची जल्द ही उपलब्ध होगी।")
    st.markdown("🔁 अगले अपडेट में Google से डीलर डेटा, मंडी भाव और साप्ताहिक कार्य भी जोड़े जाएंगे।")
else:
    st.info("📝 खेती की सलाह पाने के लिए ऊपर अपना पिनकोड दर्ज करें।")
