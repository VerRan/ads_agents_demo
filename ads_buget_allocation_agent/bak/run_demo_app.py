#!/usr/bin/env python3
"""
启动预算分配Agent演示应用
"""

import subprocess
import sys
import os

def main():
    """启动Streamlit演示应用"""
    print("🚀 启动AI预算分配优化系统演示...")
    
    # 确保在正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    demo_app_path = os.path.join(script_dir, "demo_app.py")
    
    if not os.path.exists(demo_app_path):
        print("❌ 找不到demo_app.py文件")
        return
    
    try:
        # 启动Streamlit应用
        cmd = [sys.executable, "-m", "streamlit", "run", demo_app_path, "--server.port=8501"]
        print(f"📱 启动命令: {' '.join(cmd)}")
        print("🌐 应用将在 http://localhost:8501 启动")
        print("💡 按 Ctrl+C 停止应用")
        
        subprocess.run(cmd, cwd=script_dir)
        
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")

if __name__ == "__main__":
    main()