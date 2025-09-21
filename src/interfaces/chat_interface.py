"""
Chat Interface Module

Provides an interactive chat interface for users to describe their requirements
and receive generated AxieStudio flows.
"""

import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table
from rich.syntax import Syntax

from flow_generator import flow_generator, FlowRequirement, FlowType
from component_kb import component_kb

@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

class ChatInterface:
    """Interactive chat interface for flow generation."""
    
    def __init__(self):
        self.console = Console()
        self.conversation_history: List[ChatMessage] = []
        self.current_flow: Optional[Dict[str, Any]] = None
        self.flow_generator = flow_generator
        self.component_kb = component_kb
    
    def start_chat(self):
        """Start the interactive chat session."""
        self.console.print(Panel.fit(
            "[bold blue]AxieStudio Chat Flow Generator[/bold blue]\n"
            "Describe what you want to build, and I'll generate a complete flow for you!",
            title="Welcome"
        ))
        
        self._show_examples()
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]You[/bold green]")
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self.console.print("[yellow]Goodbye! Happy flow building! 🚀[/yellow]")
                    break
                
                if user_input.lower() in ['help', '?']:
                    self._show_help()
                    continue
                
                if user_input.lower() == 'examples':
                    self._show_examples()
                    continue
                
                if user_input.lower() == 'components':
                    self._show_components()
                    continue
                
                # Process user request
                self._process_user_request(user_input)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Goodbye! Happy flow building! 🚀[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")
    
    def _process_user_request(self, user_input: str):
        """Process user request and generate flow."""
        # Add user message to history
        self.conversation_history.append(ChatMessage(
            role="user",
            content=user_input,
            timestamp=datetime.now()
        ))
        
        # Analyze user intent
        requirement = self.flow_generator.analyze_user_intent(user_input)
        
        # Generate response
        response = self._generate_response(requirement)
        
        # Add assistant message to history
        self.conversation_history.append(ChatMessage(
            role="assistant",
            content=response,
            timestamp=datetime.now(),
            metadata={"requirement": requirement}
        ))
        
        # Display response
        self.console.print(f"\n[bold blue]Assistant[/bold blue]: {response}")
        
        # Generate and display flow
        self._generate_and_display_flow(requirement)
    
    def _generate_response(self, requirement: FlowRequirement) -> str:
        """Generate conversational response based on requirements."""
        flow_type_descriptions = {
            FlowType.BASIC_CHAT: "a simple chat interface",
            FlowType.DOCUMENT_QA: "a document Q&A system with RAG",
            FlowType.AGENT_TOOLS: "an AI agent with tools",
            FlowType.RAG_SYSTEM: "a Retrieval Augmented Generation system",
            FlowType.DATA_PROCESSING: "a data processing pipeline",
            FlowType.MULTI_AGENT: "a multi-agent system"
        }
        
        description = flow_type_descriptions.get(requirement.flow_type, "a custom flow")
        
        response = f"I'll help you create {description}! "
        
        if requirement.components_needed:
            components_list = ", ".join(requirement.components_needed)
            response += f"This will include components like: {components_list}. "
        
        if requirement.specific_models:
            models_list = ", ".join(requirement.specific_models)
            response += f"I'll use {models_list} as requested. "
        
        response += "Let me generate the complete flow for you..."
        
        return response
    
    def _generate_and_display_flow(self, requirement: FlowRequirement):
        """Generate flow and display it to the user."""
        try:
            # Generate flow JSON
            flow_json = self.flow_generator.generate_flow_json(requirement)
            self.current_flow = flow_json
            
            # Display flow summary
            self._display_flow_summary(flow_json)
            
            # Ask if user wants to see the JSON or save it
            self._handle_flow_actions()
            
        except Exception as e:
            self.console.print(f"[red]Error generating flow: {str(e)}[/red]")
    
    def _display_flow_summary(self, flow_json: Dict[str, Any]):
        """Display a summary of the generated flow."""
        nodes = flow_json["data"]["nodes"]
        edges = flow_json["data"]["edges"]
        
        table = Table(title="Generated Flow Summary")
        table.add_column("Component", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Description", style="green")
        
        for node in nodes:
            node_data = node["data"]
            component_type = node_data["type"]
            display_name = node_data["node"]["display_name"]
            description = node_data["node"]["description"]
            
            table.add_row(display_name, component_type, description[:50] + "...")
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print(f"\n[bold]Flow Details:[/bold]")
        self.console.print(f"• Components: {len(nodes)}")
        self.console.print(f"• Connections: {len(edges)}")
        self.console.print(f"• Name: {flow_json['name']}")
    
    def _handle_flow_actions(self):
        """Handle user actions for the generated flow."""
        while True:
            action = Prompt.ask(
                "\nWhat would you like to do?",
                choices=["save", "json", "modify", "new", "quit"],
                default="save"
            )
            
            if action == "save":
                self._save_flow()
                break
            elif action == "json":
                self._show_flow_json()
            elif action == "modify":
                self._modify_flow()
                break
            elif action == "new":
                break
            elif action == "quit":
                return "quit"
    
    def _save_flow(self):
        """Save the generated flow to a file."""
        if not self.current_flow:
            self.console.print("[red]No flow to save![/red]")
            return
        
        filename = Prompt.ask(
            "Enter filename (without extension)",
            default=f"generated_flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        filepath = f"{filename}.json"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.current_flow, f, indent=2, ensure_ascii=False)
            
            self.console.print(f"[green]✅ Flow saved to {filepath}[/green]")
            self.console.print("[blue]You can now import this file into AxieStudio![/blue]")
            
        except Exception as e:
            self.console.print(f"[red]Error saving flow: {str(e)}[/red]")
    
    def _show_flow_json(self):
        """Display the flow JSON."""
        if not self.current_flow:
            self.console.print("[red]No flow to display![/red]")
            return
        
        json_str = json.dumps(self.current_flow, indent=2)
        syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
        
        self.console.print("\n[bold]Generated Flow JSON:[/bold]")
        self.console.print(syntax)
    
    def _modify_flow(self):
        """Allow user to modify the current flow."""
        self.console.print("[yellow]Flow modification coming soon![/yellow]")
        self.console.print("For now, you can describe changes and I'll generate a new flow.")
        
        modification = Prompt.ask("What changes would you like to make?")
        self._process_user_request(f"Modify the current flow: {modification}")
    
    def _show_examples(self):
        """Show example requests."""
        examples = [
            "Create a chatbot that can answer questions about PDF documents",
            "Build an AI agent that can search the web and do calculations",
            "Make a simple chat interface with GPT-4",
            "Create a document processing pipeline with embeddings",
            "Build a multi-agent system for research tasks"
        ]
        
        self.console.print("\n[bold]Example requests:[/bold]")
        for i, example in enumerate(examples, 1):
            self.console.print(f"{i}. {example}")
    
    def _show_help(self):
        """Show help information."""
        help_text = """
[bold]Available Commands:[/bold]
• [cyan]help[/cyan] or [cyan]?[/cyan] - Show this help
• [cyan]examples[/cyan] - Show example requests
• [cyan]components[/cyan] - Show available components
• [cyan]quit[/cyan] or [cyan]exit[/cyan] - Exit the chat

[bold]How to use:[/bold]
1. Describe what you want to build in natural language
2. I'll analyze your request and generate a complete flow
3. You can save the flow, view the JSON, or make modifications

[bold]Tips:[/bold]
• Be specific about the AI models you want (GPT-4, Claude, etc.)
• Mention data sources (PDFs, web search, etc.)
• Describe the type of interaction (chat, agent, processing)
        """
        self.console.print(Panel(help_text, title="Help"))
    
    def _show_components(self):
        """Show available components."""
        table = Table(title="Available AxieStudio Components")
        table.add_column("Component", style="cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Description", style="green")
        
        for component in self.component_kb.components.values():
            table.add_row(
                component.display_name,
                component.category.value,
                component.description[:60] + "..."
            )
        
        self.console.print("\n")
        self.console.print(table)

# Create global instance
chat_interface = ChatInterface()
