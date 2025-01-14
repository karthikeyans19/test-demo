import pytest
from app.schemas import AudioFile
import base64

def test_valid_audio_file():
    encoded_audio = base64.b64encode(b"\x01" * 8000).decode()
    audio_file = AudioFile(file_name="valid.wav", encoded_audio=encoded_audio)
    assert audio_file.file_name == "valid.wav"

def test_invalid_base64():
    with pytest.raises(ValueError, match="Invalid base64-encoded string"):
        AudioFile(file_name="invalid.wav", encoded_audio="InvalidBase64")

def test_short_audio():
    encoded_audio = base64.b64encode(b"\x01" * 2000).decode()
    with pytest.raises(ValueError, match="Audio file is too short"):
        AudioFile(file_name="short.wav", encoded_audio=encoded_audio)