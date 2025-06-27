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
export GOOGLE_AI_API_KEY="your-api-key-here"
export PORT=8000
```

5. **Start the server**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🐳 Docker Deployment

### Build and Run Locally
```bash
docker build -t insight-project .
docker run -p 8000:8000 insight-project
```

### Environment Variables
```bash
docker run -p 8000:8000 \
  -e GOOGLE_AI_API_KEY="your-api-key" \
  -e PORT=8000 \
  insight-project
```

## ☁️ Cloud Deployment

### Render.com
1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service
4. Select this repository
5. Use the included `render.yaml` configuration
6. Deploy!

### AWS/Other Platforms
The Docker container can be deployed on any platform that supports Docker containers:
- AWS ECS
- AWS Fargate  
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

## 📡 API Endpoints

### Main Endpoints
- `GET /` - Service information
- `GET /health` - Health check
- `GET /services` - Detailed service information
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

### Form Reader Endpoints
- `POST /form-reader/upload-image` - Analyze form image
- `POST /form-reader/analyze-boxes` - Detect form fields only
- `POST /form-reader/text-to-speech` - Convert text to speech

### Money Reader Endpoints
- `POST /money-reader/upload-image` - Analyze currency image
- `POST /money-reader/analyze-currency` - Specific currency analysis
- `POST /money-reader/count-money` - Count total money amount
- `GET /money-reader/supported-currencies` - List supported currencies

### PPT/PDF Reader Endpoints
- `POST /ppt-pdf-reader/upload-document` - Upload and analyze document
- `GET /ppt-pdf-reader/document/{session_id}/page/{page_number}` - Get page analysis
- `GET /ppt-pdf-reader/document/{session_id}/summary` - Get document summary
- `POST /ppt-pdf-reader/navigate` - Voice navigation
- `GET /ppt-pdf-reader/sessions` - List active sessions

## 🧪 Testing

### API Testing
Access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Test UIs
The project includes Streamlit test interfaces:

```bash
# Run individual service UIs
streamlit run test/form_reader_ui.py
streamlit run test/money_reader_ui.py  
streamlit run test/ppt_pdf_reader_ui.py

# Run combined UI (recommended)
streamlit run test/combined_ui.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_AI_API_KEY` | Google Gemini API key | Required |
| `PORT` | Server port | 8000 |
| `HOST` | Server host | 0.0.0.0 |
| `DEBUG` | Debug mode | false |
| `MAX_FILE_SIZE` | Maximum upload size | 50MB |
| `SESSION_TIMEOUT` | Session timeout | 3600s |

### Service Configuration

Each service can be enabled/disabled:
- `FORM_READER_ENABLED`: Enable/disable form reader (default: true)
- `MONEY_READER_ENABLED`: Enable/disable money reader (default: true)
- `PPT_PDF_READER_ENABLED`: Enable/disable PPT/PDF reader (default: true)

## 🛡️ Security

- All file uploads are validated
- Temporary files are automatically cleaned up
- Session data is stored in memory (not persistent)
- API key is configurable via environment variables
- CORS is configured for cross-origin requests

## 🌍 Internationalization

The platform supports:
- **Arabic**: Full RTL support with proper text rendering
- **English**: Complete LTR support
- **Multilingual AI**: Context-aware responses in both languages

## 📊 Performance

- **Concurrent Processing**: Multiple requests handled simultaneously
- **Memory Management**: Automatic cleanup of temporary files
- **Caching**: Intelligent caching for better performance
- **Scalable**: Designed for horizontal scaling

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure all dependencies are installed
   pip install -r requirements.txt
   ```

2. **Tesseract Not Found** (Form Reader)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-ara
   
   # macOS
   brew install tesseract tesseract-lang
   
   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

3. **YOLO Model Missing** (Form Reader)
   - Ensure `boxes.pt` and `dot_line.pt` are in `app/models/`

4. **Spire.Presentation Issues** (PPT Reader)
   ```bash
   pip install spire.presentation
   ```

### Health Check
Visit http://localhost:8000/health to check service status.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For support and questions:
- Check the API documentation: `/docs`
- Review the health check: `/health`
- Open an issue on GitHub

## 🔮 Future Enhancements

- [ ] Database persistence for sessions
- [ ] User authentication and authorization
- [ ] Advanced analytics dashboard
- [ ] Additional document formats
- [ ] Real-time collaboration features
- [ ] Mobile app integration
- [ ] Advanced AI model fine-tuning

---

**Built with ❤️ using FastAPI, Google Gemini AI, and modern Python technologies.** 