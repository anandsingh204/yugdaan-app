import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Yugdaan - खेती सलाह", layout="centered")

st.title("🌾 Yugdaan - Bihar Smart Farming Assistant")
st.markdown("आपके जिले और ज़रूरत के अनुसार फ़सल की सिफ़ारिश (Crop recommendation based on your district and needs)")

# District selector
districts = ["Darbhanga", "Vaishali", "Aara", "Chapra", "Balia"]
district = st.selectbox("📍 Select your district (जिला चुनें)", districts)

# Basic need assessment
goal = st.selectbox("🎯 What do you want from your crop? (आपकी प्राथमिकता)", [
    "High Profit (ज्यादा कमाई)",
    "Less Water Need (कम पानी वाली फ़सल)",
    "Quick Harvest (तेज़ी से तैयार होने वाली फ़सल)"
])

# Simulated soil moisture data
soil_moisture = random.choice(["Low", "Medium", "High"])

st.info(f"💧 Current Soil Moisture (मिट्टी में नमी): **{soil_moisture}**")

# Simulated crop database (can expand later)
crops = {
    "Darbhanga": ["Paddy (धान)", "Maize (मक्का)", "Banana (केला)", "Marigold (गेंदा)"],
    "Vaishali": ["Wheat (गेहूं)", "Potato (आलू)", "Litchi (लीची)", "Mustard (सरसों)"],
    "Aara": ["Sugarcane (गन्ना)", "Brinjal (बैंगन)", "Cauliflower (फूलगोभी)"],
    "Chapra": ["Paddy (धान)", "Tomato (टमाटर)", "Garlic (लहसुन)"],
    "Balia": ["Wheat (गेहूं)", "Onion (प्याज)", "Pumpkin (कद्दू)"]
}

recommendation = crops.get(district, [])[:3]  # pick top 3 crops

st.subheader("🌱 Suggested Crops (अनुशंसित फ़सलें):")
for crop in recommendation:
    st.markdown(f"- ✅ {crop}")

# Optional advice
if soil_moisture == "Low":
    st.warning("💧 मिट्टी में नमी कम है, सुबह सिंचाई करें (Low soil moisture – irrigate in the morning).")
elif soil_moisture == "High":
    st.success("🌦 मिट्टी में अच्छी नमी है, अभी सिंचाई की आवश्यकता नहीं।")

st.markdown("---")
st.caption("📊 Prototype version - powered by mock data. Real-time satellite & market integration coming soon.")
