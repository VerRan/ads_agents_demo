#!/usr/bin/env python3
"""
测试回调函数是否正常工作
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# 模拟回调测试
def test_callback_simulation():
    """测试回调模拟"""
    st.title("🧪 回调函数测试")
    
    # 创建占位符
    content_placeholder = st.empty()
    status_placeholder = st.empty()
    code_stats_placeholder = st.empty()
    
    # 初始化显示
    content_placeholder.markdown("**等待测试开始...**")
    status_placeholder.info("准备中...")
    code_stats_placeholder.markdown("**🐍 代码执行:** 等待中...")
    
    if st.button("🚀 开始测试回调"):
        # 模拟回调数据
        test_callbacks = [
            {
                "current_tool_use": {
                    "name": "python_repl",
                    "input": {
                        "code": "import pandas as pd\nimport numpy as np"
                    }
                }
            },
            {
                "tool_result": "库导入成功"
            },
            {
                "current_tool_use": {
                    "name": "python_repl", 
                    "input": {
                        "code": "df = pd.read_csv('google.campaign_daily_geo_stats.csv')\nprint(f'数据形状: {df.shape}')"
                    }
                }
            },
            {
                "tool_result": "数据形状: (10000, 32)"
            },
            {
                "current_tool_use": {
                    "name": "python_repl",
                    "input": {
                        "code": "df.describe()"
                    }
                }
            },
            {
                "tool_result": "       clicks    impressions         cost  conversions\ncount  10000.0      10000.0    10000.0     10000.0\nmean     150.5       1505.2       75.3         7.5"
            }
        ]
        
        # 模拟回调处理
        content = ""
        code_execution_count = 0
        
        for i, callback_data in enumerate(test_callbacks):
            st.write(f"**步骤 {i+1}:** 处理回调 {list(callback_data.keys())}")
            
            if "current_tool_use" in callback_data:
                tool_use = callback_data["current_tool_use"]
                
                if tool_use.get("name") == "python_repl":
                    code = tool_use.get("input", {}).get("code", "")
                    if code:
                        code_execution_count += 1
                        
                        # 分析代码
                        from demo_app import analyze_code_purpose, estimate_code_complexity, get_execution_time_estimate
                        
                        code_purpose = analyze_code_purpose(code)
                        code_complexity = estimate_code_complexity(code)
                        time_estimate = get_execution_time_estimate(code)
                        
                        # 显示代码执行
                        code_display = f"""
---
**🐍 正在执行Python代码 (第{code_execution_count}步):**

📋 **代码信息:**
- 目的: {code_purpose}
- 复杂度: {code_complexity}
- 预计用时: {time_estimate}

```python
{code}
```

⏳ 执行中，请稍候...
"""
                        content += code_display
                        content_placeholder.markdown(content)
                        
                        # 更新状态
                        status_placeholder.info(f"🐍 第{code_execution_count}步: {code.split(chr(10))[0][:50]}...")
                        
                        # 更新统计
                        code_stats_placeholder.markdown(f"""**🐍 代码执行统计:**
- 已执行: {code_execution_count} 步
- 当前: {code_purpose}
- 状态: 执行中 ⏳""")
            
            elif "tool_result" in callback_data:
                result = callback_data["tool_result"]
                
                # 显示结果
                result_display = f"""
**📊 执行结果:**

```
{result}
```

---
"""
                content += result_display
                content_placeholder.markdown(content)
                
                # 更新状态
                status_placeholder.success(f"✅ 代码执行完成")
                
                # 更新统计
                code_stats_placeholder.markdown(f"""**🐍 代码执行统计:**
- 已完成: {code_execution_count} 步
- 状态: 完成 ✅""")
            
            # 添加延迟以便观察
            import time
            time.sleep(1)
        
        st.success("🎉 回调测试完成！")

def main():
    st.set_page_config(
        page_title="回调测试",
        page_icon="🧪",
        layout="wide"
    )
    
    test_callback_simulation()
    
    st.markdown("---")
    st.markdown("**说明:** 这个测试模拟了真实的回调处理过程，用于验证代码执行显示功能。")

if __name__ == "__main__":
    main()