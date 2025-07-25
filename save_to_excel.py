import pandas as pd
from extractor import extract_invoice_fields

def save_invoice_to_excel(invoice_texts, output_file="extracted_invoices.xlsx"):
    rows = []

    for text in invoice_texts:
        data = extract_invoice_fields(text)

        for item in data.get("items", [{}]):
            row = {
                "Invoice Number": data.get("invoice_number"),
                "Invoice Date": data.get("invoice_date"),
                "Seller Name": data.get("seller_name"),
                "Seller GST": data.get("seller_gst"),
                "Buyer Name": data.get("buyer_name"),
                "Buyer GST": data.get("buyer_gst"),
                "Item Description": item.get("description", None),
                "Quantity": item.get("quantity", None),
                "Unit Price": item.get("unit_price", None),
                "Tax": item.get("tax", None),
                "Line Total": item.get("line_total", None),
                "Subtotal": data.get("subtotal"),
                "Tax Amount": data.get("tax_amount"),
                "Grand Total": data.get("total"),
                "Payment Status": data.get("payment_status"),
                "Flag": data.get("flag")
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"✅ Extracted data saved to: {output_file}")
