#!/usr/bin/env python3
"""
Test script for the AxieStudio Flow Generator

This script tests the flow generation functionality with various examples.
"""

import json
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from flow_generator import flow_generator
from component_kb import component_kb
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def test_flow_generation():
    """Test flow generation with various examples."""
    
    test_cases = [
        {
            "description": "Create a chatbot that can answer questions about PDF documents",
            "expected_type": "document_qa"
        },
        {
            "description": "Build an AI agent that can search the web and do calculations",
            "expected_type": "agent_tools"
        },
        {
            "description": "Make a simple chat interface with GPT-4",
            "expected_type": "basic_chat"
        },
        {
            "description": "Create a document processing pipeline with embeddings",
            "expected_type": "rag_system"
        },
        {
            "description": "I want to build a chatbot using Claude",
            "expected_type": "basic_chat"
        }
    ]
    
    console.print(Panel.fit(
        "[bold blue]Testing AxieStudio Flow Generator[/bold blue]",
        title="Test Suite"
    ))
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        console.print(f"\n[bold]Test {i}:[/bold] {test_case['description']}")
        
        try:
            # Analyze user intent
            requirement = flow_generator.analyze_user_intent(test_case['description'])
            
            # Generate flow
            flow_json = flow_generator.generate_flow_json(requirement)
            
            # Validate flow
            nodes = flow_json["data"]["nodes"]
            edges = flow_json["data"]["edges"]
            
            result = {
                "test_case": test_case['description'],
                "flow_type": requirement.flow_type.value,
                "components": len(nodes),
                "connections": len(edges),
                "success": True,
                "components_list": [node["data"]["type"] for node in nodes]
            }
            
            console.print(f"  ✅ Generated flow with {len(nodes)} components and {len(edges)} connections")
            console.print(f"  📋 Flow type: {requirement.flow_type.value}")
            console.print(f"  🔧 Components: {', '.join(result['components_list'])}")
            
            # Save test flow
            filename = f"test_flow_{i}_{requirement.flow_type.value}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(flow_json, f, indent=2, ensure_ascii=False)
            console.print(f"  💾 Saved to {filename}")
            
        except Exception as e:
            result = {
                "test_case": test_case['description'],
                "success": False,
                "error": str(e)
            }
            console.print(f"  ❌ Error: {str(e)}")
        
        results.append(result)
    
    # Display summary
    display_test_summary(results)
    
    return results

def display_test_summary(results):
    """Display test results summary."""
    console.print("\n")
    
    table = Table(title="Test Results Summary")
    table.add_column("Test", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Flow Type", style="magenta")
    table.add_column("Components", style="yellow")
    table.add_column("Connections", style="blue")
    
    successful_tests = 0
    
    for i, result in enumerate(results, 1):
        if result["success"]:
            successful_tests += 1
            status = "✅ Pass"
            flow_type = result["flow_type"]
            components = str(result["components"])
            connections = str(result["connections"])
        else:
            status = "❌ Fail"
            flow_type = "N/A"
            components = "N/A"
            connections = "N/A"
        
        table.add_row(
            f"Test {i}",
            status,
            flow_type,
            components,
            connections
        )
    
    console.print(table)
    
    # Overall summary
    total_tests = len(results)
    success_rate = (successful_tests / total_tests) * 100
    
    console.print(f"\n[bold]Overall Results:[/bold]")
    console.print(f"• Total Tests: {total_tests}")
    console.print(f"• Successful: {successful_tests}")
    console.print(f"• Failed: {total_tests - successful_tests}")
    console.print(f"• Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        console.print("[green]🎉 All tests passed![/green]")
    elif success_rate >= 80:
        console.print("[yellow]⚠️  Most tests passed, some issues to address[/yellow]")
    else:
        console.print("[red]❌ Multiple test failures, needs investigation[/red]")

def test_component_knowledge():
    """Test the component knowledge base."""
    console.print("\n[bold]Testing Component Knowledge Base[/bold]")
    
    # Test component retrieval
    test_components = ["ChatInput", "OpenAIModel", "Agent", "ChromaDB"]
    
    for comp_name in test_components:
        component = component_kb.get_component(comp_name)
        if component:
            console.print(f"  ✅ {comp_name}: {component.description}")
        else:
            console.print(f"  ❌ {comp_name}: Not found")
    
    # Test search functionality
    console.print("\n[bold]Testing Component Search[/bold]")
    search_queries = ["chat", "document", "agent", "embedding"]
    
    for query in search_queries:
        results = component_kb.search_components(query)
        console.print(f"  🔍 '{query}': Found {len(results)} components")
        for result in results[:2]:  # Show first 2 results
            console.print(f"    • {result.display_name}")

def main():
    """Main test function."""
    console.print("[bold blue]AxieStudio Flow Generator Test Suite[/bold blue]\n")
    
    # Test component knowledge base
    test_component_knowledge()
    
    # Test flow generation
    results = test_flow_generation()
    
    console.print("\n[bold green]Testing completed![/bold green]")
    console.print("Check the generated test_flow_*.json files to see the results.")

if __name__ == "__main__":
    main()
