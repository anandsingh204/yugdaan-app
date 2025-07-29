import streamlit as st
from geopy.geocoders import Nominatim

# Google Maps API Key
API_KEY = "AIzaSyCsfJgoE10pmFhxAKLN4EXRX4ESmbTpB7A"

st.set_page_config(page_title="Yugdaan – Personalized Farming Assistant", layout="centered")
st.title("🌾 Yugdaan – Personalized Farming Assistant for Bihar")

# Input pincode
pincode = st.text_input("📮 Enter your pincode (पिनकोड दर्ज करें):")

# Function to fetch satellite image URL
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

# Show satellite image if valid pincode is entered
if pincode:
    satellite_url = get_satellite_image_url(pincode)
    if satellite_url:
        st.image(satellite_url, caption="📍 आपके खेत का सैटेलाइट दृश्य")
    else:
        st.warning("⚠️ यह पिनकोड हमारे सिस्टम में नहीं मिला। कृपया जांचें।")
else:
    st.info("🔍 लाइव सैटेलाइट व्यू देखने के लिए ऊपर पिनकोड दर्ज करें।")
