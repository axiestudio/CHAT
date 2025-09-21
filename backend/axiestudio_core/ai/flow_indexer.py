"""
Production Flow Indexer

Indexes all AxieStudio components, starter projects, and flows for AI-powered
intelligent flow generation and component selection.
"""

import json
import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import hashlib

@dataclass
class ComponentInfo:
    """Detailed information about an AxieStudio component."""
    name: str
    file_path: str
    class_name: str
    display_name: str
    description: str
    category: str
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    dependencies: List[str]
    use_cases: List[str]
    examples: List[str]
    code_hash: str

@dataclass
class FlowInfo:
    """Information about a starter project flow."""
    name: str
    file_path: str
    description: str
    flow_type: str
    components: List[str]
    connections: List[Dict[str, Any]]
    use_case: str
    complexity: str
    json_structure: Dict[str, Any]

class FlowIndexer:
    """Production-grade indexer for AxieStudio components and flows."""
    
    def __init__(self):
        self.components: Dict[str, ComponentInfo] = {}
        self.flows: Dict[str, FlowInfo] = {}
        self.component_categories: Dict[str, List[str]] = defaultdict(list)
        self.use_case_mapping: Dict[str, List[str]] = defaultdict(list)
        self.component_connections: Dict[str, List[str]] = defaultdict(list)
        
        # Index everything on initialization
        self._index_all()
    
    def _index_all(self):
        """Index all components and flows."""
        print("🔍 Indexing AxieStudio components and flows...")

        # Get paths relative to project root
        current_dir = Path(__file__).parent
        root_dir = current_dir.parent.parent
        data_dir = root_dir / "data" / "axiestudio"

        # Index components
        components_path = data_dir / "axiestudio_components"
        if components_path.exists():
            self._index_components(components_path)

        # Index starter projects
        starter_projects_path = data_dir / "axiestudio_initial_setup" / "starter_projects"
        if starter_projects_path.exists():
            self._index_starter_projects(starter_projects_path)

        print(f"✅ Indexed {len(self.components)} components and {len(self.flows)} flows")
    
    def _index_components(self, components_path: Path):
        """Index all component files."""
        for category_dir in components_path.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('__'):
                category_name = category_dir.name.upper()
                
                for component_file in category_dir.glob("*.py"):
                    if component_file.name != "__init__.py":
                        try:
                            component_info = self._analyze_component_file(component_file, category_name)
                            if component_info:
                                self.components[component_info.name] = component_info
                                self.component_categories[category_name].append(component_info.name)
                                
                                # Map use cases
                                for use_case in component_info.use_cases:
                                    self.use_case_mapping[use_case.lower()].append(component_info.name)
                        except Exception as e:
                            print(f"⚠️  Error analyzing {component_file}: {e}")
    
    def _analyze_component_file(self, file_path: Path, category: str) -> Optional[ComponentInfo]:
        """Analyze a component Python file to extract metadata."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Find component class
            component_class = None
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Look for classes that inherit from Component
                    for base in node.bases:
                        if isinstance(base, ast.Name) and 'Component' in base.id:
                            component_class = node
                            break
                    if component_class:
                        break
            
            if not component_class:
                return None
            
            # Extract component information
            class_name = component_class.name
            display_name = self._extract_display_name(content, class_name)
            description = self._extract_description(content, class_name)
            inputs = self._extract_inputs(content)
            outputs = self._extract_outputs(content)
            dependencies = self._extract_dependencies(content)
            use_cases = self._extract_use_cases(content, category)
            examples = self._extract_examples(content)
            
            # Generate code hash for change detection
            code_hash = hashlib.md5(content.encode()).hexdigest()
            
            return ComponentInfo(
                name=class_name,
                file_path=str(file_path),
                class_name=class_name,
                display_name=display_name,
                description=description,
                category=category,
                inputs=inputs,
                outputs=outputs,
                dependencies=dependencies,
                use_cases=use_cases,
                examples=examples,
                code_hash=code_hash
            )
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def _extract_display_name(self, content: str, class_name: str) -> str:
        """Extract display name from component."""
        # Look for display_name attribute
        display_name_match = re.search(r'display_name\s*=\s*["\']([^"\']+)["\']', content)
        if display_name_match:
            return display_name_match.group(1)
        
        # Fallback to class name with spaces
        return re.sub(r'([A-Z])', r' \1', class_name).strip()
    
    def _extract_description(self, content: str, class_name: str) -> str:
        """Extract description from component."""
        # Look for description attribute
        desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
        if desc_match:
            return desc_match.group(1)
        
        # Look for class docstring
        docstring_match = re.search(rf'class {class_name}.*?:\s*["\']([^"\']+)["\']', content, re.DOTALL)
        if docstring_match:
            return docstring_match.group(1).strip()
        
        return f"{class_name} component"
    
    def _extract_inputs(self, content: str) -> List[Dict[str, Any]]:
        """Extract input definitions from component."""
        inputs = []
        
        # Look for input field definitions
        input_patterns = [
            r'(\w+)\s*:\s*(\w+Input)\s*=\s*(\w+Input)\(',
            r'(\w+)\s*=\s*(\w+Input)\(',
        ]
        
        for pattern in input_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                field_name = match.group(1)
                input_type = match.group(2) if len(match.groups()) > 2 else match.group(2)
                inputs.append({
                    "name": field_name,
                    "type": input_type,
                    "required": "required=True" in content
                })
        
        return inputs
    
    def _extract_outputs(self, content: str) -> List[Dict[str, Any]]:
        """Extract output definitions from component."""
        outputs = []
        
        # Look for output definitions in build method
        output_patterns = [
            r'return\s+(\w+)\(',
            r'self\.status\s*=\s*(\w+)',
        ]
        
        for pattern in output_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                output_type = match.group(1)
                if output_type not in ['self', 'super']:
                    outputs.append({
                        "name": "output",
                        "type": output_type
                    })
        
        return outputs
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from imports."""
        dependencies = []
        
        # Extract import statements
        import_matches = re.finditer(r'from\s+(\S+)\s+import|import\s+(\S+)', content)
        for match in import_matches:
            module = match.group(1) or match.group(2)
            if module and not module.startswith('.') and module not in ['typing', 'os', 'sys']:
                dependencies.append(module.split('.')[0])
        
        return list(set(dependencies))
    
    def _extract_use_cases(self, content: str, category: str) -> List[str]:
        """Extract use cases based on category and content analysis."""
        use_cases = []
        
        # Category-based use cases
        category_mapping = {
            'INPUT_OUTPUT': ['chat', 'user_interface', 'data_input'],
            'MODELS': ['text_generation', 'language_model', 'ai_inference'],
            'AGENTS': ['autonomous_agent', 'tool_usage', 'reasoning'],
            'DATA': ['data_processing', 'file_handling', 'web_scraping'],
            'EMBEDDINGS': ['semantic_search', 'similarity', 'vector_operations'],
            'VECTORSTORES': ['vector_database', 'similarity_search', 'rag'],
            'TOOLS': ['external_apis', 'calculations', 'utilities'],
            'PROCESSING': ['data_transformation', 'text_processing', 'parsing']
        }
        
        use_cases.extend(category_mapping.get(category, []))
        
        # Content-based use cases
        content_lower = content.lower()
        if 'chat' in content_lower:
            use_cases.append('chat')
        if 'search' in content_lower:
            use_cases.append('search')
        if 'document' in content_lower or 'pdf' in content_lower:
            use_cases.append('document_processing')
        if 'embedding' in content_lower:
            use_cases.append('embeddings')
        
        return list(set(use_cases))
    
    def _extract_examples(self, content: str) -> List[str]:
        """Extract usage examples from comments or docstrings."""
        examples = []
        
        # Look for example patterns in comments
        example_matches = re.finditer(r'#\s*[Ee]xample:?\s*(.+)', content)
        for match in examples:
            examples.append(match.group(1).strip())
        
        return examples
    
    def _index_starter_projects(self, starter_path: Path):
        """Index all starter project JSON files."""
        for json_file in starter_path.glob("*.json"):
            try:
                flow_info = self._analyze_flow_file(json_file)
                if flow_info:
                    self.flows[flow_info.name] = flow_info
            except Exception as e:
                print(f"⚠️  Error analyzing flow {json_file}: {e}")
    
    def _analyze_flow_file(self, file_path: Path) -> Optional[FlowInfo]:
        """Analyze a flow JSON file to extract metadata."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                flow_data = json.load(f)
            
            name = flow_data.get('name', file_path.stem)
            description = flow_data.get('description', '')
            
            # Extract components from nodes
            components = []
            if 'data' in flow_data and 'nodes' in flow_data['data']:
                for node in flow_data['data']['nodes']:
                    if 'type' in node:
                        components.append(node['type'])
            
            # Extract connections from edges
            connections = []
            if 'data' in flow_data and 'edges' in flow_data['data']:
                connections = flow_data['data']['edges']
            
            # Determine flow type and complexity
            flow_type = self._determine_flow_type(components, description)
            complexity = self._determine_complexity(components, connections)
            use_case = self._determine_use_case(name, description, components)
            
            return FlowInfo(
                name=name,
                file_path=str(file_path),
                description=description,
                flow_type=flow_type,
                components=components,
                connections=connections,
                use_case=use_case,
                complexity=complexity,
                json_structure=flow_data
            )
            
        except Exception as e:
            print(f"Error analyzing flow {file_path}: {e}")
            return None
    
    def _determine_flow_type(self, components: List[str], description: str) -> str:
        """Determine the type of flow based on components."""
        desc_lower = description.lower()
        
        if any('Agent' in comp for comp in components):
            return 'agent_workflow'
        elif any('Embedding' in comp or 'Vector' in comp for comp in components):
            return 'rag_system'
        elif 'document' in desc_lower or 'pdf' in desc_lower:
            return 'document_qa'
        elif 'chat' in desc_lower:
            return 'basic_chat'
        else:
            return 'general_workflow'
    
    def _determine_complexity(self, components: List[str], connections: List[Dict]) -> str:
        """Determine complexity based on number of components and connections."""
        comp_count = len(components)
        conn_count = len(connections)
        
        if comp_count <= 3 and conn_count <= 2:
            return 'simple'
        elif comp_count <= 7 and conn_count <= 6:
            return 'medium'
        else:
            return 'complex'
    
    def _determine_use_case(self, name: str, description: str, components: List[str]) -> str:
        """Determine the primary use case."""
        text = f"{name} {description}".lower()
        
        if 'document' in text or 'pdf' in text:
            return 'document_processing'
        elif 'agent' in text:
            return 'autonomous_agent'
        elif 'chat' in text:
            return 'conversational_ai'
        elif 'search' in text:
            return 'information_retrieval'
        else:
            return 'general_ai'
    
    def find_similar_flows(self, description: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find flows similar to the given description."""
        desc_lower = description.lower()
        scored_flows = []
        
        for flow_name, flow_info in self.flows.items():
            score = 0
            
            # Score based on description similarity
            flow_desc_lower = flow_info.description.lower()
            common_words = set(desc_lower.split()) & set(flow_desc_lower.split())
            score += len(common_words) * 2
            
            # Score based on use case match
            if flow_info.use_case in desc_lower:
                score += 5
            
            # Score based on component relevance
            for component in flow_info.components:
                if component.lower() in desc_lower:
                    score += 3
            
            if score > 0:
                scored_flows.append({
                    'flow': flow_info,
                    'score': score,
                    'similarity_reasons': f"Matched {len(common_words)} keywords, use case: {flow_info.use_case}"
                })
        
        # Sort by score and return top results
        scored_flows.sort(key=lambda x: x['score'], reverse=True)
        return scored_flows[:limit]
    
    def get_component_by_name(self, name: str) -> Optional[ComponentInfo]:
        """Get component information by name."""
        return self.components.get(name)
    
    def search_components(self, query: str, category: Optional[str] = None) -> List[ComponentInfo]:
        """Search components by query and optional category."""
        query_lower = query.lower()
        results = []
        
        for comp_name, comp_info in self.components.items():
            if category and comp_info.category != category.upper():
                continue
            
            # Search in name, description, and use cases
            searchable_text = f"{comp_info.name} {comp_info.description} {' '.join(comp_info.use_cases)}".lower()
            
            if query_lower in searchable_text:
                results.append(comp_info)
        
        return results
    
    def get_flow_templates(self, flow_type: str) -> List[FlowInfo]:
        """Get flow templates by type."""
        return [flow for flow in self.flows.values() if flow.flow_type == flow_type]
    
    def export_index(self, output_path: str):
        """Export the complete index to JSON for caching."""
        index_data = {
            'components': {name: asdict(info) for name, info in self.components.items()},
            'flows': {name: asdict(info) for name, info in self.flows.items()},
            'component_categories': dict(self.component_categories),
            'use_case_mapping': dict(self.use_case_mapping)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Index exported to {output_path}")

# Global instance
flow_indexer = FlowIndexer()
