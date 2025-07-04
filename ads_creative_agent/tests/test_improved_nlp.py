#!/usr/bin/env python3
"""
Test the improved natural language processing
"""

import streamlit as st

st.title("🧪 改进的自然语言处理测试")

st.markdown("""
### 测试改进的功能：

1. **智能图片收集**：
   - 优先查找本地文件
   - 然后下载URL图片
   - 避免重复处理

2. **智能图片分配**：
   - 自动识别人物照片和衣服图片
   - 智能分配源图片和参考图片
   - 单张图片时给出明确指导

3. **增强的日志**：
   - 显示收集到的图片数量
   - 详细的处理步骤
   - 更好的错误提示

### 测试用例：
""")

test_cases = [
    {
        "title": "完整虚拟试穿",
        "task": "用lht.jpg试穿这个衣服：https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg",
        "expected": "应该找到本地lht.jpg，下载衣服图片，然后执行虚拟试穿"
    },
    {
        "title": "单张图片下载",
        "task": "下载这个图片：https://cbu01.alicdn.com/img/ibank/8904729072_509441886.jpg",
        "expected": "应该下载图片并显示预览"
    },
    {
        "title": "混合任务",
        "task": "下载这个衣服图片：https://example.com/shirt.jpg，然后用lht.jpg进行虚拟试穿",
        "expected": "应该下载图片，找到本地文件，然后执行虚拟试穿"
    }
]

for i, case in enumerate(test_cases, 1):
    with st.expander(f"测试案例 {i}: {case['title']}"):
        st.write(f"**任务**: {case['task']}")
        st.write(f"**预期**: {case['expected']}")
        
        if st.button(f"测试案例 {i}", key=f"test_{i}"):
            st.session_state.test_task = case['task']
            st.rerun()

# Show test input
if 'test_task' in st.session_state and st.session_state.test_task:
    st.markdown("---")
    st.subheader("🔄 执行测试")
    st.write(f"**测试任务**: {st.session_state.test_task}")
    
    # Here you would call the actual execution function
    st.info("请在主UI中执行此任务以查看改进效果")
    
    if st.button("清除测试"):
        st.session_state.test_task = ""
        st.rerun()

st.markdown("---")
st.write("💡 **提示**: 运行主UI (`python run_nlp_ui.py`) 来测试这些改进功能")