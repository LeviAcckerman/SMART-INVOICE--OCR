import re

def extract_invoice_fields(text):
    fields = {
        "invoice_number": None,
        "invoice_date": None,
        "due_date": None,
        "total_amount": None
    }

    # Invoice Number
    match = re.search(r'(Invoice\s*Number|Invoice\s*No\.?|#)\s*[:\-]?\s*(\w+)', text, re.IGNORECASE)
    if match:
        fields["invoice_number"] = match.group(2)

    # Invoice Date
    match = re.search(r'(Invoice\s*Date)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
    if match:
        fields["invoice_date"] = match.group(2)

    # Due Date
    match = re.search(r'(Due\s*Date)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
    if match:
        fields["due_date"] = match.group(2)

    # Total Amount
    match = re.search(r'(Total\s*Amount|Total)\s*[:\-]?\s*\$?([0-9,]+\.\d{2})', text, re.IGNORECASE)
    if match:
        fields["total_amount"] = match.group(2)

    return fields
