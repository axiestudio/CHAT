"""
Pydantic models for flow generation API
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from enum import Enum

class FlowType(str, Enum):
    """Supported flow types."""
    BASIC_CHAT = "basic_chat"
    DOCUMENT_QA = "document_qa"
    AGENT_TOOLS = "agent_tools"
    RAG_SYSTEM = "rag_system"
    BLOG_WRITER = "blog_writer"
    RESEARCH = "research"
    MEMORY_CHAT = "memory_chat"

class FlowGenerationRequest(BaseModel):
    """Request model for flow generation."""
    description: str = Field(..., min_length=5, max_length=500, description="Natural language description of the desired flow")
    flow_type: Optional[FlowType] = Field(None, description="Specific flow type (auto-detected if not provided)")
    use_ai: bool = Field(True, description="Use AI for intelligent generation")
    model: str = Field("gpt-4", description="AI model to use")
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "Create a chatbot that answers questions about PDF documents",
                "flow_type": "document_qa",
                "use_ai": True,
                "model": "gpt-4"
            }
        }

class ComponentInfo(BaseModel):
    """Information about a flow component."""
    name: str
    display_name: str
    category: str
    description: str

class FlowGenerationResponse(BaseModel):
    """Response model for flow generation."""
    success: bool
    flow_data: Dict[str, Any]
    metadata: Dict[str, Any]
    components: List[ComponentInfo]
    generation_time: float
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "flow_data": {"data": {"nodes": [], "edges": []}},
                "metadata": {
                    "generated_by": "AxieStudio AI Flow Generator",
                    "template_used": "Basic Prompting",
                    "components_count": 6
                },
                "components": [
                    {
                        "name": "ChatInput",
                        "display_name": "Chat Input",
                        "category": "INPUT_OUTPUT",
                        "description": "Get chat inputs from the Playground"
                    }
                ],
                "generation_time": 2.34,
                "message": "Flow generated successfully"
            }
        }

class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    details: Optional[str] = None
    
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    openai_configured: bool
    components_loaded: bool
    templates_available: int
