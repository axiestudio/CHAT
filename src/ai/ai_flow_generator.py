"""
AI-Powered Flow Generator

Production-grade flow generation using OpenAI GPT models for intelligent
understanding and flow creation based on indexed AxieStudio components and examples.
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from openai import OpenAI
from pathlib import Path

from .component_kb import component_kb
from .flow_indexer import flow_indexer

class AIFlowGenerator:
    """Production AI-powered flow generator using OpenAI for intelligent flow creation."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)
        self.component_kb = component_kb
        self.flow_indexer = flow_indexer

    
    def generate_flow_with_ai(self, user_description: str) -> Dict[str, Any]:
        """Generate flow using AI understanding of user requirements."""
        
        # Step 1: Analyze user intent with AI
        intent_analysis = self._analyze_intent_with_ai(user_description)

        # Step 2: Find similar flows from index
        similar_flows_raw = self.flow_indexer.find_similar_flows(user_description, limit=3)
        similar_flows = [{"name": sf["flow"].name, "description": sf["flow"].description,
                         "components": sf["flow"].components, "flow_type": sf["flow"].flow_type}
                        for sf in similar_flows_raw]

        # Step 3: Select optimal components with AI
        component_selection = self._select_components_with_ai(
            user_description, intent_analysis, similar_flows
        )

        # Step 4: Generate flow structure with AI
        flow_structure = self._generate_flow_structure_with_ai(
            user_description, component_selection, similar_flows
        )
        
        # Step 5: Create final JSON
        flow_json = self._create_flow_json(flow_structure, user_description)
        
        return flow_json
    
    def _analyze_intent_with_ai(self, user_description: str) -> Dict[str, Any]:
        """Use AI to analyze user intent and extract requirements."""
        
        system_prompt = """You are an expert AxieStudio flow architect. Analyze user requirements and extract:
1. Primary use case (document_qa, agent_tools, basic_chat, data_processing, etc.)
2. Required capabilities (file processing, web search, calculations, etc.)
3. Preferred AI models (OpenAI, Anthropic, etc.)
4. Data sources (PDFs, web, databases, etc.)
5. Output format (chat, data, visualization, etc.)

Respond in JSON format with clear categorization."""

        user_prompt = f"""Analyze this flow requirement:
"{user_description}"

Available AxieStudio component categories:
- Input/Output: ChatInput, TextInput, FileInput, ChatOutput
- Models: OpenAI, Anthropic, Mistral, Groq
- Agents: Agent, CrewAI, ToolCallingAgent
- Data: FileComponent, TextSplitter, DocumentLoader
- Embeddings: OpenAIEmbeddings, HuggingFaceEmbeddings
- VectorStores: ChromaDB, Pinecone, FAISS
- Tools: WebSearch, Calculator, APIs
- Processing: DataTransformer, ConditionalRouter

Provide detailed analysis in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception:
            # Fallback to rule-based analysis
            return self._fallback_intent_analysis(user_description)
    
    def _select_components_with_ai(self, user_description: str,
                                       intent_analysis: Dict[str, Any],
                                       similar_flows: List[Dict]) -> List[str]:
        """Use AI to select optimal components based on requirements."""
        
        # Get all available components
        available_components = []
        for comp in self.component_kb.components.values():
            available_components.append({
                "name": comp.name,
                "display_name": comp.display_name,
                "description": comp.description,
                "category": comp.category.value,
                "use_cases": comp.use_cases,
                "inputs": [inp["name"] for inp in comp.inputs],
                "outputs": [out["name"] for out in comp.outputs]
            })
        
        system_prompt = """You are an expert AxieStudio component architect. Select the optimal components 
for a flow based on user requirements and similar flow examples.

Rules:
1. Always include ChatInput for user interaction (unless pure data processing)
2. Always include ChatOutput for displaying results (unless pure data processing)
3. Include appropriate AI model (OpenAI, Anthropic, etc.)
4. Add necessary data processing components (FileComponent, TextSplitter, etc.)
5. Include vector stores for RAG systems (ChromaDB, Pinecone, etc.)
6. Add tools for agents (WebSearch, Calculator, etc.)
7. Ensure components can connect properly (matching input/output types)

Respond with a JSON array of component names in execution order."""

        user_prompt = f"""Select components for this flow:
User Description: "{user_description}"

Intent Analysis: {json.dumps(intent_analysis, indent=2)}

Similar Flows: {json.dumps(similar_flows, indent=2)}

Available Components: {json.dumps(available_components, indent=2)}

Return JSON array of component names in optimal execution order."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )

            content = response.choices[0].message.content
            components = json.loads(content)
            return components if isinstance(components, list) else []

        except Exception:
            # Fallback to rule-based selection
            return self._fallback_component_selection(intent_analysis)
    
    def _generate_flow_structure_with_ai(self, user_description: str,
                                             components: List[str],
                                             similar_flows: List[Dict]) -> Dict[str, Any]:
        """Use AI to generate the complete flow structure with connections."""
        
        system_prompt = """You are an expert AxieStudio flow designer. Create a complete flow structure 
with nodes and edges (connections) based on selected components.

Flow Structure Requirements:
1. Each component becomes a node with unique ID
2. Nodes must have proper positioning (x, y coordinates)
3. Edges connect compatible outputs to inputs
4. Follow AxieStudio JSON format exactly
5. Include all necessary template fields for each component
6. Ensure proper data flow from input to output

Respond with complete flow structure in AxieStudio JSON format."""

        # Get component details for AI
        component_details = []
        for comp_name in components:
            comp = self.component_kb.get_component(comp_name)
            if comp:
                component_details.append({
                    "name": comp.name,
                    "inputs": comp.inputs,
                    "outputs": comp.outputs,
                    "connections": comp.common_connections
                })

        user_prompt = f"""Generate complete flow structure for:
User Description: "{user_description}"

Selected Components: {json.dumps(components)}

Component Details: {json.dumps(component_details, indent=2)}

Similar Flow Examples: {json.dumps(similar_flows, indent=2)}

Create complete AxieStudio flow JSON with nodes, edges, and proper connections."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=3000
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception:
            # Fallback to template-based generation
            return self._fallback_flow_structure(components, user_description)
    
    def _create_flow_json(self, flow_structure: Dict[str, Any], 
                         user_description: str) -> Dict[str, Any]:
        """Create final AxieStudio-compatible flow JSON."""
        
        return {
            "data": flow_structure.get("data", {
                "edges": flow_structure.get("edges", []),
                "nodes": flow_structure.get("nodes", []),
                "viewport": {"x": 0, "y": 0, "zoom": 1}
            }),
            "description": f"AI-generated flow: {user_description}",
            "name": f"AI Flow - {user_description[:50]}...",
            "last_tested_version": "1.0.0",
            "metadata": {
                "generated_by": "AI Flow Generator",
                "generation_method": "OpenAI GPT-4",
                "user_description": user_description
            }
        }
    
    def _fallback_intent_analysis(self, user_description: str) -> Dict[str, Any]:
        """Fallback rule-based intent analysis."""
        user_lower = user_description.lower()
        
        if any(kw in user_lower for kw in ["document", "pdf", "file", "q&a"]):
            return {"primary_use_case": "document_qa", "capabilities": ["file_processing", "embeddings"]}
        elif any(kw in user_lower for kw in ["agent", "tool", "search"]):
            return {"primary_use_case": "agent_tools", "capabilities": ["tools", "reasoning"]}
        else:
            return {"primary_use_case": "basic_chat", "capabilities": ["conversation"]}
    
    def _fallback_component_selection(self, intent_analysis: Dict[str, Any]) -> List[str]:
        """Fallback rule-based component selection."""
        use_case = intent_analysis.get("primary_use_case", "basic_chat")
        
        if use_case == "document_qa":
            return ["ChatInput", "FileComponent", "TextSplitter", "OpenAIEmbeddings", 
                   "ChromaDB", "OpenAIModel", "ChatOutput"]
        elif use_case == "agent_tools":
            return ["ChatInput", "Agent", "OpenAIModel", "WebSearchTool", "ChatOutput"]
        else:
            return ["ChatInput", "OpenAIModel", "ChatOutput"]
    
    def _fallback_flow_structure(self, components: List[str], 
                                user_description: str) -> Dict[str, Any]:
        """Fallback template-based flow structure generation."""
        # Use simple fallback template
        return {
            "nodes": [
                {
                    "id": "input-1",
                    "type": "ChatInput",
                    "position": {"x": 100, "y": 100},
                    "data": {"template": {"input_value": {"value": ""}}}
                },
                {
                    "id": "model-1",
                    "type": "OpenAIModel",
                    "position": {"x": 300, "y": 100},
                    "data": {"template": {"model_name": {"value": "gpt-4"}}}
                },
                {
                    "id": "output-1",
                    "type": "ChatOutput",
                    "position": {"x": 500, "y": 100},
                    "data": {"template": {"input_value": {"value": ""}}}
                }
            ],
            "edges": [
                {"id": "e1", "source": "input-1", "target": "model-1"},
                {"id": "e2", "source": "model-1", "target": "output-1"}
            ]
        }
