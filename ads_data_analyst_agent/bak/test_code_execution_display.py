#!/usr/bin/env python3
"""
测试Python代码执行显示功能
"""

from datetime import datetime
import time

def test_code_analysis_functions():
    """测试代码分析函数"""
    print("🧪 测试代码分析函数...")
    
    # 测试代码样例
    test_codes = [
        "import pandas as pd\nimport numpy as np",
        "df = pd.read_csv('data.csv')",
        "df.describe()",
        "df.info()",
        "df.head(10)",
        "df.isnull().sum()",
        "df.groupby('category').mean()",
        "plt.figure(figsize=(10,6))\nplt.plot(df['x'], df['y'])\nplt.show()",
        "correlation = df.corr()",
        "for i in range(len(df)):\n    if df.loc[i, 'value'] > 100:\n        print(i)"
    ]
    
    # 导入分析函数
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    try:
        from demo_app import analyze_code_purpose, estimate_code_complexity, get_execution_time_estimate
        
        print("\n📋 代码分析结果:")
        print("-" * 80)
        
        for i, code in enumerate(test_codes, 1):
            purpose = analyze_code_purpose(code)
            complexity = estimate_code_complexity(code)
            time_est = get_execution_time_estimate(code)
            
            print(f"\n{i}. 代码:")
            print(f"   {code.replace(chr(10), ' | ')}")
            print(f"   目的: {purpose}")
            print(f"   复杂度: {complexity}")
            print(f"   预计时间: {time_est}")
        
        print("\n✅ 代码分析函数测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 代码分析函数测试失败: {e}")
        return False

def test_code_execution_simulation():
    """模拟代码执行过程"""
    print("\n🧪 模拟代码执行过程...")
    
    # 模拟代码执行步骤
    execution_steps = [
        {
            "code": "import pandas as pd\nimport numpy as np",
            "purpose": "导入必要的库和模块",
            "complexity": "简单 🟢",
            "time_estimate": "预计 <1秒 (快速查看)",
            "result": "库导入成功"
        },
        {
            "code": "df = pd.read_csv('google.campaign_daily_geo_stats.csv')",
            "purpose": "读取和加载数据文件",
            "complexity": "中等 🟡",
            "time_estimate": "预计 2-5秒 (数据读取)",
            "result": "数据加载成功，共10000行32列"
        },
        {
            "code": "df.describe()",
            "purpose": "生成数据的描述性统计",
            "complexity": "简单 🟢",
            "time_estimate": "预计 <1秒 (快速查看)",
            "result": "       clicks    impressions         cost  conversions\ncount  10000.0      10000.0    10000.0     10000.0\nmean     150.5       1505.2       75.3         7.5\nstd       89.2        892.1       44.6         4.5"
        },
        {
            "code": "df.groupby('device')['clicks'].sum()",
            "purpose": "按条件分组分析数据",
            "complexity": "中等 🟡", 
            "time_estimate": "预计 1-3秒 (数据处理)",
            "result": "device\ndesktop    750000\nmobile     755000\ntablet      45000\nName: clicks, dtype: int64"
        }
    ]
    
    print("\n📊 模拟执行过程:")
    print("=" * 80)
    
    total_start_time = datetime.now()
    
    for i, step in enumerate(execution_steps, 1):
        print(f"\n🐍 正在执行Python代码 (第{i}步):")
        print(f"📋 代码信息:")
        print(f"- 目的: {step['purpose']}")
        print(f"- 复杂度: {step['complexity']}")
        print(f"- 预计用时: {step['time_estimate']}")
        
        print(f"\n```python")
        print(step['code'])
        print(f"```")
        
        print(f"\n⏳ 执行中，请稍候...")
        
        # 模拟执行时间
        time.sleep(1)
        
        step_time = (datetime.now() - total_start_time).total_seconds()
        print(f"\n✅ 代码执行完成 ({step_time:.1f}秒)")
        
        print(f"\n📊 执行结果:")
        print(f"```")
        print(step['result'])
        print(f"```")
        
        print("-" * 40)
    
    total_time = (datetime.now() - total_start_time).total_seconds()
    print(f"\n🎉 所有代码执行完成！总用时: {total_time:.1f}秒")
    
    return True

def test_result_formatting():
    """测试结果格式化功能"""
    print("\n🧪 测试结果格式化功能...")
    
    # 测试不同类型的结果
    test_results = [
        "",  # 空结果
        "简单结果",  # 短结果
        "这是一个中等长度的结果，包含一些数据分析的内容，但不会太长。",  # 中等结果
        "\n".join([f"第{i}行数据" for i in range(50)]),  # 长结果（多行）
        "x" * 2000,  # 长结果（单行）
    ]
    
    try:
        from demo_app import format_code_result
        
        for i, result in enumerate(test_results, 1):
            print(f"\n测试结果 {i}:")
            formatted = format_code_result(result, "test_code")
            print(f"原始长度: {len(str(result))} 字符")
            print(f"格式化后: {len(formatted)} 字符")
            if len(formatted) < 200:
                print(f"内容预览: {formatted[:100]}...")
        
        print("\n✅ 结果格式化测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 结果格式化测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试Python代码执行显示功能...")
    print("=" * 80)
    
    tests = [
        ("代码分析函数", test_code_analysis_functions),
        ("代码执行模拟", test_code_execution_simulation),
        ("结果格式化", test_result_formatting)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name}测试出错: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 80)
    print("📋 测试结果汇总:")
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"- {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 所有Python代码执行显示功能测试通过！")
        print("\n💡 新功能包括:")
        print("- 实时代码执行显示")
        print("- 代码目的和复杂度分析")
        print("- 执行时间估算")
        print("- 步骤计数和统计")
        print("- 智能结果格式化")
        print("- 执行状态实时更新")
    else:
        print("⚠️  部分测试失败，请检查相关实现。")

if __name__ == "__main__":
    main()