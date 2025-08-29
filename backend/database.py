from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from models import Resume, Experience, Education, ContactMessage, User
from datetime import datetime

# Database configuration
mongo_url = os.environ.get('MONGO_URL')

# For Railway deployment, add SSL parameters if not in connection string
if mongo_url and 'ssl=true' not in mongo_url and 'tls=true' not in mongo_url:
    separator = '&' if '?' in mongo_url else '?'
    mongo_url += f'{separator}ssl=true&retryWrites=true&w=majority'

client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'resume_db')]

# Collections
resumes_collection = db.resumes
contacts_collection = db.contact_messages
users_collection = db.users

class ResumeDatabase:
    
    @staticmethod
    async def get_resume() -> Optional[dict]:
        """Get the main resume document"""
        resume = await resumes_collection.find_one({"active": True})
        if not resume:
            # Create default resume if none exists
            await ResumeDatabase.create_default_resume()
            resume = await resumes_collection.find_one({"active": True})
        return resume
    
    @staticmethod
    async def create_default_resume():
        """Create default resume from mock data"""
        from data.mock import resumeData
        
        default_resume = {
            "active": True,
            "personal_info": resumeData["personalInfo"],
            "highlights": resumeData["highlights"],
            "experience": resumeData["experience"],
            "education": resumeData["education"],
            "skills": resumeData["skills"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await resumes_collection.insert_one(default_resume)
    
    @staticmethod
    async def update_personal_info(personal_info: dict) -> bool:
        """Update personal information"""
        # Create update fields with dot notation to merge instead of replace
        update_fields = {}
        for key, value in personal_info.items():
            update_fields[f"personal_info.{key}"] = value
        
        update_fields["updated_at"] = datetime.utcnow()
        
        result = await resumes_collection.update_one(
            {"active": True},
            {"$set": update_fields}
        )
        return result.modified_count > 0
    
    @staticmethod
    async def update_highlights(highlights: list) -> bool:
        """Update professional highlights"""
        result = await resumes_collection.update_one(
            {"active": True},
            {
                "$set": {
                    "highlights": highlights,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    @staticmethod
    async def update_skills(skills: list) -> bool:
        """Update skills list"""
        result = await resumes_collection.update_one(
            {"active": True},
            {
                "$set": {
                    "skills": skills,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    @staticmethod
    async def get_experiences() -> list:
        """Get all work experiences"""
        resume = await ResumeDatabase.get_resume()
        return resume.get("experience", []) if resume else []
    
    @staticmethod
    async def add_experience(experience: dict) -> bool:
        """Add new work experience"""
        experience["created_at"] = datetime.utcnow()
        experience["updated_at"] = datetime.utcnow()
        
        result = await resumes_collection.update_one(
            {"active": True},
            {
                "$push": {"experience": experience},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    @staticmethod
    async def update_experience(exp_id: str, experience: dict) -> bool:
        """Update existing work experience"""
        experience["updated_at"] = datetime.utcnow()
        
        result = await resumes_collection.update_one(
            {"active": True, "experience.id": exp_id},
            {
                "$set": {
                    **{f"experience.$.{k}": v for k, v in experience.items()},
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    @staticmethod
    async def delete_experience(exp_id: str) -> bool:
        """Remove work experience"""
        result = await resumes_collection.update_one(
            {"active": True},
            {
                "$pull": {"experience": {"id": exp_id}},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    @staticmethod
    async def get_education() -> list:
        """Get all education entries"""
        resume = await ResumeDatabase.get_resume()
        return resume.get("education", []) if resume else []
    
    @staticmethod
    async def add_education(education: dict) -> bool:
        """Add new education entry"""
        result = await resumes_collection.update_one(
            {"active": True},
            {
                "$push": {"education": education},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    @staticmethod
    async def update_education(edu_id: str, education: dict) -> bool:
        """Update existing education entry"""
        result = await resumes_collection.update_one(
            {"active": True, "education.id": edu_id},
            {
                "$set": {
                    **{f"education.$.{k}": v for k, v in education.items()},
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    @staticmethod
    async def delete_education(edu_id: str) -> bool:
        """Remove education entry"""
        result = await resumes_collection.update_one(
            {"active": True},
            {
                "$pull": {"education": {"id": edu_id}},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0

class ContactDatabase:
    
    @staticmethod
    async def save_contact_message(message: dict) -> str:
        """Save contact form message"""
        message["created_at"] = datetime.utcnow()
        result = await contacts_collection.insert_one(message)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_contact_messages(limit: int = 50) -> list:
        """Get recent contact messages"""
        cursor = contacts_collection.find().sort("created_at", -1).limit(limit)
        messages = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            messages.append(doc)
        return messages
    
    @staticmethod
    async def mark_message_as_read(message_id: str) -> bool:
        """Mark message as read"""
        from bson import ObjectId
        result = await contacts_collection.update_one(
            {"_id": ObjectId(message_id)},
            {"$set": {"status": "read"}}
        )
        return result.modified_count > 0

class UserDatabase:
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[dict]:
        """Get user by username"""
        return await users_collection.find_one({"username": username})
    
    @staticmethod
    async def create_user(user: dict) -> str:
        """Create new user"""
        user["created_at"] = datetime.utcnow()
        result = await users_collection.insert_one(user)
        return str(result.inserted_id)
    
    @staticmethod
    async def update_last_login(username: str) -> bool:
        """Update user's last login time"""
        result = await users_collection.update_one(
            {"username": username},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        return result.modified_count > 0