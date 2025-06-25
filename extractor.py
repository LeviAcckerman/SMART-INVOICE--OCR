import re

def extract_invoice_fields(text):
    """
    Extract key fields like invoice number, date, and total from raw OCR text.
    
    :param text: Raw OCR text from the invoice
    :return: Dictionary with extracted fields
    """
    data = {}

    # Extract invoice number
    match = re.search(r'Invoice\s*Number[:\-]?\s*(\S+)', text, re.IGNORECASE)
    data['Invoice Number'] = match.group(1) if match else None

    # Extract date in formats like DD/MM/YYYY or MM/DD/YYYY or YYYY-MM-DD
    date_match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})', text)
    data['Date'] = date_match.group(1) if date_match else None

    # Extract total amount (match formats like: $123.45 or 123.45)
    total_match = re.search(r'Total\s*[:\-]?\s*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text, re.IGNORECASE)
    data['Total Amount'] = total_match.group(1) if total_match else None

    return data
