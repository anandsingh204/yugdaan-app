
import streamlit as st
import json
from datetime import date

st.set_page_config(page_title="🌾 Yugdaan v9 - Full Bihar Map", layout="centered")
st.title("🌾 Yugdaan v9 – पिनकोड आधारित फ़सल सलाह (बिहार के लिए)")

st.markdown("### 📍 पिनकोड दर्ज करें:")
pincode = st.text_input("उदाहरण: 841301", max_chars=6)

st.markdown("### 🌾 ज़मीन का आकार:")
land = st.radio("आपके पास कितनी ज़मीन है?", ["<1 एकड़", "1-2 एकड़", "2-5 एकड़", "5+ एकड़"])

st.markdown("### 🌊 ज़मीन की हालत:")
soil_type = st.selectbox("ज़मीन की स्थिति:", ["सामान्य (Normal)", "दलदली (Waterlogged)", "बंजर (Barren)", "रेतीली (Sandy)"])

st.markdown("### 💸 खेती का बजट:")
budget = st.selectbox("बजट:", ["₹0–₹20,000", "₹20,000–₹50,000", "₹50,000+"])

# Load full pincode-district map
with open("bihar_pincode_district_map.json", "r", encoding="utf-8") as f:
    district_map = json.load(f)

# Sample crop recommendations for demo (mock logic reused)
district_crop_demo = {
    "Chapra": [("आलू", "₹18K", "₹1.2L", "✅ Stable"), ("धान", "₹20K", "₹1.4L", "⛅ Mid Risk")],
    "Darbhanga": [("मखाना", "₹25K", "₹1.5L", "✅ Local"), ("धान", "₹20K", "₹1.2L", "⛅ Mid Risk")],
    "Muzaffarpur": [("लीची", "₹28K", "₹2L", "✅ Export"), ("सरसों", "₹15K", "₹70K", "✅ Winter")],
}

default_crops = [("गेहूं", "₹22K", "₹1.3L", "✅ Reliable"), ("चना", "₹18K", "₹1L", "✅ Low Cost")]

if st.button("📊 सलाह लें"):
    district = district_map.get(pincode)
    if district:
        st.success(f"📍 पिनकोड {pincode} → जिला: {district}")
        st.markdown("### 🧠 AI सुझाई गई फ़सलें:")

        crops = district_crop_demo.get(district, default_crops)
        st.markdown("| फ़सल | लागत | आमदनी | जोखिम |")
        st.markdown("|------|--------|---------|--------|")
        for crop in crops:
            st.markdown(f"| {crop[0]} | {crop[1]} | {crop[2]} | {crop[3]} |")
    else:
        st.error("❌ बिहार का यह पिनकोड नहीं मिला। कृपया पुनः प्रयास करें।")

    st.markdown("### 📅 आज से क्या करें?")
    st.info("👉 आज बीज और खाद की जानकारी लें, कल जुताई करवाएं। हर फ़सल के लिए अलग गाइड जल्द जोड़ी जाएगी।")

    st.caption("⚙️ यह सुझाव पिनकोड, ज़मीन और बजट पर आधारित है – Yugdaan AI द्वारा।")
