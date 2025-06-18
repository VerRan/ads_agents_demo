#!/usr/bin/env python3
"""
Startup script for the Combined AI Advertising Analysis Suite
"""

import os
import sys
import subprocess

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['API_KEY', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these environment variables before running the application.")
        print("Example:")
        print("export API_KEY='your-exa-api-key'")
        print("export AWS_ACCESS_KEY_ID='your-aws-access-key'")
        print("export AWS_SECRET_ACCESS_KEY='your-aws-secret-key'")
        return False
    
    print("✅ Environment variables are properly configured")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "combined_requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting AI Advertising Analysis Suite...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "combined_ads_ui.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    print("🎯 AI Advertising Analysis Suite Launcher")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        return
    
    # Ask user if they want to install dependencies
    install_deps = input("\n📦 Install/update dependencies? (y/n): ").lower().strip()
    if install_deps in ['y', 'yes']:
        if not install_dependencies():
            return
    
    # Run the application
    print("\n" + "=" * 50)
    run_streamlit()

if __name__ == "__main__":
    main()
