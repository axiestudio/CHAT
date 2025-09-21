"""
Web Interface for AxieStudio Chat Flow Generator

A Streamlit-based web interface for generating AxieStudio flows through chat.
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
import sys

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from flow_generator import flow_generator, FlowType
from component_kb import component_kb

# Page configuration
st.set_page_config(
    page_title="AxieStudio Flow Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
    }
    .user-message {
        border-left-color: #28a745;
        background-color: #e8f5e9;
    }
    .assistant-message {
        border-left-color: #1f77b4;
        background-color: #e3f2fd;
    }
    .component-card {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_flow' not in st.session_state:
        st.session_state.current_flow = None
    if 'flow_generated' not in st.session_state:
        st.session_state.flow_generated = False

def display_header():
    """Display the main header."""
    st.markdown('<h1 class="main-header">🤖 AxieStudio Flow Generator</h1>', unsafe_allow_html=True)
    st.markdown("**Describe what you want to build, and I'll generate a complete AxieStudio flow for you!**")

def display_sidebar():
    """Display the sidebar with information and examples."""
    with st.sidebar:
        st.header("📚 How to Use")
        st.markdown("""
        1. **Describe** your desired workflow in natural language
        2. **Review** the generated flow components
        3. **Download** the JSON file to import into AxieStudio
        """)
        
        st.header("💡 Examples")
        examples = [
            "Create a chatbot for PDF documents",
            "Build an agent with web search",
            "Make a simple GPT-4 chat",
            "Create a RAG system",
            "Build a multi-agent workflow"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{example}"):
                st.session_state.user_input = example
        
        st.header("🔧 Available Components")
        categories = {}
        for comp in component_kb.components.values():
            cat = comp.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(comp.display_name)
        
        for category, components in categories.items():
            with st.expander(f"{category.replace('_', ' ').title()} ({len(components)})"):
                for comp in components:
                    st.write(f"• {comp}")

def display_chat_interface():
    """Display the main chat interface."""
    # Chat input
    user_input = st.text_area(
        "What would you like to build?",
        height=100,
        placeholder="Example: Create a chatbot that can answer questions about PDF documents using GPT-4",
        key="user_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        generate_button = st.button("🚀 Generate Flow", type="primary")
    
    with col2:
        clear_button = st.button("🗑️ Clear Chat")
    
    if clear_button:
        st.session_state.conversation_history = []
        st.session_state.current_flow = None
        st.session_state.flow_generated = False
        st.rerun()
    
    # Process user input
    if generate_button and user_input.strip():
        process_user_request(user_input.strip())
        st.rerun()
    
    # Display conversation history
    display_conversation_history()

def process_user_request(user_input: str):
    """Process user request and generate flow."""
    # Add user message to history
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    try:
        # Analyze user intent
        requirement = flow_generator.analyze_user_intent(user_input)
        
        # Generate response
        response = generate_response(requirement)
        
        # Generate flow
        flow_json = flow_generator.generate_flow_json(requirement)
        st.session_state.current_flow = flow_json
        st.session_state.flow_generated = True
        
        # Add assistant message to history
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now(),
            "flow": flow_json
        })
        
    except Exception as e:
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": f"Sorry, I encountered an error: {str(e)}",
            "timestamp": datetime.now()
        })

def generate_response(requirement) -> str:
    """Generate conversational response."""
    flow_type_descriptions = {
        FlowType.BASIC_CHAT: "a simple chat interface",
        FlowType.DOCUMENT_QA: "a document Q&A system with RAG",
        FlowType.AGENT_TOOLS: "an AI agent with tools",
        FlowType.RAG_SYSTEM: "a Retrieval Augmented Generation system"
    }
    
    description = flow_type_descriptions.get(requirement.flow_type, "a custom flow")
    
    response = f"Great! I've created {description} for you. "
    
    if requirement.components_needed:
        components_list = ", ".join(requirement.components_needed)
        response += f"This flow includes: {components_list}. "
    
    response += "You can download the JSON file below to import into AxieStudio!"
    
    return response

def display_conversation_history():
    """Display the conversation history."""
    if not st.session_state.conversation_history:
        st.info("👋 Start by describing what you'd like to build!")
        return
    
    st.header("💬 Conversation")
    
    for message in st.session_state.conversation_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {content}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong> {content}</div>', 
                       unsafe_allow_html=True)
            
            # Display flow if available
            if "flow" in message:
                display_flow_summary(message["flow"])

def display_flow_summary(flow_json):
    """Display flow summary and download option."""
    if not flow_json:
        return
    
    st.subheader("📊 Generated Flow")
    
    nodes = flow_json["data"]["nodes"]
    edges = flow_json["data"]["edges"]
    
    # Flow statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Components", len(nodes))
    with col2:
        st.metric("Connections", len(edges))
    with col3:
        st.metric("Flow Type", flow_json.get("name", "Custom Flow").split(" - ")[-1])
    
    # Component details
    st.subheader("🔧 Components")
    
    for i, node in enumerate(nodes):
        node_data = node["data"]
        component_type = node_data["type"]
        display_name = node_data["node"]["display_name"]
        description = node_data["node"]["description"]
        
        with st.expander(f"{i+1}. {display_name} ({component_type})"):
            st.write(description)
            
            # Show inputs if available
            template = node_data["node"].get("template", {})
            if template:
                st.write("**Inputs:**")
                for field_name, field_config in template.items():
                    if field_config.get("show", True):
                        st.write(f"• {field_config.get('display_name', field_name)}: {field_config.get('type', 'unknown')}")
    
    # Download options
    st.subheader("💾 Download Flow")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON download
        json_str = json.dumps(flow_json, indent=2)
        st.download_button(
            label="📄 Download JSON",
            data=json_str,
            file_name=f"axiestudio_flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # Show JSON button
        if st.button("👁️ View JSON"):
            st.json(flow_json)

def main():
    """Main application function."""
    initialize_session_state()
    display_header()
    display_sidebar()
    display_chat_interface()

if __name__ == "__main__":
    main()
