#!/usr/bin/env python3
"""
测试演示应用的基本功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试导入"""
    try:
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ 所有依赖包导入成功")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_demo_data():
    """测试演示数据"""
    try:
        from demo_app import DEMO_DATA
        campaigns = DEMO_DATA['campaigns']
        
        print(f"✅ 演示数据加载成功，包含 {len(campaigns)} 个Campaign")
        
        # 验证数据结构
        required_fields = ['id', 'budget', 'roas', 'purchases', 'value']
        for campaign in campaigns:
            for field in required_fields:
                if field not in campaign:
                    print(f"❌ Campaign {campaign.get('id', 'unknown')} 缺少字段: {field}")
                    return False
        
        print("✅ 数据结构验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 演示数据测试失败: {e}")
        return False

def test_functions():
    """测试主要函数"""
    try:
        from demo_app import generate_demo_result
        
        # 测试结果生成函数
        result = generate_demo_result(500, 20)
        
        if result['success'] and 'campaigns' in result:
            print(f"✅ 结果生成函数正常，生成了 {len(result['campaigns'])} 个优化建议")
            return True
        else:
            print("❌ 结果生成函数返回异常")
            return False
            
    except Exception as e:
        print(f"❌ 函数测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始测试演示应用...")
    
    tests = [
        ("导入测试", test_imports),
        ("数据测试", test_demo_data),
        ("函数测试", test_functions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} 失败")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！演示应用可以正常运行")
        print("\n🚀 启动命令:")
        print("python run_demo_app.py")
        print("或")
        print("streamlit run demo_app.py --server.port=8501")
    else:
        print("⚠️ 部分测试失败，请检查相关问题")

if __name__ == "__main__":
    main()