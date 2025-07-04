#!/usr/bin/env python3
"""
测试Streamlit回调处理器功能
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_callback_handler():
    """测试回调处理器"""
    print("🧪 测试Streamlit回调处理器...")
    
    try:
        # 测试导入
        from custom_callback_handler import create_callback_handler
        print("✅ custom_callback_handler 导入成功")
        
        # 创建回调处理器
        handler = create_callback_handler(handler_type="complete")
        print("✅ 回调处理器创建成功")
        
        # 测试回调处理器
        handler(
            current_tool_use={'name': 'python_repl', 'input': {'code': 'print("Hello World")'}},
            tool_result="Hello World"
        )
        print("✅ 回调处理器测试成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 回调处理器测试失败: {e}")
        return False

def test_agent_components():
    """测试AI代理组件"""
    print("\n🤖 测试AI代理组件...")
    
    try:
        from buget_allocation_agent import get_llm, PROMPT
        print("✅ AI代理组件导入成功")
        
        # 测试LLM初始化
        llm = get_llm()
        print("✅ LLM初始化成功")
        
        # 测试Agent创建
        from strands import Agent
        from strands_tools import file_read, python_repl
        
        agent = Agent(
            model=llm,
            system_prompt=PROMPT,
            tools=[file_read, python_repl],
            callback_handler=None
        )
        print("✅ Agent创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ AI代理组件测试失败: {e}")
        print("💡 这可能需要AWS配置")
        return False

def test_streamlit_imports():
    """测试Streamlit相关导入"""
    print("\n📱 测试Streamlit导入...")
    
    try:
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        print("✅ Streamlit相关包导入成功")
        return True
        
    except ImportError as e:
        print(f"❌ Streamlit导入失败: {e}")
        print("💡 请安装: pip install streamlit plotly pandas")
        return False

def main():
    """主测试函数"""
    print("🔍 AI预算分配演示UI - 回调处理器测试")
    print("=" * 50)
    
    tests = [
        ("Streamlit导入", test_streamlit_imports),
        ("回调处理器", test_callback_handler),
        ("AI代理组件", test_agent_components)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体状态: {passed}/{len(results)} 项测试通过")
    
    if passed >= 2:  # 至少Streamlit和回调处理器要通过
        print("🎉 演示UI基本功能可用!")
        print("\n💡 启动建议:")
        print("   streamlit run demo_ui_with_agent.py --server.port 8502")
    else:
        print("⚠️ 部分关键功能不可用")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()