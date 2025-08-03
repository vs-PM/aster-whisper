from pydantic_settings import BaseSettings
from pydantic import Field, validator
from pathlib import Path
from typing import Optional

class DocxSettings(BaseSettings):
    SHARED_DIR: Path = Field(..., description="Директория для общих документов")
    TEMPLATE_FILENAME: str = Field(..., description="Имя файла шаблона")
    TEMPLATE_PATH: Optional[Path] = Field(None, description="Полный путь к шаблону")

    @validator('SHARED_DIR', 'TEMPLATE_PATH', pre=True)
    def validate_paths(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            return Path(value)
        return value

    @validator('TEMPLATE_PATH', always=True)
    def assemble_template_path(cls, v, values):
        if v:
            return v
        if 'SHARED_DIR' in values and 'TEMPLATE_FILENAME' in values:
            return values['SHARED_DIR'] / values['TEMPLATE_FILENAME']
        raise ValueError("Необходимо указать либо TEMPLATE_PATH, либо SHARED_DIR и TEMPLATE_FILENAME")

    class Config:
        env_file = ".env"
        env_prefix = "DOCX_"
        case_sensitive = False
        extra = "ignore"

docx_settings = DocxSettings()
