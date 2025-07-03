#!/usr/bin/env python3
"""
Launcher script for the Google Ads Data Analyst Streamlit app
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        print("🚀 Starting Google Ads Data Analyst Web UI...")
        print(f"📁 Working directory: {script_dir}")
        print("🌐 The app will open in your default browser")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down the server...")
    except Exception as e:
        print(f"❌ Error starting the app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
