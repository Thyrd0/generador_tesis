from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from generators.content_generator import ContentGenerator
from generators.document_generator import DocumentGenerator

app = FastAPI(title="API Generador de Proyecto de Tesis")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse
import os

# Modelos de datos
class TesisRequest(BaseModel):
    tema: str
    autores: List[str]
    asesor: str
    linea_investigacion: str
    ciudad: str
    año: int
    jurados: Optional[dict] = None
    gemini_api_key: Optional[str] = None

class TesisResponse(BaseModel):
    contenido: dict
    mensaje: str

class ExportRequest(BaseModel):
    request_data: TesisRequest
    contenido: dict

# Instancias de generadores
content_gen = ContentGenerator()
doc_gen = DocumentGenerator()

@app.post("/generar_tesis", response_model=TesisResponse)
async def generar_tesis(request: TesisRequest):
    try:
        # Generar contenido estructurado
        contenido = content_gen.generar_contenido_completo(request)
        
        return TesisResponse(
            contenido=contenido,
            mensaje="Proyecto de tesis generado exitosamente"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/exportar_pdf")
async def exportar_pdf(export_req: ExportRequest):
    try:
        pdf_path = doc_gen.generar_pdf(export_req.contenido, export_req.request_data)
        return {"pdf_path": pdf_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/exportar_docx")
async def exportar_docx(export_req: ExportRequest):
    try:
        docx_path = doc_gen.generar_docx(export_req.contenido, export_req.request_data)
        return {"docx_path": docx_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/descargar_archivo")
async def descargar_archivo(filepath: str):
    try:
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        # Asegurar que esté dentro del directorio de generados por seguridad
        normalized_path = os.path.normpath(filepath)
        if not (normalized_path.startswith("generated_docs") or normalized_path.startswith("backend\\generated_docs") or normalized_path.startswith("backend/generated_docs")):
            raise HTTPException(status_code=403, detail="Acceso denegado")
        return FileResponse(normalized_path, media_type='application/octet-stream', filename=os.path.basename(normalized_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)