 
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path


def extract_text_from_pdf(pdf_path):
    """
    First tries to extract text directly from digital PDF.
    If that fails or returns very little text, runs OCR on scanned PDF.
    """
    text = ""

    try:
        #  direct text extraction
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()

        if len(text.strip()) > 200:
            print("Digital PDF detected. Text extracted directly.")
            return text.strip()

    except Exception as e:
        print(f"Direct extraction failed: {e}")

    print("Scanned PDF detected. Running OCR...")

    try:
        images = convert_from_path(pdf_path, dpi=300)
        ocr_text = ""
        for i, image in enumerate(images):
            print(f"OCR processing page {i+1}...")
            ocr_text += pytesseract.image_to_string(image, lang='eng')
        return ocr_text.strip()

    except Exception as e:
        print(f"OCR failed: {e}")
        return ""