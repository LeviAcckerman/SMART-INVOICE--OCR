import streamlit as st
import os
import pandas as pd
from ocr import extract_text_from_image, extract_text_from_pdf
from extractor import extract_invoice_fields
from classifier import predict_category
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="Smart Invoice Scanner", layout="wide")

st.title("📄 Smart Invoice Scanner + Classifier")
st.markdown("Upload one or more invoices (Image or PDF) to extract details, classify, and export to Excel.")

uploaded_files = st.file_uploader("Upload Invoices", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)

if uploaded_files:
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    all_rows = []
    excel_ready = False

    for uploaded_file in uploaded_files:
        st.divider()
        st.subheader(f"📁 File: {uploaded_file.name}")

        file_path = os.path.join(upload_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Preview image
        if uploaded_file.type.startswith("image/"):
            try:
                img = Image.open(file_path)
                st.image(img, caption="Invoice Preview", use_container_width=True)
            except Exception as imerr:
                st.warning(f"Image preview error: {imerr}")

        # OCR
        with st.spinner("🔍 Extracting text..."):
            try:
                if uploaded_file.type == "application/pdf":
                    text = extract_text_from_pdf(file_path)
                else:
                    text = extract_text_from_image(file_path)
            except Exception as ocrerr:
                st.error(f"OCR failed: {ocrerr}")
                continue

        if not text.strip():
            st.warning("❌ No text found in document.")
            continue

        st.text_area("📝 Extracted Text Preview", text[:1000], height=150)

        # Extract Fields
        with st.spinner("🔍 Extracting Invoice Fields..."):
            try:
                fields = extract_invoice_fields(text)
                st.success("✅ Invoice fields extracted.")

                # Display fields
                for key, value in fields.items():
                    if isinstance(value, list):
                        st.markdown(f"**{key.capitalize()}**:")
                        if not value:
                            st.markdown("_No items found_")
                        else:
                            for item in value:
                                st.markdown(f"- {item}")
                    else:
                        st.markdown(f"**{key.replace('_',' ').capitalize()}**: {value}")

                # Predict Category
                category = predict_category(text)
                st.markdown(f"📂 **Predicted Category**: `{category}`")

                # Prepare Excel row(s)
                for item in fields.get("items", [{}]):
                    row = {
                        "File": uploaded_file.name,
                        "Invoice Number": fields.get("invoice_number"),
                        "Invoice Date": fields.get("invoice_date"),
                        "Seller Name": fields.get("seller_name"),
                        "Seller GST": fields.get("seller_gst"),
                        "Buyer Name": fields.get("buyer_name"),
                        "Buyer GST": fields.get("buyer_gst"),
                        "Item Description": item.get("description"),
                        "Quantity": item.get("quantity"),
                        "Unit Price": item.get("unit_price"),
                        "Tax": item.get("tax"),
                        "Line Total": item.get("line_total"),
                        "Subtotal": fields.get("subtotal"),
                        "Tax Amount": fields.get("tax_amount"),
                        "Grand Total": fields.get("total"),
                        "Payment Status": fields.get("payment_status"),
                        "Flag": fields.get("flag"),
                        "Predicted Category": category
                    }
                    all_rows.append(row)

                excel_ready = True

            except Exception as ferr:
                st.error(f"Field extraction failed: {ferr}")

    # Export to Excel
    if excel_ready and all_rows:
        df = pd.DataFrame(all_rows)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_path = f"extracted_invoices_{timestamp}.xlsx"
        df.to_excel(excel_path, index=False, engine='openpyxl')

        with open(excel_path, "rb") as f:
            st.download_button("⬇️ Download Extracted Excel", f, file_name=excel_path, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
