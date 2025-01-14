from sqlalchemy import Column, Integer, String, Float
from .base import Base    # changed to relative import
from datetime import datetime

class AudioMetadata(Base):
    __tablename__ = "audio_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    timestamp = Column(String)
    file_name = Column(String)
    
    length_seconds = Column(Integer)
