import re
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_invoice_fields(text):
    doc = nlp(text)
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    data = {
        "invoice_number": None,
        "Order No": None,
        "invoice_date": None,
        "due_date": None,
        "po_number": None,
        "seller_name": None,
        "seller_gst": None,
        "buyer_name": None,
        "buyer_gst": None,
        "items": [],
        "subtotal": None,
        "discount": None,
        "taxable_amount": None,
        "tax_rate": None,
        "total": None,
        "payment_status": None,
        "flags": {"fraud_suspected": False, "gst_mismatch": False, "total_mismatch": False}
    }

    def find_line(keywords):
        for line in lines:
            if any(k.lower() in line.lower() for k in keywords):
                return line
        return None

    # Invoice number
    inv_line = find_line(["Invoice No", "Invoice Number", "Inv"])
    if inv_line:
        for token in inv_line.split():
            if "INV" in token.upper():
                data["invoice_number"] = token.strip(":#")

    # Date
    date_line = find_line(["Date"])
    if date_line:
        for token in date_line.split():
            if re.match(r"\d{4}-\d{2}-\d{2}", token) or re.match(r"\d{2}/\d{2}/\d{4}", token):
                data["invoice_date"] = token

    # Seller
    seller_block = find_line(["Seller", "From", "Issued by"])
    if seller_block:
        idx = lines.index(seller_block)
        data["seller_name"] = lines[idx + 1] if idx + 1 < len(lines) else None

    # Seller GST
    gst_line = find_line(["GSTIN", "GST No"])
    if gst_line:
        gst_tokens = gst_line.split()
        for token in gst_tokens:
            if len(token) == 15 and token.isalnum():
                data["seller_gst"] = token

    # Buyer
    buyer_block = find_line(["Buyer", "To", "Billed to"])
    if buyer_block:
        idx = lines.index(buyer_block)
        data["buyer_name"] = lines[idx + 1] if idx + 1 < len(lines) else None

    # Buyer GST
    for line in lines:
        if "GST" in line and data["seller_gst"] and data["seller_gst"] not in line:
            parts = line.split()
            for token in parts:
                if len(token) == 15 and token.isalnum():
                    data["buyer_gst"] = token

    # Items Table Extraction
    table_started = False
    for line in lines:
        if any(word in line.lower() for word in ["description", "qty", "unit", "price", "tax"]):
            table_started = True
            continue
        if table_started:
            tokens = line.split()
            if len(tokens) >= 5:
                try:
                    description = " ".join(tokens[:-4])
                    qty = float(tokens[-4])
                    price = float(tokens[-3])
                    tax = tokens[-2]
                    total = float(tokens[-1])
                    data["items"].append({
                        "description": description,
                        "quantity": qty,
                        "unit_price": price,
                        "tax": tax,
                        "line_total": total
                    })
                except:
                    continue

    # Subtotal
    sub_line = find_line(["Subtotal", "Sub Total", "Amount before Tax"])
    if sub_line:
        amounts = [float(tok.replace(",", "")) for tok in sub_line.split() if tok.replace(",", "").replace(".", "").isdigit()]
        if amounts:
            data["subtotal"] = amounts[-1]

    # Total
    total_line = find_line(["Grand Total", "Total Amount", "Amount Payable"])
    if total_line:
        amounts = [float(tok.replace(",", "")) for tok in total_line.split() if tok.replace(",", "").replace(".", "").isdigit()]
        if amounts:
            data["total"] = amounts[-1]

    # Payment Status
    pay_line = find_line(["Payment Status", "Paid", "Unpaid"])
    if pay_line:
        if "paid" in pay_line.lower():
            data["payment_status"] = "Paid"
        elif "unpaid" in pay_line.lower():
            data["payment_status"] = "Unpaid"
        else:
            data["payment_status"] = pay_line.split(":")[-1].strip()

    # Flags
    if data["total"] and data["subtotal"]:
        expected_total = round(data["subtotal"] + 0.12 * data["subtotal"], 2)  # Assume 12% tax
        if abs(data["total"] - expected_total) > 5:
            data["flags"]["total_mismatch"] = True

    return data
