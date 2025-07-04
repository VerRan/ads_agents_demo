#!/usr/bin/env python3
"""
Launch the UI with Natural Language Processing capabilities
"""

import subprocess
import sys
import os

def main():
    print("🚀 启动带自然语言处理的广告创意Agent UI")
    print("🎯 新功能:")
    print("  • 💬 自然语言任务输入")
    print("  • 🔍 智能任务解析")
    print("  • 🤖 自动任务执行")
    print("  • 💡 任务示例库")
    print("  • 📋 实时处理日志")
    print("-" * 50)
    
    print("📝 支持的任务类型:")
    print("  • 虚拟试穿 - 用自然语言描述试穿需求")
    print("  • 图片下载 - 从URL批量下载图片")
    print("  • 图片处理 - 自动调整图片尺寸和格式")
    print("  • 混合任务 - 组合多个操作")
    print()
    
    print("🌟 示例任务:")
    print('  "用lht.jpg试穿这个衣服：https://example.com/shirt.jpg"')
    print('  "下载并处理这些图片：url1, url2"')
    print('  "用我的照片试穿这个连衣裙：url"')
    print("-" * 50)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ui_path = os.path.join(script_dir, "ui.py")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", ui_path,
            "--server.address", "localhost",
            "--server.port", "8503",  # Different port
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 UI服务器已停止")
    except Exception as e:
        print(f"❌ 启动UI时出错: {e}")

if __name__ == "__main__":
    main()