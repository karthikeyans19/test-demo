from sqlalchemy import Column, Integer, String, Float, DateTime
from app.base import Base
from datetime import datetime, timezone

class AudioMetadata(Base):


    __tablename__ = "audio_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    # timestamp = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # changed from String to DateTime
    file_name = Column(String)
    length_seconds = Column(Float)   # changed from Integer to Float
    # print("AudioMetadata")