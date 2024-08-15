from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://diptighumare2002:System22@cluster0.4ysuay5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Initialize MongoDB client
try:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client['Recruitment']
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

# Collections
candidates_collection = db['recruitment_candidate']
jobs_collection = db['jobs']
resumes_collection = db['resumes']
