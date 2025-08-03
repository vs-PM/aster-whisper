import tempfile
from fastapi import APIRouter, HTTPException
from pathlib import Path

from ..db.docx_dao import MfgBotDAO
from v1.config.docx_config import docx_settings
from .schemas import DocxGenerateRequest, DocxGenerateResponse
from .utils import extract_tags_from_docx, generate_filled_docx

router = APIRouter(
    prefix="/docx",
    tags=["Docx"]
)

@router.get("/ping", summary="Проверка docx-сервиса")
def ping():
    return {"status": "docx ok"}

@router.post("/generate", response_model=DocxGenerateResponse)
async def generate_docx(request: DocxGenerateRequest):
    # Используем настройки из единого конфига
    template_path = docx_settings.TEMPLATE_PATH
    
    if not template_path or not template_path.is_file():
        raise HTTPException(
            status_code=500,
            detail=f"Template file not found at {template_path}"
        )

    tags = extract_tags_from_docx(str(template_path))
    db_row = await MfgBotDAO.get_by_id(request.id)
    
    if not db_row:
        raise HTTPException(
            status_code=404,
            detail=f"Document with id {request.id} not found"
        )

    fill_values = {tag: getattr(db_row[0], tag, None) for tag in tags}
    if request.values:
        fill_values.update(request.values)
    
    missing_fields = [tag for tag in tags if tag not in fill_values]
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing fields: {', '.join(missing_fields)}"
        )

    output_filename = f"docx_{request.id}_output.docx"
    output_path = Path(tempfile.gettempdir()) / output_filename
    
    generate_filled_docx(str(template_path), str(output_path), fill_values)
    
    return DocxGenerateResponse(
        status="success",
        filename=output_filename
    )
