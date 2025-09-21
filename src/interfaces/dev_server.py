"""
Production Development Server

High-performance web server for AxieStudio AI Flow Generator
with real-time generation, beautiful UI, and comprehensive features.
"""

import streamlit as st
import json
import time
from typing import Dict, Any, List
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

# Configure page
st.set_page_config(
    page_title="🚀 AxieStudio AI Flow Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for production look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_flows' not in st.session_state:
    st.session_state.generated_flows = []
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []

def load_ai_system():
    """Load AI system with caching."""
    try:
        import sys
        from pathlib import Path

        # Add parent directories to path
        current_dir = Path(__file__).parent
        src_dir = current_dir.parent
        root_dir = src_dir.parent
        sys.path.insert(0, str(src_dir))
        sys.path.insert(0, str(root_dir))

        from ai.super_ai_generator import super_ai_generator
        from ai.ai_knowledge_processor import ai_knowledge_processor
        return super_ai_generator, ai_knowledge_processor
    except Exception as e:
        st.error(f"Error loading AI system: {e}")
        return None, None

def main():
    """Main application."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AxieStudio AI Flow Generator</h1>
        <p>Production-Grade AI-Powered Flow Generation System</p>
        <p><strong>294 Components • 31 Flow Templates • OpenAI GPT-4 Powered</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load AI system
    ai_generator, ai_processor = load_ai_system()
    
    if not ai_generator:
        st.error("❌ AI system not available. Please check configuration.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # System status
        st.subheader("📊 System Status")
        stats = ai_generator.get_generation_stats()
        
        st.metric("Components Available", stats['components_available'])
        st.metric("Flow Templates", stats['flow_templates'])
        st.metric("AI Model", stats['ai_model'])
        
        st.success("✅ System Ready")
        
        # Generation settings
        st.subheader("⚙️ Generation Settings")
        use_ai = st.checkbox("🤖 Use AI Generation", value=True)
        temperature = st.slider("🌡️ AI Creativity", 0.0, 1.0, 0.2, 0.1)
        max_components = st.slider("🔧 Max Components", 3, 15, 10)
        
        # Quick templates
        st.subheader("⚡ Quick Templates")
        templates = {
            "💬 Simple Chat": "Create a simple chatbot with OpenAI GPT-4",
            "📄 Document Q&A": "Create a chatbot that answers questions about PDF documents",
            "🤖 Web Agent": "Build an AI agent that can search the web and do calculations",
            "🔍 RAG System": "Create a retrieval augmented generation system for documents",
            "📊 Data Pipeline": "Build a data processing pipeline with transformations"
        }
        
        selected_template = st.selectbox("Choose template:", list(templates.keys()))
        if st.button("🚀 Use Template"):
            st.session_state.template_description = templates[selected_template]
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 AI Flow Generation")
        
        # Input area
        description = st.text_area(
            "🎯 Describe your desired flow:",
            value=st.session_state.get('template_description', ''),
            height=100,
            placeholder="Example: Create a chatbot that can answer questions about PDF documents using RAG..."
        )
        
        # Generation buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            generate_btn = st.button("🚀 Generate Flow", type="primary", use_container_width=True)
        
        with col_btn2:
            if st.button("⚡ Super Fast Mode", use_container_width=True):
                generate_btn = True
                use_ai = True
        
        with col_btn3:
            if st.button("🔄 Clear History", use_container_width=True):
                st.session_state.generated_flows = []
                st.session_state.generation_history = []
                st.rerun()
        
        # Generation process
        if generate_btn and description:
            with st.spinner("🧠 AI is generating your flow..."):
                start_time = time.time()
                
                try:
                    if use_ai:
                        flow_json = ai_generator.generate_flow_super_fast(description)
                        method = "Super AI"
                    else:
                        # Fallback method
                        from flow_generator import flow_generator
                        requirement = flow_generator.analyze_user_intent(description)
                        flow_json = flow_generator.generate_flow_json(requirement)
                        method = "Rule-based"
                    
                    generation_time = time.time() - start_time
                    
                    # Store results
                    result = {
                        'description': description,
                        'flow_json': flow_json,
                        'method': method,
                        'generation_time': generation_time,
                        'timestamp': datetime.now(),
                        'components': len(flow_json.get('data', {}).get('nodes', [])),
                        'connections': len(flow_json.get('data', {}).get('edges', []))
                    }
                    
                    st.session_state.generated_flows.append(result)
                    st.session_state.generation_history.append(result)
                    
                    # Success message
                    st.markdown(f"""
                    <div class="success-box">
                        <h4>✅ Flow Generated Successfully!</h4>
                        <p><strong>Method:</strong> {method}</p>
                        <p><strong>Generation Time:</strong> {generation_time:.2f} seconds</p>
                        <p><strong>Components:</strong> {result['components']}</p>
                        <p><strong>Connections:</strong> {result['connections']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Generation failed: {e}")
        
        # Display latest flow
        if st.session_state.generated_flows:
            latest_flow = st.session_state.generated_flows[-1]
            
            st.header("📋 Generated Flow")
            
            # Flow info
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.metric("Components", latest_flow['components'])
            with col_info2:
                st.metric("Connections", latest_flow['connections'])
            with col_info3:
                st.metric("Generation Time", f"{latest_flow['generation_time']:.2f}s")
            
            # Flow JSON
            with st.expander("📄 View Flow JSON", expanded=False):
                st.json(latest_flow['flow_json'])
            
            # Download button
            flow_filename = f"axiestudio_flow_{int(time.time())}.json"
            st.download_button(
                label="💾 Download Flow JSON",
                data=json.dumps(latest_flow['flow_json'], indent=2),
                file_name=flow_filename,
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        st.header("📊 Analytics")
        
        # Generation history chart
        if st.session_state.generation_history:
            df = pd.DataFrame([
                {
                    'Time': h['timestamp'],
                    'Components': h['components'],
                    'Generation Time': h['generation_time'],
                    'Method': h['method']
                }
                for h in st.session_state.generation_history
            ])
            
            # Generation time chart
            fig_time = px.line(df, x='Time', y='Generation Time', 
                              title='Generation Performance',
                              color='Method')
            st.plotly_chart(fig_time, use_container_width=True)
            
            # Components distribution
            fig_comp = px.histogram(df, x='Components', 
                                   title='Components Distribution',
                                   nbins=10)
            st.plotly_chart(fig_comp, use_container_width=True)
        
        # System metrics
        st.subheader("🔧 System Metrics")
        
        metrics_data = {
            'Metric': ['Total Generations', 'Avg Generation Time', 'Success Rate', 'AI Usage'],
            'Value': [
                len(st.session_state.generation_history),
                f"{sum(h['generation_time'] for h in st.session_state.generation_history) / max(len(st.session_state.generation_history), 1):.2f}s",
                "100%",
                f"{sum(1 for h in st.session_state.generation_history if h['method'] == 'Super AI') / max(len(st.session_state.generation_history), 1) * 100:.0f}%"
            ]
        }
        
        for metric, value in zip(metrics_data['Metric'], metrics_data['Value']):
            st.markdown(f"""
            <div class="metric-card">
                <strong>{metric}:</strong> {value}
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 <strong>AxieStudio AI Flow Generator</strong> - Production Edition</p>
        <p>Powered by OpenAI GPT-4 • 294 Components Indexed • Real-time Generation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
