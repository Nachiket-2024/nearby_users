# ---------------------------- External Imports ----------------------------

# Import requests to call the RandomUser API
import requests

# Import SQLAlchemy session and SQL functions
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

# Import datetime for timestamp parsing
from datetime import datetime

# Import math for Haversine distance calculations
import math

# ---------------------------- Internal Imports ----------------------------

# Import the User model
from .model import User

# ---------------------------- Function: fetch_and_store_users ----------------------------

def fetch_and_store_users(db: Session, num_users: int, run_id: int):
    """
    Fetch 'num_users' users from randomuser.me API and store them in the database.
    Each user is assigned the provided 'run_id'.
    """
    # Call the RandomUser API with the specified number of results
    response = requests.get(f"https://randomuser.me/api/?results={num_users}")

    # Raise an exception if the API call fails
    if response.status_code != 200:
        raise Exception("Failed to fetch users from RandomUser API")

    # Parse JSON response to extract user data
    users = response.json()["results"]

    # Loop through each user and create a User object for the database
    for user_data in users:
        user_obj = User(
            email=user_data["email"],  # User's email
            first_name=user_data["name"]["first"],  # First name
            last_name=user_data["name"]["last"],    # Last name
            gender=user_data["gender"],             # Gender
            latitude=float(user_data["location"]["coordinates"]["latitude"]),  # Latitude
            longitude=float(user_data["location"]["coordinates"]["longitude"]),# Longitude
            run_id=run_id,                          # Batch/run ID
            ingestion_time=datetime.fromisoformat(
                user_data["registered"]["date"].replace("Z", "+00:00")
            ),  # Timestamp of registration
        )
        db.add(user_obj)  # Add the user to the database session

    db.commit()  # Commit all added users at once

# ---------------------------- Function: get_random_user ----------------------------

def get_random_user(db: Session) -> User | None:
    """
    Retrieve a random user from the database.
    Returns None if the database is empty.
    """
    return db.query(User).order_by(func.random()).first()

# ---------------------------- Function: haversine ----------------------------

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points 
    on the Earth specified in decimal degrees using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371.0  # Radius of Earth in kilometers
    # Convert degrees to radians
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c  # Distance in km

# ---------------------------- Function: get_nearest_users ----------------------------

def get_nearest_users(db: Session, uid: int, num_users: int) -> list[User]:
    """
    Retrieve 'num_users' closest users to the user with ID 'uid'.
    Raises ValueError if the reference user does not exist.
    """
    # Get the reference user by ID
    ref_user = db.query(User).filter(User.id == uid).first()
    if not ref_user:
        raise ValueError("User not found")

    # Fetch all other users excluding the reference user
    other_users = db.query(User).filter(User.id != uid).all()

    # Calculate Haversine distance to each other user
    users_with_distance = [
        (user, haversine(ref_user.latitude, ref_user.longitude, user.latitude, user.longitude))
        for user in other_users
    ]

    # Sort users by distance
    sorted_users = sorted(users_with_distance, key=lambda x: x[1])

    # Return only the User objects of the closest 'num_users' users
    return [user for user, dist in sorted_users[:num_users]]
