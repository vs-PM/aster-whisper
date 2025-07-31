from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from . import Base

class WhisperTranscript(Base):
    __tablename__ = "whisper_transcripts"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=True)
    channel_id = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
