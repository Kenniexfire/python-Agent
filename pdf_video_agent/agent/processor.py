import pdfplumber
from agent.claude_client import generate_content

def process_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    generate_content(text)