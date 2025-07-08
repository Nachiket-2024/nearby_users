# Import FastAPI core components
from fastapi import FastAPI, Depends, HTTPException

# Import SQLAlchemy session type
from sqlalchemy.orm import Session

# Import DB setup: session factory and engine
from .database import SessionLocal, engine

# Import User model and Base class
from .model import Base, User

# Import CRUD logic (we'll define this in crud.py)
from .user_operations import fetch_and_store_users, get_random_user, get_nearest_users

# Import request/response schemas
from .schema import UserCreate, UserOut

# Create FastAPI app instance
app = FastAPI()

# Create database tables if they don't exist already
Base.metadata.create_all(bind=engine)

# Dependency that provides a DB session to each request
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db          # Yield it to the route handler
    finally:
        db.close()        # Close it when done

# POST endpoint to fetch users and store them in DB
@app.post("/fetch-users/")
def fetch_users(num_users: int, db: Session = Depends(get_db)):
    # Compute run_id = batch number
    run_id = db.query(User).count() // num_users + 1

    # Call helper to fetch from randomuser.me and store
    fetch_and_store_users(db, num_users, run_id)

    return {"status": "Users fetched and stored", "run_id": run_id}

# GET endpoint to retrieve one random user from DB
@app.get("/random-user/", response_model=UserOut)
def random_user(db: Session = Depends(get_db)):
    user = get_random_user(db)
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return user

# GET endpoint to retrieve nearest users to a given user ID
@app.get("/nearest-users/", response_model=list[UserOut])
def nearest_users(uid: int, num_users: int, db: Session = Depends(get_db)):
    try:
        users = get_nearest_users(db, uid, num_users)
        if not users:
            raise HTTPException(status_code=404, detail="No nearest users found")
        return users
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
