# ---------------------------- External Imports ----------------------------

# Import SQLAlchemy components to create engine, base, and sessions
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------------------------- Database Configuration ----------------------------

# SQLite connection URL (database file will be named 'users.db')
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# ---------------------------- SQLAlchemy Engine ----------------------------

# Create the SQLAlchemy engine that manages DB connections
# `connect_args={"check_same_thread": False}` allows multi-threaded access for FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# ---------------------------- Session Factory ----------------------------

# Create a configured "SessionLocal" class that will generate DB sessions
# Used in FastAPI route dependencies via `Depends(get_db)`
SessionLocal = sessionmaker(
    autocommit=False,  # Disable autocommit; commit manually
    autoflush=False,   # Disable autoflush; flush manually
    bind=engine        # Bind this session to the engine
)

# ---------------------------- Declarative Base ----------------------------

# Base class for all ORM models (used in models.py)
# All SQLAlchemy models will inherit from this class to register with metadata
Base = declarative_base()
