import app.models
import app.database
import app.schemas
from typing import Union, Optional, Dict, Any, List

async def create_candidate(candidate: app.models.Candidate) -> None:
    """Create a new candidate."""
    await app.database.db.candidates.insert_one(candidate.dict())

async def get_user_by_email(email: str) -> Union[app.models.Candidate, app.models.Admin, None]:
    """
    Retrieve a user by email.
    This function searches for a candidate first, 
    if not found, it searches for an admin.
    """
    candidate = await app.database.db.candidates.find_one({"email": email})
    if candidate:
        return candidate
    else:
        return await app.database.db.admins.find_one({"email": email})

async def create_job(job: app.models.Job) -> None:
    """Create a new job."""
    await app.database.db.jobs.insert_one(job.dict())

async def update_job(job_id: str, job: app.schemas.JobUpdate) -> None:
    """Update an existing job."""
    await app.database.db.jobs.update_one({"_id": app.schemas.ObjectId(job_id)}, {"$set": job.dict(exclude_unset=True)})

async def get_all_jobs() -> List[Dict[str, Any]]:
    """Get all jobs."""
    return await app.database.db.jobs.find().to_list(100)

async def get_all_candidates() -> List[Dict[str, Any]]:
    """Get all candidates."""
    return await app.database.db.candidates.find().to_list(100)
