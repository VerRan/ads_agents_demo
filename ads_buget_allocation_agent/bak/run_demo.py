#!/usr/bin/env python3
"""
预算分配Agent API演示运行脚本
自动启动API服务器并运行演示
"""

import subprocess
import time
import sys
import os
import signal
import requests
from threading import Thread

class APIServerManager:
    """API服务器管理器"""
    
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.process = None
        self.url = f"http://{host}:{port}"
    
    def start_server(self):
        """启动API服务器"""
        try:
            print(f"🚀 启动API服务器: {self.url}")
            
            # 启动服务器进程
            self.process = subprocess.Popen(
                [sys.executable, "start_api.py", "--host", self.host, "--port", str(self.port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # 等待服务器启动
            print("   等待服务器启动...")
            if self.wait_for_server(timeout=30):
                print("   ✅ API服务器启动成功")
                return True
            else:
                print("   ❌ API服务器启动失败")
                self.stop_server()
                return False
                
        except Exception as e:
            print(f"   ❌ 启动服务器时发生错误: {str(e)}")
            return False
    
    def wait_for_server(self, timeout=30):
        """等待服务器启动"""
        for i in range(timeout):
            try:
                response = requests.get(f"{self.url}/health", timeout=2)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(1)
            if i % 5 == 0 and i > 0:
                print(f"   等待中... ({i}/{timeout}秒)")
        
        return False
    
    def stop_server(self):
        """停止API服务器"""
        if self.process:
            print("⏹️ 停止API服务器...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            
            self.process = None
            print("   ✅ API服务器已停止")
    
    def is_running(self):
        """检查服务器是否运行"""
        try:
            response = requests.get(f"{self.url}/health", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

def run_demo():
    """运行演示"""
    try:
        print("\n🎯 运行API演示...")
        print("-" * 30)
        
        # 导入并运行演示
        from demo_api import main as demo_main
        demo_main()
        
        return True
        
    except Exception as e:
        print(f"❌ 演示运行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_tests():
    """运行API测试"""
    try:
        print("\n🧪 运行API测试...")
        print("-" * 30)
        
        # 导入并运行测试
        from test_api import test_api
        test_api()
        
        return True
        
    except Exception as e:
        print(f"❌ 测试运行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🎯 预算分配Agent API演示系统")
    print("=" * 50)
    
    # 检查是否已有服务器运行
    server_manager = APIServerManager()
    
    if server_manager.is_running():
        print("ℹ️ 检测到API服务器已在运行")
        use_existing = input("是否使用现有服务器? (y/n): ").lower().strip()
        
        if use_existing != 'y':
            print("请先停止现有服务器，然后重新运行此脚本")
            return
        
        server_started_by_us = False
    else:
        # 启动服务器
        if not server_manager.start_server():
            print("❌ 无法启动API服务器，演示终止")
            return
        
        server_started_by_us = True
    
    try:
        # 显示选项菜单
        while True:
            print(f"\n📋 选择操作:")
            print("1. 运行完整演示")
            print("2. 运行API测试")
            print("3. 打开API文档 (浏览器)")
            print("4. 显示服务器信息")
            print("5. 退出")
            
            choice = input("\n请选择 (1-5): ").strip()
            
            if choice == "1":
                run_demo()
            elif choice == "2":
                run_tests()
            elif choice == "3":
                import webbrowser
                webbrowser.open(f"{server_manager.url}/docs")
                print(f"📖 已在浏览器中打开API文档: {server_manager.url}/docs")
            elif choice == "4":
                print(f"\n📊 服务器信息:")
                print(f"   URL: {server_manager.url}")
                print(f"   状态: {'运行中' if server_manager.is_running() else '已停止'}")
                print(f"   API文档: {server_manager.url}/docs")
                print(f"   健康检查: {server_manager.url}/health")
            elif choice == "5":
                break
            else:
                print("❌ 无效选择，请重新输入")
    
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断操作")
    
    finally:
        # 清理资源
        if server_started_by_us:
            server_manager.stop_server()
        
        print("\n🎉 演示系统已退出")

if __name__ == "__main__":
    main()