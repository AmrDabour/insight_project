# 🧠 Insight Project - AI Services Platform

A unified platform combining three powerful AI services for document and image analysis.

## 🌟 Services Overview

### 📋 Form Reader
- **AI-powered form analysis and data extraction**
- Form field detection using YOLO
- OCR text extraction (Arabic & English)
- Checkbox and field recognition
- Smart form understanding with Gemini AI

### 💰 Money Reader  
- **Currency detection and financial analysis**
- Multi-currency bill and coin recognition
- Automatic counting and denomination
- Support for major currencies (USD, SAR, EUR, etc.)
- AI-powered financial document analysis

### 📄 PPT/PDF Reader
- **Document analysis with AI insights**
- PowerPoint (.pptx, .ppt) and PDF processing
- Page-by-page content extraction
- AI-powered summarization and explanation
- Voice navigation and multilingual support

## 🚀 Features

- **Unified API**: Single endpoint for all three services
- **Multi-language Support**: Arabic and English
- **AI-Powered Analysis**: Google Gemini integration
- **Text-to-Speech**: Voice output for all services
- **High-Quality Processing**: Advanced image and document processing
- **Docker Ready**: Easy deployment with Docker
- **Cloud Deployment**: Ready for Render, AWS, or other platforms
- **Essential Models Included**: YOLO models ready for production

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### System Dependencies (for local development)
- Tesseract OCR (for form reading)
- FFmpeg (for audio processing)

## 🛠️ Installation

### Quick Start (Recommended)

#### Windows
```powershell
git clone <your-repo-url>
cd insight_project
.\start.ps1
```

#### Linux/Mac
```bash
git clone <your-repo-url>
cd insight_project
chmod +x start.sh
./start.sh
```

### Manual Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd insight_project
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
# Copy the example file
cp env.example .env
# Edit .env with your actual API key
```

5. **Start the server**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔑 Configuration

### Environment Variables Setup

1. **Copy the example configuration:**
```bash
cp env.example .env
```

2. **Edit `.env` file with your settings:**
```bash
# Required: Your Google AI API Key
GOOGLE_AI_API_KEY=your-actual-api-key-here

# Optional: Customize other settings
PORT=8000
DEBUG=false
```

### Essential Files Included

✅ **YOLO Models** (21MB total):
- `app/models/boxes.pt` - Form field detection
- `app/models/dot_line.pt` - Form boundary detection
- **These are included in the repository for immediate deployment**

✅ **Directory Structure**:
- `uploads/` - File upload storage (with .gitkeep)
- `temp/` - Temporary processing (with .gitkeep)
- `logs/` - Application logs (with .gitkeep)

## 🐳 Docker Deployment

### Build and Run Locally
```bash
docker build -t insight-project .
docker run -p 8000:8000 -e GOOGLE_AI_API_KEY="your-api-key" insight-project
```

### With Custom Environment
```bash
docker run -p 8000:8000 \
  -e GOOGLE_AI_API_KEY="your-api-key" \
  -e PORT=8000 \
  -e DEBUG=false \
  insight-project
```

## ☁️ Cloud Deployment

### Render.com (Recommended)
1. **Fork this repository to your GitHub**
2. **Connect GitHub to Render**
3. **Create new Web Service**
4. **Select this repository**
5. **Environment Variables:**
   ```
   GOOGLE_AI_API_KEY=your-api-key-here
   PORT=8000
   ```
6. **Deploy!** (All models and dependencies are included)

### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set GOOGLE_AI_API_KEY=your-api-key
git push heroku main
```

### AWS/Azure/GCP
The Docker container works on any platform:
- **AWS ECS/Fargate**
- **Azure Container Instances** 
- **Google Cloud Run**
- **DigitalOcean App Platform**

## 📡 API Endpoints

### Main Endpoints
- `GET /` - Service information
- `GET /health` - Health check
- `GET /services` - Detailed service information
- `GET /docs` - Interactive API documentation

### Form Reader Endpoints
- `POST /form-reader/upload-image` - Analyze form image
- `POST /form-reader/analyze-boxes` - Detect form fields only
- `POST /form-reader/text-to-speech` - Convert text to speech

### Money Reader Endpoints
- `POST /money-reader/upload-image` - Analyze currency image
- `POST /money-reader/supported-currencies` - List supported currencies

### PPT/PDF Reader Endpoints
- `POST /ppt-pdf-reader/upload-document` - Upload and analyze document
- `GET /ppt-pdf-reader/document/{session_id}/page/{page_number}` - Get page analysis
- `GET /ppt-pdf-reader/document/{session_id}/summary` - Get document summary

## 🧪 Testing

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Test UI
```bash
streamlit run test/combined_ui.py
```

## 🔧 Production Considerations

### Required for Cloud Deployment ✅
- [x] YOLO models included (boxes.pt, dot_line.pt)
- [x] All Python dependencies in requirements.txt
- [x] Docker configuration ready
- [x] Environment variables template
- [x] Essential directories with .gitkeep files
- [x] Startup scripts for different platforms

### Performance Optimization
- Models are optimized for fast inference
- Automatic cleanup of temporary files
- Session management with configurable timeouts
- Concurrent request handling

### Security Features
- Environment variable configuration
- File upload validation
- Temporary file cleanup
- CORS configuration
- Input sanitization

## 🛡️ File Structure for Cloud

```
insight_project/
├── app/
│   ├── models/
│   │   ├── boxes.pt           ✅ Included (15MB)
│   │   ├── dot_line.pt        ✅ Included (6MB)
│   │   └── README.md          ✅ Model documentation
│   ├── services/              ✅ All service code
│   └── main.py               ✅ FastAPI application
├── uploads/.gitkeep          ✅ Upload directory
├── temp/.gitkeep             ✅ Temp directory  
├── logs/.gitkeep             ✅ Logs directory
├── env.example               ✅ Environment template
├── requirements.txt          ✅ All dependencies
├── Dockerfile               ✅ Container config
├── render.yaml              ✅ Cloud deployment
└── start.sh / start.ps1     ✅ Platform scripts
```

## 🚨 Important Notes for Cloud Deployment

1. **API Key Required**: Set `GOOGLE_AI_API_KEY` environment variable
2. **Models Included**: YOLO models are in the repository (21MB total)
3. **Dependencies Complete**: All required packages in requirements.txt
4. **Directories Ready**: Upload/temp/logs directories will be created
5. **No Manual Setup**: Everything needed is included

## 🐛 Troubleshooting

### Cloud Deployment Issues

1. **Missing Models Error**
   - ✅ Fixed: Models are now included in repository
   
2. **Environment Variables**
   - Copy `env.example` to `.env`
   - Set your `GOOGLE_AI_API_KEY`

3. **Directory Errors**
   - ✅ Fixed: .gitkeep files ensure directories exist

4. **Memory Issues**
   - Models are optimized for cloud deployment
   - Increase memory limits if needed (recommended: 1GB+)

### Health Check
Visit `/health` endpoint to verify all services are running.

## 📊 Repository Size

- **Total Size**: ~25MB (including models)
- **Models**: 21MB (essential for functionality)
- **Code**: 4MB (application and configuration)

**Note**: Repository size is optimized for cloud deployment while including all necessary models.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test with included models
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**🌟 Ready for Production Deployment**
**All models, dependencies, and configurations included!** 