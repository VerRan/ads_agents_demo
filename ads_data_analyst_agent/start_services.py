#!/usr/bin/env python3
"""
启动AI数据分析师服务
支持同时启动Streamlit Web界面和REST API服务
"""

import subprocess
import sys
import time
import signal
import os
from multiprocessing import Process

def start_streamlit():
    """启动Streamlit服务"""
    print("🌐 启动Streamlit Web界面...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "demo_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ])

def start_api():
    """启动FastAPI服务"""
    print("🚀 启动REST API服务...")
    subprocess.run([
        sys.executable, "-m", "uvicorn", "api_server:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

def start_both_services():
    """同时启动两个服务"""
    print("🎯 启动AI数据分析师服务...")
    print("=" * 50)
    
    # 创建进程
    streamlit_process = Process(target=start_streamlit)
    api_process = Process(target=start_api)
    
    try:
        # 启动API服务
        api_process.start()
        time.sleep(2)  # 等待API服务启动
        
        # 启动Streamlit服务
        streamlit_process.start()
        time.sleep(2)  # 等待Streamlit服务启动
        
        print("✅ 服务启动成功！")
        print("📱 Streamlit Web界面: http://localhost:8501")
        print("🔗 REST API服务: http://localhost:8000")
        print("📚 API文档: http://localhost:8000/docs")
        print("🔧 API Redoc: http://localhost:8000/redoc")
        print("\n按 Ctrl+C 停止服务")
        
        # 等待进程
        streamlit_process.join()
        api_process.join()
        
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        
        # 终止进程
        if streamlit_process.is_alive():
            streamlit_process.terminate()
            streamlit_process.join()
        
        if api_process.is_alive():
            api_process.terminate()
            api_process.join()
        
        print("✅ 服务已停止")

def show_help():
    """显示帮助信息"""
    print("AI数据分析师服务启动器")
    print("=" * 30)
    print("使用方法:")
    print("  python start_services.py [选项]")
    print()
    print("选项:")
    print("  --streamlit    只启动Streamlit Web界面")
    print("  --api          只启动REST API服务")
    print("  --both         同时启动两个服务 (默认)")
    print("  --help         显示帮助信息")
    print()
    print("示例:")
    print("  python start_services.py                # 启动所有服务")
    print("  python start_services.py --streamlit    # 只启动Web界面")
    print("  python start_services.py --api          # 只启动API服务")

def main():
    """主函数"""
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        show_help()
        return
    
    if "--streamlit" in args:
        start_streamlit()
    elif "--api" in args:
        start_api()
    else:
        # 默认启动所有服务
        start_both_services()

if __name__ == "__main__":
    main()