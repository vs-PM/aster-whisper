from pydantic import BaseModel
from typing import Optional

class WhisperTranscriptCreate(BaseModel):
    file_name: str
    channel_id: Optional[str] = None
    text: str
