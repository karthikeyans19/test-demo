from fastapi import FastAPI, HTTPException, Depends
from app.schemas import ProcessAudioRequest, ProcessAudioResponse
from app.models import AudioMetadata 
from app.database import SessionLocal, engine
import numpy as np
import base64
from sqlalchemy.orm import Session

app = FastAPI()

SAMPLE_RATE = 4000 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/process-audio", response_model=ProcessAudioResponse)
async def process_audio(request: ProcessAudioRequest, db: Session = Depends(get_db)):
    processed_files = []

    for audio_file in request.audio_files:
        try:
            decoded_audio = base64.b64decode(audio_file.encoded_audio)
            
            audio_data = np.frombuffer(decoded_audio, dtype=np.int16)

            length_seconds = len(audio_data) // SAMPLE_RATE
            
            if length_seconds <= 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid audio length: {length_seconds:.2f}s"
                )

            db_metadata = AudioMetadata(
                session_id=request.session_id,
                timestamp=request.timestamp,
                file_name=audio_file.file_name,
                length_seconds=length_seconds
            )
            db.add(db_metadata)
            db.commit()
            db.refresh(db_metadata)

            processed_files.append({
                "file_name": audio_file.file_name,
                "length_seconds": length_seconds
            })

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing file {audio_file.file_name}: {str(e)}"
            )

    return ProcessAudioResponse(
        status="success",
        processed_files=processed_files
    )
