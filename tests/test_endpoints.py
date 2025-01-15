from datetime import datetime, timezone
from fastapi.encoders import isoformat
from fastapi.testclient import TestClient
from app.main import app
import base64
import json
from app.schemas import ProcessAudioResponse

client = TestClient(app)

def test_process_audio_valid():
    payload = {
        "session_id": "test_session",
         "timestamp": datetime.now(timezone.utc).isoformat(),
        "audio_files": [
            {
                "file_name": "test.wav",
                "encoded_audio": base64.b64encode(b"\x01" * 8000).decode()
            }
        ]
    }
    response = client.post("/process-audio", json=payload)
    #assert response.status_code == 200
    #assert response.status_code == 400
    if response.status_code != 200:
        print(f"Response status code: {response.status_code}")
        print(f"Response JSON: {json.dumps(response.json(), indent=4)}")
        print(response.json())  # Print the response JSON for debugging
    assert response.status_code == 200
    response_json = response.json()
    assert response_json()["status"] == "success"
    assert len(response_json()["processed_files"]) == 1
    

def test_process_audio_invalid_base64():
    payload = {
        "session_id": "test_session",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "audio_files": [
            {
                "file_name": "test_file.wav",
                "encoded_audio": "InvalidBase64String==="
            }
        ]
    }
    response = client.post("/process-audio", json=payload)
    #assert response.status_code == 400
    assert response.status_code == 422  # Expecting 422 Unprocessable Entity
    response_json = response.json()

