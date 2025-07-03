#!/usr/bin/env python3
"""
测试原始agent是否正常工作
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(__file__))

def test_original_agent():
    """测试原始agent"""
    print("🧪 测试原始Agent...")
    
    try:
        from google_ads_anlyst_agent import agent, filename
        
        print(f"📁 使用数据文件: {filename}")
        
        # 执行简单查询
        query = f"当前目录{filename}的文件，请告诉我这个文件有多少行数据？"
        print(f"🔍 查询: {query}")
        
        print("⏳ 执行中...")
        result = agent(query)
        
        print(f"📊 结果: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 开始测试原始Agent...")
    print("=" * 50)
    
    success = test_original_agent()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 原始Agent测试成功！")
    else:
        print("❌ 原始Agent测试失败！")

if __name__ == "__main__":
    main()