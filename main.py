from ocr import ocr_from_image
from extractor import extract_invoice_fields
from classifier import classify_invoice

image_path = "C:\\Users\\Harikumar\\OneDrive\\Pictures\\Screenshots 1\\Screenshot 2025-06-25 153912.png"
# Step 1: OCR
text = ocr_from_image(image_path, preprocess=True)
print("\n🔍 OCR Text:\n", text)

# Step 2: Extract fields
fields = extract_invoice_fields(text)
print("\n📄 Extracted Fields:")
for key, val in fields.items():
    print(f"{key}: {val}")

# Step 3: Classify
category = classify_invoice(text)
print(f"\n📂 Invoice Category: {category}")
