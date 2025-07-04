#!/usr/bin/env python3
"""
测试回调处理器对比 - 验证是否能完全捕获PrintingCallbackHandler的输出
"""

from strands import Agent
from strands_tools import file_read, python_repl
from strands.handlers.callback_handler import PrintingCallbackHandler
from custom_callback_handler import create_callback_handler
from buget_allocation_agent import get_llm
import os
import time

def test_original_printing_handler():
    """测试原始的PrintingCallbackHandler"""
    print("🔍 测试原始PrintingCallbackHandler...")
    print("=" * 50)
    
    agent = Agent(
        model=get_llm(),
        system_prompt="你是一个数据分析专家，请分析给定的数据。",
        tools=[file_read, python_repl],
        callback_handler=PrintingCallbackHandler()
    )
    
    # 简单的测试查询
    query = "请执行这个Python代码：print('Hello from Python!'); import pandas as pd; print(f'Pandas version: {pd.__version__}')"
    
    print("📝 执行查询:", query)
    print("-" * 30)
    
    result = agent(query)
    
    print("-" * 30)
    print("✅ 原始PrintingCallbackHandler测试完成")
    return result

def test_custom_callback_handler(handler_type="perfect"):
    """测试自定义回调处理器"""
    print(f"\n🔍 测试自定义回调处理器 ({handler_type})...")
    print("=" * 50)
    
    # 创建自定义日志文件
    log_file = f"test_{handler_type}_callback.log"
    
    callback_handler = create_callback_handler(
        handler_type=handler_type,
        log_file=log_file
    )
    
    agent = Agent(
        model=get_llm(),
        system_prompt="你是一个数据分析专家，请分析给定的数据。",
        tools=[file_read, python_repl],
        callback_handler=callback_handler
    )
    
    # 相同的测试查询
    query = "请执行这个Python代码：print('Hello from Python!'); import pandas as pd; print(f'Pandas version: {pd.__version__}')"
    
    print("📝 执行查询:", query)
    print("-" * 30)
    
    result = agent(query)
    
    print("-" * 30)
    print(f"✅ 自定义回调处理器 ({handler_type}) 测试完成")
    print(f"📁 日志文件: {log_file}")
    
    return result, log_file

def compare_outputs():
    """对比输出结果"""
    print("\n🔍 对比测试开始...")
    print("=" * 60)
    
    # 测试原始处理器
    print("第一轮：原始PrintingCallbackHandler")
    original_result = test_original_printing_handler()
    
    # 等待一下
    time.sleep(2)
    
    # 测试自定义处理器
    print("\n第二轮：自定义PerfectDualCallbackHandler")
    custom_result, log_file = test_custom_callback_handler("perfect")
    
    # 检查日志文件内容
    print(f"\n📋 检查日志文件内容...")
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
        
        print(f"📄 日志文件大小: {len(log_content)} 字符")
        print(f"📄 日志文件行数: {len(log_content.splitlines())} 行")
        
        # 检查是否包含Python代码和结果
        if "print('Hello from Python!')" in log_content:
            print("✅ 日志包含Python代码")
        else:
            print("❌ 日志缺少Python代码")
        
        if "Hello from Python!" in log_content:
            print("✅ 日志包含Python执行结果")
        else:
            print("❌ 日志缺少Python执行结果")
        
        if "Pandas version:" in log_content:
            print("✅ 日志包含Pandas版本信息")
        else:
            print("❌ 日志缺少Pandas版本信息")
        
        # 显示日志文件的最后几行
        print(f"\n📄 日志文件最后10行:")
        print("-" * 40)
        lines = log_content.splitlines()
        for line in lines[-10:]:
            print(line)
        print("-" * 40)
        
    else:
        print("❌ 日志文件不存在")
    
    print(f"\n🎉 对比测试完成！")

def test_all_handler_types():
    """测试所有处理器类型"""
    print("\n🧪 测试所有处理器类型...")
    print("=" * 60)
    
    handler_types = ["simple", "dual", "enhanced", "perfect", "structured"]
    
    for handler_type in handler_types:
        print(f"\n📋 测试处理器类型: {handler_type}")
        try:
            result, log_file = test_custom_callback_handler(handler_type)
            print(f"✅ {handler_type} 处理器测试成功")
            
            # 简单检查日志文件
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"📄 日志大小: {len(content)} 字符")
            
        except Exception as e:
            print(f"❌ {handler_type} 处理器测试失败: {str(e)}")
        
        print("-" * 30)

def main():
    """主函数"""
    print("🧪 回调处理器对比测试")
    print("=" * 60)
    
    print("选择测试模式:")
    print("1. 对比原始和自定义处理器")
    print("2. 测试所有处理器类型")
    print("3. 只测试perfect处理器")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        compare_outputs()
    elif choice == "2":
        test_all_handler_types()
    elif choice == "3":
        print("\n🔍 测试perfect处理器...")
        result, log_file = test_custom_callback_handler("perfect")
        print(f"✅ 测试完成，日志文件: {log_file}")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()