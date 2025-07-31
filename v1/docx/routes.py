
from fastapi import APIRouter, HTTPException
import os
import tempfile
from .utils import extract_tags_from_docx, generate_filled_docx
from .schemas import DocxGenerateRequest, DocxGenerateResponse
from ..db.docx_dao import MfgBotDAO


router = APIRouter(
    prefix="/docx",
    tags=["Docx"]
)


@router.get(
    "/ping",
    summary="Проверка docx-сервиса",
    description="Проверка работоспособности docx-сервиса."
)
def ping():
    return {"status": "docx ok"}


@router.post(
    "/generate",
    response_model=DocxGenerateResponse,
    summary="Генерация docx",
    description="Генерирует docx-файл по шаблону на основе данных из БД и запроса."
)
async def generate_docx(request: DocxGenerateRequest):
    template_path = os.getenv('DOCX_TEMPLATE_PATH', 'template.docx')
    if not os.path.isfile(template_path):
        raise HTTPException(status_code=500, detail="Template file not found.")

    tags = extract_tags_from_docx(template_path)
    db_row = await MfgBotDAO.get_by_id(request.id)
    if not db_row:
        raise HTTPException(status_code=404, detail=f"Document with id {request.id} not found")

    fill_values = {tag: getattr(db_row[0], tag, None) for tag in tags}
    if request.values:
        fill_values.update(request.values)
    missing_fields = [tag for tag in tags if tag not in fill_values]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing fields: {', '.join(missing_fields)}")

    output_filename = f"docx_{request.id}_output.docx"
    tmp_dir = tempfile.gettempdir()
    output_path = os.path.join(tmp_dir, output_filename)
    generate_filled_docx(template_path, output_path, fill_values)
    return DocxGenerateResponse(status="success", filename=output_filename)
