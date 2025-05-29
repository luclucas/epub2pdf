import os
from uuid import uuid4
from fastapi import UploadFile
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


UPLOAD_DIR = 'uploaded_epubs'
OUTPUT_DIR = 'converted_pdfs'

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def convert_epub_to_pdf(file: UploadFile) -> str:
    file_id = str(uuid4())
    epub_path = os.path.join(UPLOAD_DIR, f"{file_id}.epub")
    pdf_path = os.path.join(OUTPUT_DIR, f'{file_id}.pdf')

    with open(epub_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    
    book = epub.read_epub(epub_path)
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text().strip()
            if text: 
                paragraphs = text.split('\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), styles['Normal']))
                        story.append(Spacer(1,12))
    doc.build(story)
    return pdf_path