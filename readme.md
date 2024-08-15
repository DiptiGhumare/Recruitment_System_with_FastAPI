## Recruitment System with FastAPI

### Objective:
Develop a comprehensive recruitment system using FastAPI that includes features for user authentication, job posting, viewing, updating, job application, resume uploading, and viewing candidate details. The system will interact with MongoDB for data storage and retrieval.

### Requirements:
User Authentication:
Implement user signup and login functionality.
Use OAuth2 with token-based authentication for secure access.

### Job Management:
Allow authorized users to post, view, and update job listings.
Store job details such as title, description, department, location, employment type, salary range, application deadline, required skills, additional information, and status.

### Job Application:
Enable candidates to apply for jobs.
Allow candidates to upload resumes.

### Resume Management:
Store and retrieve resumes uploaded by candidates.
Allow authorized users to view candidate details and resumes.

### Implementation:
FastAPI:
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

### Project Description
This project provides a comprehensive recruitment system with an API for user authentication, job management, job applications, and resume management. The API interacts with MongoDB for efficient data storage and retrieval, ensuring a seamless and secure recruitment process.

### Key Features
User Authentication: Secure signup and login functionality.
Job Management: Create, view, and update job postings.
Job Application: Apply for jobs and upload resumes.
Resume Management: Store and view candidate resumes.

### Requirements
Python 3.8+
FastAPI
Uvicorn
Motor (MongoDB driver)
Pydantic
Passlib (for password hashing)
PyJWT (for token handling)
MongoDB

### Set Up a Virtual Environment
python -m venv .venv
source .venv/bin/activate

### Install Required Packages:
pip install -r requirements.txt

### Running the Application
Start the FastAPI Server:
uvicorn main:app --reload

### Access API Documentation:
Open a web browser and navigate to http://127.0.0.1:8000/docs to view the interactive API documentation.

### API Endpoints

POST /signup: User signup.
POST /login: User login.
POST /jobs: Create a new job posting.
GET /jobs: View all job postings.
GET /jobs/{job_id}: View a specific job posting.
PUT /jobs/{job_id}: Update a specific job posting.
POST /apply/{job_id}: Apply for a job and upload a resume.
GET /candidates/{job_id}: View candidates who applied for a specific job.
GET /resumes/{candidate_id}: View a specific candidate's resume.

### Directory Structure


├── main.py                   # Main FastAPI application
├── auth.py                   # Authentication logic
├── jobs.py                   # Job management logic
├── applications.py           # Job application logic
├── data.py                   # Functions for saving data
├── requirements.txt          # List of required Python packages
├── uploads/                  # Directory to save uploaded resumes
├── results/                  # Directory to store job postings and applications

### File Descriptions
main.py:
The main entry point for the FastAPI application. It defines the API endpoints and orchestrates the job management, application, and authentication processes.

### auth.py:
Implements user authentication functionality, including signup and login, and handles token-based authentication using OAuth2.

### jobs.py:
Contains logic for creating, viewing, and updating job postings.

### applications.py:
Handles job application functionality, including applying for jobs and uploading resumes.

### data.py:
Includes functions to save and retrieve data from MongoDB, ensuring secure and efficient data management.

### requirements.txt:
Lists all the dependencies required for the project, including FastAPI, Uvicorn, Motor (MongoDB driver), Pydantic, Passlib, and PyJWT.
