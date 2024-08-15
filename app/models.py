from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Candidate(BaseModel):
    email: EmailStr
    password: str
    name: str
    resume: Optional[str] = None

class Admin(BaseModel):
    email: EmailStr
    password: str

class Job(BaseModel):
    title: str
    description: str
    department: str
    location: str
    employment_type: str
    salary_range: Optional[str] = None
    application_deadline: Optional[datetime] = None
    required_skills: List[str]
    additional_info: Optional[str] = None
    status: str
