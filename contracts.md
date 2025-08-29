# Kyle Lynch Parchment Resume - Backend Integration Contracts

## Overview
This document outlines the API contracts and integration requirements for the interactive parchment resume application for Kyle Lynch.

## Current Mock Data Implementation
The frontend currently uses mock data from `/app/frontend/src/data/mock.js` which includes:
- Personal information (name, email, phone, LinkedIn, location)
- Professional highlights
- Work experience history (9 positions)
- Education & certifications (6 entries)
- Core skills/competencies

## Required Backend API Endpoints

### 1. Resume Data Management

#### GET /api/resume
- **Purpose**: Retrieve complete resume data
- **Response**: Full resume object with all sections
- **Mock Data Source**: `resumeData` from mock.js

#### PUT /api/resume/personal-info
- **Purpose**: Update personal information
- **Request Body**: 
```json
{
  "name": "string",
  "email": "string", 
  "phone": "string",
  "linkedin": "string",
  "title": "string",
  "location": "string"
}
```

#### PUT /api/resume/highlights
- **Purpose**: Update professional highlights
- **Request Body**: 
```json
{
  "highlights": ["string", "string"]
}
```

### 2. Experience Management

#### GET /api/resume/experience
- **Purpose**: Get all work experiences
- **Response**: Array of experience objects

#### POST /api/resume/experience
- **Purpose**: Add new work experience
- **Request Body**:
```json
{
  "position": "string",
  "company": "string", 
  "location": "string",
  "duration": "string",
  "description": "string",
  "current": "boolean",
  "achievements": ["string"]
}
```

#### PUT /api/resume/experience/:id
- **Purpose**: Update existing work experience
- **Frontend Integration**: EditExperienceModal component
- **Request Body**: Same as POST experience

#### DELETE /api/resume/experience/:id
- **Purpose**: Remove work experience

### 3. Education Management

#### GET /api/resume/education
- **Purpose**: Get all education entries

#### POST /api/resume/education
- **Purpose**: Add new education/certification

#### PUT /api/resume/education/:id
- **Purpose**: Update education entry

#### DELETE /api/resume/education/:id
- **Purpose**: Remove education entry

### 4. Skills Management

#### PUT /api/resume/skills
- **Purpose**: Update skills list
- **Request Body**:
```json
{
  "skills": ["string", "string", "string"]
}
```

### 5. Contact & Communication

#### POST /api/contact
- **Purpose**: Handle contact form submissions
- **Frontend Integration**: ContactForm component
- **Request Body**:
```json
{
  "name": "string",
  "email": "string",
  "subject": "string", 
  "message": "string",
  "recipientEmail": "kyle.lynch@comcast.net"
}
```

### 6. PDF Generation

#### GET /api/resume/download-pdf
- **Purpose**: Generate and download resume as PDF
- **Frontend Integration**: Download PDF button in ParchmentResume component
- **Response**: PDF file with parchment styling

### 7. Authentication (CMS Access)

#### POST /api/auth/login
- **Purpose**: Admin login for CMS functionality
- **Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

#### GET /api/auth/verify
- **Purpose**: Verify authentication token
- **Headers**: Authorization: Bearer <token>

#### POST /api/auth/logout
- **Purpose**: Logout and invalidate token

## Database Schema Requirements

### Resume Collection
```javascript
{
  _id: ObjectId,
  personalInfo: {
    name: String,
    email: String,
    phone: String, 
    linkedin: String,
    title: String,
    location: String
  },
  highlights: [String],
  experience: [{
    _id: ObjectId,
    position: String,
    company: String,
    location: String,
    duration: String,
    description: String,
    current: Boolean,
    achievements: [String],
    sortOrder: Number,
    createdAt: Date,
    updatedAt: Date
  }],
  education: [{
    _id: ObjectId,
    degree: String,
    institution: String,
    location: String,
    duration: String,
    sortOrder: Number
  }],
  skills: [String],
  createdAt: Date,
  updatedAt: Date
}
```

### Contact Messages Collection
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  subject: String,
  message: String,
  recipientEmail: String,
  status: String, // 'new', 'read', 'replied'
  createdAt: Date,
  ipAddress: String
}
```

### Users Collection (Admin)
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  passwordHash: String,
  role: String, // 'admin'
  lastLogin: Date,
  createdAt: Date
}
```

## Frontend Integration Points

### Components Requiring Backend Integration:
1. **ParchmentResume.jsx** - Main resume display
2. **ContactForm.jsx** - Contact form submissions  
3. **EditExperienceModal.jsx** - Experience editing functionality

### Mock Data Removal:
- Remove mock.js imports from components
- Replace with API calls using axios
- Add loading states and error handling
- Implement authentication context for admin features

### Environment Variables:
- Backend will use existing REACT_APP_BACKEND_URL from frontend/.env
- All API calls will use `/api` prefix for proper routing

## Security Considerations:
- JWT authentication for admin access
- Rate limiting on contact form
- Input validation and sanitization
- CORS configuration for frontend domain
- Password hashing with bcrypt

## Implementation Priority:
1. Resume data CRUD operations
2. Contact form functionality  
3. PDF generation
4. Authentication system
5. Admin CMS features

This contract ensures seamless integration between the existing frontend mock implementation and the upcoming backend development.