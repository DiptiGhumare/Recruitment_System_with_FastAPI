# auth.py
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext
from bson import ObjectId
import certifi

# MongoDB setup
client = MongoClient(f"mongodb+srv://diptighumare2002:System22@cluster0.4ysuay5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tlsCAFile=certifi.where())
db = client['Recruitment']
candidates_collection = db['recruitment_candidate']

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Utility functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = candidates_collection.find_one({"username": username})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = candidates_collection.find_one({"token": token})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Pydantic models
class Candidate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    is_admin: bool = False  # Add this field to the Candidate model

# Authentication routes
def setup_auth_routes(app):
    @app.post("/signup")
    def signup(candidate: Candidate):
        try:
            hashed_password = get_password_hash(candidate.password)
            candidate_data = candidate.dict()
            candidate_data["password"] = hashed_password
            candidates_collection.insert_one(candidate_data)
            logger.info(f"New user signed up: {candidate.username}")
            return {"message": "Signup successful"}
        except Exception as e:
            logger.error(f"Error occurred while signing up: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @app.post("/token")
    def login(form_data: OAuth2PasswordRequestForm = Depends()):
        try:
            user = authenticate_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            token = str(ObjectId())
            candidates_collection.update_one({"_id": user["_id"]}, {"$set": {"token": token}})
            logger.info(f"User logged in: {form_data.username}")
            return {"access_token": token, "token_type": "bearer"}
        except Exception as e:
            logger.error(f"Error occurred while logging in: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
