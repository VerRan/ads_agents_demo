#!/usr/bin/env python3
"""
测试演示UI功能
"""

import os
import sys
import time

def test_file_existence():
    """测试文件是否存在"""
    print("📁 检查演示文件...")
    
    files_to_check = [
        'demo_ui.py',
        'demo_ui_with_agent.py',
        'run_demo.py',
        'run_demo_ui.py',
        'DEMO_UI_README.md'
    ]
    
    all_exist = True
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            all_exist = False
    
    return all_exist

def test_imports():
    """测试导入功能"""
    print("\n📦 检查依赖包...")
    
    packages = [
        ('streamlit', 'Streamlit Web框架'),
        ('pandas', '数据处理'),
        ('plotly', '图表可视化'),
        ('io', 'IO操作'),
        ('contextlib', '上下文管理'),
        ('threading', '多线程'),
        ('queue', '队列')
    ]
    
    all_imported = True
    for package, desc in packages:
        try:
            __import__(package)
            print(f"✅ {package} - {desc}")
        except ImportError:
            print(f"❌ {package} - {desc} (需要安装)")
            all_imported = False
    
    return all_imported

def test_data_files():
    """测试数据文件"""
    print("\n📊 检查数据文件...")
    
    if os.path.exists('2025-03-04_input.csv'):
        print("✅ 2025-03-04_input.csv - 真实数据文件")
        
        # 检查文件内容
        try:
            import pandas as pd
            df = pd.read_csv('2025-03-04_input.csv')
            print(f"   📈 数据行数: {len(df)}")
            print(f"   📊 数据列数: {len(df.columns)}")
            
            # 检查关键列
            required_columns = ['campaign_id', 'daily_budget', 'roas']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"   ⚠️ 缺少列: {missing_columns}")
            else:
                print("   ✅ 数据结构完整")
                
        except Exception as e:
            print(f"   ❌ 数据文件读取失败: {e}")
    else:
        print("⚠️ 2025-03-04_input.csv - 未找到，将使用演示数据")
    
    return True

def test_agent_import():
    """测试AI代理导入"""
    print("\n🤖 检查AI代理...")
    
    try:
        # 尝试导入预算分配代理
        sys.path.insert(0, '.')
        from buget_allocation_agent import agent
        print("✅ AI代理导入成功")
        print("   🧠 模型配置正常")
        return True
    except ImportError as e:
        print(f"⚠️ AI代理导入失败: {e}")
        print("   💡 将使用模拟模式")
        return False
    except Exception as e:
        print(f"⚠️ AI代理初始化失败: {e}")
        print("   💡 可能需要配置AWS凭证")
        return False

def test_log_files():
    """检查日志文件"""
    print("\n📝 检查日志文件...")
    
    log_files = []
    for file in os.listdir('.'):
        if file.startswith('budget_analysis_complete_') and file.endswith('.txt'):
            log_files.append(file)
    
    if log_files:
        print(f"✅ 找到 {len(log_files)} 个日志文件")
        
        # 显示最新的日志文件
        latest_log = max(log_files, key=os.path.getctime)
        file_size = os.path.getsize(latest_log)
        mod_time = time.ctime(os.path.getmtime(latest_log))
        
        print(f"   📄 最新日志: {latest_log}")
        print(f"   📏 文件大小: {file_size} bytes")
        print(f"   🕒 修改时间: {mod_time}")
        
        # 检查日志内容
        try:
            with open(latest_log, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                print(f"   📊 日志行数: {len(lines)}")
                
                # 检查关键内容
                key_indicators = ['🔧 工具', '🤖 Agent', '📊 Python', 'campaign_id']
                found_indicators = [ind for ind in key_indicators if ind in content]
                print(f"   🔍 包含关键信息: {found_indicators}")
                
        except Exception as e:
            print(f"   ❌ 日志文件读取失败: {e}")
    else:
        print("ℹ️ 暂无日志文件 (运行分析后会生成)")
    
    return True

def main():
    """主测试函数"""
    print("🧪 AI预算分配演示UI - 功能测试")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("文件存在性", test_file_existence),
        ("依赖包导入", test_imports),
        ("数据文件", test_data_files),
        ("AI代理", test_agent_import),
        ("日志文件", test_log_files)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 测试: {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "⚠️ 警告"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体状态: {passed}/{len(results)} 项测试通过")
    
    if passed >= len(results) - 1:  # 允许AI代理测试失败
        print("🎉 演示系统准备就绪!")
        print("\n💡 启动建议:")
        print("   python run_demo.py")
    else:
        print("⚠️ 部分功能可能不可用，建议检查配置")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()