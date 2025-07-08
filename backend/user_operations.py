# Import typing and dependencies
import requests
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime

# Import your User model and schema
from .model import User
from .schema import UserCreate

# for distance calculation
import math  

# Function to fetch N users from RandomUser API and store them in the database
def fetch_and_store_users(db: Session, num_users: int, run_id: int):
    # Call the RandomUser API with desired number of results
    response = requests.get(f"https://randomuser.me/api/?results={num_users}")

    # Raise exception if the API call fails
    if response.status_code != 200:
        raise Exception("Failed to fetch users from RandomUser API")

    # Parse JSON response
    users = response.json()["results"]

    # Loop through users and store them in DB
    for user_data in users:
        user_obj = User(
            email=user_data["email"],
            first_name=user_data["name"]["first"],
            last_name=user_data["name"]["last"],
            gender=user_data["gender"],
            latitude=float(user_data["location"]["coordinates"]["latitude"]),
            longitude=float(user_data["location"]["coordinates"]["longitude"]),
            run_id=run_id,
            ingestion_time=datetime.fromisoformat(user_data["registered"]["date"].replace("Z", "+00:00")),
        )
        db.add(user_obj)  # Add user to session

    db.commit()  # Commit all users at once

# Function to return a random user from the database
def get_random_user(db: Session) -> User | None:
    return db.query(User).order_by(func.random()).first()

# Function to compute the Haversine distance between two points
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers

# Function to get N users closest to a given user ID
def get_nearest_users(db: Session, uid: int, num_users: int) -> list[User]:
    # Get the reference user by ID
    ref_user = db.query(User).filter(User.id == uid).first()
    if not ref_user:
        raise ValueError("User not found")

    # Fetch all other users except the reference user
    other_users = db.query(User).filter(User.id != uid).all()

    # Calculate distance to each user
    users_with_distance = [
        (user, haversine(ref_user.latitude, ref_user.longitude, user.latitude, user.longitude))
        for user in other_users
    ]

    # Sort by distance and return the top N
    sorted_users = sorted(users_with_distance, key=lambda x: x[1])
    return [user for user, dist in sorted_users[:num_users]]
