from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import timedelta
import os
import logging
from pathlib import Path
from io import BytesIO

# Import our modules
from models import *
from database import ResumeDatabase, ContactDatabase, UserDatabase
from auth import authenticate_user, create_access_token, get_current_user, require_admin, create_default_admin
from pdf_generator import pdf_generator

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(title="Kyle Lynch Resume API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database with default data"""
    await create_default_admin()
    # Initialize resume data if needed
    await ResumeDatabase.get_resume()
    logger.info("✅ Resume API server started successfully")

# Health check
@api_router.get("/")
async def root():
    return {"message": "Kyle Lynch Resume API is running", "status": "healthy"}

# Resume endpoints
@api_router.get("/resume", response_model=dict)
async def get_resume():
    """Get complete resume data"""
    try:
        resume = await ResumeDatabase.get_resume()
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Remove MongoDB _id field
        resume.pop('_id', None)
        return resume
    except Exception as e:
        logger.error(f"Error fetching resume: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.put("/resume/personal-info")
async def update_personal_info(
    personal_info: PersonalInfoUpdate,
    current_user: dict = Depends(require_admin)
):
    """Update personal information (admin only)"""
    try:
        # Convert to dict and remove None values
        update_data = {k: v for k, v in personal_info.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid data provided")
        
        success = await ResumeDatabase.update_personal_info(update_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update personal information")
        
        return SuccessResponse(message="Personal information updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating personal info: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.put("/resume/highlights")
async def update_highlights(
    highlights_data: HighlightsUpdate,
    current_user: dict = Depends(require_admin)
):
    """Update professional highlights (admin only)"""
    try:
        success = await ResumeDatabase.update_highlights(highlights_data.highlights)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update highlights")
        
        return SuccessResponse(message="Highlights updated successfully")
    except Exception as e:
        logger.error(f"Error updating highlights: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.put("/resume/skills")
async def update_skills(
    skills_data: SkillsUpdate,
    current_user: dict = Depends(require_admin)
):
    """Update skills list (admin only)"""
    try:
        success = await ResumeDatabase.update_skills(skills_data.skills)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update skills")
        
        return SuccessResponse(message="Skills updated successfully")
    except Exception as e:
        logger.error(f"Error updating skills: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Experience endpoints
@api_router.get("/resume/experience")
async def get_experiences():
    """Get all work experiences"""
    try:
        experiences = await ResumeDatabase.get_experiences()
        return {"experiences": experiences}
    except Exception as e:
        logger.error(f"Error fetching experiences: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.post("/resume/experience")
async def add_experience(
    experience: ExperienceCreate,
    current_user: dict = Depends(require_admin)
):
    """Add new work experience (admin only)"""
    try:
        # Convert to Experience model to get ID and timestamps
        exp_data = Experience(**experience.dict()).dict()
        
        success = await ResumeDatabase.add_experience(exp_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to add experience")
        
        return SuccessResponse(message="Experience added successfully", data={"id": exp_data["id"]})
    except Exception as e:
        logger.error(f"Error adding experience: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.put("/resume/experience/{exp_id}")
async def update_experience(
    exp_id: str,
    experience: ExperienceUpdate,
    current_user: dict = Depends(require_admin)
):
    """Update existing work experience (admin only)"""
    try:
        # Convert to dict and remove None values
        update_data = {k: v for k, v in experience.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid data provided")
        
        success = await ResumeDatabase.update_experience(exp_id, update_data)
        if not success:
            raise HTTPException(status_code=404, detail="Experience not found")
        
        return SuccessResponse(message="Experience updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating experience: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.delete("/resume/experience/{exp_id}")
async def delete_experience(
    exp_id: str,
    current_user: dict = Depends(require_admin)
):
    """Delete work experience (admin only)"""
    try:
        success = await ResumeDatabase.delete_experience(exp_id)
        if not success:
            raise HTTPException(status_code=404, detail="Experience not found")
        
        return SuccessResponse(message="Experience deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting experience: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Education endpoints
@api_router.get("/resume/education")
async def get_education():
    """Get all education entries"""
    try:
        education = await ResumeDatabase.get_education()
        return {"education": education}
    except Exception as e:
        logger.error(f"Error fetching education: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.post("/resume/education")
async def add_education(
    education: EducationCreate,
    current_user: dict = Depends(require_admin)
):
    """Add new education entry (admin only)"""
    try:
        edu_data = Education(**education.dict()).dict()
        
        success = await ResumeDatabase.add_education(edu_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to add education")
        
        return SuccessResponse(message="Education added successfully", data={"id": edu_data["id"]})
    except Exception as e:
        logger.error(f"Error adding education: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.put("/resume/education/{edu_id}")
async def update_education(
    edu_id: str,
    education: EducationUpdate,
    current_user: dict = Depends(require_admin)
):
    """Update existing education entry (admin only)"""
    try:
        update_data = {k: v for k, v in education.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid data provided")
        
        success = await ResumeDatabase.update_education(edu_id, update_data)
        if not success:
            raise HTTPException(status_code=404, detail="Education entry not found")
        
        return SuccessResponse(message="Education updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating education: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.delete("/resume/education/{edu_id}")
async def delete_education(
    edu_id: str,
    current_user: dict = Depends(require_admin)
):
    """Delete education entry (admin only)"""
    try:
        success = await ResumeDatabase.delete_education(edu_id)
        if not success:
            raise HTTPException(status_code=404, detail="Education entry not found")
        
        return SuccessResponse(message="Education deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting education: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Contact form endpoint
@api_router.post("/contact")
async def submit_contact_form(message: ContactMessageCreate):
    """Handle contact form submissions"""
    try:
        # Create contact message
        contact_data = ContactMessage(**message.dict()).dict()
        
        # Save to database
        message_id = await ContactDatabase.save_contact_message(contact_data)
        
        # Send email notification (mock for now)
        logger.info(f"New contact message received from {message.email}: {message.subject}")
        
        return SuccessResponse(
            message="Message sent successfully! Kyle will get back to you soon.",
            data={"message_id": message_id}
        )
    except Exception as e:
        logger.error(f"Error handling contact form: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send message")

# PDF generation endpoint
@api_router.get("/resume/download-pdf")
async def download_resume_pdf():
    """Generate and download resume as PDF"""
    try:
        # Get resume data
        resume_data = await ResumeDatabase.get_resume()
        if not resume_data:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Generate PDF
        pdf_bytes = pdf_generator.generate_resume_pdf(resume_data)
        
        # Create response
        buffer = BytesIO(pdf_bytes)
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=Kyle_Lynch_Resume.pdf"}
        )
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

# Authentication endpoints
@api_router.post("/auth/login", response_model=Token)
async def login(user_login: UserLogin):
    """Admin login"""
    try:
        user = await authenticate_user(user_login.username, user_login.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login
        await UserDatabase.update_last_login(user["username"])
        
        # Create access token
        access_token_expires = timedelta(minutes=1440)  # 24 hours
        access_token = create_access_token(
            data={"sub": user["username"]}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@api_router.get("/auth/verify")
async def verify_token(current_user: dict = Depends(get_current_user)):
    """Verify authentication token"""
    return SuccessResponse(
        message="Token is valid",
        data={
            "username": current_user["username"],
            "role": current_user["role"],
            "email": current_user["email"]
        }
    )

@api_router.post("/auth/logout")
async def logout():
    """Logout (client should remove token)"""
    return SuccessResponse(message="Logged out successfully")

# Admin endpoints
@api_router.get("/admin/contact-messages")
async def get_contact_messages(
    current_user: dict = Depends(require_admin),
    limit: int = 50
):
    """Get contact messages (admin only)"""
    try:
        messages = await ContactDatabase.get_contact_messages(limit)
        return {"messages": messages}
    except Exception as e:
        logger.error(f"Error fetching contact messages: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.put("/admin/contact-messages/{message_id}/read")
async def mark_message_read(
    message_id: str,
    current_user: dict = Depends(require_admin)
):
    """Mark contact message as read (admin only)"""
    try:
        success = await ContactDatabase.mark_message_as_read(message_id)
        if not success:
            raise HTTPException(status_code=404, detail="Message not found")
        
        return SuccessResponse(message="Message marked as read")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking message as read: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Include the router in the main app
app.include_router(api_router)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Resume API server shutting down")

if __name__ == "__main__":
    import uvicorn
    # Use Railway's PORT environment variable or default to 8001
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)