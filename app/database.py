from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base     # changed to relative import
# from .models import AudioMetadata
# Corrected spelling of AudioMetadata and moved import in right place

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():

    """Create database tables based on models."""
    print(f"Using database at: {SQLALCHEMY_DATABASE_URL}")
    try:
        print("Models imported successfully.")
        # print(f"Tables in metadata before create_all: {Base.metadata.tables.keys()}")
        print(f"before create_all: {Base.metadata.tables.keys()}")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
        # print(f"Tables in metadata after create_all: {Base.metadata.tables.keys()}")
        print(f"after create_all: {Base.metadata.tables.keys()}")
    except Exception as e:
        print(f"Error creating tables: {e}")


if __name__ == "__main__":
    create_tables()
