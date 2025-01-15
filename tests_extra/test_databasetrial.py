import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import AudioMetadata  # Use relative import
from app.base import Base  # Use relative import
from app.database import create_tables, SessionLocal  # Use absolute import
from datetime import datetime

@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()

def test_create_tables():
    try:
        create_tables()
        assert True
    except Exception as e:
        pytest.fail(f"Table creation failed: {e}")

def test_crud_operations(db_session):
    # Create
    audio = AudioMetadata(
        session_id="test_session",
        # timestamp=datetime.strptime("2025-01-14T00:00:00", "%Y-%m-%dT%H:%M:%S"),  # Ensure timestamp is a datetime object
        timestamp=datetime.now(),
        file_name="test_file.wav",
        length_seconds=120
    )
    db_session.add(audio)
    db_session.commit()
    
    # Read
    fetched_audio = db_session.query(AudioMetadata).filter_by(file_name="test_file.wav").first()
    assert fetched_audio is not None
    assert fetched_audio.length_seconds == 120

    # Update
    fetched_audio.length_seconds = 150
    db_session.commit()
    updated_audio = db_session.query(AudioMetadata).filter_by(file_name="test_file.wav").first()
    assert updated_audio.length_seconds == 150

    # Delete
    db_session.delete(updated_audio)
    db_session.commit()
    assert db_session.query(AudioMetadata).filter_by(file_name="test_file.wav").first() is None
