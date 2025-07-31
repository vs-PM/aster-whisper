from pydantic_settings import BaseSettings
from dotenv import load_dotenv; load_dotenv()

class DocxSettings(BaseSettings):
    DOCX_SHARED_DIR: str
    DOCX_TEMPLATE_FILENAME: str = "template.docx"

docx_settings = DocxSettings()
