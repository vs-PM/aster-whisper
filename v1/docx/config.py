
import os

from pydantic_settings import BaseSettings

from dotenv import load_dotenv; load_dotenv()

class DocxSettings(BaseSettings):
    DOCX_SHARED_DIR: str = os.getenv("DOCX_SHARED_DIR", "path_to_shared_dir")
    DOCX_TEMPLATE_FILENAME: str = os.getenv("DOCX_TEMPLATE_FILENAME", "template.docx")
    DOCX_TEMPLATE_PATH: str = os.getenv("DOCX_TEMPLATE_PATH", "template.docx")

docx_settings = DocxSettings()
