"""
AxieStudio Component Knowledge Base

This module contains comprehensive information about all available AxieStudio components,
their capabilities, inputs, outputs, and usage patterns.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import json

class ComponentCategory(Enum):
    INPUT_OUTPUT = "input_output"
    MODELS = "models"
    AGENTS = "agents"
    DATA = "data"
    EMBEDDINGS = "embeddings"
    VECTORSTORES = "vectorstores"
    TOOLS = "tools"
    LOGIC = "logic"
    PROCESSING = "processing"
    CHAINS = "chains"

@dataclass
class ComponentInfo:
    name: str
    display_name: str
    category: ComponentCategory
    description: str
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    use_cases: List[str]
    common_connections: List[str]
    icon: str = ""

class AxieStudioComponentKB:
    """Knowledge base of all AxieStudio components and their capabilities."""
    
    def __init__(self):
        self.components = self._initialize_components()
        self._load_indexed_components()
    
    def _initialize_components(self) -> Dict[str, ComponentInfo]:
        """Initialize the component knowledge base."""
        components = {}
        
        # Input/Output Components
        components["ChatInput"] = ComponentInfo(
            name="ChatInput",
            display_name="Chat Input",
            category=ComponentCategory.INPUT_OUTPUT,
            description="Get chat inputs from the Playground",
            inputs=[
                {"name": "input_value", "type": "str", "display_name": "Input Text"},
                {"name": "should_store_message", "type": "bool", "display_name": "Store Messages"},
                {"name": "sender", "type": "str", "display_name": "Sender Type"},
                {"name": "files", "type": "file", "display_name": "Files"}
            ],
            outputs=[
                {"name": "message", "type": "Message", "display_name": "Message"}
            ],
            use_cases=["chat interfaces", "user input", "conversation starters"],
            common_connections=["LanguageModelComponent", "Agent", "ChatOutput"],
            icon="MessagesSquare"
        )
        
        components["ChatOutput"] = ComponentInfo(
            name="ChatOutput",
            display_name="Chat Output",
            category=ComponentCategory.INPUT_OUTPUT,
            description="Display chat outputs in the Playground",
            inputs=[
                {"name": "input_value", "type": "Message", "display_name": "Text"},
                {"name": "should_store_message", "type": "bool", "display_name": "Store Messages"}
            ],
            outputs=[],
            use_cases=["displaying results", "chat responses", "final output"],
            common_connections=["LanguageModelComponent", "Agent", "ChatInput"],
            icon="MessagesSquare"
        )
        
        components["TextInput"] = ComponentInfo(
            name="TextInput",
            display_name="Text Input",
            category=ComponentCategory.INPUT_OUTPUT,
            description="Get text inputs from the Playground",
            inputs=[
                {"name": "input_value", "type": "str", "display_name": "Text"}
            ],
            outputs=[
                {"name": "text", "type": "Message", "display_name": "Text"}
            ],
            use_cases=["static text input", "prompts", "templates"],
            common_connections=["LanguageModelComponent", "Agent", "Prompt"],
            icon="type"
        )
        
        # Language Models
        components["OpenAIModel"] = ComponentInfo(
            name="OpenAIModel",
            display_name="OpenAI",
            category=ComponentCategory.MODELS,
            description="OpenAI language models (GPT-3.5, GPT-4, etc.)",
            inputs=[
                {"name": "input_value", "type": "Message", "display_name": "Input"},
                {"name": "model_name", "type": "str", "display_name": "Model Name"},
                {"name": "temperature", "type": "float", "display_name": "Temperature"},
                {"name": "max_tokens", "type": "int", "display_name": "Max Tokens"},
                {"name": "api_key", "type": "str", "display_name": "OpenAI API Key"}
            ],
            outputs=[
                {"name": "text_output", "type": "Message", "display_name": "Text"},
                {"name": "model_output", "type": "LanguageModel", "display_name": "Language Model"}
            ],
            use_cases=["text generation", "chat completion", "question answering"],
            common_connections=["ChatInput", "Prompt", "Agent", "ChatOutput"],
            icon="openai"
        )
        
        components["AnthropicModel"] = ComponentInfo(
            name="AnthropicModel",
            display_name="Anthropic",
            category=ComponentCategory.MODELS,
            description="Anthropic Claude models",
            inputs=[
                {"name": "input_value", "type": "Message", "display_name": "Input"},
                {"name": "model_name", "type": "str", "display_name": "Model Name"},
                {"name": "temperature", "type": "float", "display_name": "Temperature"},
                {"name": "max_tokens", "type": "int", "display_name": "Max Tokens"},
                {"name": "api_key", "type": "str", "display_name": "Anthropic API Key"}
            ],
            outputs=[
                {"name": "text_output", "type": "Message", "display_name": "Text"},
                {"name": "model_output", "type": "LanguageModel", "display_name": "Language Model"}
            ],
            use_cases=["text generation", "analysis", "reasoning tasks"],
            common_connections=["ChatInput", "Prompt", "Agent", "ChatOutput"],
            icon="anthropic"
        )
        
        # Agents
        components["Agent"] = ComponentInfo(
            name="Agent",
            display_name="Agent",
            category=ComponentCategory.AGENTS,
            description="AI agent that can use tools and follow instructions",
            inputs=[
                {"name": "llm", "type": "LanguageModel", "display_name": "Language Model"},
                {"name": "tools", "type": "Tool", "display_name": "Tools"},
                {"name": "agent_llm", "type": "LanguageModel", "display_name": "Agent LLM"},
                {"name": "system_message", "type": "str", "display_name": "System Message"},
                {"name": "user_message", "type": "Message", "display_name": "User Message"}
            ],
            outputs=[
                {"name": "response", "type": "Message", "display_name": "Response"}
            ],
            use_cases=["autonomous agents", "tool usage", "complex reasoning"],
            common_connections=["OpenAIModel", "Tools", "ChatInput", "ChatOutput"],
            icon="bot"
        )

        # Document Processing
        components["FileComponent"] = ComponentInfo(
            name="FileComponent",
            display_name="File",
            category=ComponentCategory.DATA,
            description="Load and process files (PDF, TXT, DOCX, etc.)",
            inputs=[
                {"name": "path", "type": "str", "display_name": "File Path"}
            ],
            outputs=[
                {"name": "data", "type": "Data", "display_name": "Data"}
            ],
            use_cases=["document loading", "file processing", "data ingestion"],
            common_connections=["TextSplitter", "DocumentLoader", "VectorStore"],
            icon="file"
        )

        components["TextSplitter"] = ComponentInfo(
            name="TextSplitter",
            display_name="Text Splitter",
            category=ComponentCategory.PROCESSING,
            description="Split text into chunks for processing",
            inputs=[
                {"name": "documents", "type": "Data", "display_name": "Documents"},
                {"name": "chunk_size", "type": "int", "display_name": "Chunk Size"},
                {"name": "chunk_overlap", "type": "int", "display_name": "Chunk Overlap"}
            ],
            outputs=[
                {"name": "chunks", "type": "Data", "display_name": "Text Chunks"}
            ],
            use_cases=["document chunking", "text preprocessing", "RAG preparation"],
            common_connections=["FileComponent", "VectorStore", "Embeddings"],
            icon="scissors"
        )

        # Vector Stores
        components["ChromaDB"] = ComponentInfo(
            name="ChromaDB",
            display_name="Chroma",
            category=ComponentCategory.VECTORSTORES,
            description="Chroma vector database for semantic search",
            inputs=[
                {"name": "documents", "type": "Data", "display_name": "Documents"},
                {"name": "embedding", "type": "Embeddings", "display_name": "Embedding Model"},
                {"name": "collection_name", "type": "str", "display_name": "Collection Name"}
            ],
            outputs=[
                {"name": "retriever", "type": "Retriever", "display_name": "Retriever"}
            ],
            use_cases=["semantic search", "RAG systems", "document retrieval"],
            common_connections=["TextSplitter", "OpenAIEmbeddings", "RetrievalQA"],
            icon="database"
        )

        # Embeddings
        components["OpenAIEmbeddings"] = ComponentInfo(
            name="OpenAIEmbeddings",
            display_name="OpenAI Embeddings",
            category=ComponentCategory.EMBEDDINGS,
            description="OpenAI text embedding models",
            inputs=[
                {"name": "api_key", "type": "str", "display_name": "OpenAI API Key"},
                {"name": "model", "type": "str", "display_name": "Model Name"}
            ],
            outputs=[
                {"name": "embeddings", "type": "Embeddings", "display_name": "Embeddings"}
            ],
            use_cases=["text embeddings", "semantic similarity", "vector search"],
            common_connections=["ChromaDB", "VectorStore", "TextSplitter"],
            icon="openai"
        )

        # Tools
        components["CalculatorComponent"] = ComponentInfo(
            name="CalculatorComponent",
            display_name="Calculator",
            category=ComponentCategory.TOOLS,
            description="Perform mathematical calculations",
            inputs=[
                {"name": "expression", "type": "str", "display_name": "Expression"}
            ],
            outputs=[
                {"name": "result", "type": "str", "display_name": "Result"},
                {"name": "component_as_tool", "type": "Tool", "display_name": "Tool"}
            ],
            use_cases=["mathematical operations", "agent tools", "calculations"],
            common_connections=["Agent", "ToolCallingAgent"],
            icon="calculator"
        )

        components["WebSearchTool"] = ComponentInfo(
            name="WebSearchTool",
            display_name="Web Search",
            category=ComponentCategory.TOOLS,
            description="Search the web for information",
            inputs=[
                {"name": "query", "type": "str", "display_name": "Search Query"},
                {"name": "api_key", "type": "str", "display_name": "API Key"}
            ],
            outputs=[
                {"name": "results", "type": "str", "display_name": "Search Results"},
                {"name": "component_as_tool", "type": "Tool", "display_name": "Tool"}
            ],
            use_cases=["web search", "information retrieval", "agent tools"],
            common_connections=["Agent", "ToolCallingAgent"],
            icon="search"
        )

        return components
    
    def get_component(self, name: str) -> ComponentInfo:
        """Get component information by name."""
        return self.components.get(name)
    
    def get_components_by_category(self, category: ComponentCategory) -> List[ComponentInfo]:
        """Get all components in a specific category."""
        return [comp for comp in self.components.values() if comp.category == category]
    
    def search_components(self, query: str) -> List[ComponentInfo]:
        """Search components by name, description, or use cases."""
        query = query.lower()
        results = []
        
        for comp in self.components.values():
            if (query in comp.name.lower() or 
                query in comp.description.lower() or
                any(query in use_case.lower() for use_case in comp.use_cases)):
                results.append(comp)
        
        return results
    
    def get_compatible_components(self, component_name: str, output_type: str) -> List[ComponentInfo]:
        """Get components that can connect to the given component's output."""
        compatible = []
        
        for comp in self.components.values():
            for input_field in comp.inputs:
                if input_field["type"] == output_type:
                    compatible.append(comp)
                    break
        
        return compatible

    def _load_indexed_components(self):
        """Load components from indexed AxieStudio files."""
        try:
            # Load from flow indexer if available
            from .flow_indexer import flow_indexer

            # Add indexed components to our knowledge base
            for comp_name, comp_info in flow_indexer.components.items():
                if comp_name not in self.components:
                    # Convert indexed component to our format
                    component = ComponentInfo(
                        name=comp_info.name,
                        display_name=comp_info.display_name,
                        description=comp_info.description,
                        category=ComponentCategory.PROCESSING,  # Default category
                        inputs=comp_info.inputs,
                        outputs=comp_info.outputs,
                        use_cases=comp_info.use_cases,
                        common_connections=[]
                    )
                    self.components[comp_name] = component

            print(f"✅ Loaded {len(flow_indexer.components)} indexed components")

        except Exception as e:
            print(f"⚠️  Could not load indexed components: {e}")
            # Continue with hardcoded components only

# Global instance
component_kb = AxieStudioComponentKB()
