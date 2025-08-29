from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid
from enum import Enum

class ContactStatus(str, Enum):
    NEW = "new"
    READ = "read"
    REPLIED = "replied"

# Personal Information Models
class PersonalInfo(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    linkedin: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=200)
    location: str = Field(..., min_length=1, max_length=100)

class PersonalInfoUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    linkedin: Optional[str] = Field(None, min_length=1)
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1, max_length=100)

# Experience Models
class Experience(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    position: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    location: str = Field(..., min_length=1, max_length=100)
    duration: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1)
    current: bool = False
    achievements: List[str] = Field(default_factory=list)
    sort_order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ExperienceCreate(BaseModel):
    position: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    location: str = Field(..., min_length=1, max_length=100)
    duration: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1)
    current: bool = False
    achievements: List[str] = Field(default_factory=list)
    sort_order: Optional[int] = 0

class ExperienceUpdate(BaseModel):
    position: Optional[str] = Field(None, min_length=1, max_length=200)
    company: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1, max_length=100)
    duration: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1)
    current: Optional[bool] = None
    achievements: Optional[List[str]] = None
    sort_order: Optional[int] = None

# Education Models
class Education(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    degree: str = Field(..., min_length=1, max_length=200)
    institution: str = Field(..., min_length=1, max_length=200)
    location: str = Field(..., max_length=100)
    duration: str = Field(..., min_length=1, max_length=50)
    sort_order: int = Field(default=0)

class EducationCreate(BaseModel):
    degree: str = Field(..., min_length=1, max_length=200)
    institution: str = Field(..., min_length=1, max_length=200)
    location: str = Field(default="", max_length=100)
    duration: str = Field(..., min_length=1, max_length=50)
    sort_order: Optional[int] = 0

class EducationUpdate(BaseModel):
    degree: Optional[str] = Field(None, min_length=1, max_length=200)
    institution: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, max_length=100)
    duration: Optional[str] = Field(None, min_length=1, max_length=50)
    sort_order: Optional[int] = None

# Skills Models
class SkillsUpdate(BaseModel):
    skills: List[str] = Field(..., min_items=1)

class HighlightsUpdate(BaseModel):
    highlights: List[str] = Field(..., min_items=1)

# Resume Models
class Resume(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    personal_info: PersonalInfo
    highlights: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Contact Models
class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1)
    recipient_email: EmailStr
    status: ContactStatus = ContactStatus.NEW
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = None

class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1)
    recipient_email: Optional[EmailStr] = Field(default="kclynch@uh.edu")

# User Models (for authentication)
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password_hash: str
    role: str = Field(default="admin")
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

# Response Models
class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: Optional[str] = None