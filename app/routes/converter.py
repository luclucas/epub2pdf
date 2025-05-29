from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.convert_service import convert_epub_to_pdf
import os

router = APIRouter(prefix='/convert', tags=['Conversão'])

@router.post('/epub-to-pdf')
async def upload_epub(file: UploadFile = File(...)):
    if not file.filename.endswith('.epub'):
        raise HTTPException(status_code=400, detail='arquivo no formato errado')
    pdf_path = await convert_epub_to_pdf(file)
    return FileResponse(path=pdf_path, filename=os.path.basename(pdf_path), media_type='application/pdf')

