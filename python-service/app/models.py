from pydantic import BaseModel
from typing import List

# Pydantic models for API validation
class Candidate(BaseModel):
    name: str
    job_position: str
    skills: str
    qualifications: str
    years_of_experience: int
    email:str
    password:str

class Expert(BaseModel):
    name: str
    email:str
    password:str
    skills: str
    qualifications: str
    years_of_experience: int
    date_of_availability: str
