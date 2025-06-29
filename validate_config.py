"""
Configuration validator for Slack AI Chatbot

This script validates the environment configuration and dependencies
before running the application.
"""

import os
import sys
from typing import List, Tuple

def check_environment_variables() -> List[str]:
    """Check required environment variables"""
    missing = []
    required_vars = [
        ("SLACK_BOT_TOKEN", "Bot user OAuth token"),
        ("SLACK_SIGNING_SECRET", "Slack app signing secret"),
        ("GCP_PROJECT_ID", "Google Cloud project ID"),
    ]
    
    for var, description in required_vars:
        if not os.getenv(var):
            missing.append(f"❌ {var}: {description}")
    
    return missing

def check_optional_variables() -> List[str]:
    """Check optional environment variables and show warnings"""
    warnings = []
    optional_vars = [
        ("SLACK_APP_TOKEN", "App-level token for Socket Mode development"),
        ("GOOGLE_APPLICATION_CREDENTIALS", "Path to service account key"),
        ("VERTEX_AI_LOCATION", "VertexAI region (defaults to us-central1)"),
        ("VERTEX_AI_MODEL", "Gemini model name (defaults to gemini-1.5-flash)"),
    ]
    
    for var, description in optional_vars:
        if not os.getenv(var):
            warnings.append(f"⚠️  {var}: {description} (optional)")
    
    return warnings

def check_dependencies() -> List[str]:
    """Check if required Python packages are available"""
    missing = []
    required_packages = [
        ("slack_bolt", "Slack Bolt for Python"),
        ("google.cloud.aiplatform", "Google Cloud AI Platform"),
        ("dotenv", "Python dotenv"),
    ]
    
    for package, description in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(f"❌ {package}: {description}")
    
    return missing

def check_files() -> List[str]:
    """Check if required files exist"""
    missing = []
    required_files = [
        ("main.py", "Main application file"),
        ("app/gemini_client.py", "Gemini client module"),
        ("listeners/assistant.py", "Assistant listeners module"),
        ("manifest.json", "Slack app manifest"),
    ]
    
    for file_path, description in required_files:
        if not os.path.exists(file_path):
            missing.append(f"❌ {file_path}: {description}")
    
    return missing

def main():
    """Main validation function"""
    print("🔍 Validating Slack AI Chatbot configuration...\n")
    
    # Check files
    missing_files = check_files()
    if missing_files:
        print("📁 Missing Files:")
        for item in missing_files:
            print(f"  {item}")
        print()
    
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        print("📦 Missing Dependencies:")
        for item in missing_deps:
            print(f"  {item}")
        print("  Run: pip install -r requirements.txt")
        print()
    
    # Check environment variables
    missing_env = check_environment_variables()
    if missing_env:
        print("🔧 Missing Required Environment Variables:")
        for item in missing_env:
            print(f"  {item}")
        print("  Copy .env.example to .env and fill in the values")
        print()
    
    # Check optional variables
    optional_warnings = check_optional_variables()
    if optional_warnings:
        print("⚠️  Optional Configuration:")
        for item in optional_warnings:
            print(f"  {item}")
        print()
    
    # Summary
    total_issues = len(missing_files) + len(missing_deps) + len(missing_env)
    
    if total_issues == 0:
        print("✅ Configuration validation passed!")
        print("🚀 Ready to run: python main.py")
        sys.exit(0)
    else:
        print(f"❌ Found {total_issues} issue(s) that need to be resolved.")
        print("\n📋 Quick fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Copy environment template: cp .env.example .env")
        print("  3. Update .env with your actual values")
        print("  4. Set up Google Cloud credentials")
        sys.exit(1)

if __name__ == "__main__":
    main()