# ---------------------------- External Imports ----------------------------

# Import the base class for all Pydantic models
from pydantic import BaseModel

# Import datetime class for timestamp fields
from datetime import datetime

# ---------------------------- Schema: UserCreate ----------------------------

# Schema for incoming user creation requests or internal DB insertions
class UserCreate(BaseModel):
    """
    Defines the data structure required to create a new user.
    All fields correspond to database columns or API input fields.
    """
    
    # User's email address (used as unique identifier)
    email: str

    # First name of the user
    first_name: str

    # Last name of the user
    last_name: str

    # Gender of the user ("male" or "female", based on RandomUser API)
    gender: str

    # Latitude coordinate of the user (used for proximity queries)
    latitude: float

    # Longitude coordinate of the user (used for proximity queries)
    longitude: float

    # Run ID to group which API batch the user came from
    run_id: int

    # Timestamp indicating when the user was ingested into the database
    ingestion_time: datetime

# ---------------------------- Schema: UserOut ----------------------------

# Schema for returning user objects in API responses
# This extends UserCreate but includes the database-assigned ID
class UserOut(UserCreate):
    """
    Schema used when sending user data back in API responses.
    Inherits all fields from UserCreate and adds the database ID.
    """
    
    # ID is the primary key of the user record (added by the DB)
    id: int

    # Enables compatibility with SQLAlchemy ORM objects
    class Config:
        # Allows Pydantic to read data directly from ORM objects
        from_attributes = True
