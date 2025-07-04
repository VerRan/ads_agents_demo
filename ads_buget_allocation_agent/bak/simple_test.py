#!/usr/bin/env python3
"""
简单测试 - 验证回调处理器是否能捕获Python执行结果
"""

from strands import Agent
from strands_tools import python_repl
from custom_callback_handler import create_callback_handler
from buget_allocation_agent import get_llm

def simple_test():
    """简单测试"""
    print("🧪 简单测试...")
    
    # 创建回调处理器
    callback_handler = create_callback_handler(
        handler_type="complete",
        log_file="simple_test.log"
    )
    
    # 创建Agent
    agent = Agent(
        model=get_llm(),
        system_prompt="你是一个Python专家，请执行用户的代码。",
        tools=[python_repl],
        callback_handler=callback_handler
    )
    
    # 简单的测试
    query = "请执行这个Python代码：print('Hello World'); result = 2 + 3; print(f'2 + 3 = {result}')"
    
    print("📝 执行查询:", query)
    print("-" * 30)
    
    result = agent(query)
    
    print("-" * 30)
    print("✅ 测试完成")
    print("📁 日志文件: simple_test.log")
    
    return result

if __name__ == "__main__":
    simple_test()