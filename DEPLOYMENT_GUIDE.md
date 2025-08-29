# Kyle Lynch Resume - Deployment Guide

## Recommended Setup: kylelynch.site

**Architecture:**
- **Frontend**: Static React build → kylelynch.site (DreamHost)  
- **Backend**: FastAPI → Railway/Render (free tier)
- **Database**: MongoDB Atlas (free tier)

## Step 1: Get Domain & Setup DNS
1. **Register kylelynch.site** 
2. **Point domain to DreamHost** (update nameservers)
3. **Add domain in DreamHost panel**

## Step 2: Setup Database (MongoDB Atlas)
1. **Go to**: https://www.mongodb.com/atlas
2. **Create free account** → Create free cluster
3. **Database Access**: Create user with read/write permissions
4. **Network Access**: Add IP 0.0.0.0/0 (allow all - for development)
5. **Get connection string**: mongodb+srv://username:password@cluster.mongodb.net/resume_db
6. **Save this** - you'll need it for backend deployment

## Step 3: Deploy Backend to Railway
1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **New Project** → Deploy from GitHub repo
4. **Upload these backend files to GitHub:**
   ```
   backend/
   ├── server.py
   ├── models.py  
   ├── database.py
   ├── auth.py
   ├── pdf_generator.py
   ├── requirements.txt
   └── data/mock.py
   ```

5. **Environment Variables in Railway:**
   ```
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DB_NAME=resume_db
   SECRET_KEY=your-secret-key-here
   PORT=8001
   ```

6. **Railway will give you a URL**: https://your-app.railway.app

## Step 4: Build & Deploy Frontend
1. **Update frontend environment:**
   ```bash
   # In /app/frontend/.env
   REACT_APP_BACKEND_URL=https://your-app.railway.app
   ```

2. **Build React app:**
   ```bash
   cd /app/frontend
   npm run build
   ```

3. **Upload build folder to DreamHost:**
   - **Via FTP/cPanel File Manager**
   - Upload contents of `build/` folder to `public_html/` 
   - Your site will be live at kylelynch.site

## Step 5: Test Everything
- **Frontend**: kylelynch.site
- **Contact form**: Should send emails
- **Admin login**: admin / admin123  
- **PDF download**: Should work
- **Experience editing**: Should update database

## Alternative: All-in-One Deployment (Easier)

**Option B: Use Netlify + Railway**
1. **Frontend**: Deploy to Netlify (drag & drop build folder)
2. **Backend**: Same Railway setup as above
3. **Custom Domain**: Point kylelynch.site to Netlify

## Files You'll Need

**For GitHub (Backend):**
- All files from `/app/backend/` folder
- Create new GitHub repo: "kyle-lynch-resume-backend"

**For DreamHost (Frontend):**
- Contents of `/app/frontend/build/` after running `npm run build`

## Cost Breakdown
- **Domain**: ~$10-15/year for kylelynch.site
- **Backend**: Free (Railway free tier)  
- **Database**: Free (MongoDB Atlas free tier)
- **Frontend hosting**: Free (DreamHost shared hosting you already have)

**Total additional cost: Just the domain!**

## Admin Access
- **Login**: admin / admin123
- **Change password** in production!
- **Add experiences**, update info, view contact messages

## Next Steps
1. Grab kylelynch.site domain
2. Set up MongoDB Atlas (5 minutes)
3. Deploy backend to Railway (10 minutes)  
4. Build frontend and upload to DreamHost (15 minutes)

**Total deployment time: ~30 minutes!**

Would you like me to help you with any of these steps?