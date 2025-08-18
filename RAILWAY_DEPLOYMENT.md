# 🚂 Railway Deployment Guide

## Quick Fix for Host Blocking Issue

The Vite configuration has been updated to support Railway deployment. The `allowedHosts` now includes `.railway.app` domains.

## 🚀 Deployment Steps

### 1. Backend Deployment

1. **Create a new Railway project**
2. **Deploy Backend Service:**
   - Connect your GitHub repository
   - Set the **Root Directory** to `backend`
   - Railway will auto-detect the Python app

3. **Set Environment Variables:**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=false
   LOG_LEVEL=INFO
   PORT=5000
   CORS_ORIGINS=*
   
   # Trading Bot Config
   VIABILITY_THRESHOLD=70.0
   MAX_POSITION_SIZE=1000.0
   SLIPPAGE_TOLERANCE=0.02
   STOP_LOSS_PERCENTAGE=0.15
   TAKE_PROFIT_PERCENTAGE=0.25
   MAX_CONCURRENT_POSITIONS=5
   
   # Your API Keys
   ALCHEMY_API_KEY=your-actual-key
   QUICKNODE_API_KEY=your-actual-key
   GOPLUS_API_KEY=your-actual-key
   ```

4. **Note the Backend URL** (e.g., `https://backend-production-abc123.up.railway.app`)

### 2. Frontend Deployment

1. **Create another Railway service** (or add to existing project)
2. **Deploy Frontend Service:**
   - Connect your GitHub repository
   - Set the **Root Directory** to `frontend`
   - Use the updated Dockerfile

3. **Set Environment Variables:**
   ```
   VITE_API_URL=https://your-backend-url.up.railway.app
   ```
   ⚠️ **Important:** Replace `your-backend-url` with the actual Railway backend URL from step 1.

4. **Build and Deploy**

### 3. Alternative: Single Service Deployment

If you want to deploy both frontend and backend in a single Railway service:

1. **Use the root railway.json** (already configured)
2. **Set Environment Variables:**
   ```
   VITE_API_URL=https://your-service-name.up.railway.app
   SECRET_KEY=your-secret-key
   DEBUG=false
   # ... other environment variables
   ```

## 🔧 Configuration Files Updated

- ✅ `frontend/vite.config.js` - Added Railway hosts support
- ✅ `frontend/Dockerfile` - Enhanced for Railway deployment
- ✅ `railway.json` - Updated build configuration
- ✅ `frontend/start.sh` - Railway startup script

## 🐛 Troubleshooting

### Host Blocking Error
- **Fixed**: Added `.railway.app` to `allowedHosts` in Vite config
- **Solution**: The updated configuration now accepts Railway domains

### API Connection Issues
1. **Check Environment Variables**: Ensure `VITE_API_URL` points to your Railway backend
2. **CORS Configuration**: Backend should allow Railway frontend domain
3. **SSL/HTTPS**: Railway uses HTTPS, ensure your API calls match

### Build Issues
1. **Check Dockerfile Path**: Ensure Railway points to correct Dockerfile
2. **Environment Variables**: Set `VITE_API_URL` during build time
3. **Dependencies**: Verify all npm packages install correctly

## 📝 Environment Variable Checklist

### Backend Service:
- [ ] `SECRET_KEY`
- [ ] `DEBUG=false`
- [ ] `PORT=5000`
- [ ] `CORS_ORIGINS=*`
- [ ] Trading bot configuration variables
- [ ] API keys

### Frontend Service:
- [ ] `VITE_API_URL=https://your-backend.up.railway.app`

## 🔗 Railway Dashboard Steps

1. Go to [Railway Dashboard](https://railway.app)
2. Create new project or select existing
3. Add services (Backend and Frontend)
4. Configure environment variables
5. Deploy and test

## ✅ Verification

After deployment:
1. **Backend Health**: Visit `https://your-backend.up.railway.app/api/trading/status`
2. **Frontend Access**: Visit your frontend Railway URL
3. **API Connection**: Check browser console for any CORS or connection errors

The host blocking issue should now be resolved with the updated Vite configuration!