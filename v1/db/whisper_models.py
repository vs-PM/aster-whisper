from sqlalchemy import TIMESTAMP, Column, Integer, String, Text

# Модель для существующей таблицы vosk_text (без создания через Base)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VoskText(Base):
    __tablename__ = "vosk_text"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=True)
    channel_id = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
