#!/usr/bin/env python3
"""
AxieStudio AI Flow Generator - Main Entry Point

Production-grade AI-powered flow generation system for AxieStudio.
Organized, clean, and ready for enterprise deployment.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main entry point with interface selection."""
    
    print("🚀 AxieStudio AI Flow Generator")
    print("=" * 50)
    print("1. 🖥️  Web Interface (Production UI)")
    print("2. 💬 Interactive Chat")
    print("3. ⚡ Command Line Interface")
    print("4. 🧪 Run Tests")
    print("5. 📊 System Status")
    print("=" * 50)
    
    choice = input("Select interface (1-5): ").strip()
    
    if choice == "1":
        print("🖥️ Starting Web Interface...")
        from interfaces.dev_server import main as web_main
        web_main()
        
    elif choice == "2":
        print("💬 Starting Interactive Chat...")
        from interfaces.enhanced_main import main as cli_main
        sys.argv = ["enhanced_main.py", "ai-chat"]
        cli_main()
        
    elif choice == "3":
        print("⚡ Starting CLI...")
        from interfaces.enhanced_main import main as cli_main
        cli_main()
        
    elif choice == "4":
        print("🧪 Running Tests...")
        os.system(f'"{sys.executable}" tests/test_generator.py')
        
    elif choice == "5":
        print("📊 System Status...")
        from ai.super_ai_generator import super_ai_generator
        stats = super_ai_generator.get_generation_stats()
        
        print("\n✅ System Status:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    else:
        print("❌ Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()
