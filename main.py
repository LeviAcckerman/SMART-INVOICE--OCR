import streamlit as st
import os
from ocr import extract_text_from_image
from extractor import extract_invoice_fields
from classifier import predict_category
from PIL import Image

st.set_page_config(page_title="Smart Invoice Scanner", layout="wide")

st.title("📄 Smart Invoice Scanner + Classifier")
st.markdown("Upload an invoice image to extract details and predict its category.")

uploaded_file = st.file_uploader("Upload an Invoice Image", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    # Save file to 'uploads/' folder
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Show uploaded image
    if uploaded_file.type.startswith("image/"):
        st.image(Image.open(file_path), caption="Uploaded Invoice", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        text = extract_text_from_image(file_path)
        st.subheader("📝 Extracted Text (Preview):")
        st.text(text[:2000])

    with st.spinner("🔍 Extracting Fields..."):
        fields = extract_invoice_fields(text)
        st.subheader("📋 Invoice Fields:")
        for key, value in fields.items():
            st.markdown(f"**{key}**: {value}")

    with st.spinner("🤖 Predicting Category..."):
        try:
            category = predict_category(text)
            st.success(f"📂 Predicted Category: **{category}**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
