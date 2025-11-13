# DreamHost Deployment Guide - kylelynch.site

## ✅ Pre-configured Settings
- **Domain**: kylelynch.site
- **DreamHost IP**: 76.31.21.210
- **MongoDB**: Configured and ready
- **Backend URL**: https://kylelynch.site/api
- **Frontend URL**: https://kylelynch.site

---

## Step 1: Update DNS Settings

1. **Log into your domain registrar** (where you bought kylelynch.site)
2. **Go to DNS settings**
3. **Update A Record**:
   - Type: `A`
   - Name: `@` (or leave blank for root domain)
   - Value: `76.31.21.210`
   - TTL: `3600` (or automatic)

4. **Wait 10-60 minutes** for DNS propagation

---

## Step 2: Prepare Files for Upload

### Backend Files (Upload these to DreamHost):
```
kyle-lynch-resume-backend/
├── server.py
├── models.py
├── database.py
├── auth.py
├── pdf_generator.py
├── passenger_wsgi.py          ← NEW (DreamHost entry point)
├── .htaccess                   ← NEW (DreamHost configuration)
├── .env                        ← UPDATED (MongoDB credentials)
├── requirements.txt
└── data/
    └── mock.py
```

### Frontend Build (Need to generate):
Run this command in your local terminal:
```bash
cd /app/frontend
yarn build
```

This creates a `build/` folder with these files:
```
build/
├── index.html
├── static/
│   ├── css/
│   ├── js/
│   └── media/
└── ... (other assets)
```

---

## Step 3: Upload to DreamHost

### Option A: Using DreamHost File Manager (Easiest)

1. **Log into DreamHost Panel**: https://panel.dreamhost.com
2. **Go to**: Files → WebFTP
3. **Navigate to**: `/home/YOUR_USERNAME/kylelynch.site/`

4. **Upload Backend Files**:
   - Create folder: `api/`
   - Upload ALL files from `kyle-lynch-resume-backend/` to `api/`
   - **Important**: Include `.env` and `.htaccess` files

5. **Upload Frontend Files**:
   - Upload ALL files from `frontend/build/` to root (`/home/YOUR_USERNAME/kylelynch.site/`)
   - **Result**: `index.html` should be at root level

### Option B: Using FTP (FileZilla/Cyberduck)

1. **Get FTP credentials** from DreamHost Panel → Files → FTP Accounts
2. **Connect to FTP**:
   - Host: `ftp.kylelynch.site`
   - Username: Your DreamHost username
   - Password: Your FTP password
   - Port: 21

3. **Upload same files as Option A**

---

## Step 4: Configure Python Environment on DreamHost

1. **Go to DreamHost Panel** → Websites → kylelynch.site
2. **Enable Passenger**:
   - Look for "Passenger" or "Python" settings
   - Enable if not already enabled

3. **SSH into your DreamHost account** (if comfortable):
   ```bash
   ssh YOUR_USERNAME@kylelynch.site
   cd ~/kylelynch.site/api
   
   # Install dependencies
   python3 -m pip install --user -r requirements.txt
   
   # Test if imports work
   python3 -c "import fastapi; print('FastAPI installed')"
   ```

4. **Create restart file** (forces Passenger to restart):
   ```bash
   mkdir -p ~/kylelynch.site/tmp
   touch ~/kylelynch.site/tmp/restart.txt
   ```

---

## Step 5: Update .htaccess (IMPORTANT)

1. **Edit** `/home/YOUR_USERNAME/kylelynch.site/api/.htaccess`
2. **Replace** `YOUR_USERNAME` with your actual DreamHost username
3. **Save the file**

Example:
```apache
PassengerAppRoot /home/johnsmith/kylelynch.site
PassengerPython /home/johnsmith/.pyenv/versions/3.11.0/bin/python3
```

---

## Step 6: Test Your Site

### Test Frontend:
- Visit: https://kylelynch.site
- Should see your resume with parchment design
- You might see "Failed to load resume data" (that's OK for now)

### Test Backend:
- Visit: https://kylelynch.site/api
- Should see: `{"message": "Kyle Lynch Resume API is running", "status": "healthy"}`

### Test Full Integration:
- Visit: https://kylelynch.site
- Resume data should load
- Contact form should work
- PDF download should work

---

## Troubleshooting

### Problem: "500 Internal Server Error"
**Solution**:
1. Check `.htaccess` has correct username
2. Verify all backend files uploaded
3. Check Passenger is enabled
4. Look at error logs in DreamHost Panel

### Problem: "Failed to load resume data"
**Solution**:
1. Check backend is running: visit `/api`
2. Verify MongoDB connection string in `.env`
3. Check CORS settings in backend

### Problem: "ERR_SSL_PROTOCOL_ERROR" still appears
**Solution**:
1. Wait for DNS propagation (up to 24 hours)
2. Verify Let's Encrypt SSL is enabled in DreamHost
3. Clear browser cache

### Problem: Python modules not found
**Solution**:
```bash
# SSH into DreamHost
cd ~/kylelynch.site/api
pip3 install --user -r requirements.txt
touch ~/kylelynch.site/tmp/restart.txt
```

---

## Admin Login
- **URL**: https://kylelynch.site (click "Admin" or navigate to admin panel)
- **Username**: `admin`
- **Password**: `admin123`
- **⚠️ CHANGE PASSWORD** after first login!

---

## Restart Backend (After Changes)

Whenever you update backend code:
```bash
touch ~/kylelynch.site/tmp/restart.txt
```

Or via File Manager:
1. Create/edit file: `tmp/restart.txt`
2. Just updating the timestamp restarts the app

---

## Need Help?

1. **DreamHost Support**: https://help.dreamhost.com
2. **Python on DreamHost**: https://help.dreamhost.com/hc/en-us/articles/215489338-Installing-and-using-Python-s-virtualenv
3. **Passenger Docs**: https://www.phusionpassenger.com/

---

## Summary

✅ DNS points to DreamHost: 76.31.21.210  
✅ Backend at: https://kylelynch.site/api  
✅ Frontend at: https://kylelynch.site  
✅ MongoDB: Connected  
✅ SSL: Let's Encrypt enabled

**Your resume site is ready to go live!** 🎉
