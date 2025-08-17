# ---------------------------- External Imports ----------------------------

# Import SQLAlchemy column types used for model field definitions
from sqlalchemy import Column, Integer, String, Float, DateTime

# ---------------------------- Internal Imports ----------------------------

# Import the declarative base class from your local database setup
# All models will inherit from this Base
from .database import Base

# ---------------------------- Model: User ----------------------------

# SQLAlchemy model representing a "users" table in the database
class User(Base):
    """
    Defines the database structure for storing user information.
    Each instance corresponds to a row in the 'users' table.
    """
    
    # Define the table name in the database
    __tablename__ = "users"

    # ---------------------------- Columns ----------------------------

    # Primary key column (auto-incrementing integer)
    id = Column(Integer, primary_key=True, index=True)

    # Email of the user, must be unique and not null
    email = Column(String, unique=True, index=True, nullable=False)

    # First name of the user, cannot be null
    first_name = Column(String, nullable=False)

    # Last name of the user, cannot be null
    last_name = Column(String, nullable=False)

    # Gender of the user, stored as a string ("male"/"female"), cannot be null
    gender = Column(String, nullable=False)

    # Latitude of the user's location, required for proximity logic
    latitude = Column(Float, nullable=False)

    # Longitude of the user's location, required for proximity logic
    longitude = Column(Float, nullable=False)

    # Batch run ID for tracking which API fetch this user came from
    run_id = Column(Integer, nullable=False)

    # Timestamp of when the user was fetched and stored
    ingestion_time = Column(DateTime, nullable=False)
