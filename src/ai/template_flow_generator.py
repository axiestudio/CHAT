"""
Template-based AxieStudio Flow Generator
Uses real AxieStudio JSON templates to generate compatible flows.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List
import uuid
import random

class TemplateFlowGenerator:
    """Generate AxieStudio flows using real templates."""
    
    def __init__(self):
        self.templates_dir = Path("data/axiestudio/axiestudio_initial_setup/starter_projects")
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load all available AxieStudio templates."""
        templates = {}
        
        if not self.templates_dir.exists():
            print(f"⚠️ Templates directory not found: {self.templates_dir}")
            return templates
            
        for json_file in self.templates_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    template = json.load(f)
                    templates[json_file.stem] = template
                    print(f"✅ Loaded template: {json_file.stem}")
            except Exception as e:
                print(f"⚠️ Failed to load {json_file}: {e}")
                
        print(f"📁 Loaded {len(templates)} AxieStudio templates")
        return templates
    
    def generate_flow(self, user_description: str, use_case: str = "basic_chat") -> Dict[str, Any]:
        """Generate flow using appropriate template."""
        
        # Select best template based on use case
        template_name = self._select_template(use_case)
        
        if template_name not in self.templates:
            print(f"⚠️ Template {template_name} not found, using Basic Prompting")
            template_name = "Basic Prompting"
            
        if template_name not in self.templates:
            print("❌ No templates available, creating minimal flow")
            return self._create_minimal_flow(user_description)
            
        # Clone and customize template
        template = json.loads(json.dumps(self.templates[template_name]))
        
        # Customize template
        template["description"] = f"AI generated flow: {user_description}"
        template["name"] = f"AI Flow - {user_description[:50]}..."
        
        # Update metadata if present
        if "metadata" in template:
            template["metadata"]["generated_by"] = "AxieStudio AI Flow Generator"
            template["metadata"]["user_description"] = user_description
        else:
            template["metadata"] = {
                "generated_by": "AxieStudio AI Flow Generator",
                "user_description": user_description,
                "template_used": template_name
            }
            
        return template
    
    def _select_template(self, use_case: str) -> str:
        """Select appropriate template based on use case."""
        
        template_mapping = {
            "basic_chat": "Basic Prompting",
            "document_qa": "Document Q&A", 
            "agent_tools": "Simple Agent",
            "rag_system": "Vector Store RAG",
            "blog_writer": "Blog Writer",
            "research": "Research Agent",
            "memory_chat": "Memory Chatbot"
        }
        
        return template_mapping.get(use_case, "Basic Prompting")
    
    def _create_minimal_flow(self, user_description: str) -> Dict[str, Any]:
        """Create minimal working AxieStudio flow as fallback."""
        return {
            "data": {
                "edges": [],
                "nodes": [],
                "viewport": {"x": 0, "y": 0, "zoom": 1}
            },
            "description": f"AI generated flow: {user_description}",
            "name": f"AI Flow - {user_description[:50]}...",
            "last_tested_version": "1.0.0",
            "metadata": {
                "generated_by": "AxieStudio AI Flow Generator (Minimal)",
                "user_description": user_description,
                "note": "Minimal flow - templates not available"
            }
        }
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template names."""
        return list(self.templates.keys())
    
    def get_template_info(self, template_name: str) -> Dict[str, Any]:
        """Get information about a specific template."""
        if template_name not in self.templates:
            return {"error": "Template not found"}
            
        template = self.templates[template_name]
        
        return {
            "name": template.get("name", template_name),
            "description": template.get("description", "No description"),
            "nodes_count": len(template.get("data", {}).get("nodes", [])),
            "edges_count": len(template.get("data", {}).get("edges", [])),
            "components": [node.get("data", {}).get("display_name", "Unknown") 
                          for node in template.get("data", {}).get("nodes", [])]
        }

# Global instance
template_generator = TemplateFlowGenerator()
