# ---------------------------- External Imports ----------------------------

# Import FastAPI core components to create app, handle dependencies, and HTTP exceptions
from fastapi import FastAPI, Depends, HTTPException

# Import SQLAlchemy Session type for type hints and dependency injection
from sqlalchemy.orm import Session

# ---------------------------- Internal Imports ----------------------------

# Import database session factory and engine from local database module
from .database import SessionLocal, engine

# Import User model and Base metadata for table creation
from .model import Base, User

# Import CRUD operations for users
from .user_operations import fetch_and_store_users, get_random_user, get_nearest_users

# Import request/response Pydantic schemas
from .schema import UserOut

# ---------------------------- FastAPI App Instance ----------------------------

# Create an instance of the FastAPI application
app = FastAPI()

# ---------------------------- Database Initialization ----------------------------

# Create all database tables defined in Base.metadata (if they don't already exist)
Base.metadata.create_all(bind=engine)

# ---------------------------- Dependency: Database Session ----------------------------

# Dependency function that yields a database session for request handlers
def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session to the route
        yield db
    finally:
        # Close the session after request is complete
        db.close()

# ---------------------------- Route: POST /fetch-users/ ----------------------------

# Route to fetch users from external API and store in the database
@app.post("/fetch-users/")
def fetch_users(num_users: int, db: Session = Depends(get_db)):
    """
    Fetch 'num_users' users from randomuser.me API and store in the database.
    Returns status and run_id.
    """
    # Compute run_id as the batch number based on how many users already exist
    run_id = db.query(User).count() // num_users + 1

    # Call helper function to fetch users and store them in DB
    fetch_and_store_users(db, num_users, run_id)

    # Return success message with batch/run ID
    return {"status": "Users fetched and stored", "run_id": run_id}

# ---------------------------- Route: GET /random-user/ ----------------------------

# Route to retrieve a random user from the database
@app.get("/random-user/", response_model=UserOut)
def random_user(db: Session = Depends(get_db)):
    """
    Retrieve one random user from the database.
    Raises 404 if no users are found.
    """
    # Call helper function to get a random user
    user = get_random_user(db)

    # Raise 404 error if database is empty
    if not user:
        raise HTTPException(status_code=404, detail="No users found")

    # Return the retrieved user
    return user

# ---------------------------- Route: GET /nearest-users/ ----------------------------

# Route to retrieve nearest users to a given user ID
@app.get("/nearest-users/", response_model=list[UserOut])
def nearest_users(uid: int, num_users: int, db: Session = Depends(get_db)):
    """
    Retrieve 'num_users' closest users to the user with ID 'uid'.
    Raises 404 if no users are found, 400 for invalid input.
    """
    try:
        # Call helper function to find nearest users
        users = get_nearest_users(db, uid, num_users)

        # Raise 404 error if no nearest users found
        if not users:
            raise HTTPException(status_code=404, detail="No nearest users found")

        # Return list of nearest users
        return users

    except ValueError as e:
        # Invalid input (e.g., user ID doesn't exist)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch-all for unexpected server errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
