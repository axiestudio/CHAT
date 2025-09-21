# 🚀 AxieStudio AI Flow Generator

**Production-ready AI system for generating AxieStudio flows from natural language descriptions.**

Transform your ideas into working AxieStudio flows in seconds using advanced AI and real AxieStudio templates.

## ✨ Features

- 🧠 **AI-Powered Generation** - Uses OpenAI GPT-4 for intelligent flow creation
- 📊 **Real AxieStudio Data** - Built with 294 indexed components and 31 templates
- ⚡ **Lightning Fast** - Generate complete flows in 2-5 seconds
- 🎯 **Production Ready** - 100% compatible with AxieStudio applications
- 🌐 **Modern Architecture** - FastAPI backend + React frontend
- 🚀 **Deployment Ready** - Configured for Vercel (frontend) + Render (backend)

## 🏗️ Architecture

```
Frontend (React)     Backend (FastAPI)     AxieStudio Core
     ↓                      ↓                    ↓
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│  Vercel     │    │  Render/Railway │    │ 294 Components │
│  Deployment │ ←→ │  Deployment     │ ←→ │ 31 Templates   │
└─────────────┘    └─────────────────┘    └─────────────┘
```

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy .env file and add your OpenAI API key
   cp .env.example .env
   # Edit .env and add: OPENAI_API_KEY=your_key_here
   ```

4. **Start the backend server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📡 API Endpoints

### Core Endpoints

- `POST /api/v1/generate` - Generate a flow from description
- `GET /api/v1/templates` - Get available templates
- `GET /api/v1/components` - Get available components
- `GET /api/v1/status` - Get service status
- `GET /health` - Health check

### Example API Usage

```javascript
// Generate a flow
const response = await fetch('http://localhost:8000/api/v1/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    description: "Create a chatbot that answers questions about PDF documents",
    use_ai: true,
    model: "gpt-4"
  })
});

const result = await response.json();
console.log(result.flow_data); // AxieStudio-compatible JSON
```

## 🎯 Usage Examples

### Basic Chat Flow
```
Input: "Create a simple chatbot"
Output: 6-component flow with ChatInput → LanguageModel → ChatOutput
```

### Document Q&A System
```
Input: "Create a system that answers questions about PDF documents"
Output: RAG flow with PDF processing, vector storage, and retrieval
```

### Research Agent
```
Input: "Build an agent that can search the web and write reports"
Output: Multi-agent flow with web search, analysis, and report generation
```

## 🚀 Deployment

### Backend Deployment (Render)

1. **Connect your GitHub repository to Render**
2. **Create a new Web Service**
3. **Configure environment variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key
4. **Deploy using the included `render.yaml` configuration**

### Frontend Deployment (Vercel)

1. **Connect your GitHub repository to Vercel**
2. **Set the root directory to `frontend`**
3. **Configure environment variables:**
   - `REACT_APP_API_URL`: Your backend URL (e.g., `https://your-app.onrender.com/api/v1`)
4. **Deploy automatically with the included `vercel.json` configuration**

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=false
LOG_LEVEL=INFO
BACKEND_CORS_ORIGINS=["http://localhost:3000","https://*.vercel.app"]
```

**Frontend:**
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 📊 System Status

The system includes comprehensive monitoring:

- **Component Indexing**: 294 AxieStudio components analyzed
- **Template Library**: 31 real AxieStudio starter projects
- **AI Integration**: OpenAI GPT-4 for intelligent generation
- **Generation Speed**: 2-5 seconds per complete flow
- **Compatibility**: 100% AxieStudio-compatible JSON output

## 🛠️ Development

### Project Structure
```
axiestudio-chat-flow-generator/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration
│   │   ├── models/         # Pydantic models
│   │   └── services/       # Business logic
│   ├── axiestudio_core/    # AxieStudio components & AI
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   └── package.json
└── README.md
```

### Adding New Templates

1. Add template JSON files to `backend/axiestudio_core/axiestudio/axiestudio_initial_setup/starter_projects/`
2. The system automatically indexes new templates on startup
3. Update template mapping in `template_flow_generator.py` if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the system status at `/health`
- Ensure OpenAI API key is properly configured

---

**Built with ❤️ for the AxieStudio community**
