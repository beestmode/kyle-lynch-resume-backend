# Railway Backend Deployment Fix

## Issue Fixed
✅ **MongoDB SSL Connection Error**: The backend was crashing with SSL handshake failures when connecting to MongoDB Atlas from Railway.

## Solution Applied
Modified `/app/backend/database.py` to properly handle SSL connections for MongoDB Atlas:

```python
# Auto-append SSL parameters if not present in connection string
if mongo_url and 'ssl=true' not in mongo_url and 'tls=true' not in mongo_url:
    separator = '&' if '?' in mongo_url else '?'
    mongo_url += f'{separator}ssl=true&retryWrites=true&w=majority'
```

## Deployment Options

### Option 1: Redeploy to Existing Railway Project
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Find your existing project (look for the resume backend)
3. Go to the project settings
4. Find the Git repository settings
5. Get the Git URL and reconnect:
   ```bash
   cd /app
   git remote add origin YOUR_RAILWAY_GIT_URL
   git push origin main --force
   ```

### Option 2: Create New Railway Project
1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub account
4. Create a new repo from `/app/backend` folder
5. Deploy it with these environment variables:
   - `MONGO_URL`: Your MongoDB Atlas connection string
   - `DB_NAME`: Your database name (e.g., `resume_db`)
   - `SECRET_KEY`: Your JWT secret key
   - `PORT`: `8001`

### Option 3: Manual File Upload
If you can't find the original project:
1. Create a new Railway project
2. Upload these fixed backend files manually
3. Set the environment variables

## Finding Your Railway URL
Once deployed successfully:
1. Go to your Railway project dashboard
2. Click on your service
3. Go to the "Deployments" tab
4. Look for the public URL (usually ends with `.railway.app`)
5. Your API will be available at: `https://your-app-name.railway.app/api/`

## Testing the Fix
Once redeployed, test with:
```bash
curl https://your-railway-url.railway.app/api/
```

Should return:
```json
{"message":"Kyle Lynch Resume API is running","status":"healthy"}
```

## Files Modified
- `/app/backend/database.py` - Added SSL connection handling
- `/app/backend/requirements.txt` - Updated pymongo to include srv support

The fix ensures MongoDB Atlas SSL connections work properly on Railway's infrastructure.