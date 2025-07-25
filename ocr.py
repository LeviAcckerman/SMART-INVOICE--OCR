from PIL import Image
import pytesseract
from textblob import TextBlob
import fitz  # PyMuPDF

# Optional: for Windows, specify tesseract path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Keywords that should never be auto-corrected
SKIP_KEYWORDS = [
    "Invoice", "Qty", "INVOICE", "GST", "CGST", "SGST", "HSN", "MRP", "PAN",
    "Acme", "Globex", "USD", "INR", "₹", "$"
]

def is_correctable(line):
    """Decide if a line should go through correction."""
    if any(char.isdigit() for char in line):
        return False
    if any(keyword.lower() in line.lower() for keyword in SKIP_KEYWORDS):
        return False
    if len(line.strip()) < 4:
        return False
    return True

def smart_spell_correct(text):
    """
    Applies smart spell correction only on correctable text lines.
    Skips lines with numbers, invoice-specific terms, short lines, etc.
    """
    corrected_lines = []
    for line in text.splitlines():
        if is_correctable(line):
            try:
                blob = TextBlob(line)
                corrected = str(blob.correct())
                corrected_lines.append(corrected)
            except Exception:
                corrected_lines.append(line)
        else:
            corrected_lines.append(line)
    return "\n".join(corrected_lines)

def extract_text_from_image(image_path):
    """
    Extracts text from an invoice image and applies smart spelling correction.
    """
    image = Image.open(image_path)
    # IMPROVED: Specify language and page segmentation, normalize line endings
    raw_text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    raw_text = raw_text.replace('\r\n', '\n').replace('\r', '\n')
    corrected_text = smart_spell_correct(raw_text)
    return corrected_text

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF. If text is not found, uses OCR on each page.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text + "\n"
            else:
                # If no text, use OCR on image-rendered page (with DPI and language config)
                try:
                    pix = page.get_pixmap(dpi=300)
                except Exception:
                    pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                raw_text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
                raw_text = raw_text.replace('\r\n', '\n').replace('\r', '\n')
                corrected_text = smart_spell_correct(raw_text)
                text += corrected_text + "\n"
    return text.strip()
