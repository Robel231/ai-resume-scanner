# backend/services/parser.py

import fitz  # PyMuPDF
from fastapi import UploadFile

def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extracts text content from an uploaded PDF file.
    """
    try:
        # Read the file content into memory
        file_content = file.file.read()

        # Open the PDF from the in-memory content
        pdf_document = fitz.open(stream=file_content, filetype="pdf")

        # Initialize an empty string to store the text
        text = ""
        # Iterate over each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        pdf_document.close()
        return text

    except Exception as e:
        print(f"Error parsing PDF: {e}")
        # Depending on requirements, you might want to raise a custom exception
        # or return an error message.
        return f"Error: Could not parse the PDF file '{file.filename}'. It may be corrupted or in an unsupported format."