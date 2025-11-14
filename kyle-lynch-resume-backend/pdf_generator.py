from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from io import BytesIO
import tempfile
import os
from typing import Dict, Any

class ParchmentResumeGenerator:
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom parchment-themed styles"""
        # Title style - large, bold, center
        self.styles.add(ParagraphStyle(
            name='ParchmentTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.Color(0.545, 0.271, 0.075),  # Saddle brown
            alignment=1,  # Center
            spaceAfter=12,
            fontName='Times-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='ParchmentSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.Color(0.545, 0.271, 0.075),
            alignment=1,
            spaceAfter=20,
            fontName='Times-Italic'
        ))
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='ParchmentHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.Color(0.545, 0.271, 0.075),
            spaceBefore=20,
            spaceAfter=10,
            fontName='Times-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='ParchmentBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.Color(0.4, 0.2, 0.1),
            spaceAfter=6,
            fontName='Times-Roman'
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.Color(0.545, 0.271, 0.075),
            alignment=1,
            spaceAfter=10,
            fontName='Times-Roman'
        ))
    
    def generate_resume_pdf(self, resume_data: Dict[Any, Any]) -> bytes:
        """Generate PDF resume with parchment styling"""
        buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        story = []
        
        # Header section
        story.extend(self._build_header(resume_data))
        
        # Highlights section
        story.extend(self._build_highlights(resume_data))
        
        # Experience section
        story.extend(self._build_experience(resume_data))
        
        # Education section
        story.extend(self._build_education(resume_data))
        
        # Skills section
        story.extend(self._build_skills(resume_data))
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_parchment_background,
                 onLaterPages=self._add_parchment_background)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    
    def _add_parchment_background(self, canvas, doc):
        """Add parchment-style background to pages"""
        # Set background color to warm cream
        canvas.setFillColor(colors.Color(0.957, 0.945, 0.910))  # Warm cream
        canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        
        # Add decorative border
        canvas.setStrokeColor(colors.Color(0.545, 0.271, 0.075))  # Saddle brown
        canvas.setLineWidth(2)
        canvas.rect(50, 50, letter[0]-100, letter[1]-100, fill=0, stroke=1)
        
        # Add inner border
        canvas.setStrokeColor(colors.Color(0.627, 0.322, 0.176))  # Sienna
        canvas.setLineWidth(1)
        canvas.rect(60, 60, letter[0]-120, letter[1]-120, fill=0, stroke=1)
    
    def _build_header(self, resume_data: Dict[Any, Any]) -> list:
        """Build header section"""
        story = []
        personal_info = resume_data.get('personal_info', {})
        
        # Name
        name = personal_info.get('name', 'Kyle J. Lynch')
        story.append(Paragraph(name, self.styles['ParchmentTitle']))
        
        # Title
        title = personal_info.get('title', 'Facilities Coordinator & Technical Systems Professional')
        story.append(Paragraph(title, self.styles['ParchmentSubtitle']))
        
        # Contact information
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        
        contact_text = ' • '.join(contact_parts)
        story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        if personal_info.get('linkedin'):
            linkedin_text = f"LinkedIn: {personal_info['linkedin']}"
            story.append(Paragraph(linkedin_text, self.styles['ContactInfo']))
        
        story.append(Spacer(1, 20))
        return story
    
    def _build_highlights(self, resume_data: Dict[Any, Any]) -> list:
        """Build highlights section"""
        story = []
        highlights = resume_data.get('highlights', [])
        
        if highlights:
            story.append(Paragraph("Highlights of Qualifications", self.styles['ParchmentHeading']))
            
            for highlight in highlights:
                bullet_text = f"• {highlight}"
                story.append(Paragraph(bullet_text, self.styles['ParchmentBody']))
            
            story.append(Spacer(1, 15))
        
        return story
    
    def _build_experience(self, resume_data: Dict[Any, Any]) -> list:
        """Build experience section"""
        story = []
        experiences = resume_data.get('experience', [])
        
        if experiences:
            story.append(Paragraph("Professional Experience", self.styles['ParchmentHeading']))
            
            for exp in experiences:
                # Position and company
                position_text = f"<b>{exp.get('position', '')}</b>"
                story.append(Paragraph(position_text, self.styles['ParchmentBody']))
                
                # Company and location
                company_info = f"{exp.get('company', '')} • {exp.get('location', '')}"
                story.append(Paragraph(company_info, self.styles['ParchmentBody']))
                
                # Duration
                duration = exp.get('duration', '')
                if exp.get('current'):
                    duration += " (Current)"
                story.append(Paragraph(f"<i>{duration}</i>", self.styles['ParchmentBody']))
                
                # Description
                description = exp.get('description', '')
                story.append(Paragraph(description, self.styles['ParchmentBody']))
                
                # Achievements
                achievements = exp.get('achievements', [])
                if achievements:
                    for achievement in achievements:
                        story.append(Paragraph(f"• {achievement}", self.styles['ParchmentBody']))
                
                story.append(Spacer(1, 12))
        
        return story
    
    def _build_education(self, resume_data: Dict[Any, Any]) -> list:
        """Build education section"""
        story = []
        education = resume_data.get('education', [])
        
        if education:
            story.append(Paragraph("Education & Certifications", self.styles['ParchmentHeading']))
            
            for edu in education:
                # Degree
                degree_text = f"<b>{edu.get('degree', '')}</b>"
                story.append(Paragraph(degree_text, self.styles['ParchmentBody']))
                
                # Institution and location
                institution_info = edu.get('institution', '')
                if edu.get('location'):
                    institution_info += f" • {edu['location']}"
                story.append(Paragraph(institution_info, self.styles['ParchmentBody']))
                
                # Duration
                duration = edu.get('duration', '')
                story.append(Paragraph(f"<i>{duration}</i>", self.styles['ParchmentBody']))
                
                story.append(Spacer(1, 8))
        
        return story
    
    def _build_skills(self, resume_data: Dict[Any, Any]) -> list:
        """Build skills section"""
        story = []
        skills = resume_data.get('skills', [])
        
        if skills:
            story.append(Paragraph("Core Competencies", self.styles['ParchmentHeading']))
            
            # Create skills as a comma-separated list
            skills_text = ' • '.join(skills)
            story.append(Paragraph(skills_text, self.styles['ParchmentBody']))
        
        return story

# Global PDF generator instance
pdf_generator = ParchmentResumeGenerator()
