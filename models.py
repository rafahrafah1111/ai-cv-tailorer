from pydantic import BaseModel, Field
from typing import List, Optional

class ProfileSummary(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number with country code")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")

class ExperienceItem(BaseModel):
    company: str = Field(description="Name of the company or institution")
    role: str = Field(description="Job title or role")
    duration: str = Field(description="Time period, e.g., 'October 2025 - Present'")
    bullet_points: List[str] = Field(description="Key responsibilities and achievements tailored to the role")

class EducationItem(BaseModel):
    institution: str = Field(description="University or training center name")
    degree: str = Field(description="Degree or program name")
    duration: str = Field(description="Graduation year or duration")

class TailoredCV(BaseModel):
    profile: ProfileSummary
    objective: str = Field(description="Professional summary optimized for the target job description")
    experience: List[ExperienceItem]
    education: List[EducationItem]
    skills: List[str] = Field(description="List of technical and core skills relevant to the role")