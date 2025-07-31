from pydantic import BaseModel
from typing import Dict, Optional

class DocxGenerateRequest(BaseModel):
    id: int
    values: Optional[Dict[str, str]] = None

class DocxGenerateResponse(BaseModel):
    status: str
    filename: str
    detail: Optional[str] = None
