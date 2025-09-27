import streamlit as st
import requests
from PIL import Image
import os

# ====== CONFIG ======
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")  # read from Streamlit secrets
MODEL_ID = "cattle-buffalo-breeds-v2.0-hb3bt/1"
ROBOFLOW_URL = f"https://detect.roboflow.com/{MODEL_ID}"

# Breed → Food dictionary (expand as needed)
breed_food = {
    # Cows
    "Gir": "High-protein fodder, cottonseed cake, and green grass.",
    "Sahiwal": "Balanced diet with wheat bran, maize silage, and legumes.",
    "Red Sindhi": "Lucerne, berseem, and groundnut cake for better milk yield.",
    "Tharparkar": "Green fodder, dry wheat straw, and oilseed cakes.",
    "Nagori": "Millet straw, guar phalgati, and leguminous fodder.",

    # Buffaloes
    "Murrah": "Green fodder, dry straw, and mineral mixture for better milk yield.",
    "Jaffarabadi": "Sugarcane tops, sorghum, and mineral-rich supplements.",
    "Mehsana": "Hybrid napier grass, maize fodder, and mineral supplements.",
    "Banni": "Grass, cactus, and dry fodder suited for arid regions.",
}

# ====== STREAMLIT UI ======
st.set_page_config(page_title="Cattle & Buffalo Breed Recognition", layout="centered")
st.title("🐄 Cattle & Buffalo Breed Recognition (India)")
st.write("Upload an image of a cow or buffalo, and the app will identify the breed and suggest suitable food.")

uploaded_file = st.file_uploader("📸 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("🔎 Identifying breed..."):
        response = requests.post(
            ROBOFLOW_URL,
            params={"api_key": ROBOFLOW_API_KEY},
            files={"file": uploaded_file.getvalue()}
        )

    if response.status_code == 200:
        result = response.json()
        predictions = result.get("predictions", [])

        if predictions:
            breed = predictions[0]["class"]
            confidence = predictions[0]["confidence"] * 100

            st.success(f"✅ Identified Breed: **{breed}** ({confidence:.2f}% confidence)")

            food = breed_food.get(breed, "General cattle diet: green fodder, dry straw, and mineral supplements.")
            st.subheader("🍀 Suggested Food")
            st.write(food)

            # Debugging: Show raw API response (optional)
            with st.expander("🔧 Debug: Raw API Response"):
                st.json(result)

        else:
            st.error("❌ No breed detected. Try another image.")
    else:
        st.error("⚠️ Error contacting Roboflow API. Check your API key or model ID.")
