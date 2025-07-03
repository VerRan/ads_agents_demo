#!/usr/bin/env python3
"""
API服务测试脚本
"""

import requests
import json
import time
from api_client import AIAnalystAPIClient

def test_api_endpoints():
    """测试API端点"""
    print("🧪 测试AI数据分析师API")
    print("=" * 40)
    
    client = AIAnalystAPIClient("http://localhost:8000")
    
    try:
        # 1. 健康检查
        print("1. 健康检查...")
        health = client.health_check()
        print(f"   ✅ 状态: {health['status']}")
        
        # 2. 获取根信息
        print("\n2. 获取API信息...")
        response = requests.get("http://localhost:8000/")
        root_info = response.json()
        print(f"   ✅ API版本: {root_info['version']}")
        
        # 3. 获取分析模板
        print("\n3. 获取分析模板...")
        templates = client.get_templates()
        print(f"   ✅ 可用模板数量: {len(templates['templates'])}")
        for key in list(templates['templates'].keys())[:3]:
            print(f"      - {key}")
        
        # 4. 预览默认数据
        print("\n4. 预览默认数据...")
        preview = client.preview_data(rows=3)
        print(f"   ✅ 数据形状: {preview['rows']} 行 x {preview['columns']} 列")
        print(f"   ✅ 列名: {preview['column_names'][:5]}")
        
        # 5. 基本统计分析
        print("\n5. 基本统计分析...")
        start_time = time.time()
        result = client.analyze_with_template("basic_stats")
        end_time = time.time()
        print(f"   ✅ 分析完成，用时: {end_time - start_time:.2f}秒")
        print(f"   ✅ 结果长度: {len(result['result'])} 字符")
        print(f"   📊 结果预览: {result['result'][:100]}...")
        
        # 6. 自定义查询
        print("\n6. 自定义查询...")
        custom_result = client.analyze_data("这个数据集有多少行数据？")
        print(f"   ✅ 查询结果: {custom_result['result']}")
        
        # 7. 数据质量检查
        print("\n7. 数据质量检查...")
        quality_result = client.analyze_with_template("data_quality")
        print(f"   ✅ 质量检查完成")
        print(f"   📊 结果预览: {quality_result['result'][:150]}...")
        
        # 8. 流式分析测试
        print("\n8. 流式分析测试...")
        print("   开始流式分析...")
        chunk_count = 0
        for chunk in client.analyze_data_stream("请简单介绍一下这个数据集的基本情况"):
            chunk_count += 1
            if chunk['type'] == 'start':
                print(f"   🚀 {chunk['message']}")
            elif chunk['type'] == 'chunk':
                print(f"   📦 接收数据块 {chunk_count}: {len(chunk['data'])} 字符")
            elif chunk['type'] == 'end':
                print(f"   ✅ {chunk['message']}")
                break
            elif chunk['type'] == 'error':
                print(f"   ❌ 错误: {chunk['message']}")
                break
        
        print(f"\n🎉 所有API测试完成！")
        print("📊 测试统计:")
        print(f"   - 健康检查: ✅")
        print(f"   - 模板查询: ✅")
        print(f"   - 数据预览: ✅")
        print(f"   - 基本分析: ✅")
        print(f"   - 自定义查询: ✅")
        print(f"   - 质量检查: ✅")
        print(f"   - 流式分析: ✅")
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务")
        print("💡 请确保API服务正在运行:")
        print("   python api_server.py")
        print("   或")
        print("   python start_services.py --api")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_api_performance():
    """测试API性能"""
    print("\n🚀 API性能测试")
    print("=" * 30)
    
    client = AIAnalystAPIClient("http://localhost:8000")
    
    # 测试查询
    queries = [
        "数据集有多少行？",
        "数据集有多少列？",
        "有缺失值吗？",
        "数据类型分布如何？"
    ]
    
    total_time = 0
    successful_queries = 0
    
    for i, query in enumerate(queries, 1):
        try:
            print(f"{i}. 查询: {query}")
            start_time = time.time()
            result = client.analyze_data(query)
            end_time = time.time()
            
            query_time = end_time - start_time
            total_time += query_time
            successful_queries += 1
            
            print(f"   ⏱️  用时: {query_time:.2f}秒")
            print(f"   📝 结果: {result['result'][:50]}...")
            
        except Exception as e:
            print(f"   ❌ 查询失败: {e}")
    
    if successful_queries > 0:
        avg_time = total_time / successful_queries
        print(f"\n📊 性能统计:")
        print(f"   - 成功查询: {successful_queries}/{len(queries)}")
        print(f"   - 总用时: {total_time:.2f}秒")
        print(f"   - 平均用时: {avg_time:.2f}秒")
        print(f"   - 查询速率: {successful_queries/total_time:.2f} 查询/秒")

def main():
    """主测试函数"""
    print("🧪 AI数据分析师API测试套件")
    print("=" * 50)
    
    # 基本功能测试
    test_api_endpoints()
    
    # 性能测试
    test_api_performance()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")

if __name__ == "__main__":
    main()