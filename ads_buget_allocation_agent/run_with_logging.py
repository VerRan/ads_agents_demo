#!/usr/bin/env python3
"""
带日志记录的预算分配Agent运行脚本
演示不同的日志记录方式
"""

from strands import Agent
from strands_tools import file_read, python_repl
from custom_callback_handler import create_callback_handler
from buget_allocation_agent import get_llm, PROMPT
from datetime import datetime
import os

def run_budget_analysis_with_logging(handler_type="dual", custom_log_file=None):
    """
    运行预算分析并记录日志
    
    Args:
        handler_type: 日志处理器类型
            - "simple": 简单文件记录
            - "dual": 同时输出到终端和文件 (推荐)
            - "structured": 结构化详细日志
        custom_log_file: 自定义日志文件名
    """
    
    print(f"🚀 启动预算分配分析 - 日志模式: {handler_type}")
    print("=" * 50)
    
    # 创建回调处理器
    if custom_log_file:
        callback_handler = create_callback_handler(
            handler_type=handler_type,
            log_file=custom_log_file
        )
    else:
        callback_handler = create_callback_handler(handler_type=handler_type)
    
    # 创建Agent
    agent = Agent(
        model=get_llm(),
        system_prompt=PROMPT,
        tools=[file_read, python_repl],
        callback_handler=callback_handler
    )
    
    # 分析参数
    filename = "2025-03-04_input.csv"
    daily_budget = 500
    ROAS = 20
    
    task = f"""你必须在用户的日预算{daily_budget}
    及目标KPI{ROAS}的基础上，对用户提供的广告数据{filename}进行深度分析，后给出预算调整建议。"""
    
    print(f"📊 分析参数:")
    print(f"   - 数据文件: {filename}")
    print(f"   - 日预算: ${daily_budget}")
    print(f"   - 目标ROAS: {ROAS}")
    print(f"   - 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🔄 开始分析...")
    print("-" * 50)
    
    try:
        # 执行分析
        result = agent(task)
        
        print("\n" + "=" * 50)
        print("✅ 分析完成！")
        print(f"📝 最终结果:")
        print("-" * 30)
        print(result)
        
        return result
        
    except Exception as e:
        print(f"\n❌ 分析失败: {str(e)}")
        return None

def demo_different_logging_modes():
    """演示不同的日志记录模式"""
    
    print("🧪 演示不同的日志记录模式")
    print("=" * 60)
    
    modes = [
        ("simple", "简单文件记录 - 只记录关键信息"),
        ("dual", "双输出模式 - 终端+文件同时输出"),
        ("structured", "结构化日志 - 详细的步骤记录")
    ]
    
    for mode, description in modes:
        print(f"\n📋 模式: {mode}")
        print(f"📄 描述: {description}")
        
        choice = input(f"是否运行此模式的演示? (y/N): ").lower().strip()
        
        if choice == 'y':
            # 创建自定义日志文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"demo_{mode}_{timestamp}.log"
            
            print(f"🚀 运行模式: {mode}")
            print(f"📝 日志文件: {log_file}")
            
            # 运行分析（简化版本用于演示）
            try:
                callback_handler = create_callback_handler(
                    handler_type=mode,
                    log_file=log_file
                )
                
                # 简单的测试调用
                callback_handler(
                    step="演示步骤",
                    action="测试回调处理器",
                    data=f"这是{mode}模式的测试数据",
                    timestamp=datetime.now().isoformat()
                )
                
                print(f"✅ {mode}模式演示完成，请查看日志文件: {log_file}")
                
            except Exception as e:
                print(f"❌ {mode}模式演示失败: {str(e)}")
        
        print("-" * 40)

def main():
    """主函数"""
    print("🤖 预算分配Agent日志记录工具")
    print("=" * 40)
    
    print("选择运行模式:")
    print("1. 运行完整的预算分析 (推荐)")
    print("2. 演示不同的日志模式")
    print("3. 自定义配置运行")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        # 运行完整分析 - 使用推荐的dual模式
        print("\n🚀 使用推荐配置运行完整分析...")
        result = run_budget_analysis_with_logging(handler_type="dual")
        
        if result:
            print(f"\n🎉 分析成功完成！")
            print(f"📁 日志文件已保存，可以查看详细的执行过程。")
    
    elif choice == "2":
        # 演示不同模式
        demo_different_logging_modes()
    
    elif choice == "3":
        # 自定义配置
        print("\n⚙️ 自定义配置:")
        
        handler_type = input("日志处理器类型 (simple/dual/structured) [dual]: ").strip() or "dual"
        custom_file = input("自定义日志文件名 (留空自动生成): ").strip() or None
        
        print(f"\n🚀 使用自定义配置运行...")
        print(f"   - 处理器类型: {handler_type}")
        print(f"   - 日志文件: {custom_file or '自动生成'}")
        
        result = run_budget_analysis_with_logging(handler_type, custom_file)
        
        if result:
            print(f"\n🎉 自定义配置分析完成！")
    
    else:
        print("❌ 无效选择，退出程序。")

if __name__ == "__main__":
    main()