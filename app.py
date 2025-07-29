
import streamlit as st

st.set_page_config(page_title="🌾 Yugdaan v4 - ROI & Risk Engine", layout="centered")
st.title("🌾 Yugdaan v4 – किसान का मुनाफ़ा और जोखिम सलाहकार")

districts = {
    "Darbhanga": {"mandi_price": 1860, "rain_mm": 60, "soil": "Low"},
    "Vaishali": {"mandi_price": 2100, "rain_mm": 100, "soil": "Medium"},
    "Aara": {"mandi_price": 1750, "rain_mm": 40, "soil": "Low"},
    "Chapra": {"mandi_price": 2000, "rain_mm": 120, "soil": "High"},
    "Balia": {"mandi_price": 2200, "rain_mm": 90, "soil": "Medium"}
}

st.markdown("### 🧑‍🌾 Farmer Details")
district = st.selectbox("📍 District", list(districts.keys()))
land_size = st.slider("🟫 Land in acres", 1, 10, 2)
irrigated = st.radio("🚿 Do you have irrigation?", ["Yes", "No"])
crop = st.selectbox("🌱 Choose Crop", ["Wheat", "Paddy", "Maize", "Mustard", "Tomato", "Banana"])

# Base yield & cost per crop
crop_data = {
    "Wheat": {"yield_qtl_per_acre": 18, "cost_per_acre": 12000},
    "Paddy": {"yield_qtl_per_acre": 22, "cost_per_acre": 14000},
    "Maize": {"yield_qtl_per_acre": 16, "cost_per_acre": 11000},
    "Mustard": {"yield_qtl_per_acre": 10, "cost_per_acre": 9000},
    "Tomato": {"yield_qtl_per_acre": 80, "cost_per_acre": 25000},
    "Banana": {"yield_qtl_per_acre": 160, "cost_per_acre": 45000},
}

st.markdown("### 📊 ROI Calculator")
data = crop_data[crop]
mandi = districts[district]["mandi_price"]
yield_total = data["yield_qtl_per_acre"] * land_size
revenue = yield_total * mandi
cost_total = data["cost_per_acre"] * land_size
profit = revenue - cost_total
roi_pct = (profit / cost_total) * 100

st.success(f"💰 Estimated Profit: ₹{profit:,.0f} | ROI: {roi_pct:.1f}%")

# Risk Score logic
st.markdown("### ⚠️ Crop Risk Score")
soil = districts[district]["soil"]
rain = districts[district]["rain_mm"]

risk_score = 100
if soil == "Low": risk_score -= 30
if rain < 60: risk_score -= 20
if irrigated == "No": risk_score -= 20

risk_label = "🔴 High Risk" if risk_score < 60 else "🟡 Medium Risk" if risk_score < 80 else "🟢 Low Risk"
st.warning(f"{risk_label} – Risk Score: {risk_score}/100")

st.markdown("---")
st.info("📈 Powered by real mandi price logic, rainfall data and local farming patterns")
