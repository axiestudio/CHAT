"""
FastAPI routes for flow generation
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import os
import time

from app.models.flow_models import (
    FlowGenerationRequest, 
    FlowGenerationResponse, 
    ErrorResponse,
    HealthResponse
)
from app.services.flow_service import flow_service

# Import the new Real AxieStudio AI Chat system
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "axiestudio_core"))

try:
    from ai.real_axiestudio_ai_chat import real_axiestudio_ai_chat
    REAL_AI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Real AxieStudio AI not available: {e}")
    REAL_AI_AVAILABLE = False

router = APIRouter()

@router.post("/generate", response_model=FlowGenerationResponse)
async def generate_flow(request: FlowGenerationRequest):
    """Generate an AxieStudio flow based on natural language description."""

    # Validate OpenAI API key if AI is requested
    if request.use_ai and not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=400,
            detail="OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
        )

    try:
        # Use Real AxieStudio AI Chat if available and AI is requested
        if request.use_ai and REAL_AI_AVAILABLE:
            result = real_axiestudio_ai_chat.chat(request.description)

            if result["success"]:
                return FlowGenerationResponse(
                    success=True,
                    message=result["message"],
                    flow=result["flow"],
                    metadata={
                        "generator": "Real AxieStudio AI Chat",
                        "conversation_id": result.get("conversation_id"),
                        "intent": result.get("intent", {})
                    }
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=result.get("message", "Real AI generation failed")
                )
        else:
            # Fallback to original service
            result = await flow_service.generate_flow(
                description=request.description,
                flow_type=request.flow_type,
                use_ai=request.use_ai
            )

            if result["success"]:
                return FlowGenerationResponse(**result)
            else:
                raise HTTPException(
                    status_code=500,
                    detail=result.get("error", "Flow generation failed")
                )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/chat")
async def chat_with_ai(request: dict):
    """Chat with the Real AxieStudio AI system."""

    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=400,
            detail="OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
        )

    if not REAL_AI_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Real AxieStudio AI system not available."
        )

    try:
        message = request.get("message", "")
        if not message.strip():
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        # Chat with the AI
        result = real_axiestudio_ai_chat.chat(message)

        return {
            "success": result["success"],
            "message": result["message"],
            "flow": result.get("flow"),
            "intent": result.get("intent", {}),
            "conversation_id": result.get("conversation_id"),
            "timestamp": time.time()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}"
        )

@router.get("/chat/history")
async def get_chat_history():
    """Get the current chat conversation history."""

    if not REAL_AI_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Real AxieStudio AI system not available."
        )

    try:
        history = real_axiestudio_ai_chat.get_conversation_history()
        return {
            "success": True,
            "history": history,
            "count": len(history)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat history: {str(e)}"
        )

@router.post("/chat/clear")
async def clear_chat_history():
    """Clear the chat conversation history."""

    if not REAL_AI_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Real AxieStudio AI system not available."
        )

    try:
        real_axiestudio_ai_chat.clear_conversation()
        return {
            "success": True,
            "message": "Chat history cleared successfully."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing chat history: {str(e)}"
        )

@router.get("/templates")
async def get_available_templates():
    """Get list of available flow templates."""
    
    try:
        # Import here to avoid circular imports
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent / "axiestudio_core"))
        
        from ai.template_flow_generator import template_generator
        
        templates = template_generator.get_available_templates()
        template_info = {}
        
        for template_name in templates:
            info = template_generator.get_template_info(template_name)
            template_info[template_name] = info
        
        return {
            "success": True,
            "templates": template_info,
            "count": len(templates)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "templates": {},
            "count": 0
        }

@router.get("/components")
async def get_available_components():
    """Get list of available AxieStudio components."""
    
    try:
        # Import here to avoid circular imports
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent / "axiestudio_core"))
        
        from ai.flow_indexer import flow_indexer
        
        components = {}
        for comp_name, comp_info in flow_indexer.components.items():
            components[comp_name] = {
                "name": comp_name,
                "category": comp_info.category,
                "description": comp_info.description,
                "file_path": comp_info.file_path
            }
        
        return {
            "success": True,
            "components": components,
            "count": len(components)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "components": {},
            "count": 0
        }

@router.get("/status", response_model=HealthResponse)
async def get_service_status():
    """Get detailed service status."""
    
    status = flow_service.get_status()
    
    return HealthResponse(
        status="healthy" if status["initialized"] else "unhealthy",
        openai_configured=bool(os.getenv("OPENAI_API_KEY")),
        components_loaded=status["components_count"] > 0,
        templates_available=status["templates_count"]
    )
