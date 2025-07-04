#!/usr/bin/env python3
"""
预算分配Agent演示系统启动器
提供多种演示模式选择
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def check_dependencies():
    """检查依赖包"""
    required_packages = ['streamlit', 'plotly', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(packages):
    """安装缺失的依赖包"""
    print(f"📦 正在安装依赖包: {', '.join(packages)}")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install"
        ] + packages)
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

def run_streamlit_app(app_file, port=8501):
    """运行Streamlit应用"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, app_file)
    
    if not os.path.exists(app_path):
        print(f"❌ 找不到应用文件: {app_path}")
        return False
    
    print(f"🚀 启动应用: {app_file}")
    print(f"📱 访问地址: http://localhost:{port}")
    print("💡 使用 Ctrl+C 停止应用")
    print("=" * 50)
    
    # 启动浏览器
    browser_thread = Thread(
        target=open_browser,
        args=(f"http://localhost:{port}", 3)
    )
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            app_path,
            "--server.port", str(port),
            "--server.headless", "true"
        ], cwd=script_dir)
        return True
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断，正在停止应用...")
        return True
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        return False

def show_menu():
    """显示菜单选项"""
    print("🤖 AI预算分配优化系统演示")
    print("=" * 50)
    print("请选择演示模式:")
    print()
    print("1. 📊 基础演示版 (模拟AI分析过程)")
    print("   - 快速启动，无需AI模型")
    print("   - 模拟完整的分析流程")
    print("   - 适合快速演示和测试")
    print()
    print("2. 🤖 真实AI版 (集成真实AI代理)")
    print("   - 调用真实的AI模型分析")
    print("   - 需要AWS Bedrock访问权限")
    print("   - 提供真实的AI分析结果")
    print()
    print("3. 🔧 命令行版 (直接运行AI代理)")
    print("   - 在终端中直接运行")
    print("   - 查看完整的AI执行过程")
    print("   - 适合开发和调试")
    print()
    print("4. ❌ 退出")
    print("=" * 50)

def run_command_line_version():
    """运行命令行版本"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agent_path = os.path.join(script_dir, "buget_allocation_agent.py")
    
    if not os.path.exists(agent_path):
        print(f"❌ 找不到代理文件: {agent_path}")
        return
    
    print("🤖 启动命令行版AI代理...")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, agent_path], cwd=script_dir)
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断")
    except Exception as e:
        print(f"❌ 执行失败: {str(e)}")

def main():
    """主函数"""
    # 检查依赖
    missing_deps = check_dependencies()
    if missing_deps:
        print("⚠️ 检测到缺失的依赖包")
        if input(f"是否安装 {', '.join(missing_deps)}? (y/n): ").lower() == 'y':
            if not install_dependencies(missing_deps):
                print("❌ 无法安装依赖，请手动安装后重试")
                return
        else:
            print("❌ 缺少必要依赖，程序退出")
            return
    
    while True:
        show_menu()
        
        try:
            choice = input("请输入选项 (1-4): ").strip()
            
            if choice == '1':
                print("\n🚀 启动基础演示版...")
                run_streamlit_app("demo_ui.py", 8501)
                
            elif choice == '2':
                print("\n🚀 启动真实AI版...")
                print("⚠️ 注意: 需要配置AWS Bedrock访问权限")
                if input("确认继续? (y/n): ").lower() == 'y':
                    run_streamlit_app("demo_ui_with_agent.py", 8502)
                
            elif choice == '3':
                print("\n🚀 启动命令行版...")
                run_command_line_version()
                
            elif choice == '4':
                print("👋 再见!")
                break
                
            else:
                print("❌ 无效选项，请重新选择")
                continue
            
            # 询问是否继续
            print("\n" + "=" * 50)
            if input("是否继续使用其他模式? (y/n): ").lower() != 'y':
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，程序退出")
            break
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")
            continue
    
    print("🎉 演示系统已退出")

if __name__ == "__main__":
    main()