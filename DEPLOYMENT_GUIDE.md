# 🚀 **DEPLOYMENT GUIDE - AXIESTUDIO AI FLOW GENERATOR**

## 📋 **QUICK DEPLOYMENT SUMMARY**

**✅ Repository:** https://github.com/axiestudio/CHAT  
**✅ Backend:** Koyeb (Free Tier - Perfect!)  
**✅ Frontend:** Vercel (Free Tier)  
**✅ Status:** Production-Ready  

---

## 🎯 **KOYEB BACKEND DEPLOYMENT**

### **Why Koyeb?**
- ✅ **1 free web service** (perfect for your backend)
- ✅ **512MB RAM** (sufficient for FastAPI + AI processing)
- ✅ **0.1 vCPU** (adequate for API requests)
- ✅ **2GB SSD storage** (enough for your AxieStudio files)
- ✅ **100GB outbound bandwidth/month** (very generous!)
- ✅ **No time limits** - truly forever free!

### **Step-by-Step Koyeb Deployment:**

1. **Sign up at Koyeb:**
   - Go to https://www.koyeb.com/
   - Create free account

2. **Create New Service:**
   - Click "Create Service"
   - Select "GitHub" as source
   - Connect your GitHub account
   - Select repository: `axiestudio/CHAT`

3. **Configure Service:**
   - **Name:** `axiestudio-ai-backend`
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Working Directory:** `backend`
   - **Region:** Frankfurt (free tier)

4. **Set Environment Variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PYTHON_VERSION`: `3.11`

5. **Deploy:**
   - Click "Deploy"
   - Wait for deployment (2-3 minutes)
   - Get your backend URL: `https://your-app-name.koyeb.app`

---

## 🎨 **VERCEL FRONTEND DEPLOYMENT**

### **Step-by-Step Vercel Deployment:**

1. **Sign up at Vercel:**
   - Go to https://vercel.com/
   - Sign up with GitHub

2. **Import Project:**
   - Click "New Project"
   - Import from GitHub: `axiestudio/CHAT`
   - **Root Directory:** `frontend`

3. **Configure Build Settings:**
   - **Framework Preset:** Create React App
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`

4. **Set Environment Variables:**
   - `REACT_APP_API_URL`: `https://worthwhile-pelican-axiestudio-7ed1c7d6.koyeb.app/api/v1`

5. **Deploy:**
   - Click "Deploy"
   - Wait for deployment (1-2 minutes)
   - Get your frontend URL: `https://your-app.vercel.app`

### **✅ FRONTEND STATUS:**
- **Local Development:** ✅ Running on http://localhost:3000
- **Backend Connection:** ✅ Configured for https://worthwhile-pelican-axiestudio-7ed1c7d6.koyeb.app
- **Vercel Ready:** ✅ All configurations updated
- **GitHub Pushed:** ✅ Latest code available for deployment

---

## 🔧 **CONFIGURATION CHECKLIST**

### **Backend Configuration:**
- ✅ OpenAI API key configured
- ✅ CORS origins include Vercel domain
- ✅ Health check endpoint working
- ✅ API documentation accessible at `/docs`

### **Frontend Configuration:**
- ✅ API URL pointing to Koyeb backend
- ✅ CORS configured for cross-origin requests
- ✅ Error handling for API failures
- ✅ Toast notifications working

---

## 🧪 **TESTING DEPLOYMENT**

### **Backend Testing:**
```bash
# Test health endpoint
curl https://your-backend.koyeb.app/health

# Test API documentation
# Visit: https://your-backend.koyeb.app/docs

# Test flow generation
curl -X POST https://your-backend.koyeb.app/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "Create a simple chatbot", "use_ai": true}'
```

### **Frontend Testing:**
1. Visit your Vercel URL
2. Enter a flow description
3. Click "Generate Flow"
4. Download the generated JSON
5. Import into AxieStudio

---

## 💰 **COST BREAKDOWN**

### **FREE TIER USAGE:**
- **Koyeb Backend:** $0/month (free tier)
- **Vercel Frontend:** $0/month (free tier)
- **OpenAI API:** Pay-per-use (typically $1-5/month for moderate usage)
- **Total Monthly Cost:** ~$1-5 (OpenAI only)

### **Scaling Options:**
- **Koyeb Pro:** $7/month for more resources
- **Vercel Pro:** $20/month for team features
- **OpenAI Credits:** Scale based on usage

---

## 🔒 **SECURITY CONSIDERATIONS**

### **Environment Variables:**
- ✅ OpenAI API key stored securely in Koyeb
- ✅ No sensitive data in frontend
- ✅ CORS properly configured
- ✅ HTTPS enforced on both services

### **API Security:**
- ✅ Rate limiting (built into OpenAI)
- ✅ Input validation with Pydantic
- ✅ Error handling without data leaks
- ✅ Health checks for monitoring

---

## 📊 **MONITORING & MAINTENANCE**

### **Koyeb Monitoring:**
- Built-in metrics dashboard
- Application logs
- Health check monitoring
- Automatic restarts on failure

### **Vercel Monitoring:**
- Analytics dashboard
- Build logs
- Performance metrics
- Error tracking

---

## 🚀 **GOING LIVE CHECKLIST**

- [ ] Koyeb backend deployed and healthy
- [ ] Vercel frontend deployed and accessible
- [ ] OpenAI API key configured and working
- [ ] CORS configured for production domains
- [ ] Environment variables set correctly
- [ ] Health checks passing
- [ ] API documentation accessible
- [ ] Frontend can generate flows successfully
- [ ] Generated JSON files work in AxieStudio
- [ ] Error handling working properly
- [ ] Performance acceptable (2-5 second generation)

---

## 🆘 **TROUBLESHOOTING**

### **Common Issues:**

**Backend not starting:**
- Check OpenAI API key is set
- Verify Python dependencies installed
- Check Koyeb logs for errors

**Frontend can't connect to backend:**
- Verify REACT_APP_API_URL is correct
- Check CORS configuration
- Ensure backend is healthy

**Flow generation failing:**
- Check OpenAI API key validity
- Verify API quota not exceeded
- Check backend logs for errors

**Generated flows not working in AxieStudio:**
- Ensure using template-based generation
- Check JSON structure matches AxieStudio format
- Verify all required fields present

---

## 🎉 **SUCCESS!**

**Your AxieStudio AI Flow Generator is now live and ready for production use!**

- **Backend:** https://your-backend.koyeb.app
- **Frontend:** https://your-frontend.vercel.app
- **API Docs:** https://your-backend.koyeb.app/docs

**Generate AxieStudio flows in seconds with natural language!** 🚀
