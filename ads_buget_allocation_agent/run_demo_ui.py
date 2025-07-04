#!/usr/bin/env python3
"""
预算分配Agent演示UI启动脚本
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def check_streamlit():
    """检查Streamlit是否安装"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_streamlit():
    """安装Streamlit和相关依赖"""
    print("📦 正在安装Streamlit和相关依赖...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "streamlit", "plotly", "pandas"
        ])
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {str(e)}")
        return False

def open_browser(url, delay=3):
    """延迟打开浏览器"""
    time.sleep(delay)
    try:
        webbrowser.open(url)
        print(f"🌐 已在浏览器中打开: {url}")
    except Exception as e:
        print(f"⚠️ 无法自动打开浏览器: {str(e)}")
        print(f"请手动访问: {url}")

def main():
    """主函数"""
    print("🚀 启动预算分配Agent演示UI")
    print("=" * 50)
    
    # 检查并安装依赖
    if not check_streamlit():
        print("⚠️ 检测到Streamlit未安装")
        if not install_streamlit():
            print("❌ 无法安装依赖，请手动安装:")
            print("pip install streamlit plotly pandas")
            return
    
    # 获取当前脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    demo_ui_path = os.path.join(script_dir, "demo_ui.py")
    
    if not os.path.exists(demo_ui_path):
        print(f"❌ 找不到演示文件: {demo_ui_path}")
        return
    
    print("✅ 准备启动Streamlit应用...")
    print("📱 应用将在 http://localhost:8501 运行")
    print("💡 使用 Ctrl+C 停止应用")
    print("=" * 50)
    
    # 启动浏览器（延迟3秒）
    browser_thread = Thread(
        target=open_browser,
        args=("http://localhost:8501", 3)
    )
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # 启动Streamlit应用
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            demo_ui_path,
            "--server.port", "8501",
            "--server.headless", "true"
        ], cwd=script_dir)
    
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断，正在停止应用...")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
    
    print("🎉 演示应用已停止")

if __name__ == "__main__":
    main()