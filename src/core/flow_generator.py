"""
Flow Generator Module

This module uses machine learning to understand user requirements and generate
complete AxieStudio flow JSON structures.
"""

import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from component_kb import component_kb, ComponentCategory, ComponentInfo

class FlowType(Enum):
    BASIC_CHAT = "basic_chat"
    DOCUMENT_QA = "document_qa"
    AGENT_TOOLS = "agent_tools"
    DATA_PROCESSING = "data_processing"
    MULTI_AGENT = "multi_agent"
    RAG_SYSTEM = "rag_system"
    CONTENT_GENERATION = "content_generation"

@dataclass
class FlowRequirement:
    flow_type: FlowType
    components_needed: List[str]
    user_description: str
    specific_models: List[str] = None
    data_sources: List[str] = None
    output_format: str = "chat"

class FlowGenerator:
    """Generates AxieStudio flows based on user requirements using ML understanding."""
    
    def __init__(self):
        self.component_kb = component_kb
        self.flow_templates = self._load_flow_templates()
    
    def _load_flow_templates(self) -> Dict[str, Dict]:
        """Load base flow templates for different use cases."""
        return {
            FlowType.BASIC_CHAT: {
                "components": ["ChatInput", "OpenAIModel", "ChatOutput"],
                "description": "Simple chat interface with AI model"
            },
            FlowType.DOCUMENT_QA: {
                "components": ["ChatInput", "FileComponent", "TextSplitter", 
                             "OpenAIEmbeddings", "ChromaDB", "OpenAIModel", "ChatOutput"],
                "description": "Document Q&A with RAG"
            },
            FlowType.AGENT_TOOLS: {
                "components": ["ChatInput", "Agent", "OpenAIModel", "CalculatorComponent", 
                             "WebSearchTool", "ChatOutput"],
                "description": "Agent with tools"
            },
            FlowType.RAG_SYSTEM: {
                "components": ["FileComponent", "TextSplitter", "OpenAIEmbeddings", 
                             "ChromaDB", "ChatInput", "OpenAIModel", "ChatOutput"],
                "description": "Retrieval Augmented Generation system"
            }
        }
    
    def analyze_user_intent(self, user_input: str) -> FlowRequirement:
        """Analyze user input to determine flow requirements."""
        user_input_lower = user_input.lower()
        
        # Intent classification based on keywords
        if any(keyword in user_input_lower for keyword in 
               ["document", "pdf", "file", "upload", "q&a", "question", "answer"]):
            flow_type = FlowType.DOCUMENT_QA
            components = ["ChatInput", "FileComponent", "TextSplitter", 
                         "OpenAIEmbeddings", "ChromaDB", "OpenAIModel", "ChatOutput"]
        
        elif any(keyword in user_input_lower for keyword in 
                ["agent", "tool", "search", "calculator", "autonomous"]):
            flow_type = FlowType.AGENT_TOOLS
            components = ["ChatInput", "Agent", "OpenAIModel", "ChatOutput"]
            
            # Add specific tools based on mentions
            if "calculator" in user_input_lower or "math" in user_input_lower:
                components.append("CalculatorComponent")
            if "search" in user_input_lower or "web" in user_input_lower:
                components.append("WebSearchTool")
        
        elif any(keyword in user_input_lower for keyword in 
                ["chat", "conversation", "talk", "bot"]):
            flow_type = FlowType.BASIC_CHAT
            components = ["ChatInput", "OpenAIModel", "ChatOutput"]
        
        else:
            # Default to basic chat
            flow_type = FlowType.BASIC_CHAT
            components = ["ChatInput", "OpenAIModel", "ChatOutput"]
        
        # Extract model preferences
        specific_models = []
        if "gpt-4" in user_input_lower or "openai" in user_input_lower:
            specific_models.append("OpenAIModel")
        elif "claude" in user_input_lower or "anthropic" in user_input_lower:
            specific_models.append("AnthropicModel")
        
        return FlowRequirement(
            flow_type=flow_type,
            components_needed=components,
            user_description=user_input,
            specific_models=specific_models
        )
    
    def generate_flow_json(self, requirement: FlowRequirement) -> Dict[str, Any]:
        """Generate complete AxieStudio flow JSON from requirements."""
        nodes = []
        edges = []
        node_positions = self._calculate_node_positions(requirement.components_needed)
        
        # Generate nodes
        for i, component_name in enumerate(requirement.components_needed):
            component_info = self.component_kb.get_component(component_name)
            if not component_info:
                continue
            
            node_id = f"{component_name}-{self._generate_short_id()}"
            position = node_positions[i]
            
            node = self._create_node(node_id, component_info, position)
            nodes.append(node)
        
        # Generate edges (connections between components)
        edges = self._create_edges(nodes, requirement)
        
        # Create complete flow structure
        flow_json = {
            "data": {
                "edges": edges,
                "nodes": nodes,
                "viewport": {"x": 0, "y": 0, "zoom": 1}
            },
            "description": f"Generated flow: {requirement.user_description}",
            "name": f"Generated Flow - {requirement.flow_type.value.title()}",
            "last_tested_version": "1.0.0"
        }
        
        return flow_json
    
    def _generate_short_id(self) -> str:
        """Generate a short unique ID for components."""
        return str(uuid.uuid4())[:5]
    
    def _calculate_node_positions(self, components: List[str]) -> List[Dict[str, float]]:
        """Calculate positions for nodes in the flow."""
        positions = []
        x_spacing = 300
        y_spacing = 200
        start_x = 100
        start_y = 100
        
        for i, _ in enumerate(components):
            x = start_x + (i % 3) * x_spacing
            y = start_y + (i // 3) * y_spacing
            positions.append({"x": x, "y": y})
        
        return positions
    
    def _create_node(self, node_id: str, component_info: ComponentInfo, 
                    position: Dict[str, float]) -> Dict[str, Any]:
        """Create a node structure for the flow."""
        template = {}
        
        # Create template fields for inputs
        for input_field in component_info.inputs:
            field_name = input_field["name"]
            field_type = input_field["type"]
            
            template[field_name] = {
                "type": field_type.lower() if field_type != "Message" else "str",
                "required": field_name in ["input_value", "llm", "documents"],
                "show": True,
                "name": field_name,
                "display_name": input_field["display_name"],
                "value": self._get_default_value(field_name, field_type)
            }
        
        node = {
            "data": {
                "type": component_info.name,
                "node": {
                    "template": template,
                    "description": component_info.description,
                    "base_classes": ["Component"],
                    "display_name": component_info.display_name,
                    "custom_fields": {},
                    "output_types": [output["type"] for output in component_info.outputs],
                    "field_order": [input_field["name"] for input_field in component_info.inputs]
                },
                "id": node_id
            },
            "id": node_id,
            "position": position,
            "type": "genericNode"
        }
        
        return node
    
    def _get_default_value(self, field_name: str, field_type: str) -> Any:
        """Get default values for common fields."""
        defaults = {
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000,
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "collection_name": "documents",
            "should_store_message": True,
            "sender": "User"
        }
        return defaults.get(field_name, "")
    
    def _create_edges(self, nodes: List[Dict], requirement: FlowRequirement) -> List[Dict[str, Any]]:
        """Create edges (connections) between nodes."""
        edges = []
        
        # Simple linear connection for basic flows
        for i in range(len(nodes) - 1):
            source_node = nodes[i]
            target_node = nodes[i + 1]
            
            # Find compatible output/input pair
            source_outputs = source_node["data"]["node"].get("output_types", [])
            target_inputs = target_node["data"]["node"]["template"]
            
            # Create edge if compatible
            for output_type in source_outputs:
                for input_name, input_config in target_inputs.items():
                    if (input_config.get("type") == output_type.lower() or 
                        output_type == "Message" and input_config.get("type") == "str"):
                        
                        edge = self._create_edge(source_node, target_node, 
                                               output_type, input_name)
                        edges.append(edge)
                        break
                else:
                    continue
                break
        
        return edges
    
    def _create_edge(self, source_node: Dict, target_node: Dict, 
                    output_type: str, input_name: str) -> Dict[str, Any]:
        """Create an edge between two nodes."""
        source_id = source_node["id"]
        target_id = target_node["id"]
        
        edge_id = f"reactflow__edge-{source_id}-{target_id}"
        
        return {
            "id": edge_id,
            "source": source_id,
            "target": target_id,
            "animated": False,
            "data": {
                "sourceHandle": {
                    "dataType": source_node["data"]["type"],
                    "id": source_id,
                    "name": "output",
                    "output_types": [output_type]
                },
                "targetHandle": {
                    "fieldName": input_name,
                    "id": target_id,
                    "inputTypes": [output_type],
                    "type": output_type.lower()
                }
            }
        }

# Global instance
flow_generator = FlowGenerator()
