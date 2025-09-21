"""
AxieStudio AI Flow Generator - FastAPI Backend
Production-ready API for generating AxieStudio flows
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from app.api.flow_generator import router as flow_router
from app.core.config import settings

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AxieStudio AI Flow Generator API",
    description="Production API for generating AxieStudio flows using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://*.vercel.app",   # Vercel deployments
        "https://*.koyeb.app",    # Koyeb deployments
        "https://your-frontend-domain.com"  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(flow_router, prefix="/api/v1", tags=["flows"])

@app.get("/")
async def root():
    """Root endpoint - API status."""
    return {
        "message": "AxieStudio AI Flow Generator API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "components_loaded": True  # Will be dynamic later
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
