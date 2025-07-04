#!/usr/bin/env python3
"""
预算分配Agent API演示脚本
展示如何使用API进行预算分析
"""

import time
import json
from api_client import BudgetAllocationAPIClient

def demo_basic_usage():
    """基础使用演示"""
    print("🎯 预算分配Agent API演示")
    print("=" * 50)
    
    # 创建客户端
    print("\n1️⃣ 创建API客户端...")
    client = BudgetAllocationAPIClient("http://localhost:8000")
    print("   ✅ 客户端创建成功")
    
    # 健康检查
    print("\n2️⃣ 健康检查...")
    health = client.health_check()
    if health.get('status') == 'healthy':
        print("   ✅ API服务器运行正常")
        print(f"   📊 Agent状态: {health.get('agent_status')}")
        print(f"   🔢 版本: {health.get('version')}")
    else:
        print("   ❌ API服务器异常，请检查服务是否启动")
        print("   💡 启动命令: python start_api.py")
        return False
    
    return True

def demo_quick_analysis(client):
    """快速分析演示"""
    print("\n3️⃣ 快速分析演示...")
    
    # 基础分析
    print("   📊 执行基础数据分析...")
    start_time = time.time()
    result = client.quick_analysis(analysis_type="basic")
    
    if result.get("success"):
        elapsed = time.time() - start_time
        print(f"   ✅ 分析完成 (耗时: {result['execution_time']:.2f}秒)")
        print(f"   📄 结果长度: {len(result['result'])} 字符")
        
        # 显示结果摘要
        lines = result['result'].split('\n')[:5]
        print("   📝 结果预览:")
        for line in lines:
            if line.strip():
                print(f"      {line}")
        print("      ...")
    else:
        print(f"   ❌ 分析失败: {result.get('error')}")
        return False
    
    return True

def demo_budget_analysis(client):
    """预算分析演示"""
    print("\n4️⃣ 预算分析演示...")
    
    # 设置分析参数
    daily_budget = 500
    target_roas = 20
    
    print(f"   💰 日预算: ${daily_budget}")
    print(f"   🎯 目标ROAS: {target_roas}")
    print("   📊 执行预算优化分析...")
    
    start_time = time.time()
    result = client.analyze_budget(
        daily_budget=daily_budget,
        target_roas=target_roas,
        enable_logging=True
    )
    
    if result.get("success"):
        elapsed = time.time() - start_time
        print(f"   ✅ 预算分析完成 (耗时: {result['execution_time']:.2f}秒)")
        print(f"   📝 日志文件: {result.get('log_file', 'None')}")
        print(f"   📄 结果长度: {len(result['result'])} 字符")
        
        # 检查是否包含预算调整建议
        if "Campaign ID" in result['result'] and "调整后预算" in result['result']:
            print("   ✅ 包含详细的预算调整建议表格")
        
        if "风险" in result['result']:
            print("   ✅ 包含风险评估分析")
        
        # 显示摘要信息
        if result.get('summary'):
            summary = result['summary']
            print("   📊 分析摘要:")
            print(f"      - 分析类型: {summary.get('analysis_type', 'unknown')}")
            print(f"      - 包含表格: {'是' if summary.get('contains_table') else '否'}")
            print(f"      - 包含建议: {'是' if summary.get('contains_recommendations') else '否'}")
        
        return result
    else:
        print(f"   ❌ 预算分析失败: {result.get('error')}")
        return None

def demo_templates(client):
    """分析模板演示"""
    print("\n5️⃣ 分析模板演示...")
    
    # 获取可用模板
    print("   📋 获取分析模板...")
    templates = client.get_analysis_templates()
    
    if "templates" in templates:
        print("   ✅ 可用模板:")
        for name, info in templates["templates"].items():
            print(f"      - {name}: {info['description']}")
        
        # 使用表现分析模板
        print("\n   📊 使用表现分析模板...")
        result = client.analyze_with_template("performance_analysis")
        
        if result.get("success"):
            print(f"   ✅ 模板分析完成 (耗时: {result['execution_time']:.2f}秒)")
            
            # 显示结果片段
            lines = result['result'].split('\n')[:3]
            print("   📝 结果预览:")
            for line in lines:
                if line.strip():
                    print(f"      {line}")
        else:
            print(f"   ❌ 模板分析失败: {result.get('error')}")
    else:
        print(f"   ❌ 获取模板失败: {templates.get('error')}")

def demo_log_management(client):
    """日志管理演示"""
    print("\n6️⃣ 日志管理演示...")
    
    # 列出日志文件
    print("   📁 获取日志文件列表...")
    logs = client.list_log_files()
    
    if "log_files" in logs:
        total_files = logs['total_files']
        print(f"   ✅ 找到 {total_files} 个日志文件")
        
        if total_files > 0:
            # 显示最新的几个日志文件
            print("   📝 最新日志文件:")
            for i, log in enumerate(logs["log_files"][:3]):
                size_kb = log['size'] / 1024
                print(f"      {i+1}. {log['filename']} ({size_kb:.1f}KB)")
                print(f"         创建时间: {log['created']}")
            
            # 读取最新日志文件的部分内容
            if logs["log_files"]:
                latest_log = logs["log_files"][0]["filename"]
                print(f"\n   📖 读取最新日志: {latest_log}")
                
                log_content = client.get_log_file(latest_log)
                if "content" in log_content:
                    lines = log_content['content'].split('\n')
                    print(f"   📄 文件信息: {log_content['lines']} 行, {log_content['size']} 字符")
                    
                    # 显示日志开头
                    print("   📝 日志开头:")
                    for line in lines[:5]:
                        if line.strip():
                            print(f"      {line}")
                    
                    # 检查是否包含Python执行结果
                    if "📊 Python执行结果" in log_content['content']:
                        print("   ✅ 日志包含完整的Python执行结果")
                    
                    if "🤖 Agent回复" in log_content['content']:
                        print("   ✅ 日志包含Agent分析回复")
                else:
                    print(f"   ❌ 读取日志失败: {log_content.get('error')}")
        else:
            print("   ℹ️ 暂无日志文件")
    else:
        print(f"   ❌ 获取日志列表失败: {logs.get('error')}")

def demo_error_handling(client):
    """错误处理演示"""
    print("\n7️⃣ 错误处理演示...")
    
    # 测试无效文件ID
    print("   🧪 测试无效文件ID...")
    result = client.analyze_budget(
        daily_budget=500,
        target_roas=20,
        file_name="invalid_file_id_12345"
    )
    
    if not result.get("success"):
        print("   ✅ 正确处理了无效文件ID错误")
        print(f"      错误信息: {result.get('error')}")
    else:
        print("   ⚠️ 未能正确处理无效文件ID")
    
    # 测试无效模板
    print("\n   🧪 测试无效模板...")
    result = client.analyze_with_template("invalid_template_name")
    
    if not result.get("success"):
        print("   ✅ 正确处理了无效模板错误")
        print(f"      错误信息: {result.get('error')}")
    else:
        print("   ⚠️ 未能正确处理无效模板")

def show_integration_example():
    """显示集成示例"""
    print("\n8️⃣ 集成示例...")
    
    print("""
   💡 Python集成示例:
   
   from api_client import BudgetAllocationAPIClient
   
   # 创建客户端
   client = BudgetAllocationAPIClient("http://localhost:8000")
   
   # 预算优化
   result = client.analyze_budget(
       daily_budget=500,
       target_roas=20,
       enable_logging=True
   )
   
   if result['success']:
       print("预算优化建议:")
       print(result['result'])
       
       # 保存日志
       if result['log_file']:
           print(f"详细日志: {result['log_file']}")
   """)
    
    print("""
   💡 cURL集成示例:
   
   # 预算分析
   curl -X POST http://localhost:8000/analyze/budget \\
     -H "Content-Type: application/json" \\
     -d '{
       "daily_budget": 500,
       "target_roas": 20,
       "enable_logging": true
     }'
   """)

def main():
    """主演示函数"""
    try:
        # 基础使用演示
        if not demo_basic_usage():
            return
        
        # 创建客户端
        client = BudgetAllocationAPIClient("http://localhost:8000")
        
        # 快速分析演示
        if not demo_quick_analysis(client):
            return
        
        # 预算分析演示
        budget_result = demo_budget_analysis(client)
        
        # 分析模板演示
        demo_templates(client)
        
        # 日志管理演示
        demo_log_management(client)
        
        # 错误处理演示
        demo_error_handling(client)
        
        # 集成示例
        show_integration_example()
        
        print("\n🎉 API演示完成！")
        print("\n📚 更多信息:")
        print("   - API文档: http://localhost:8000/docs")
        print("   - 详细指南: API_README.md")
        print("   - 日志指南: LOGGING_GUIDE.md")
        
        # 如果有预算分析结果，显示简要摘要
        if budget_result and budget_result.get('success'):
            print(f"\n💰 本次演示预算分析摘要:")
            print(f"   - 执行时间: {budget_result['execution_time']:.2f}秒")
            print(f"   - 日志文件: {budget_result.get('log_file', 'None')}")
            print(f"   - 结果包含预算调整建议: {'是' if 'Campaign ID' in budget_result['result'] else '否'}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 演示被用户中断")
    except Exception as e:
        print(f"\n\n❌ 演示过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()