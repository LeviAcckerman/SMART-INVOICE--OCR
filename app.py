# app.py
import streamlit as st
from ocr import extract_text_from_image
from extractor import extract_invoice_fields
from classifier import load_model, predict_category
import os
import tempfile

# Load ML model
model = load_model()

st.set_page_config(page_title="Smart Invoice Scanner", layout="centered")

st.title("📄 Smart Invoice Scanner")
st.markdown("Upload an invoice and let AI do the rest!")

uploaded_file = st.file_uploader("Upload Invoice (Image or PDF)", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.image(tmp_path, caption="Uploaded Invoice", use_column_width=True)
    st.info("🔍 Extracting text from invoice...")

    # Run OCR
    extracted_text = extract_text_from_image(tmp_path)
    st.subheader("📝 OCR Text")
    st.code(extracted_text)

    # Extract fields
    fields = extract_invoice_fields(extracted_text)
    st.subheader("📄 Extracted Invoice Fields")
    for k, v in fields.items():
        st.write(f"**{k.replace('_', ' ').title()}**: {v if v else '❌ Not Found'}")

    # Predict category
    st.subheader("📊 Predicted Invoice Category")
    category = predict_category(extracted_text, model)
    st.success(f"✅ {category}")
