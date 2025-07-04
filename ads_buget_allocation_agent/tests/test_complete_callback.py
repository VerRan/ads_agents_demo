#!/usr/bin/env python3
"""
测试完整回调处理器 - 验证是否能捕获所有输出包括Python执行结果
"""

from strands import Agent
from strands_tools import python_repl
from custom_callback_handler import create_callback_handler
from buget_allocation_agent import get_llm
import os

def test_complete_callback():
    """测试完整的回调处理器"""
    print("🧪 测试完整回调处理器...")
    print("=" * 50)
    
    # 创建完整回调处理器
    callback_handler = create_callback_handler(
        handler_type="complete",
        log_file="test_complete_output.log"
    )
    
    # 创建Agent
    agent = Agent(
        model=get_llm(),
        system_prompt="你是一个Python代码执行专家，请执行用户提供的代码并显示结果。",
        tools=[python_repl],
        callback_handler=callback_handler
    )
    
    # 测试Python代码执行
    test_code = """
请执行以下Python代码：

import pandas as pd
import numpy as np

# 创建测试数据
data = {
    'campaign_id': ['A', 'B', 'C'],
    'spend': [100, 200, 150],
    'revenue': [500, 800, 600]
}

df = pd.DataFrame(data)
print("数据框:")
print(df)

# 计算ROAS
df['roas'] = df['revenue'] / df['spend']
print("\\n计算ROAS后:")
print(df)

# 统计信息
print(f"\\n总花费: {df['spend'].sum()}")
print(f"总收入: {df['revenue'].sum()}")
print(f"平均ROAS: {df['roas'].mean():.2f}")
"""
    
    print("📝 执行测试查询...")
    print("-" * 30)
    
    result = agent(test_code)
    
    print("-" * 30)
    print("✅ 测试完成")
    
    # 检查日志文件
    log_file = "test_complete_output.log"
    if os.path.exists(log_file):
        print(f"\n📋 检查日志文件: {log_file}")
        
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 日志文件大小: {len(content)} 字符")
        print(f"📄 日志文件行数: {len(content.splitlines())} 行")
        
        # 检查关键内容
        checks = [
            ("Python代码", "import pandas as pd"),
            ("数据框输出", "campaign_id"),
            ("ROAS计算", "roas"),
            ("统计信息", "总花费"),
            ("平均ROAS", "平均ROAS")
        ]
        
        print(f"\n🔍 内容检查:")
        for check_name, check_text in checks:
            if check_text in content:
                print(f"✅ {check_name}: 已包含")
            else:
                print(f"❌ {check_name}: 缺失")
        
        # 显示日志文件的最后20行
        print(f"\n📄 日志文件最后20行:")
        print("-" * 40)
        lines = content.splitlines()
        for line in lines[-20:]:
            print(line)
        print("-" * 40)
        
    else:
        print("❌ 日志文件不存在")
    
    return result

if __name__ == "__main__":
    test_complete_callback()