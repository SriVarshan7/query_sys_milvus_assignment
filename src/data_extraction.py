import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import pdfplumber

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_url(url):
    """Extract text from a URL using BeautifulSoup."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Error extracting text from URL: {e}")
        return None

def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None