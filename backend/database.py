# Import necessary SQLAlchemy components
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite connection URL (database file will be named 'users.db')
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Create the SQLAlchemy engine that manages DB connections
# `connect_args={"check_same_thread": False}` is needed for SQLite in multi-threaded FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "SessionLocal" class that will create DB sessions
# Used in routes via `Depends(get_db)`
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models (used by models.py)
# All models will inherit from this to register with metadata
Base = declarative_base()
