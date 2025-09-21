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
        # Generate flow using service
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
