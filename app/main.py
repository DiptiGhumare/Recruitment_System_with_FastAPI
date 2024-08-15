# main.py
import logging
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
import shutil
import os
from dotenv import load_dotenv
import certifi
from auth import setup_auth_routes, get_current_user, Candidate

# Load environment variables
load_dotenv()

# MongoDB password obtained from environment variable
mongodb_password = os.getenv("System22")

# MongoDB setup
client = MongoClient(f"mongodb+srv://diptighumare2002:System22@cluster0.4ysuay5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tlsCAFile=certifi.where())
db = client['Recruitment']
candidates_collection = db['recruitment_candidate']
jobs_collection = db['jobs']
resumes_collection = db['resumes']

# FastAPI setup
app = FastAPI()

# Initialize logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Pydantic models
class Job(BaseModel):
    title: str
    description: str
    department: str
    location: str
    employment_type: str
    salary_range: Optional[str] = None
    application_deadline: Optional[str] = None
    required_skills: List[str]
    additional_information: Optional[str] = None
    status: str = "Open"

# Setup authentication routes
setup_auth_routes(app)

# Job routes
@app.get("/jobs", response_model=List[Job])
def view_jobs():
    try:
        jobs = list(jobs_collection.find())
        return jobs
    except Exception as e:
        logger.error(f"Error occurred while retrieving jobs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/jobs")
def post_job(job: Job, current_user: dict = Depends(get_current_user)):
    try:
        if not current_user.get("is_admin"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        job_data = job.dict()
        jobs_collection.insert_one(job_data)
        logger.info(f"Job posted: {job.title}")
        return {"message": "Job posted successfully"}
    except Exception as e:
        logger.error(f"Error occurred while posting job: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.put("/jobs/{job_id}")
def update_job(job_id: str, job: Job, current_user: dict = Depends(get_current_user)):
    try:
        if not current_user.get("is_admin"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        jobs_collection.update_one({"_id": ObjectId(job_id)}, {"$set": job.dict()})
        logger.info(f"Job updated: {job_id}")
        return {"message": "Job updated successfully"}
    except Exception as e:
        logger.error(f"Error occurred while updating job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/apply/{job_id}")
def apply_job(job_id: str, current_user: dict = Depends(get_current_user)):
    try:
        application = {"candidate_id": current_user["_id"], "job_id": job_id}
        db["applications"].insert_one(application)
        logger.info(f"Job application submitted: {job_id} by {current_user['_id']}")
        return {"message": "Job application successful"}
    except Exception as e:
        logger.error(f"Error occurred while applying for job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/upload_resume")
def upload_resume(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    try:
        # Ensure the resumes directory exists
        os.makedirs("resumes", exist_ok=True)
        
        file_location = f"resumes/{current_user['_id']}.pdf"
        
        # Save the uploaded file to the file system
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Insert file path information into the database
        resumes_collection.insert_one({"candidate_id": current_user["_id"], "file_path": file_location})
        
        logger.info(f"Resume uploaded for user: {current_user['_id']}")
        return {"message": "Resume uploaded successfully"}
    except Exception as e:
        logger.error(f"Error occurred while uploading resume: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/candidates", response_model=List[Candidate])
def view_candidates(current_user: dict = Depends(get_current_user)):
    try:
        if not current_user.get("is_admin"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        candidates = list(candidates_collection.find())
        return candidates
    except Exception as e:
        logger.error(f"Error occurred while retrieving candidates: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/resumes")
def view_resumes(current_user: dict = Depends(get_current_user)):
    try:
        if not current_user.get("is_admin"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        
        # Fetch resumes from the database
        resumes = list(resumes_collection.find())
        
        # Ensure the resumes are returned in a proper format
        response = []
        for resume in resumes:
            resume_data = {
                "candidate_id": str(resume["candidate_id"]),
                "file_path": resume["file_path"]
            }
            response.append(resume_data)
        
        logger.info("Resumes retrieved successfully")
        return response
    except Exception as e:
        logger.error(f"Error occurred while retrieving resumes: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
