
import streamlit as st

st.set_page_config(page_title="Yugdaan – Smart Farming", layout="centered")

# ----------------- Branding -------------------
st.markdown("## 🌾 Welcome to Yugdaan – Your Farming Guide")
st.markdown("##### 🚀 Let's begin your smart farming journey")

# ----------------- Step 1: Login or Guest -------------------
st.markdown("### 🔐 Step 1: Login or Continue")
login_method = st.radio("How would you like to continue?", ["Continue as Guest", "Login with Google (Coming Soon)"])

# ----------------- Step 2: Location Access -------------------
st.markdown("### 📍 Step 2: Location")
location_mode = st.radio("Choose how to provide your location:", ["📍 Use Current Location (Coming Soon)", "📌 Enter Pincode Manually"])
pincode = ""
if location_mode == "📌 Enter Pincode Manually":
    pincode = st.text_input("Enter your Pincode")

if pincode:
    st.success(f"📍 Location set to Pincode: {pincode}")

# ----------------- Step 3: Farming Category -------------------
st.markdown("### 🗂️ Step 3: Choose Your Farming Category")

category = st.selectbox("What type of farming help do you need?", [
    "🌾 Crop Cultivation",
    "🥬 Kitchen/Urban Farming",
    "🐄 Dairy & Livestock",
    "🌱 Organic/Natural Farming",
    "☀️ Solar-powered Farming",
    "🚜 Agri-Machinery Leasing",
    "🧪 Soil & Weather Advisory",
    "📦 Farm-to-Market Help",
    "🛡️ Crop Insurance Help",
    "💸 Subsidies & Government Schemes"
])

# ----------------- Category Follow-up -------------------
if category == "🌾 Crop Cultivation":
    st.markdown("### 🌱 Let's help you plan your crop")
    selected_crop = st.selectbox("Which crop are you thinking to grow?", [
        "गेहूं (Wheat)", "धान (Paddy)", "मूली (Radish)", "टमाटर (Tomato)",
        "धनिया (Coriander)", "मक्का (Maize)", "गन्ना (Sugarcane)", 
        "बैंगन (Brinjal)", "सरसों (Mustard)", "चना (Chickpea)"
    ])
    if st.button("📊 Validate this crop choice with AI"):
        st.markdown("✅ *This is where FarmGPT will validate your choice and suggest inputs, profit, and insurance options...*")

elif category == "🐄 Dairy & Livestock":
    st.info("🚧 Dairy & Livestock guidance is coming soon...")

elif category == "🧪 Soil & Weather Advisory":
    st.info("🚧 We will soon provide soil & weather trends for your location...")

else:
    st.info(f"🚧 Guidance for '{category}' is under development. Stay tuned!")

st.markdown("---")
st.markdown("🔐 Note: We respect your privacy. No personal data is stored.")
