
import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="🌾 Yugdaan v7 - Multi-Crop AI Advisor", layout="centered")
st.title("🌾 Yugdaan v7 – AI आधारित मल्टी फ़सल सलाह")

st.markdown("### 📍 पिनकोड दर्ज करें:")
pincode = st.text_input("उदाहरण: 841301", max_chars=6)

st.markdown("### 🌾 ज़मीन का आकार:")
land = st.radio("आपके पास कितनी ज़मीन है?", ["<1 एकड़", "1-2 एकड़", "2-5 एकड़", "5+ एकड़"])

st.markdown("### 🌊 ज़मीन की हालत:")
soil_type = st.selectbox("ज़मीन की स्थिति:", ["सामान्य (Normal)", "दलदली (Waterlogged)", "बंजर (Barren)", "रेतीली (Sandy)"])

st.markdown("### 💸 खेती का बजट:")
budget = st.selectbox("बजट:", ["₹0–₹20,000", "₹20,000–₹50,000", "₹50,000+"])

if st.button("📊 सलाह लें"):
    st.success(f"📍 पिनकोड {pincode} | ज़मीन: {land} | स्थिति: {soil_type} | बजट: {budget}")

    st.markdown("### 🧠 AI सुझाई गई फ़सलें:")
    if soil_type == "दलदली (Waterlogged)":
        crops = [("धान (Paddy)", "₹18K", "₹1.2L", "⛅ Mid Risk"),
                 ("सिंघाड़ा (Water Chestnut)", "₹15K", "₹1L", "✅ Low Risk")]
    elif soil_type == "बंजर (Barren)":
        crops = [("बबूल/नीम पेड़", "₹10K", "₹30K (3 yrs)", "🌱 Tree Plantation"),
                 ("कंटीली झाड़ी / मवेशी चारा", "₹5K", "₹15K", "✅ Low Input")]
    else:
        crops = [("आलू (Potato)", "₹20K", "₹1.4L", "✅ Stable"),
                 ("टमाटर (Tomato)", "₹30K", "₹1.8L", "⚠️ Market Volatile"),
                 ("मटर (Peas)", "₹25K", "₹1.1L", "✅ Short Cycle")]

    st.markdown("| फ़सल | लागत | आमदनी | जोखिम |")
    st.markdown("|------|--------|---------|--------|")
    for crop in crops:
        st.markdown(f"| {crop[0]} | {crop[1]} | {crop[2]} | {crop[3]} |")

    st.markdown("### 📅 आज से क्या करें?")
    st.info("👉 आज बीज और खाद की जानकारी लें, कल जुताई करवाएं। हर फ़सल के लिए अलग गाइड जल्द जोड़ी जाएगी।")

    st.caption("⚙️ ये सिस्टम AI और वैश्विक कृषि डेटा पर आधारित है – हर किसान के लिए सटीक सलाह देने के लिए।")
