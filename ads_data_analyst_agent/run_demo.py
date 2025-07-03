#!/usr/bin/env python3
"""
AI数据分析师演示启动脚本
"""

import subprocess
import sys
import os

def check_requirements():
    """检查必要的依赖"""
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def main():
    print("🚀 启动AI数据分析师演示...")
    
    # 检查依赖
    if not check_requirements():
        sys.exit(1)
    
    # 检查数据文件
    data_file = "google.campaign_daily_geo_stats.csv"
    if os.path.exists(data_file):
        print(f"✅ 找到示例数据文件: {data_file}")
    else:
        print(f"⚠️  未找到示例数据文件: {data_file}")
        print("您仍然可以上传自己的CSV文件进行分析")
    
    # 启动Streamlit应用
    try:
        print("🌐 启动Web应用...")
        print("📱 应用将在浏览器中自动打开")
        print("🔗 如果没有自动打开，请访问: http://localhost:8501")
        print("⏹️  按 Ctrl+C 停止应用")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "demo_app.py",
            "--server.headless", "true",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()