import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.models import AudioMetadata
from app.base import Base
from datetime import datetime, timezone

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_read_update_delete_audio_metadata(db_session: Session):
    # Create audio metadata
    audio = AudioMetadata(
        session_id="test_session",
        #timestamp=datetime.strptime("2025-01-14T00:00:00", "%Y-%m-%dT%H:%M:%S"),
        #timestamp=datetime.now(),
        timestamp=datetime.now(timezone.utc),
        file_name="test_file.wav",
        length_seconds=180
    )
    db_session.add(audio)
    db_session.commit()
    print("Audio metadata created successfully.")

    # Read audio metadata
    fetched_audio = db_session.query(AudioMetadata).filter_by(file_name="test_file.wav").first()
    assert fetched_audio is not None
    assert fetched_audio.length_seconds == 180
    print("Audio metadata fetched successfully.")

    # Update audio metadata
    fetched_audio.length_seconds = 150
    db_session.commit()
    updated_audio = db_session.query(AudioMetadata).filter_by(file_name="test_file.wav").first()
    assert updated_audio.length_seconds == 150
    print("Audio metadata updated successfully.")

    # Delete audio metadata
    db_session.delete(updated_audio)
    db_session.commit()
    assert db_session.query(AudioMetadata).filter_by(file_name="test_file.wav").first() is None
    print("Audio metadata deleted successfully.")
    