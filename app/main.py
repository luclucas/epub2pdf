from fastapi import FastAPI
from app.routes import converter

app = FastAPI(title='EPUB to PDF')

app.include_router(converter.router)