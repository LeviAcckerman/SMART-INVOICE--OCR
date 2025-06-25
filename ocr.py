import pytesseract
import cv2

# Set path to the installed Tesseract-OCR binary
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



def ocr_from_image(image_path, preprocess=False):
    """
    Extract text from an image using Tesseract OCR.
    
    :param image_path: Path to the image file
    :param preprocess: Whether to apply preprocessing to the image
    :return: Extracted text as a string
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return "[ERROR] Cannot read image. Check path."

        if preprocess:
            image = preprocess_image(image)

        text = pytesseract.image_to_string(image)
        return text.strip()

    except Exception as e:
        return f"[ERROR] OCR failed: {e}"

def preprocess_image(image):
    """
    Enhance image for better OCR accuracy.
    Convert to grayscale, blur, and apply adaptive thresholding.
    """
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(blur, 255,
                                       cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        return thresh
    except Exception as e:
        print(f"[ERROR] in preprocess_image: {e}")
        return image  # Fallback to original image
