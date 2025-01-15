from pydantic import BaseModel, field_validator  # field-removed as it is unused
from typing import List, Optional
from datetime import datetime
import base64
import numpy as np


class AudioFile(BaseModel):
    file_name: str
    encoded_audio: str


    @classmethod
    def validate_base64(cls, encoded_audio: str):
        try:
            return base64.b64decode(encoded_audio)
        except Exception:
            raise ValueError("Invalid Base64 encoding")


    @field_validator('encoded_audio')
    def validate_audio_length(cls, encoded_audio: str):
        from app.main import SAMPLE_RATE
        
        decoded_audio = base64.b64decode(encoded_audio)
        
        audio_data = np.frombuffer(decoded_audio, dtype=np.int16)

        if len(audio_data) == 0:
            raise ValueError("Audio file is empty or has no valid data")

        min_length_samples = SAMPLE_RATE
        if len(audio_data) < min_length_samples:
            raise ValueError(f"Audio file is too short. Minimum length is {len(audio_data) / SAMPLE_RATE} seconds.")

        return encoded_audio

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_base64
        yield cls.validate_audio_length


class ProcessAudioRequest(BaseModel):
    session_id: str
    timestamp: datetime
    audio_files: List[AudioFile]

    class ConfigDict:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ProcessAudioResponse(BaseModel):
    status: str
    processed_files: Optional[List[dict]] = None
