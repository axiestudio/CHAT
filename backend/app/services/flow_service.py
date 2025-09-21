"""
Flow generation service - Core business logic
"""

import sys
import os
import time
from pathlib import Path
from typing import Dict, Any, List

# Add axiestudio_core to path
axiestudio_core_path = str(Path(__file__).parent.parent.parent / "axiestudio_core")
sys.path.insert(0, axiestudio_core_path)
print(f"DEBUG: Added to path: {axiestudio_core_path}")

try:
    from ai.template_flow_generator import template_generator
    from ai.super_ai_generator import super_ai_generator
    from ai.flow_indexer import flow_indexer
except ImportError as e:
    print(f"Warning: Could not import AI modules: {e}")
    template_generator = None
    super_ai_generator = None
    flow_indexer = None

class FlowGenerationService:
    """Service for generating AxieStudio flows."""
    
    def __init__(self):
        self.initialized = False
        self._initialize()
    
    def _initialize(self):
        """Initialize the service."""
        try:
            if template_generator:
                # Template generator initializes automatically
                self.templates_count = len(template_generator.get_available_templates())
            else:
                self.templates_count = 0
                
            if flow_indexer:
                # Flow indexer initializes automatically
                self.components_count = len(flow_indexer.components)
            else:
                self.components_count = 0
                
            self.initialized = True
            print(f"✅ Flow service initialized: {self.components_count} components, {self.templates_count} templates")
            
        except Exception as e:
            print(f"⚠️ Flow service initialization failed: {e}")
            self.initialized = False
    
    async def generate_flow(self, description: str, flow_type: str = None, use_ai: bool = True) -> Dict[str, Any]:
        """Generate a flow based on description."""
        
        start_time = time.time()
        
        try:
            if not self.initialized:
                raise Exception("Flow service not initialized")
            
            # Use super AI generator if available
            if super_ai_generator and use_ai:
                print(f"🚀 Generating flow with AI: {description}")
                flow_data = super_ai_generator.generate_flow_super_fast(description)
            
            # Fallback to template generator
            elif template_generator:
                print(f"📋 Generating flow with templates: {description}")
                use_case = flow_type or "basic_chat"
                flow_data = template_generator.generate_flow(description, use_case)
            
            else:
                raise Exception("No flow generators available")
            
            # Extract components info
            components = self._extract_components_info(flow_data)
            
            generation_time = time.time() - start_time
            
            return {
                "success": True,
                "flow_data": flow_data,
                "metadata": {
                    "generated_by": "AxieStudio AI Flow Generator API",
                    "generation_method": "AI-Powered" if use_ai else "Template-Based",
                    "generation_time": generation_time,
                    "components_count": len(components),
                    "template_used": flow_data.get("metadata", {}).get("template_used", "Unknown")
                },
                "components": components,
                "generation_time": generation_time,
                "message": "Flow generated successfully"
            }
            
        except Exception as e:
            generation_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "generation_time": generation_time,
                "message": "Flow generation failed"
            }
    
    def _extract_components_info(self, flow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract component information from flow data."""
        components = []
        
        try:
            nodes = flow_data.get("data", {}).get("nodes", [])
            
            for node in nodes:
                node_data = node.get("data", {})
                components.append({
                    "name": node.get("type", "Unknown"),
                    "display_name": node_data.get("display_name", node.get("type", "Unknown")),
                    "category": node_data.get("node", {}).get("metadata", {}).get("module", "Unknown"),
                    "description": node_data.get("description", "No description available")
                })
                
        except Exception as e:
            print(f"⚠️ Error extracting components: {e}")
        
        return components
    
    def get_status(self) -> Dict[str, Any]:
        """Get service status."""
        return {
            "initialized": self.initialized,
            "components_count": self.components_count,
            "templates_count": self.templates_count,
            "ai_available": super_ai_generator is not None,
            "templates_available": template_generator is not None
        }

# Global service instance
flow_service = FlowGenerationService()
