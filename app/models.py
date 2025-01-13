from sqlalchemy import Column, Integer, String   # Error : remove Float as it is not used
from app.base import Base
# from datetime import datetime   # Error : remove datetime.datetime as it is not used


class AudioMetadata(Base):
    __tablename__ = "audio_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    timestamp = Column(String)
    file_name = Column(String)

    length_seconds = Column(Integer)
