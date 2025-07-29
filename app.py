
import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="🤖 Yugdaan v6 - Smart Kisan AI", layout="centered")
st.title("🤖 Yugdaan v6 – AI से चलने वाली किसान मार्गदर्शक")

st.markdown("### 📍 आपके पिनकोड की जानकारी दें:")
pincode = st.text_input("उदाहरण: 841301", max_chars=6)

st.markdown("### 🌾 आपकी ज़मीन कितनी है?")
land = st.radio("जमीन का आकार चुनें:", ["<1 एकड़", "1-2 एकड़", "2-5 एकड़", "5+ एकड़"])

st.markdown("### 💸 खेती के लिए आपका बजट?")
budget = st.selectbox("बजट चुनें:", ["₹0–₹20,000", "₹20,000–₹50,000", "₹50,000+"])

if st.button("👉 सलाह लें (Get Smart Advice)"):
    st.success(f"✅ पिनकोड {pincode} में, {land} ज़मीन और {budget} बजट के अनुसार:")

    st.markdown("### 🧠 क्या उगाएं?")
    st.info("🥔 **आलू** – कम लागत, तेज़ उत्पादन, हर जगह बिकता है।")

    st.markdown("### 📦 क्या-क्या चाहिए?")
    st.write("- बीज: 10 क्विंटल (~₹20,000)")
    st.write("- खाद: NPK + जैविक खाद (~₹5,000)")
    st.write("- छिड़काव: Confidor / नीम ऑइल (~₹3,000)")

    st.markdown("### 📍 कहाँ मिलेगा?")
    st.write("🔍 अपने नज़दीकी डीलर के लिए Google पर खोजें: ‘आलू बीज विक्रेता पास में’")

    st.markdown("### 📅 कब क्या करें?")
    today = date.today()
    st.write(f"- 🌱 **बुवाई करें**: {today.strftime('%d %b %Y')}")
    st.write(f"- 💧 पहली सिंचाई: {(today + timedelta(days=5)).strftime('%d %b %Y')}")
    st.write(f"- 🌾 कटाई की तैयारी: {(today + timedelta(days=90)).strftime('%d %b %Y')}")

    st.markdown("### 📈 बाज़ार रुझान (Trend)")
    st.warning("⚠️ इस समय जिले में आलू की खेती ज़्यादा हो रही है — मंडी कीमतें गिर सकती हैं।")

    st.markdown("### 🧭 आज से क्या करें?")
    st.success("✅ आज खाद और बीज का इंतज़ाम करें। कल ज़मीन की जुताई करवाएं।")

    st.caption("📲 ये सलाह आपके क्षेत्र, बजट और खेती के आकार पर आधारित है। और भी स्मार्ट जानकारी के लिए अपडेट करते रहें।")
