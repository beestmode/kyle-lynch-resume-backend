# Kyle Lynch Resume Backend

FastAPI backend for the interactive parchment resume application.

## Deployment Instructions

### Environment Variables Required:
```
MONGO_URL=mongodb+srv://machinatax_db_user:YDlTtsDF65rbwl9A@resumecluster.ga7e4xy.mongodb.net/?retryWrites=true&w=majority&appName=ResumeCluster
DB_NAME=resume_db  
SECRET_KEY=kyle-lynch-resume-secret-key-2025
PORT=8001
```

### Railway Deployment:
1. Connect this GitHub repo to Railway
2. Add environment variables above
3. Railway will auto-deploy from `server.py`

### Default Admin Access:
- Username: `admin`
- Password: `admin123` 
- **⚠️ Change this password in production!**

### Features:
- Resume CRUD operations
- Contact form handling  
- PDF generation
- JWT authentication
- MongoDB integration

### API Endpoints:
- `GET /api/` - Health check
- `GET /api/resume` - Get resume data
- `POST /api/contact` - Submit contact form
- `POST /api/auth/login` - Admin login
- `PUT /api/resume/experience/{id}` - Update experience
- `GET /api/resume/download-pdf` - Download PDF

Built for Kyle Lynch's professional resume at kylelynch.site