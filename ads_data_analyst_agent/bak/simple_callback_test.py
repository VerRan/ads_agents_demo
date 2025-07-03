#!/usr/bin/env python3
"""
简单的回调测试
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(__file__))

def test_agent_callback():
    """测试agent回调"""
    print("🧪 测试Agent回调功能...")
    
    try:
        from google_ads_anlyst_agent import get_llm
        from strands import Agent
        from strands_tools import file_read, python_repl
        from strands.handlers.callback_handler import CallbackHandler
        
        # 创建测试回调处理器
        class TestCallbackHandler(CallbackHandler):
            def __init__(self):
                super().__init__()
                self.events = []
            
            def on_llm_new_token(self, token: str, **kwargs) -> None:
                print(f"📝 Token: {token[:20]}...")
                self.events.append(("token", token))
            
            def on_tool_start(self, serialized, inputs, **kwargs) -> None:
                print(f"🔧 Tool start: {serialized}")
                self.events.append(("tool_start", serialized, inputs))
            
            def on_tool_end(self, output, **kwargs) -> None:
                print(f"✅ Tool end: {str(output)[:50]}...")
                self.events.append(("tool_end", output))
            
            def on_text(self, text: str, **kwargs) -> None:
                print(f"💬 Text: {text[:30]}...")
                self.events.append(("text", text))
        
        # 创建测试代理
        callback_handler = TestCallbackHandler()
        
        test_agent = Agent(
            model=get_llm(),
            system_prompt="你是一个数据分析专家，请分析给定的数据。",
            tools=[file_read, python_repl],
            callback_handler=callback_handler
        )
        
        print("\n🚀 开始测试查询...")
        
        # 执行简单查询
        result = test_agent("请执行这个Python代码：print('Hello, World!')")
        
        print(f"\n📊 查询结果: {result}")
        print(f"📋 捕获的事件数量: {len(callback_handler.events)}")
        
        # 显示捕获的事件
        for i, event in enumerate(callback_handler.events):
            print(f"事件 {i+1}: {event[0]} - {str(event[1:])[:100]}...")
        
        return len(callback_handler.events) > 0
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 开始简单回调测试...")
    print("=" * 50)
    
    success = test_agent_callback()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 回调测试成功！Agent可以正确触发回调事件。")
    else:
        print("❌ 回调测试失败！需要检查Agent配置。")

if __name__ == "__main__":
    main()