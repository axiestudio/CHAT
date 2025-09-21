# AxieStudio Chat Flow Generator

An intelligent chat interface that uses machine learning to generate drag-and-drop flows for AxieStudio based on user natural language input.

## Overview

This project creates a conversational AI that understands user requirements and automatically generates working AxieStudio flows. Users can simply describe what they want to accomplish, and the system will:

1. **Understand** the user's intent through natural language processing
2. **Analyze** available AxieStudio components and their capabilities
3. **Generate** a complete flow JSON structure
4. **Provide** the working flow that can be imported into AxieStudio

## Features

- 🤖 **Natural Language Understanding**: Describe your workflow in plain English
- 🔧 **Component Intelligence**: Knows all available AxieStudio components and their connections
- 📊 **Flow Generation**: Creates complete, working flow JSON files
- 🎯 **Template-Based**: Uses proven starter project patterns
- 💬 **Interactive Chat**: Conversational interface for refinement and clarification

## Architecture

### Components

1. **Chat Interface** (`chat_interface.py`)
   - Handles user conversations
   - Manages conversation context
   - Provides interactive flow refinement

2. **Flow Generator** (`flow_generator.py`)
   - Analyzes user requirements
   - Maps requirements to AxieStudio components
   - Generates flow JSON structures

3. **Component Knowledge Base** (`component_kb.py`)
   - Contains information about all AxieStudio components
   - Defines component capabilities and connections
   - Provides component usage patterns

4. **Template Engine** (`template_engine.py`)
   - Uses starter project templates as base patterns
   - Adapts templates to user requirements
   - Ensures flow validity and best practices

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd axiestudio-chat-flow-generator

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Usage

```bash
# Start the chat interface
python main.py
```

### Example Conversation

```
User: I want to create a chatbot that can answer questions about documents

AI: I'll help you create a document Q&A chatbot! Let me generate a flow that includes:
- Document loading and processing
- Vector storage for semantic search
- Question answering with context retrieval
- Chat interface for user interaction

Would you like me to include specific document types or AI models?

User: Yes, use PDF documents and OpenAI GPT-4

AI: Perfect! I'm generating a flow with:
- PDF Document Loader
- Text Splitter for chunking
- OpenAI Embeddings
- Vector Store (Chroma)
- OpenAI GPT-4 model
- Retrieval QA chain
- Chat Input/Output

[Generated Flow JSON provided]
```

## Generated Flow Types

The system can generate various types of flows:

- **Document Q&A**: RAG-based question answering
- **Chatbots**: Conversational AI with memory
- **Data Processing**: ETL and transformation workflows
- **Multi-Agent Systems**: Coordinated AI agent workflows
- **API Integrations**: External service connections
- **Content Generation**: Text, image, and media creation

## Technical Details

### Flow Generation Process

1. **Intent Recognition**: Classify user request type
2. **Component Selection**: Choose appropriate AxieStudio components
3. **Flow Architecture**: Design component connections and data flow
4. **JSON Generation**: Create valid AxieStudio flow JSON
5. **Validation**: Ensure flow completeness and correctness

### Supported Components

- **Input/Output**: Chat Input, Text Input, File Input, Chat Output
- **Models**: OpenAI, Anthropic, Mistral, Groq, Google AI
- **Agents**: Single agents, multi-agent crews, tool-calling agents
- **Data**: Document loaders, text splitters, data transformers
- **Vector Stores**: Chroma, Pinecone, Weaviate, FAISS
- **Tools**: Web search, calculators, APIs, custom tools
- **Logic**: Conditional routing, data parsing, flow control

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with various flow types
5. Submit a pull request

## License

MIT License - see LICENSE file for details
