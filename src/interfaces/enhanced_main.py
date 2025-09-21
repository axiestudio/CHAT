"""
Enhanced Main Application

Production-grade CLI application with AI-powered flow generation using
OpenAI GPT-4 and comprehensive AxieStudio component indexing.
"""

import os
import json
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
config_path = Path(__file__).parent.parent.parent / "config" / ".env"
load_dotenv(config_path)

# Add parent directories to path
import sys
current_dir = Path(__file__).parent
src_dir = current_dir.parent
root_dir = src_dir.parent
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(root_dir))

from ai.super_ai_generator import super_ai_generator
from ai.flow_indexer import flow_indexer
from ai.component_kb import component_kb

app = typer.Typer(help="🚀 AxieStudio AI Flow Generator - Production Edition")
console = Console()

def check_openai_key() -> bool:
    """Check if OpenAI API key is available."""
    return bool(os.getenv("OPENAI_API_KEY"))

@app.command()
def ai_generate(
    description: str = typer.Argument(..., help="Natural language description of the desired flow"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output JSON file path"),
    use_ai: bool = typer.Option(True, "--ai/--no-ai", help="Use AI-powered generation (requires OpenAI API key)")
):
    """🤖 Generate flow using AI-powered understanding (Production Mode)."""
    
    console.print(Panel.fit(
        f"🚀 [bold blue]AI Flow Generator[/bold blue]\n"
        f"📝 Description: {description}\n"
        f"🤖 AI Mode: {'Enabled' if use_ai else 'Disabled'}\n"
        f"🔑 OpenAI Key: {'✅ Available' if check_openai_key() else '❌ Missing'}",
        title="Production Flow Generation"
    ))
    
    if use_ai and not check_openai_key():
        console.print("❌ [red]OpenAI API key required for AI mode. Set OPENAI_API_KEY environment variable.[/red]")
        console.print("💡 [yellow]Falling back to rule-based generation...[/yellow]")
        use_ai = False
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            if use_ai:
                # AI-powered generation
                task = progress.add_task("🧠 Analyzing intent with AI...", total=None)
                # Use super AI generator for maximum efficiency
                flow_json = super_ai_generator.generate_flow_super_fast(description)
                
                progress.update(task, description="🔍 Loading templates...")
                # Templates are already loaded in super_ai_generator

                progress.update(task, description="🤖 Generating flow with AI...")
                # flow_json already generated above
                
                progress.update(task, description="✅ AI generation complete!")
                
            else:
                # Fallback to rule-based generation
                task = progress.add_task("⚙️  Generating flow (rule-based)...", total=None)
                from flow_generator import flow_generator
                requirement = flow_generator.analyze_user_intent(description)
                flow_json = flow_generator.generate_flow_json(requirement)
        
        # Save output
        if output:
            output_path = Path(output)
        else:
            safe_name = "".join(c for c in description[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_path = Path(f"ai_generated_{safe_name.replace(' ', '_').lower()}.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(flow_json, f, indent=2, ensure_ascii=False)
        
        # Display results
        console.print(f"✅ [green]Flow generated and saved to {output_path}[/green]")
        
        # Show flow summary
        data = flow_json.get('data', {})
        nodes = data.get('nodes', [])
        edges = data.get('edges', [])
        
        summary_table = Table(title="Flow Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Components", str(len(nodes)))
        summary_table.add_row("Connections", str(len(edges)))
        summary_table.add_row("Generation Method", "AI-Powered" if use_ai else "Rule-Based")
        summary_table.add_row("Output File", str(output_path))
        
        console.print(summary_table)
        
        # Show component list
        if nodes:
            comp_table = Table(title="Components Used")
            comp_table.add_column("Component", style="blue")
            comp_table.add_column("Display Name", style="green")
            
            for node in nodes:
                comp_table.add_row(
                    node.get('type', 'Unknown'),
                    node.get('data', {}).get('display_name', node.get('type', 'Unknown'))
                )
            
            console.print(comp_table)
        
    except Exception as e:
        console.print(f"❌ [red]Error generating flow: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def ai_chat():
    """💬 Start AI-powered interactive chat session."""
    
    if not check_openai_key():
        console.print("❌ [red]OpenAI API key required for AI chat. Set OPENAI_API_KEY environment variable.[/red]")
        raise typer.Exit(1)
    
    console.print(Panel.fit(
        "🤖 [bold blue]AI-Powered Flow Chat[/bold blue]\n"
        "Describe what you want to build and I'll create the perfect AxieStudio flow!\n"
        "Type 'quit' to exit.",
        title="Production AI Chat"
    ))
    
    # Use super AI generator for chat interface
    
    while True:
        try:
            user_input = typer.prompt("\n🎯 What flow would you like to create?")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("👋 [blue]Goodbye![/blue]")
                break
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("🧠 AI is thinking...", total=None)
                
                # Generate flow with AI
                flow_json = super_ai_generator.generate_flow_super_fast(user_input)
                
                progress.update(task, description="✅ Flow generated!")
            
            # Save flow
            safe_name = "".join(c for c in user_input[:20] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"ai_chat_{safe_name.replace(' ', '_').lower()}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(flow_json, f, indent=2, ensure_ascii=False)
            
            # Show results
            data = flow_json.get('data', {})
            nodes = data.get('nodes', [])
            edges = data.get('edges', [])
            
            console.print(f"\n✅ [green]Generated flow with {len(nodes)} components and {len(edges)} connections![/green]")
            console.print(f"💾 [blue]Saved to: {filename}[/blue]")
            
            # Show components
            if nodes:
                console.print("\n📦 [yellow]Components:[/yellow]")
                for i, node in enumerate(nodes, 1):
                    console.print(f"  {i}. {node.get('data', {}).get('display_name', node.get('type', 'Unknown'))}")
            
        except KeyboardInterrupt:
            console.print("\n👋 [blue]Goodbye![/blue]")
            break
        except Exception as e:
            console.print(f"❌ [red]Error: {e}[/red]")

@app.command()
def index_status():
    """📊 Show indexing status and statistics."""
    
    console.print(Panel.fit(
        "📊 [bold blue]AxieStudio Index Status[/bold blue]",
        title="Production Index"
    ))
    
    # Component statistics
    comp_table = Table(title="Component Index")
    comp_table.add_column("Category", style="cyan")
    comp_table.add_column("Count", style="green")
    
    categories = {}
    for comp in flow_indexer.components.values():
        categories[comp.category] = categories.get(comp.category, 0) + 1
    
    for category, count in sorted(categories.items()):
        comp_table.add_row(category, str(count))
    
    comp_table.add_row("[bold]TOTAL[/bold]", f"[bold]{len(flow_indexer.components)}[/bold]")
    console.print(comp_table)
    
    # Flow statistics
    flow_table = Table(title="Flow Templates")
    flow_table.add_column("Flow Type", style="cyan")
    flow_table.add_column("Count", style="green")
    
    flow_types = {}
    for flow in flow_indexer.flows.values():
        flow_types[flow.flow_type] = flow_types.get(flow.flow_type, 0) + 1
    
    for flow_type, count in sorted(flow_types.items()):
        flow_table.add_row(flow_type, str(count))
    
    flow_table.add_row("[bold]TOTAL[/bold]", f"[bold]{len(flow_indexer.flows)}[/bold]")
    console.print(flow_table)

@app.command()
def search_components(
    query: str = typer.Argument(..., help="Search query for components"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category")
):
    """🔍 Search indexed components."""
    
    results = flow_indexer.search_components(query, category)
    
    if not results:
        console.print(f"❌ [red]No components found for query: '{query}'[/red]")
        return
    
    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Component", style="blue")
    table.add_column("Category", style="cyan")
    table.add_column("Description", style="green")
    
    for comp in results[:10]:  # Limit to top 10
        table.add_row(
            comp.display_name,
            comp.category,
            comp.description[:60] + "..." if len(comp.description) > 60 else comp.description
        )
    
    console.print(table)
    
    if len(results) > 10:
        console.print(f"... and {len(results) - 10} more results")

@app.command()
def export_index(
    output: str = typer.Option("axiestudio_index.json", "--output", "-o", help="Output file path")
):
    """📁 Export complete index to JSON file."""
    
    flow_indexer.export_index(output)
    console.print(f"✅ [green]Index exported to {output}[/green]")

if __name__ == "__main__":
    app()
