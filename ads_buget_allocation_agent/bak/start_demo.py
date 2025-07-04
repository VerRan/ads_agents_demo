#!/usr/bin/env python3
"""
预算分配Agent演示系统启动脚本
同时启动API服务器和Streamlit Web应用
"""

import subprocess
import time
import sys
import os
import signal
import requests
import webbrowser
from threading import Thread
import argparse

class ServiceManager:
    """服务管理器"""
    
    def __init__(self):
        self.api_process = None
        self.streamlit_process = None
        self.api_url = "http://localhost:8000"
        self.streamlit_url = "http://localhost:8501"
    
    def start_api_server(self):
        """启动API服务器"""
        try:
            print("🚀 启动API服务器...")
            self.api_process = subprocess.Popen(
                [sys.executable, "start_api.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # 等待API服务器启动
            if self.wait_for_service(self.api_url + "/health", "API服务器", 30):
                print("   ✅ API服务器启动成功")
                return True
            else:
                print("   ❌ API服务器启动失败")
                self.stop_api_server()
                return False
                
        except Exception as e:
            print(f"   ❌ 启动API服务器时发生错误: {str(e)}")
            return False
    
    def start_streamlit_app(self):
        """启动Streamlit应用"""
        try:
            print("🎨 启动Streamlit Web应用...")
            
            # 检查streamlit是否安装
            try:
                import streamlit
            except ImportError:
                print("   ❌ Streamlit未安装，正在安装...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "plotly"])
                print("   ✅ Streamlit安装完成")
            
            self.streamlit_process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "demo_app.py", "--server.port", "8501"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # 等待Streamlit应用启动
            if self.wait_for_service(self.streamlit_url, "Streamlit应用", 30):
                print("   ✅ Streamlit应用启动成功")
                return True
            else:
                print("   ❌ Streamlit应用启动失败")
                self.stop_streamlit_app()
                return False
                
        except Exception as e:
            print(f"   ❌ 启动Streamlit应用时发生错误: {str(e)}")
            return False
    
    def wait_for_service(self, url, service_name, timeout=30):
        """等待服务启动"""
        print(f"   等待{service_name}启动...")
        
        for i in range(timeout):
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(1)
            if i % 5 == 0 and i > 0:
                print(f"   等待中... ({i}/{timeout}秒)")
        
        return False
    
    def stop_api_server(self):
        """停止API服务器"""
        if self.api_process:
            print("⏹️ 停止API服务器...")
            try:
                self.api_process.terminate()
                self.api_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.api_process.kill()
                self.api_process.wait()
            self.api_process = None
    
    def stop_streamlit_app(self):
        """停止Streamlit应用"""
        if self.streamlit_process:
            print("⏹️ 停止Streamlit应用...")
            try:
                self.streamlit_process.terminate()
                self.streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.streamlit_process.kill()
                self.streamlit_process.wait()
            self.streamlit_process = None
    
    def stop_all_services(self):
        """停止所有服务"""
        self.stop_streamlit_app()
        self.stop_api_server()
    
    def is_api_running(self):
        """检查API服务器是否运行"""
        try:
            response = requests.get(self.api_url + "/health", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def is_streamlit_running(self):
        """检查Streamlit应用是否运行"""
        try:
            response = requests.get(self.streamlit_url, timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

def check_dependencies():
    """检查依赖"""
    required_packages = [
        'streamlit',
        'plotly',
        'fastapi',
        'uvicorn',
        'pandas',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("正在安装缺少的依赖...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages)
            print("✅ 依赖安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败")
            return False
    
    print("✅ 所有依赖已安装")
    return True

def show_welcome_message():
    """显示欢迎信息"""
    print("🎯 AI预算分配优化系统演示")
    print("=" * 50)
    print("这个演示系统包含:")
    print("  🔧 REST API服务器 (http://localhost:8000)")
    print("  🎨 Streamlit Web界面 (http://localhost:8501)")
    print("  📊 实时数据分析和可视化")
    print("  💰 智能预算优化建议")
    print("=" * 50)

def show_success_message():
    """显示成功启动信息"""
    print("\n🎉 演示系统启动成功！")
    print("=" * 40)
    print("📱 Web界面: http://localhost:8501")
    print("🔧 API文档: http://localhost:8000/docs")
    print("💡 使用说明:")
    print("  1. 在Web界面上传CSV数据文件")
    print("  2. 设置日预算和目标ROAS")
    print("  3. 点击'预算优化'获得AI建议")
    print("  4. 查看可视化图表和详细分析")
    print("=" * 40)
    print("按 Ctrl+C 停止所有服务")

def open_browser(url, delay=3):
    """延迟打开浏览器"""
    time.sleep(delay)
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"无法自动打开浏览器: {str(e)}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="预算分配Agent演示系统启动脚本"
    )
    
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="不自动打开浏览器"
    )
    
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="检查依赖包"
    )
    
    parser.add_argument(
        "--api-only",
        action="store_true",
        help="只启动API服务器"
    )
    
    parser.add_argument(
        "--streamlit-only",
        action="store_true",
        help="只启动Streamlit应用"
    )
    
    args = parser.parse_args()
    
    # 检查依赖
    if args.check_deps:
        check_dependencies()
        return
    
    # 显示欢迎信息
    show_welcome_message()
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 创建服务管理器
    service_manager = ServiceManager()
    
    try:
        # 检查现有服务
        api_running = service_manager.is_api_running()
        streamlit_running = service_manager.is_streamlit_running()
        
        if api_running:
            print("ℹ️ 检测到API服务器已在运行")
        if streamlit_running:
            print("ℹ️ 检测到Streamlit应用已在运行")
        
        # 启动服务
        services_started = []
        
        if not args.streamlit_only:
            if not api_running:
                if service_manager.start_api_server():
                    services_started.append("API")
                else:
                    print("❌ 无法启动API服务器，演示终止")
                    return
            else:
                print("✅ 使用现有API服务器")
        
        if not args.api_only:
            if not streamlit_running:
                if service_manager.start_streamlit_app():
                    services_started.append("Streamlit")
                else:
                    print("❌ 无法启动Streamlit应用")
                    service_manager.stop_all_services()
                    return
            else:
                print("✅ 使用现有Streamlit应用")
        
        # 显示成功信息
        if services_started:
            show_success_message()
            
            # 自动打开浏览器
            if not args.no_browser and not args.api_only:
                browser_thread = Thread(
                    target=open_browser,
                    args=("http://localhost:8501", 3)
                )
                browser_thread.daemon = True
                browser_thread.start()
        
        # 等待用户中断
        if services_started:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n⏹️ 用户中断，正在停止服务...")
        
    except Exception as e:
        print(f"❌ 启动过程中发生错误: {str(e)}")
    
    finally:
        # 清理资源
        if services_started:
            service_manager.stop_all_services()
            print("🎉 所有服务已停止")

if __name__ == "__main__":
    main()