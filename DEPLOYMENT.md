# 🚀 Insight Project - Cloud Deployment Guide

This guide covers deploying the Insight Project to various cloud platforms.

## ✅ Pre-Deployment Checklist

All required files are included in this repository:
- [x] **YOLO Models** (21MB): `app/models/boxes.pt`, `app/models/dot_line.pt`
- [x] **Python Dependencies**: Complete `requirements.txt`
- [x] **Docker Configuration**: Ready-to-use `Dockerfile`
- [x] **Environment Template**: `env.example` with all variables
- [x] **Essential Directories**: `uploads/`, `temp/`, `logs/` with `.gitkeep`
- [x] **Startup Scripts**: Platform-specific `start.sh` and `start.ps1`
- [x] **Cloud Configuration**: `render.yaml` for easy deployment

## 🔑 Required Environment Variables

**Minimum Required:**
```bash
GOOGLE_AI_API_KEY=your-google-gemini-api-key-here
```

**Recommended for Production:**
```bash
GOOGLE_AI_API_KEY=your-google-gemini-api-key-here
PORT=8000
HOST=0.0.0.0
DEBUG=false
MAX_FILE_SIZE=52428800
```

## 🌐 Deployment Options

---

## 1. 🎯 Render.com (Recommended - Easiest)

### Quick Deploy Steps:
1. **Fork this repository** to your GitHub account
2. **Sign up/Login** to [Render.com](https://render.com)
3. **Connect GitHub** account to Render
4. **Create Web Service**:
   - Repository: Select your forked repository
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Set Environment Variables**:
   ```
   GOOGLE_AI_API_KEY = your-actual-api-key-here
   ```
6. **Deploy!** ✨

### Using render.yaml (Auto-Deploy):
The `render.yaml` file is already configured. Just:
1. Fork repository
2. Connect to Render
3. Add environment variable: `GOOGLE_AI_API_KEY`
4. Deploy automatically

### Expected Deployment Time: 5-10 minutes

---

## 2. 🚀 Heroku

### CLI Deployment:
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new app
heroku create your-insight-project

# Set environment variables
heroku config:set GOOGLE_AI_API_KEY=your-api-key-here
heroku config:set PORT=8000

# Deploy
git push heroku main

# Open app
heroku open
```

### Container Deployment:
```bash
# Login to Heroku Container Registry
heroku container:login

# Build and push
heroku container:push web --app your-insight-project

# Release
heroku container:release web --app your-insight-project
```

### Expected Deployment Time: 10-15 minutes

---

## 3. ☁️ AWS (Multiple Options)

### Option A: AWS App Runner (Easiest)
1. **Open AWS App Runner** console
2. **Create Service**:
   - Source: GitHub repository
   - Repository: Your forked repository
   - Branch: `main`
3. **Configure Build**:
   - Build command: `pip install -r requirements.txt`
   - Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. **Environment Variables**:
   ```
   GOOGLE_AI_API_KEY=your-api-key-here
   PORT=8000
   ```
5. **Deploy**

### Option B: AWS ECS Fargate
```bash
# Build and push to ECR
aws ecr create-repository --repository-name insight-project
docker build -t insight-project .
docker tag insight-project:latest AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/insight-project:latest
docker push AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/insight-project:latest

# Create ECS service (use AWS console or CLI)
```

### Expected Deployment Time: 15-20 minutes

---

## 4. 🔵 Azure

### Azure Container Instances:
```bash
# Login to Azure
az login

# Create resource group
az group create --name insight-project-rg --location eastus

# Create container instance
az container create \
  --resource-group insight-project-rg \
  --name insight-project \
  --image your-registry/insight-project:latest \
  --cpu 1 --memory 2 \
  --ports 8000 \
  --environment-variables GOOGLE_AI_API_KEY=your-api-key PORT=8000
```

### Azure Web Apps:
1. **Create Web App** in Azure portal
2. **Configure Deployment**:
   - Source: GitHub
   - Repository: Your forked repository
3. **Set Environment Variables** in Configuration
4. **Deploy**

### Expected Deployment Time: 10-15 minutes

---

## 5. 🟢 Google Cloud Platform

### Cloud Run (Recommended):
```bash
# Build and deploy
gcloud run deploy insight-project \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_AI_API_KEY=your-api-key
```

### App Engine:
1. **Create `app.yaml`**:
```yaml
runtime: python39
env: standard

env_variables:
  GOOGLE_AI_API_KEY: "your-api-key-here"
  PORT: "8080"

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

2. **Deploy**:
```bash
gcloud app deploy
```

### Expected Deployment Time: 10-15 minutes

---

## 6. 🌊 DigitalOcean

### App Platform:
1. **Connect GitHub** repository
2. **Configure App**:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Set Environment Variables**:
   ```
   GOOGLE_AI_API_KEY=your-api-key-here
   ```
4. **Deploy**

### Expected Deployment Time: 8-12 minutes

---

## 🐳 Docker Deployment (Self-Hosted)

### Quick Start:
```bash
# Clone repository
git clone https://github.com/your-username/insight-project.git
cd insight-project

# Build image
docker build -t insight-project .

# Run container
docker run -d \
  --name insight-project \
  -p 8000:8000 \
  -e GOOGLE_AI_API_KEY=your-api-key-here \
  -e PORT=8000 \
  insight-project

# Check logs
docker logs insight-project
```

### Docker Compose:
```yaml
version: '3.8'
services:
  insight-project:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_AI_API_KEY=your-api-key-here
      - PORT=8000
      - DEBUG=false
    volumes:
      - ./uploads:/app/uploads
      - ./temp:/app/temp
      - ./logs:/app/logs
    restart: unless-stopped
```

---

## 🔧 Post-Deployment

### 1. Health Check
Visit: `https://your-app-url/health`
Expected response:
```json
{
  "status": "healthy",
  "services": {
    "form_reader": "healthy",
    "money_reader": "healthy", 
    "ppt_pdf_reader": "healthy"
  }
}
```

### 2. API Documentation
Visit: `https://your-app-url/docs`

### 3. Test Upload
Use the test UI: `https://your-app-url/test/combined_ui.py`

---

## 🚨 Troubleshooting

### Common Issues:

#### 1. "Models not found"
✅ **Fixed**: Models are included in repository
- Verify `app/models/boxes.pt` and `app/models/dot_line.pt` exist

#### 2. "Environment variable not set"
- Check `GOOGLE_AI_API_KEY` is set in platform environment variables
- Copy from `env.example` and update values

#### 3. "Port binding error"
- Ensure `PORT` environment variable is set correctly
- Use platform-specific port variable (Heroku: `$PORT`, others: `8000`)

#### 4. "Out of memory"
- **Minimum RAM**: 1GB (recommended: 2GB+)
- Models require ~500MB RAM for loading

#### 5. "File upload errors"
- Check if `uploads/` directory exists (should auto-create)
- Verify file size limits (default: 50MB)

### Memory Optimization:
```python
# In production, consider:
# - Lazy model loading
# - Model quantization
# - Batch processing limits
```

---

## 📊 Performance Monitoring

### Key Metrics to Monitor:
- **Memory Usage**: Should stay under 80% of allocated
- **Response Time**: Typical: 2-10 seconds for AI processing
- **Error Rate**: Should be < 1%
- **File Upload Success**: Should be > 95%

### Recommended Monitoring:
- Health check endpoint: `/health`
- Logs directory: `logs/`
- Application metrics via platform dashboards

---

## 🔒 Security Considerations

### Production Security:
- ✅ Environment variables for sensitive data
- ✅ File upload validation
- ✅ Temporary file cleanup
- ✅ CORS configuration
- ✅ Input sanitization

### Additional Recommendations:
- Use HTTPS (automatic on most platforms)
- Implement rate limiting for production
- Regular security updates
- Monitor for unusual activity

---

## 💰 Cost Estimation

### Monthly Costs (USD):

| Platform | Basic Plan | Recommended |
|----------|------------|-------------|
| **Render** | $7-25 | $25 (1GB RAM) |
| **Heroku** | $7-25 | $25-50 (Dyno + Add-ons) |
| **AWS** | $15-50 | $30-70 (App Runner/ECS) |
| **Azure** | $10-40 | $25-60 (Container Instances) |
| **GCP** | $8-30 | $20-50 (Cloud Run) |
| **DigitalOcean** | $5-25 | $20-40 (App Platform) |

**Note**: Costs depend on usage, region, and resource allocation.

---

## 🎯 Deployment Success Checklist

After deployment, verify:
- [ ] Health check passes: `/health`
- [ ] API documentation loads: `/docs`
- [ ] Form Reader works with test image
- [ ] Money Reader processes currency image
- [ ] PPT/PDF Reader handles document upload
- [ ] Text-to-speech functions work
- [ ] All models load successfully
- [ ] Environment variables are set
- [ ] Logs are being generated

---

**🌟 Your Insight Project is now ready for production!**

For additional support, check the main README.md or open an issue on GitHub. 