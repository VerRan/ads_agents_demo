#!/usr/bin/env python3
"""
Launch the updated UI with logging support
"""

import subprocess
import sys
import os

def main():
    print("🚀 Launching Ads Creative Agent UI with Enhanced Logging...")
    print("📋 New features:")
    print("  • Real-time processing logs")
    print("  • Progress indicators")
    print("  • Detailed status updates")
    print("  • Error tracking")
    print("-" * 50)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ui_path = os.path.join(script_dir, "ui.py")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", ui_path,
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 UI server stopped.")
    except Exception as e:
        print(f"❌ Error launching UI: {e}")

if __name__ == "__main__":
    main()