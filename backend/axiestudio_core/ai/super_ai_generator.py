"""
Super AI Flow Generator

MAXIMUM EFFICIENCY AI system that uses pre-processed, optimized data
for INSTANT flow generation. No processing overhead - pure AI power!
"""

import json
import os
from typing import Dict, List, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

from .ai_knowledge_processor import ai_knowledge_processor
from .template_flow_generator import template_generator

# Load environment variables
from pathlib import Path
config_path = Path(__file__).parent.parent.parent / "config" / ".env"
load_dotenv(config_path)

class SuperAIFlowGenerator:
    """Ultra-efficient AI flow generator with pre-processed data."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.processor = ai_knowledge_processor
        
        # Pre-load optimized data for instant access
        try:
            self.ai_components = self.processor.get_ai_ready_components()
            self.ai_flows = self.processor.get_ai_ready_flows()
        except:
            # Fallback if processor fails
            self.ai_components = {}
            self.ai_flows = {}

        # Basic component selection rules
        self.component_selection_rules = {
            'basic_chat': ['ChatInput', 'OpenAIModel', 'ChatOutput'],
            'document_qa': ['ChatInput', 'FileComponent', 'TextSplitter', 'OpenAIEmbeddings', 'ChromaDB', 'OpenAIModel', 'ChatOutput'],
            'agent_tools': ['ChatInput', 'Agent', 'OpenAIModel', 'WebSearchTool', 'ChatOutput'],
            'rag_system': ['FileComponent', 'TextSplitter', 'OpenAIEmbeddings', 'ChromaDB', 'ChatInput', 'OpenAIModel', 'ChatOutput'],
        }

        print(f"🚀 Super AI Generator ready: {len(self.ai_components)} components, {len(self.ai_flows)} flows")
    
    def generate_flow_super_fast(self, user_description: str) -> Dict[str, Any]:
        """Generate flow with MAXIMUM EFFICIENCY using pre-processed data."""
        
        print("⚡ Super AI Generation Starting...")
        
        # Step 1: INSTANT intent analysis with optimized prompt
        intent = self._analyze_intent_super_fast(user_description)
        print(f"🎯 Intent: {intent.get('primary_use_case', 'general')}")
        
        # Step 2: INSTANT component selection using pre-processed rules
        components = self._select_components_super_fast(user_description, intent)
        print(f"🔧 Selected {len(components)} components")
        
        # Step 3: Use template-based generation for guaranteed compatibility
        use_case = intent.get('primary_use_case', 'basic_chat')
        flow_json = template_generator.generate_flow(user_description, use_case)
        print(f"✅ Generated flow using {use_case} template")
        
        return flow_json
    
    def _analyze_intent_super_fast(self, user_description: str) -> Dict[str, Any]:
        """Ultra-fast intent analysis using optimized prompts."""
        
        # Pre-defined use cases for instant matching
        use_cases = list(self.processor.component_selection_rules.keys())
        capabilities = ['chat', 'document_processing', 'search', 'embeddings', 'agents', 'rag']
        
        # Create simple prompt for intent analysis
        prompt = f"""
You are an expert AxieStudio flow architect. Analyze this user request:

User request: "{user_description}"

Available use cases: {', '.join(use_cases)}
Available capabilities: {', '.join(capabilities)}

Respond with JSON containing:
{{
    "primary_use_case": "one of the available use cases",
    "capabilities": ["list of required capabilities"],
    "complexity": "simple/medium/complex"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception:
            # Ultra-fast fallback using keyword matching
            return self._fallback_intent_analysis(user_description)
    
    def _select_components_super_fast(self, user_description: str, intent: Dict[str, Any]) -> List[str]:
        """Ultra-fast component selection using pre-processed rules."""
        
        primary_use_case = intent.get('primary_use_case', 'basic_chat')
        
        # Check if we have a pre-defined rule for this use case
        if primary_use_case in self.component_selection_rules:
            components = self.component_selection_rules[primary_use_case].copy()
            print(f"📋 Using pre-defined rule for {primary_use_case}")
            return components
        
        # Use AI for custom component selection with optimized data
        prompt = f"""
You are selecting optimal AxieStudio components based on this analysis:

Intent: {json.dumps(intent)}
Available components: {list(self.ai_components.keys())[:20]}

Select components in execution order. Rules:
1. Always start with input component (ChatInput, TextInput, etc.)
2. Include appropriate AI model (OpenAI, Anthropic, etc.)
3. Add processing components as needed
4. Always end with output component (ChatOutput, TextOutput, etc.)

Respond with JSON array of component names in order.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            components = json.loads(content)
            return components if isinstance(components, list) else []
            
        except Exception:
            # Fallback to basic chat
            return self.component_selection_rules['basic_chat']
    
    def _generate_flow_super_fast(self, user_description: str, components: List[str]) -> Dict[str, Any]:
        """Ultra-fast flow generation using optimized templates."""
        
        # Get component details for AI
        component_details = []
        for comp_name in components:
            if comp_name in self.ai_components:
                comp_data = self.ai_components[comp_name]
                component_details.append({
                    "name": comp_name,
                    "description": comp_data["description"],
                    "category": comp_data["category"],
                    "connections": comp_data["connections"]
                })
        
        # Create flow generation prompt
        prompt = f"""
Create complete AxieStudio flow JSON with these components: {components}

Requirements:
- Each component needs unique ID and proper positioning
- Create edges connecting compatible outputs to inputs
- Follow AxieStudio JSON format exactly
- Include all necessary template fields

Component details: {json.dumps(component_details)}

Generate complete flow JSON structure with "data" containing "nodes" and "edges".
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            flow_structure = json.loads(content)
            
            # Create final AxieStudio-compatible JSON
            return self._create_final_flow_json(flow_structure, user_description)
            
        except Exception as e:
            print(f"⚠️ AI generation failed: {e}")
            # Ultra-fast fallback using templates
            return self._fallback_flow_generation(components, user_description)
    
    def _create_final_flow_json(self, flow_structure: Dict[str, Any], user_description: str) -> Dict[str, Any]:
        """Create final AxieStudio-compatible flow JSON."""
        
        return {
            "data": flow_structure.get("data", {
                "edges": flow_structure.get("edges", []),
                "nodes": flow_structure.get("nodes", []),
                "viewport": {"x": 0, "y": 0, "zoom": 1}
            }),
            "description": f"Super AI generated flow: {user_description}",
            "name": f"Super AI Flow - {user_description[:50]}...",
            "last_tested_version": "1.0.0",
            "metadata": {
                "generated_by": "Super AI Flow Generator",
                "generation_method": "OpenAI GPT-4 + Optimized Data",
                "user_description": user_description,
                "optimization_level": "MAXIMUM"
            }
        }
    
    def _fallback_intent_analysis(self, user_description: str) -> Dict[str, Any]:
        """Ultra-fast fallback intent analysis using keyword matching."""
        desc_lower = user_description.lower()
        
        if any(kw in desc_lower for kw in ["document", "pdf", "file", "q&a", "question"]):
            return {"primary_use_case": "document_qa", "capabilities": ["document_processing", "embeddings"]}
        elif any(kw in desc_lower for kw in ["agent", "tool", "search", "autonomous"]):
            return {"primary_use_case": "agent_tools", "capabilities": ["agents", "tools"]}
        elif any(kw in desc_lower for kw in ["rag", "retrieval", "vector", "embedding"]):
            return {"primary_use_case": "rag_system", "capabilities": ["embeddings", "vectorstore"]}
        else:
            return {"primary_use_case": "basic_chat", "capabilities": ["chat"]}
    
    def _fallback_flow_generation(self, components: List[str], user_description: str) -> Dict[str, Any]:
        """Ultra-fast fallback flow generation using real AxieStudio templates."""

        # Determine use case from components
        use_case = "basic_chat"
        if "Agent" in components:
            use_case = "agent_tools"
        elif any(comp in components for comp in ["TextSplitter", "ChromaDB", "Embeddings"]):
            use_case = "rag_system"
        elif "FileComponent" in components:
            use_case = "document_qa"

        # Use template generator
        return template_generator.generate_flow(user_description, use_case)

    def _create_minimal_flow(self, user_description: str) -> Dict[str, Any]:
        """Create minimal working AxieStudio flow."""
        return {
            "data": {
                "edges": [],
                "nodes": [],
                "viewport": {"x": 0, "y": 0, "zoom": 1}
            },
            "description": f"AI generated flow: {user_description}",
            "name": f"AI Flow - {user_description[:50]}...",
            "last_tested_version": "1.0.0"
        }

    def get_generation_stats(self) -> Dict[str, Any]:
        """Get generation statistics and capabilities."""
        return {
            "components_available": len(self.ai_components),
            "flow_templates": len(self.ai_flows),
            "pre_defined_rules": len(self.processor.component_selection_rules),
            "optimization_level": "MAXIMUM",
            "ai_model": "OpenAI GPT-4",
            "processing_mode": "PRE-OPTIMIZED",
            "capabilities": [
                "instant_intent_analysis",
                "smart_component_selection", 
                "optimized_flow_generation",
                "fallback_systems",
                "production_ready_output"
            ]
        }

# Global instance
super_ai_generator = SuperAIFlowGenerator()
