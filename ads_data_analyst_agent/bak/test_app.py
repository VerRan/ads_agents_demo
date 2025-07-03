#!/usr/bin/env python3
"""
测试demo_app.py的功能
"""

import pandas as pd
import os
from datetime import datetime

def test_data_functions():
    """测试数据处理函数"""
    print("🧪 测试数据处理函数...")
    
    # 创建测试数据
    test_data = pd.DataFrame({
        'campaign_name': ['Campaign A', 'Campaign B', 'Campaign C'],
        'clicks': [100, 200, 150],
        'impressions': [1000, 2000, 1500],
        'cost': [50.0, 100.0, 75.0],
        'conversions': [5, 10, 8],
        'device': ['mobile', 'desktop', 'mobile']
    })
    
    print(f"✅ 测试数据创建成功: {len(test_data)} 行")
    
    # 测试基本统计
    print(f"📊 数据统计:")
    print(f"- 总行数: {len(test_data)}")
    print(f"- 总列数: {len(test_data.columns)}")
    print(f"- 缺失值: {test_data.isnull().sum().sum()}")
    print(f"- 数值列: {len(test_data.select_dtypes(include=['number']).columns)}")
    
    return test_data

def test_file_operations():
    """测试文件操作"""
    print("\n📁 测试文件操作...")
    
    # 检查示例数据文件
    data_file = "google.campaign_daily_geo_stats.csv"
    if os.path.exists(data_file):
        print(f"✅ 找到示例数据文件: {data_file}")
        
        # 读取文件信息
        try:
            df = pd.read_csv(data_file)
            print(f"📊 文件信息:")
            print(f"- 行数: {len(df):,}")
            print(f"- 列数: {len(df.columns)}")
            print(f"- 列名: {', '.join(df.columns[:5].tolist())}...")
            return True
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return False
    else:
        print(f"⚠️  未找到示例数据文件: {data_file}")
        return False

def test_agent_import():
    """测试AI代理导入"""
    print("\n🤖 测试AI代理导入...")
    
    try:
        from google_ads_anlyst_agent import agent, get_llm
        print("✅ AI代理导入成功")
        
        # 测试LLM
        try:
            llm = get_llm()
            print("✅ LLM创建成功")
            return True
        except Exception as e:
            print(f"❌ LLM创建失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ AI代理导入失败: {e}")
        return False

def test_streamlit_components():
    """测试Streamlit组件"""
    print("\n🎨 测试Streamlit组件...")
    
    try:
        import streamlit as st
        print("✅ Streamlit导入成功")
        
        # 测试其他依赖
        import plotly.express as px
        print("✅ Plotly导入成功")
        
        import json
        print("✅ JSON模块可用")
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit组件测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试demo_app.py功能...")
    print("=" * 50)
    
    # 测试结果
    results = {
        'data_functions': test_data_functions(),
        'file_operations': test_file_operations(),
        'agent_import': test_agent_import(),
        'streamlit_components': test_streamlit_components()
    }
    
    print("\n" + "=" * 50)
    print("📋 测试结果汇总:")
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"- {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！应用应该可以正常运行。")
        print("💡 建议:")
        print("- 运行: streamlit run demo_app.py")
        print("- 或者: python run_demo.py")
    else:
        print("⚠️  部分测试失败，请检查相关配置。")
        print("💡 建议:")
        print("- 检查依赖包是否正确安装")
        print("- 确认数据文件是否存在")
        print("- 检查AI代理配置")

if __name__ == "__main__":
    main()