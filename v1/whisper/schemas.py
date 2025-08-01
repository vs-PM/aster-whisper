from typing import Optional

from pydantic import BaseModel


class WhisperTranscriptCreate(BaseModel):
    file_name: str
    channel_id: Optional[str] = None
    text: str
