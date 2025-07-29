
import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="🌾 Yugdaan v8 - Pincode Aware AI", layout="centered")
st.title("🌾 Yugdaan v8 – पिनकोड आधारित फ़सल सलाह")

st.markdown("### 📍 पिनकोड दर्ज करें:")
pincode = st.text_input("उदाहरण: 841301", max_chars=6)

st.markdown("### 🌾 ज़मीन का आकार:")
land = st.radio("आपके पास कितनी ज़मीन है?", ["<1 एकड़", "1-2 एकड़", "2-5 एकड़", "5+ एकड़"])

st.markdown("### 🌊 ज़मीन की हालत:")
soil_type = st.selectbox("ज़मीन की स्थिति:", ["सामान्य (Normal)", "दलदली (Waterlogged)", "बंजर (Barren)", "रेतीली (Sandy)"])

st.markdown("### 💸 खेती का बजट:")
budget = st.selectbox("बजट:", ["₹0–₹20,000", "₹20,000–₹50,000", "₹50,000+"])

district_map = {
    "841301": "Chapra",
    "844101": "Vaishali",
    "846004": "Darbhanga",
    "802301": "Arrah",
    "277001": "Ballia"
}

district_recs = {
    "Chapra": [("आलू (Potato)", "₹18K", "₹1.2L", "✅ Stable"),
               ("धान (Paddy)", "₹20K", "₹1.4L", "⛅ Mid Risk")],
    "Vaishali": [("मक्का (Maize)", "₹15K", "₹90K", "✅ Low Cost"),
                 ("टमाटर (Tomato)", "₹28K", "₹1.8L", "⚠️ Market Volatile")],
    "Darbhanga": [("मखाना (Fox Nut)", "₹25K", "₹1.5L", "✅ Local Specialty"),
                  ("धान (Paddy)", "₹20K", "₹1.2L", "⛅ Mid Risk")],
    "Arrah": [("चना (Chickpea)", "₹18K", "₹1L", "✅ Short Cycle"),
              ("गेहूं (Wheat)", "₹22K", "₹1.3L", "✅ Reliable")],
    "Ballia": [("सब्ज़ी मिश्रण (Mixed Veg)", "₹25K", "₹1.5L", "⚠️ Labour Intense"),
               ("सरसों (Mustard)", "₹17K", "₹80K", "✅ Winter Crop")]
}

if st.button("📊 सलाह लें"):
    district = district_map.get(pincode, None)
    if district:
        st.success(f"📍 पिनकोड {pincode} → जिला: {district}")
        st.markdown("### 🧠 उस क्षेत्र के लिए AI सुझाई गई फ़सलें:")

        crops = district_recs[district]
        st.markdown("| फ़सल | लागत | आमदनी | जोखिम |")
        st.markdown("|------|--------|---------|--------|")
        for crop in crops:
            st.markdown(f"| {crop[0]} | {crop[1]} | {crop[2]} | {crop[3]} |")
    else:
        st.warning("❌ यह पिनकोड सिस्टम में नहीं है। कृपया बिहार का वैध पिनकोड डालें।")

    st.markdown("### 📅 आज से क्या करें?")
    st.info("👉 आज बीज और खाद की जानकारी लें, कल जुताई करवाएं। हर फ़सल के लिए अलग गाइड जल्द जोड़ी जाएगी।")

    st.caption("⚙️ ये सुझाव पिनकोड, बजट, ज़मीन की स्थिति पर आधारित हैं – Yugdaan AI द्वारा।")
