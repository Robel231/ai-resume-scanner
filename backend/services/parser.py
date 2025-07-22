

import fitz  
from fastapi import UploadFile

def extract_text_from_pdf(file: UploadFile) -> str:
    
    try:
        
        file_content = file.file.read()

        
        pdf_document = fitz.open(stream=file_content, filetype="pdf")

        
        text = ""
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        pdf_document.close()
        return text

    except Exception as e:
        print(f"Error parsing PDF: {e}")
        
        
        return f"Error: Could not parse the PDF file '{file.filename}'. It may be corrupted or in an unsupported format."