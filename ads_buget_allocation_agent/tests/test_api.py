#!/usr/bin/env python3
"""
预算分配Agent API测试脚本
"""

import time
import json
from api_client import BudgetAllocationAPIClient

def test_api():
    """测试API功能"""
    print("🧪 预算分配Agent API测试")
    print("=" * 50)
    
    # 创建客户端
    client = BudgetAllocationAPIClient("http://localhost:8000")
    
    # 1. 健康检查
    print("\n1️⃣ 健康检查...")
    health = client.health_check()
    print(f"   状态: {health.get('status', 'unknown')}")
    print(f"   Agent状态: {health.get('agent_status', 'unknown')}")
    print(f"   版本: {health.get('version', 'unknown')}")
    
    if health.get('status') != 'healthy':
        print("❌ 服务不健康，请检查API服务器是否启动")
        return
    
    # 2. 列出文件
    print("\n2️⃣ 列出可用文件...")
    files = client.list_files()
    print(f"   默认文件: {files.get('default_file')}")
    print(f"   上传文件数: {files.get('total_files', 0)}")
    
    # 3. 获取分析模板
    print("\n3️⃣ 获取分析模板...")
    templates = client.get_analysis_templates()
    if "templates" in templates:
        print("   可用模板:")
        for name, info in templates["templates"].items():
            print(f"     - {name}: {info['description']}")
    
    # 4. 快速分析
    print("\n4️⃣ 快速分析（基础）...")
    start_time = time.time()
    quick_result = client.quick_analysis(analysis_type="basic")
    
    if quick_result.get("success"):
        print(f"   ✅ 分析成功")
        print(f"   ⏱️ 耗时: {quick_result['execution_time']:.2f}秒")
        print(f"   📄 结果长度: {len(quick_result['result'])} 字符")
        print(f"   📝 结果预览: {quick_result['result'][:150]}...")
    else:
        print(f"   ❌ 分析失败: {quick_result.get('error')}")
    
    # 5. 预算分析
    print("\n5️⃣ 预算分析...")
    budget_result = client.analyze_budget(
        daily_budget=500,
        target_roas=20,
        enable_logging=True
    )
    
    if budget_result.get("success"):
        print(f"   ✅ 预算分析成功")
        print(f"   ⏱️ 耗时: {budget_result['execution_time']:.2f}秒")
        print(f"   📄 结果长度: {len(budget_result['result'])} 字符")
        print(f"   📝 日志文件: {budget_result.get('log_file', 'None')}")
        print(f"   📊 摘要: {budget_result.get('summary', {})}")
        print(f"   📝 结果预览: {budget_result['result'][:200]}...")
    else:
        print(f"   ❌ 预算分析失败: {budget_result.get('error')}")
    
    # 6. 使用模板分析
    print("\n6️⃣ 使用模板分析（表现分析）...")
    template_result = client.analyze_with_template("performance_analysis")
    
    if template_result.get("success"):
        print(f"   ✅ 模板分析成功")
        print(f"   ⏱️ 耗时: {template_result['execution_time']:.2f}秒")
        print(f"   📝 结果预览: {template_result['result'][:150]}...")
    else:
        print(f"   ❌ 模板分析失败: {template_result.get('error')}")
    
    # 7. 列出日志文件
    print("\n7️⃣ 列出日志文件...")
    logs = client.list_log_files()
    if "log_files" in logs:
        print(f"   📁 共有 {logs['total_files']} 个日志文件")
        for i, log in enumerate(logs["log_files"][:3]):  # 显示最新的3个
            print(f"     {i+1}. {log['filename']} ({log['size']} bytes)")
            print(f"        创建时间: {log['created']}")
    else:
        print(f"   ❌ 获取日志文件失败: {logs.get('error')}")
    
    # 8. 读取最新日志文件（如果有）
    if "log_files" in logs and len(logs["log_files"]) > 0:
        latest_log = logs["log_files"][0]["filename"]
        print(f"\n8️⃣ 读取最新日志文件: {latest_log}")
        log_content = client.get_log_file(latest_log)
        
        if "content" in log_content:
            print(f"   📄 文件大小: {log_content['size']} 字符")
            print(f"   📄 行数: {log_content['lines']}")
            print(f"   📝 内容预览:")
            lines = log_content['content'].split('\n')[:10]
            for line in lines:
                print(f"     {line}")
            if log_content['lines'] > 10:
                print(f"     ... (还有 {log_content['lines'] - 10} 行)")
        else:
            print(f"   ❌ 读取日志失败: {log_content.get('error')}")
    
    print("\n🎉 API测试完成！")

def test_error_handling():
    """测试错误处理"""
    print("\n🔧 错误处理测试")
    print("=" * 30)
    
    client = BudgetAllocationAPIClient("http://localhost:8000")
    
    # 测试无效文件ID
    print("\n1️⃣ 测试无效文件ID...")
    result = client.analyze_budget(
        daily_budget=500,
        target_roas=20,
        file_name="invalid_file_id"
    )
    print(f"   预期错误: {not result.get('success')}")
    if not result.get('success'):
        print(f"   错误信息: {result.get('error')}")
    
    # 测试无效模板
    print("\n2️⃣ 测试无效模板...")
    result = client.analyze_with_template("invalid_template")
    print(f"   预期错误: {not result.get('success')}")
    if not result.get('success'):
        print(f"   错误信息: {result.get('error')}")
    
    # 测试缺少参数的预算优化模板
    print("\n3️⃣ 测试缺少参数的预算优化模板...")
    result = client.analyze_with_template("budget_optimization")
    print(f"   预期错误: {not result.get('success')}")
    if not result.get('success'):
        print(f"   错误信息: {result.get('error')}")

def performance_test():
    """性能测试"""
    print("\n⚡ 性能测试")
    print("=" * 20)
    
    client = BudgetAllocationAPIClient("http://localhost:8000")
    
    # 测试多次快速分析
    print("\n1️⃣ 连续快速分析测试...")
    times = []
    for i in range(3):
        start = time.time()
        result = client.quick_analysis(analysis_type="basic")
        end = time.time()
        
        if result.get("success"):
            times.append(end - start)
            print(f"   第{i+1}次: {end - start:.2f}秒")
        else:
            print(f"   第{i+1}次失败: {result.get('error')}")
    
    if times:
        print(f"   平均耗时: {sum(times)/len(times):.2f}秒")
        print(f"   最快: {min(times):.2f}秒")
        print(f"   最慢: {max(times):.2f}秒")

if __name__ == "__main__":
    try:
        # 基础功能测试
        test_api()
        
        # 错误处理测试
        test_error_handling()
        
        # 性能测试
        performance_test()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()