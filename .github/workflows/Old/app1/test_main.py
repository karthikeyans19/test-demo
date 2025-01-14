import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
import numpy as np
import base64
from main import app, get_db
from schemas import ProcessAudioRequest, AudioFile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

print("started")

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_process_audio_success():
    print("Test Started1")
    audio_data = np.zeros(4000, dtype=np.int16).tobytes()
    encoded_audio = base64.b64encode(audio_data).decode('utf-8')
    request_data = ProcessAudioRequest(
        session_id="test_session",
        timestamp="2023-01-01T00:00:00Z",
        audio_files=[AudioFile(file_name="test.wav", encoded_audio=encoded_audio)]
    )
    response = client.post("/process-audio", json=request_data.dict())
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["processed_files"]) == 1
    assert response.json()["processed_files"][0]["file_name"] == "test.wav"
    assert response.json()["processed_files"][0]["length_seconds"] == 1

    print("Test Passed")

def test_process_audio_invalid_length():
    audio_data = np.zeros(2000, dtype=np.int16).tobytes()
    encoded_audio = base64.b64encode(audio_data).decode('utf-8')
    request_data = ProcessAudioRequest(
        session_id="test_session",
        timestamp="2023-01-01T00:00:00Z",
        audio_files=[AudioFile(file_name="test.wav", encoded_audio=encoded_audio)]
    )
    response = client.post("/process-audio", json=request_data.dict())
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid audio length: 0.50s"

def test_process_audio_invalid_base64():
    request_data = ProcessAudioRequest(
        session_id="test_session",
        timestamp="2023-01-01T00:00:00Z",
        audio_files=[AudioFile(file_name="test.wav", encoded_audio="invalid_base64")]
    )
    response = client.post("/process-audio", json=request_data.dict())
    assert response.status_code == 400
    assert "Error processing file test.wav" in response.json()["detail"]