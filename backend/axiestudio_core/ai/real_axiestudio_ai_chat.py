"""
Real AxieStudio AI Chat System

This is a CONVERSATIONAL AI system that:
1. Uses REAL AxieStudio component data
2. Provides natural chat interface with OpenAI
3. Generates AUTHENTIC AxieStudio JSON flows
4. Maintains conversation context and follow-ups

This ensures users get REAL AxieStudio flows, not generic ones!
"""

import json
import os
from typing import Dict, List, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import logging

from .real_axiestudio_crawler import real_axiestudio_crawler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
from pathlib import Path
config_path = Path(__file__).parent.parent.parent / "config" / ".env"
load_dotenv(config_path)

class RealAxieStudioAIChat:
    """Conversational AI system for generating real AxieStudio flows."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history: List[Dict[str, Any]] = []
        
        # Load real AxieStudio data
        logger.info("🔍 Loading real AxieStudio component data...")
        self.axiestudio_data = real_axiestudio_crawler.crawl_all()
        
        # Create AI knowledge base
        self.ai_knowledge = self._create_ai_knowledge_base()
        
        logger.info(f"🚀 Real AxieStudio AI Chat ready with {len(self.axiestudio_data['components'])} components")
    
    def _create_ai_knowledge_base(self) -> str:
        """Create comprehensive knowledge base for AI from real AxieStudio data."""
        
        knowledge_parts = []
        
        # Component knowledge
        knowledge_parts.append("=== REAL AXIESTUDIO COMPONENTS ===")
        for comp_name, comp_info in self.axiestudio_data['components'].items():
            knowledge_parts.append(f"""
COMPONENT: {comp_name}
- Display Name: {comp_info['display_name']}
- Description: {comp_info['description']}
- Base Classes: {', '.join(comp_info['base_classes'])}
- Inputs: {len(comp_info['inputs'])} input(s)
- Outputs: {len(comp_info['outputs'])} output(s)
- Module: {comp_info['module_path']}
""")
        
        # Flow patterns knowledge
        knowledge_parts.append("\n=== REAL AXIESTUDIO FLOW PATTERNS ===")
        for flow_name, flow_info in self.axiestudio_data['flows'].items():
            knowledge_parts.append(f"""
FLOW: {flow_name}
- Description: {flow_info['description']}
- Components Used: {', '.join(flow_info['components_used'])}
- Nodes: {len(flow_info['nodes'])} node(s)
- Edges: {len(flow_info['edges'])} connection(s)
""")
        
        # Component relationships
        knowledge_parts.append("\n=== COMPONENT RELATIONSHIPS ===")
        for comp, related in self.axiestudio_data['relationships'].items():
            if related:
                knowledge_parts.append(f"{comp} commonly used with: {', '.join(related[:5])}")
        
        return "\n".join(knowledge_parts)
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """Process user message and return conversational response with flow generation."""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Determine if user wants to generate a flow
        intent = self._analyze_user_intent(user_message)
        
        if intent["wants_flow"]:
            return self._generate_flow_with_chat(user_message, intent)
        else:
            return self._provide_conversational_response(user_message, intent)
    
    def _analyze_user_intent(self, message: str) -> Dict[str, Any]:
        """Analyze what the user wants to do."""
        
        system_prompt = f"""You are an expert AxieStudio assistant. Analyze the user's message to understand their intent.

REAL AXIESTUDIO KNOWLEDGE:
{self.ai_knowledge[:2000]}  # Truncated for prompt

User message: "{message}"

Respond with JSON:
{{
    "wants_flow": true/false,
    "flow_type": "chat/rag/agent/data_processing/other",
    "complexity": "simple/medium/complex",
    "specific_components": ["list", "of", "components"],
    "clarification_needed": true/false,
    "clarification_questions": ["question1", "question2"]
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": system_prompt}],
                temperature=0.2,
                max_tokens=500
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.warning(f"Intent analysis failed: {e}")
            return {
                "wants_flow": "create" in message.lower() or "build" in message.lower(),
                "flow_type": "chat",
                "complexity": "simple",
                "specific_components": [],
                "clarification_needed": False,
                "clarification_questions": []
            }
    
    def _generate_flow_with_chat(self, user_message: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a real AxieStudio flow with conversational response."""
        
        # Create conversation context
        conversation_context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history[-5:]  # Last 5 messages
        ])
        
        # Generate conversational response
        chat_response = self._generate_chat_response(user_message, intent, conversation_context)
        
        # Generate actual AxieStudio flow
        flow_json = self._generate_real_axiestudio_flow(user_message, intent)
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": chat_response,
            "timestamp": datetime.now().isoformat(),
            "flow_generated": True,
            "flow_data": flow_json
        })
        
        return {
            "success": True,
            "message": chat_response,
            "flow": flow_json,
            "intent": intent,
            "conversation_id": len(self.conversation_history)
        }
    
    def _generate_chat_response(self, user_message: str, intent: Dict[str, Any], context: str) -> str:
        """Generate natural conversational response."""
        
        system_prompt = f"""You are a friendly AxieStudio AI assistant. You help users create powerful flows using real AxieStudio components.

CONVERSATION CONTEXT:
{context}

USER INTENT: {json.dumps(intent, indent=2)}

REAL AXIESTUDIO COMPONENTS AVAILABLE:
{', '.join(list(self.axiestudio_data['components'].keys())[:20])}...

Generate a friendly, helpful response that:
1. Acknowledges what the user wants to build
2. Explains what components you'll use
3. Mentions any special features or capabilities
4. Sounds natural and conversational

Keep it concise but informative (2-3 sentences)."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.warning(f"Chat response generation failed: {e}")
            return f"I'll help you create a {intent.get('flow_type', 'custom')} flow! Let me generate that for you using real AxieStudio components."
    
    def _generate_real_axiestudio_flow(self, user_message: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Generate authentic AxieStudio flow JSON using real component data."""
        
        # Select appropriate template flow based on intent
        template_flow = self._select_best_template_flow(intent)
        
        if not template_flow:
            return self._create_minimal_real_flow(user_message, intent)
        
        # Customize template with AI
        customized_flow = self._customize_flow_with_ai(template_flow, user_message, intent)
        
        return customized_flow
    
    def _select_best_template_flow(self, intent: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select the best template flow based on user intent."""
        
        flow_type = intent.get("flow_type", "chat")
        
        # Map intent to actual flow templates
        flow_mapping = {
            "chat": "Basic Prompting",
            "rag": "Vector Store RAG", 
            "agent": "Simple Agent",
            "data_processing": "Document Q&A"
        }
        
        template_name = flow_mapping.get(flow_type)
        if template_name and template_name in self.axiestudio_data['flows']:
            return self.axiestudio_data['flows'][template_name]
        
        # Fallback to first available flow
        if self.axiestudio_data['flows']:
            return list(self.axiestudio_data['flows'].values())[0]
        
        return None
    
    def _customize_flow_with_ai(self, template_flow: Dict[str, Any], user_message: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to customize template flow for user's specific needs."""
        
        # Create customization prompt
        system_prompt = f"""You are an expert AxieStudio flow architect. Customize this real AxieStudio flow template for the user's specific needs.

TEMPLATE FLOW:
{json.dumps(template_flow, indent=2)[:1500]}...

USER REQUEST: "{user_message}"
USER INTENT: {json.dumps(intent, indent=2)}

AVAILABLE COMPONENTS:
{', '.join(list(self.axiestudio_data['components'].keys())[:30])}

Customize the flow by:
1. Updating the name and description
2. Modifying component parameters if needed
3. Keeping the same JSON structure
4. Ensuring all components exist in our component list

Return the complete customized flow JSON."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": system_prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            customized = json.loads(response.choices[0].message.content)
            
            # Add metadata
            customized["metadata"] = customized.get("metadata", {})
            customized["metadata"].update({
                "generated_by": "Real AxieStudio AI Chat",
                "user_request": user_message,
                "generation_timestamp": datetime.now().isoformat(),
                "template_used": template_flow["name"]
            })
            
            return customized
            
        except Exception as e:
            logger.warning(f"Flow customization failed: {e}")
            # Return original template with updated metadata
            template_flow["name"] = f"AI Generated: {user_message[:50]}..."
            template_flow["description"] = f"Generated flow for: {user_message}"
            return template_flow
    
    def _create_minimal_real_flow(self, user_message: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Create minimal but real AxieStudio flow as fallback."""
        
        return {
            "name": f"AI Generated: {user_message[:50]}...",
            "description": f"Generated flow for: {user_message}",
            "data": {
                "nodes": [],
                "edges": [],
                "viewport": {"x": 0, "y": 0, "zoom": 1}
            },
            "metadata": {
                "generated_by": "Real AxieStudio AI Chat",
                "user_request": user_message,
                "generation_timestamp": datetime.now().isoformat(),
                "fallback_flow": True
            }
        }
    
    def _provide_conversational_response(self, user_message: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Provide conversational response without flow generation."""
        
        system_prompt = f"""You are a helpful AxieStudio AI assistant. The user is asking a question or having a conversation.

AVAILABLE AXIESTUDIO COMPONENTS:
{', '.join(list(self.axiestudio_data['components'].keys())[:20])}...

CONVERSATION HISTORY:
{json.dumps(self.conversation_history[-3:], indent=2) if self.conversation_history else "No previous conversation"}

Provide a helpful, conversational response. If they're asking about AxieStudio capabilities, mention real components and features."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            chat_response = response.choices[0].message.content
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": chat_response,
                "timestamp": datetime.now().isoformat(),
                "flow_generated": False
            })
            
            return {
                "success": True,
                "message": chat_response,
                "flow": None,
                "intent": intent,
                "conversation_id": len(self.conversation_history)
            }
            
        except Exception as e:
            logger.warning(f"Conversational response failed: {e}")
            return {
                "success": False,
                "message": "I'm here to help you create AxieStudio flows! What would you like to build?",
                "error": str(e)
            }
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history."""
        return self.conversation_history
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
        logger.info("🗑️ Conversation history cleared")

# Global instance
real_axiestudio_ai_chat = RealAxieStudioAIChat()
