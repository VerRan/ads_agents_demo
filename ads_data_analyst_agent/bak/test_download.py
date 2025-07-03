#!/usr/bin/env python3
"""
测试下载功能的脚本
"""

import pandas as pd
import json
from datetime import datetime
import io

def create_analysis_report_text(query, result, file_name):
    """创建文本格式的分析报告"""
    report = f"""# 数据分析报告

## 基本信息
- **分析时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **数据文件:** {file_name}
- **分析问题:** {query}

## 分析结果

{result}

---
报告由AI数据分析师生成
"""
    return report

def create_json_report(analysis_data):
    """创建JSON格式的分析报告"""
    try:
        report_data = {
            "analysis_time": datetime.now().isoformat(),
            "file_name": analysis_data.get('file_name', ''),
            "query": analysis_data.get('query', ''),
            "result": analysis_data.get('result', ''),
            "metadata": {
                "tool": "AI数据分析师",
                "version": "1.0"
            }
        }
        return json.dumps(report_data, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"创建JSON报告失败: {str(e)}")
        return None

def create_csv_summary(data):
    """创建CSV格式的数据摘要"""
    try:
        summary_data = []
        
        # 基本信息
        summary_data.append(['数据项', '值'])
        summary_data.append(['总行数', len(data)])
        summary_data.append(['总列数', len(data.columns)])
        summary_data.append(['缺失值总数', data.isnull().sum().sum()])
        summary_data.append(['数值列数量', len(data.select_dtypes(include=['number']).columns)])
        summary_data.append([''])
        
        # 列信息
        summary_data.append(['列名', '数据类型', '缺失值数量', '唯一值数量'])
        for col in data.columns:
            summary_data.append([
                col,
                str(data[col].dtype),
                data[col].isnull().sum(),
                data[col].nunique()
            ])
        
        # 转换为DataFrame
        max_cols = max(len(row) for row in summary_data)
        for row in summary_data:
            while len(row) < max_cols:
                row.append('')
        
        df_summary = pd.DataFrame(summary_data)
        
        # 转换为CSV
        csv_buffer = io.StringIO()
        df_summary.to_csv(csv_buffer, index=False, header=False, encoding='utf-8')
        
        return csv_buffer.getvalue()
    except Exception as e:
        print(f"创建CSV摘要失败: {str(e)}")
        return None

def test_download_functions():
    """测试下载功能"""
    print("🧪 测试下载功能...")
    
    # 创建测试数据
    test_data = pd.DataFrame({
        'A': [1, 2, 3, None, 5],
        'B': ['a', 'b', 'c', 'd', 'e'],
        'C': [1.1, 2.2, 3.3, 4.4, 5.5]
    })
    
    # 测试分析数据
    test_analysis = {
        'query': '测试查询：分析数据基本信息',
        'result': '这是一个测试分析结果，包含了数据的基本统计信息。',
        'file_name': 'test_data.csv'
    }
    
    # 测试Markdown报告
    print("📄 测试Markdown报告生成...")
    markdown_report = create_analysis_report_text(
        test_analysis['query'],
        test_analysis['result'],
        test_analysis['file_name']
    )
    print("✅ Markdown报告生成成功")
    print(f"报告长度: {len(markdown_report)} 字符")
    
    # 测试JSON报告
    print("📊 测试JSON报告生成...")
    json_report = create_json_report(test_analysis)
    if json_report:
        print("✅ JSON报告生成成功")
        print(f"报告长度: {len(json_report)} 字符")
    else:
        print("❌ JSON报告生成失败")
    
    # 测试CSV摘要
    print("📈 测试CSV摘要生成...")
    csv_summary = create_csv_summary(test_data)
    if csv_summary:
        print("✅ CSV摘要生成成功")
        print(f"摘要长度: {len(csv_summary)} 字符")
        print("摘要预览:")
        print(csv_summary[:200] + "..." if len(csv_summary) > 200 else csv_summary)
    else:
        print("❌ CSV摘要生成失败")
    
    print("\n🎉 所有下载功能测试完成！")

if __name__ == "__main__":
    test_download_functions()