# app.py
import streamlit as st
from ocr import extract_text_from_image, extract_text_from_pdf
from extractor import extract_invoice_fields
from classifier import load_model, predict_category
import os
import tempfile

# Load ML model
model = load_model()

st.set_page_config(page_title="Smart Invoice Scanner", layout="centered")
st.title("📄 Smart Invoice Scanner")
st.markdown("Upload an invoice (Image or PDF) and let AI do the rest!")

uploaded_file = st.file_uploader("Upload Invoice (Image or PDF)", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Determine if PDF or Image
    if uploaded_file.type == "application/pdf":
        st.info("📄 PDF detected. Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(tmp_path)
    else:
        st.image(tmp_path, caption="🖼️ Uploaded Invoice Image", use_column_width=True)
        st.info("🔍 Extracting text from image...")
        extracted_text = extract_text_from_image(tmp_path)

    # Display OCR Text
    st.subheader("📝 OCR Extracted Text")
    st.code(extracted_text[:3000] if extracted_text else "❌ No text extracted")

    # Extract invoice fields
    st.subheader("📄 Extracted Invoice Fields")
    fields = extract_invoice_fields(extracted_text)
    for k, v in fields.items():
        st.write(f"**{k.replace('_', ' ').title()}**: {v if v else '❌ Not Found'}")

    # Predict Category
    st.subheader("📊 Predicted Invoice Category")
    category = predict_category(extracted_text, model)
    st.success(f"✅ {category}")
