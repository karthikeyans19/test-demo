import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import AudioMetadata  # Use relative import
from app.base import Base  # Use relative import

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

def test_create_read_update_audio_metadata(db_session):
    # Create
    audio = AudioMetadata(
        session_id="test_session",
        timestamp="2023-01-01T00:00:00",
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
