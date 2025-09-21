"""
AI Knowledge Processor

Pre-processes all AxieStudio data into AI-optimized format for MAXIMUM EFFICIENCY.
Creates "spoon-fed" data that AI can consume instantly without processing overhead.
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path
from dataclasses import dataclass, asdict

from .flow_indexer import flow_indexer

@dataclass
class AIOptimizedComponent:
    """AI-optimized component data structure."""
    name: str
    display_name: str
    description: str
    category: str
    primary_use_cases: List[str]
    input_types: List[str]
    output_types: List[str]
    common_connections: List[str]
    ai_selection_keywords: List[str]
    complexity_score: int  # 1-5 scale

@dataclass
class AIOptimizedFlow:
    """AI-optimized flow template."""
    name: str
    description: str
    use_case: str
    components: List[str]
    component_count: int
    complexity: str
    ai_pattern_keywords: List[str]
    json_template: Dict[str, Any]

class AIKnowledgeProcessor:
    """Processes raw AxieStudio data into AI-optimized format."""
    
    def __init__(self):
        self.optimized_components: Dict[str, AIOptimizedComponent] = {}
        self.optimized_flows: Dict[str, AIOptimizedFlow] = {}
        self.ai_prompt_templates = {}
        self.component_selection_rules = {}
        
        # Process all data on initialization
        self._process_all_data()
    
    def _process_all_data(self):
        """Process all AxieStudio data into AI-optimized format."""
        print("🧠 Processing AxieStudio data for AI optimization...")
        
        # Process components
        self._optimize_components()
        
        # Process flows
        self._optimize_flows()
        
        # Create AI prompt templates
        self._create_ai_prompts()
        
        # Create selection rules
        self._create_selection_rules()
        
        # Save optimized data
        self._save_optimized_data()
        
        print(f"✅ AI optimization complete: {len(self.optimized_components)} components, {len(self.optimized_flows)} flows")
    
    def _optimize_components(self):
        """Convert raw components to AI-optimized format."""
        for comp_name, comp_info in flow_indexer.components.items():
            # Extract AI-relevant keywords
            ai_keywords = self._extract_ai_keywords(comp_info.description, comp_info.use_cases)
            
            # Calculate complexity score
            complexity = self._calculate_complexity(comp_info)
            
            # Determine common connections
            connections = self._determine_connections(comp_info)
            
            optimized = AIOptimizedComponent(
                name=comp_info.name,
                display_name=comp_info.display_name,
                description=comp_info.description,
                category=comp_info.category,
                primary_use_cases=comp_info.use_cases[:3],  # Top 3 use cases
                input_types=[inp.get("type", "unknown") for inp in comp_info.inputs],
                output_types=[out.get("type", "unknown") for out in comp_info.outputs],
                common_connections=connections,
                ai_selection_keywords=ai_keywords,
                complexity_score=complexity
            )
            
            self.optimized_components[comp_name] = optimized
    
    def _optimize_flows(self):
        """Convert raw flows to AI-optimized format."""
        for flow_name, flow_info in flow_indexer.flows.items():
            # Extract AI pattern keywords
            pattern_keywords = self._extract_flow_patterns(flow_info)
            
            optimized = AIOptimizedFlow(
                name=flow_info.name,
                description=flow_info.description,
                use_case=flow_info.use_case,
                components=flow_info.components,
                component_count=len(flow_info.components),
                complexity=flow_info.complexity,
                ai_pattern_keywords=pattern_keywords,
                json_template=flow_info.json_structure
            )
            
            self.optimized_flows[flow_name] = optimized
    
    def _extract_ai_keywords(self, description: str, use_cases: List[str]) -> List[str]:
        """Extract AI-relevant keywords for component selection."""
        keywords = []
        
        # Common AI selection patterns
        keyword_patterns = {
            'chat': ['chat', 'conversation', 'talk', 'message', 'dialogue'],
            'document': ['document', 'pdf', 'file', 'text', 'upload'],
            'search': ['search', 'query', 'find', 'lookup', 'retrieve'],
            'embedding': ['embedding', 'vector', 'semantic', 'similarity'],
            'agent': ['agent', 'autonomous', 'reasoning', 'tool', 'action'],
            'database': ['database', 'store', 'save', 'persist', 'memory'],
            'api': ['api', 'request', 'external', 'service', 'integration'],
            'processing': ['process', 'transform', 'parse', 'clean', 'format']
        }
        
        text = f"{description} {' '.join(use_cases)}".lower()
        
        for category, patterns in keyword_patterns.items():
            if any(pattern in text for pattern in patterns):
                keywords.append(category)
        
        return keywords
    
    def _calculate_complexity(self, comp_info) -> int:
        """Calculate component complexity score (1-5)."""
        score = 1
        
        # More inputs/outputs = higher complexity
        if len(comp_info.inputs) > 3:
            score += 1
        if len(comp_info.outputs) > 2:
            score += 1
        
        # Certain categories are inherently complex
        complex_categories = ['AGENTS', 'VECTORSTORES', 'LANGCHAIN_UTILITIES']
        if comp_info.category in complex_categories:
            score += 1
        
        # Long descriptions often indicate complexity
        if len(comp_info.description) > 100:
            score += 1
        
        return min(score, 5)
    
    def _determine_connections(self, comp_info) -> List[str]:
        """Determine common component connections."""
        connections = []
        
        # Based on category, determine likely connections
        connection_patterns = {
            'INPUT_OUTPUT': ['MODELS', 'PROCESSING'],
            'MODELS': ['INPUT_OUTPUT', 'AGENTS', 'PROCESSING'],
            'AGENTS': ['MODELS', 'TOOLS', 'VECTORSTORES'],
            'VECTORSTORES': ['EMBEDDINGS', 'AGENTS', 'PROCESSING'],
            'EMBEDDINGS': ['VECTORSTORES', 'DATA'],
            'DATA': ['PROCESSING', 'EMBEDDINGS'],
            'TOOLS': ['AGENTS', 'PROCESSING']
        }
        
        return connection_patterns.get(comp_info.category, [])
    
    def _extract_flow_patterns(self, flow_info) -> List[str]:
        """Extract AI pattern keywords from flows."""
        patterns = []
        
        # Analyze component combinations
        components = flow_info.components
        
        if any('Chat' in comp for comp in components):
            patterns.append('conversational')
        if any('File' in comp or 'Document' in comp for comp in components):
            patterns.append('document_processing')
        if any('Embedding' in comp for comp in components):
            patterns.append('semantic_search')
        if any('Agent' in comp for comp in components):
            patterns.append('autonomous_agent')
        if any('Vector' in comp or 'Chroma' in comp for comp in components):
            patterns.append('rag_system')
        
        return patterns
    
    def _create_ai_prompts(self):
        """Create optimized AI prompt templates."""
        self.ai_prompt_templates = {
            'intent_analysis': """
You are an expert AxieStudio flow architect. Analyze this user request and extract:

1. PRIMARY USE CASE: {use_cases}
2. REQUIRED CAPABILITIES: {capabilities}
3. PREFERRED MODELS: {models}
4. DATA SOURCES: {data_sources}
5. COMPLEXITY LEVEL: simple/medium/complex

Available use cases: {available_use_cases}
Available capabilities: {available_capabilities}

User request: "{user_input}"

Respond with JSON containing the analysis.
""",
            
            'component_selection': """
You are selecting optimal AxieStudio components. Based on the analysis:

INTENT: {intent_analysis}
AVAILABLE COMPONENTS: {optimized_components}
SIMILAR FLOWS: {similar_flows}

Select components in execution order. Rules:
1. Always start with input component (ChatInput, TextInput, etc.)
2. Include appropriate AI model (OpenAI, Anthropic, etc.)
3. Add processing components as needed
4. Always end with output component (ChatOutput, TextOutput, etc.)
5. Ensure components can connect (matching input/output types)

Respond with JSON array of component names in order.
""",
            
            'flow_generation': """
Create complete AxieStudio flow JSON with these components: {components}

Requirements:
- Each component needs unique ID and proper positioning
- Create edges connecting compatible outputs to inputs
- Follow AxieStudio JSON format exactly
- Include all necessary template fields

Component details: {component_details}
Similar flow examples: {similar_flows}

Generate complete flow JSON structure.
"""
        }
    
    def _create_selection_rules(self):
        """Create component selection rules for AI."""
        self.component_selection_rules = {
            'basic_chat': ['ChatInput', 'OpenAIModel', 'ChatOutput'],
            'document_qa': ['ChatInput', 'FileComponent', 'TextSplitter', 'OpenAIEmbeddings', 'ChromaDB', 'OpenAIModel', 'ChatOutput'],
            'agent_tools': ['ChatInput', 'Agent', 'OpenAIModel', 'WebSearchTool', 'ChatOutput'],
            'rag_system': ['FileComponent', 'TextSplitter', 'OpenAIEmbeddings', 'ChromaDB', 'ChatInput', 'OpenAIModel', 'ChatOutput'],
            'data_processing': ['FileComponent', 'DataProcessor', 'TextSplitter', 'OutputComponent']
        }
    
    def _save_optimized_data(self):
        """Save optimized data to files for fast loading."""
        # Save components
        components_data = {name: asdict(comp) for name, comp in self.optimized_components.items()}
        with open('ai_optimized_components.json', 'w', encoding='utf-8') as f:
            json.dump(components_data, f, indent=2, ensure_ascii=False)
        
        # Save flows
        flows_data = {name: asdict(flow) for name, flow in self.optimized_flows.items()}
        with open('ai_optimized_flows.json', 'w', encoding='utf-8') as f:
            json.dump(flows_data, f, indent=2, ensure_ascii=False)
        
        # Save prompts and rules
        with open('ai_prompts_and_rules.json', 'w', encoding='utf-8') as f:
            json.dump({
                'prompts': self.ai_prompt_templates,
                'selection_rules': self.component_selection_rules
            }, f, indent=2, ensure_ascii=False)
    
    def get_optimized_prompt(self, prompt_type: str, **kwargs) -> str:
        """Get optimized prompt with data filled in."""
        template = self.ai_prompt_templates.get(prompt_type, "")
        return template.format(**kwargs)
    
    def get_components_for_use_case(self, use_case: str) -> List[str]:
        """Get pre-defined component list for common use cases."""
        return self.component_selection_rules.get(use_case, [])
    
    def get_ai_ready_components(self) -> Dict[str, Any]:
        """Get components in AI-ready format."""
        return {
            name: {
                'name': comp.name,
                'description': comp.description,
                'category': comp.category,
                'keywords': comp.ai_selection_keywords,
                'complexity': comp.complexity_score,
                'connections': comp.common_connections
            }
            for name, comp in self.optimized_components.items()
        }
    
    def get_ai_ready_flows(self) -> Dict[str, Any]:
        """Get flows in AI-ready format."""
        return {
            name: {
                'name': flow.name,
                'description': flow.description,
                'use_case': flow.use_case,
                'components': flow.components,
                'patterns': flow.ai_pattern_keywords,
                'complexity': flow.complexity
            }
            for name, flow in self.optimized_flows.items()
        }

# Global instance
ai_knowledge_processor = AIKnowledgeProcessor()
