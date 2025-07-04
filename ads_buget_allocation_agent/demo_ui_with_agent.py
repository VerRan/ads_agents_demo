#!/usr/bin/env python3
"""
预算分配Agent演示UI - 集成真实AI代理
基于Streamlit的操作界面，调用真实的预算分配代理
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import sys
from datetime import datetime
import io
import contextlib
import threading
import queue

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 页面配置
st.set_page_config(
    page_title="AI预算分配优化系统 - 真实AI版",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-log {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 0.9rem;
        max-height: 400px;
        overflow-y: auto;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """加载数据文件"""
    try:
        if os.path.exists("2025-03-04_input.csv"):
            df = pd.read_csv("2025-03-04_input.csv")
            return df, "real"
        else:
            # 使用模拟数据
            demo_data = {
                'campaign_id': ['camp_0296', 'camp_5539', 'camp_2002', 'camp_2164', 'camp_4441', 
                               'camp_3525', 'camp_3486', 'camp_6210', 'camp_0057'],
                'daily_budget': [24.5, 22.3, 34.6, 38.0, 67.1, 104.0, 56.1, 45.5, 9.6],
                'roas': [48.9, 61.8, 34.8, 31.5, 20.9, 15.25, 5.87, 10.3, 0.0],
                'purchase': [2, 4, 2, 2, 3, 5, 1, 2, 0],
                'purchase_value': [1220.0, 1378.1, 942.4, 1198.7, 2136.8, 1678.2, 201.9, 470.6, 0.0],
                'spend': [24.5, 22.3, 34.6, 38.0, 67.1, 104.0, 56.1, 45.5, 9.6]
            }
            return pd.DataFrame(demo_data), "demo"
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        return None, "error"

def initialize_agent():
    """初始化AI代理"""
    try:
        # 导入预算分配代理的组件
        from buget_allocation_agent import get_llm, PROMPT
        from strands import Agent
        from strands_tools import file_read, python_repl
        
        # 创建一个新的代理实例，这样我们可以控制回调处理器
        llm = get_llm()
        agent = Agent(
            model=llm,
            system_prompt=PROMPT,
            tools=[file_read, python_repl],
            callback_handler=None  # 我们稍后会设置
        )
        
        return agent, True
    except Exception as e:
        st.error(f"AI代理初始化失败: {str(e)}")
        st.info("将使用模拟模式运行演示")
        return None, False

class StreamlitCallbackHandler:
    """专门用于Streamlit的回调处理器"""
    
    def __init__(self, log_container=None):
        self.log_container = log_container
        self.tool_counter = 0
        self.log_content = []
        self.current_step = ""
        
    def add_log(self, message, emoji="📝"):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {emoji} {message}"
        self.log_content.append(log_entry)
        
        if self.log_container:
            # 更新显示
            formatted_content = "<br>".join(self.log_content)
            self.log_container.markdown(f'<div class="agent-log">{formatted_content}</div>', unsafe_allow_html=True)
    
    def __call__(self, **kwargs):
        """处理回调事件"""
        
        # 处理工具使用
        if 'current_tool_use' in kwargs and kwargs['current_tool_use']:
            tool_use = kwargs['current_tool_use']
            if isinstance(tool_use, dict):
                tool_name = tool_use.get('name', 'unknown')
                self.tool_counter += 1
                
                if tool_name == 'file_read':
                    self.add_log(f"工具 #{self.tool_counter}: 读取数据文件", "📂")
                elif tool_name == 'python_repl':
                    self.add_log(f"工具 #{self.tool_counter}: 执行Python分析", "🐍")
                    
                    # 显示Python代码
                    if 'input' in tool_use and isinstance(tool_use['input'], dict) and 'code' in tool_use['input']:
                        code = tool_use['input']['code']
                        # 只显示代码的前几行作为预览
                        code_lines = code.split('\n')[:3]
                        code_preview = '\n'.join(code_lines)
                        if len(code.split('\n')) > 3:
                            code_preview += '\n...'
                        self.add_log(f"执行代码预览:\n{code_preview}", "💻")
                else:
                    self.add_log(f"工具 #{self.tool_counter}: {tool_name}", "🔧")
        
        # 处理工具结果
        if 'tool_result' in kwargs and kwargs['tool_result']:
            result = str(kwargs['tool_result'])
            
            # 根据结果类型显示不同信息
            if 'DataFrame' in result or 'shape:' in result:
                self.add_log("数据分析完成，生成统计结果", "📊")
            elif 'campaign_id' in result.lower():
                self.add_log("Campaign数据处理完成", "📈")
            elif len(result) > 200:
                self.add_log(f"工具执行完成 (结果长度: {len(result)} 字符)", "✅")
            else:
                self.add_log(f"工具执行结果: {result[:100]}...", "✅")
        
        # 处理Agent消息
        if 'message' in kwargs and kwargs['message']:
            message_data = kwargs['message']
            if isinstance(message_data, dict) and 'content' in message_data:
                content = message_data['content']
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and 'text' in item:
                            text = item['text']
                            if text.strip():
                                # 只显示关键信息
                                if '分析' in text or '建议' in text or '优化' in text:
                                    preview = text[:100] + "..." if len(text) > 100 else text
                                    self.add_log(f"AI分析: {preview}", "🤖")

def capture_agent_output_with_callback(agent, task, log_container=None):
    """使用回调处理器捕获代理输出"""
    
    # 创建Streamlit回调处理器
    callback_handler = StreamlitCallbackHandler(log_container)
    
    # 显示开始信息
    if log_container:
        callback_handler.add_log("开始执行AI代理分析", "🚀")
        callback_handler.add_log(f"分析任务: {task[:100]}...", "📋")
    
    try:
        # 设置代理的回调处理器
        agent.callback_handler = callback_handler
        
        # 执行代理
        result = agent(task)
        
        # 显示完成信息
        callback_handler.add_log("AI代理分析完成!", "🎉")
        
        return result, "\n".join(callback_handler.log_content)
    
    except Exception as e:
        error_msg = f"代理执行错误: {str(e)}"
        callback_handler.add_log(error_msg, "❌")
        return error_msg, "\n".join(callback_handler.log_content)

def run_real_agent_analysis(agent, daily_budget, target_roas, filename="2025-03-04_input.csv"):
    """运行真实的AI代理分析"""
    
    # 创建任务描述
    task = f"""你必须在用户的日预算{daily_budget}及目标KPI{target_roas}的基础上，对用户提供的广告数据{filename}进行深度分析，后给出预算调整建议。"""
    
    # 显示分析过程
    st.subheader("🤖 AI代理分析过程")
    
    # 显示任务信息
    st.info(f"📋 分析任务: {task}")
    
    # 创建实时日志显示区域
    st.markdown("### 📝 实时执行日志")
    log_container = st.container()
    
    # 创建进度和状态显示
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🚀 启动AI代理...")
        progress_bar.progress(0.1)
        
        # 执行代理分析，传入日志容器用于实时显示
        status_text.text("🧠 AI代理正在分析数据...")
        progress_bar.progress(0.3)
        
        # 创建自定义回调处理器用于文件日志
        from custom_callback_handler import create_callback_handler
        file_callback_handler = create_callback_handler(
            handler_type="complete",
            log_file=None  # 自动生成文件名
        )
        
        # 在日志容器中显示实时输出
        with log_container:
            real_time_log = st.empty()
            
            # 创建组合回调处理器
            class CombinedCallbackHandler:
                def __init__(self, streamlit_handler, file_handler):
                    self.streamlit_handler = streamlit_handler
                    self.file_handler = file_handler
                
                def __call__(self, **kwargs):
                    # 同时调用两个处理器
                    self.streamlit_handler(**kwargs)
                    self.file_handler(**kwargs)
            
            streamlit_handler = StreamlitCallbackHandler(real_time_log)
            combined_handler = CombinedCallbackHandler(streamlit_handler, file_callback_handler)
            
            # 设置组合回调处理器
            agent.callback_handler = combined_handler
            
            # 执行代理
            streamlit_handler.add_log("开始执行AI代理分析", "🚀")
            streamlit_handler.add_log(f"分析任务: {task[:100]}...", "📋")
            
            try:
                result = agent(task)
                streamlit_handler.add_log("AI代理分析完成!", "🎉")
                captured_output = "\n".join(streamlit_handler.log_content)
            except Exception as e:
                error_msg = f"代理执行错误: {str(e)}"
                streamlit_handler.add_log(error_msg, "❌")
                result = error_msg
                captured_output = "\n".join(streamlit_handler.log_content)
        
        progress_bar.progress(0.9)
        status_text.text("📊 生成最终报告...")
        
        # 检查是否有日志文件生成
        time.sleep(2)  # 等待日志文件写入完成
        log_files = []
        for file in os.listdir('.'):
            if file.startswith('budget_analysis_complete_') and file.endswith('.txt'):
                log_files.append(file)
        
        if log_files:
            # 获取最新的日志文件
            latest_log = max(log_files, key=os.path.getctime)
            st.success(f"📄 完整日志已保存到: {latest_log}")
            
            # 显示日志文件预览
            try:
                with open(latest_log, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                
                # 显示日志预览
                with st.expander("📖 查看完整执行日志", expanded=True):
                    # 提取关键信息
                    lines = log_content.split('\n')
                    key_lines = []
                    for line in lines:
                        if any(keyword in line for keyword in ['🔧 工具', '🤖 Agent', '📊 Python', '执行结果', 'campaign_id', 'ROAS']):
                            key_lines.append(line)
                    
                    if key_lines:
                        st.text_area("关键执行步骤:", '\n'.join(key_lines[:50]), height=300)
                    
                    # 完整日志
                    if st.checkbox("显示完整日志"):
                        st.text_area("完整执行日志:", log_content, height=500)
                
                # 提供下载链接
                st.download_button(
                    label="📥 下载完整日志文件",
                    data=log_content,
                    file_name=latest_log,
                    mime="text/plain"
                )
            except Exception as e:
                st.warning(f"无法读取日志文件: {str(e)}")
        else:
            st.info("📝 日志文件可能正在生成中，请稍后刷新页面查看")
        
        progress_bar.progress(1.0)
        status_text.text("✅ 分析完成！")
        
        return result, captured_output
        
    except Exception as e:
        st.error(f"AI代理分析失败: {str(e)}")
        return None, str(e)

def simulate_analysis_fallback(daily_budget, target_roas, data):
    """模拟分析（备用方案）"""
    st.warning("🔄 使用模拟模式进行演示")
    
    # 模拟分析过程
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        ("🔍 正在读取数据文件...", 0.2),
        ("📊 分析数据结构...", 0.4),
        ("🧮 计算ROAS表现...", 0.6),
        ("💡 生成优化建议...", 0.8),
        ("✅ 完成分析...", 1.0)
    ]
    
    for step_text, progress in steps:
        status_text.text(step_text)
        progress_bar.progress(progress)
        time.sleep(1)
    
    # 生成模拟结果
    result = f"""
## 📊 预算分配优化建议

基于您设置的日预算 ${daily_budget} 和目标ROAS {target_roas}，以下是AI分析结果：

### 🎯 优化策略
- 高效Campaign (ROAS > {target_roas * 1.2}): 增加预算投入
- 达标Campaign (ROAS > {target_roas}): 维持或小幅增加
- 低效Campaign (ROAS < {target_roas}): 减少预算或暂停

### 📈 预期效果
- 预计整体ROAS提升 15-25%
- 预算利用效率提升 20%
- 无效投放减少 30%

*注: 这是模拟演示结果，实际使用时会调用真实的AI代理进行分析*
    """
    
    return result

def parse_agent_result(result_text):
    """解析代理结果，提取结构化数据"""
    # 这里可以添加更复杂的解析逻辑
    # 目前返回原始文本
    return result_text

def display_log_files():
    """显示可用的日志文件"""
    st.subheader("📄 执行日志文件")
    
    # 查找日志文件
    log_files = []
    for file in os.listdir('.'):
        if file.startswith('budget_analysis_complete_') and file.endswith('.txt'):
            log_files.append(file)
    
    if not log_files:
        st.info("暂无日志文件")
        return
    
    # 按时间排序，最新的在前
    log_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
    
    # 显示日志文件列表
    selected_log = st.selectbox(
        "选择要查看的日志文件:",
        log_files,
        format_func=lambda x: f"{x} ({time.ctime(os.path.getctime(x))})"
    )
    
    if selected_log:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.text(f"文件: {selected_log}")
        with col2:
            file_size = os.path.getsize(selected_log)
            st.text(f"大小: {file_size} bytes")
        with col3:
            mod_time = time.ctime(os.path.getmtime(selected_log))
            st.text(f"修改时间: {mod_time}")
        
        # 显示日志内容
        try:
            with open(selected_log, 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            # 提供查看选项
            view_option = st.radio(
                "查看方式:",
                ["摘要", "完整内容"],
                horizontal=True
            )
            
            if view_option == "摘要":
                # 显示日志摘要
                lines = log_content.split('\n')
                summary_lines = []
                
                for line in lines[:20]:  # 前20行
                    if any(keyword in line for keyword in ['🔧', '🤖', '📊', '✅', '❌', '⚠️']):
                        summary_lines.append(line)
                
                if summary_lines:
                    st.text_area("日志摘要:", '\n'.join(summary_lines), height=200)
                else:
                    st.text_area("日志摘要:", log_content[:1000] + "...", height=200)
            
            else:
                # 显示完整内容
                st.text_area("完整日志:", log_content, height=400)
            
            # 下载按钮
            st.download_button(
                label="📥 下载此日志文件",
                data=log_content,
                file_name=selected_log,
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"无法读取日志文件: {str(e)}")
    
    # 清理旧日志文件的选项
    if len(log_files) > 5:
        st.warning(f"检测到 {len(log_files)} 个日志文件，建议清理旧文件")
        if st.button("🗑️ 清理旧日志文件 (保留最新5个)"):
            files_to_delete = log_files[5:]  # 删除除最新5个外的所有文件
            deleted_count = 0
            for file in files_to_delete:
                try:
                    os.remove(file)
                    deleted_count += 1
                except Exception as e:
                    st.error(f"删除文件 {file} 失败: {str(e)}")
            
            if deleted_count > 0:
                st.success(f"已删除 {deleted_count} 个旧日志文件")
                st.rerun()

def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-header">🤖 AI预算分配优化系统 - 真实AI版</h1>', unsafe_allow_html=True)
    
    # 初始化AI代理
    with st.spinner("🔧 正在初始化AI代理..."):
        agent, agent_available = initialize_agent()
    
    if agent_available:
        st.success("✅ AI代理初始化成功！")
    else:
        st.warning("⚠️ AI代理不可用，将使用模拟模式")
    
    # 侧边栏参数设置
    st.sidebar.header("🎛️ 分析参数")
    
    daily_budget = st.sidebar.number_input(
        "日预算 ($)",
        min_value=100,
        max_value=2000,
        value=500,
        step=50,
        help="设置每日总预算"
    )
    
    target_roas = st.sidebar.number_input(
        "目标ROAS",
        min_value=5.0,
        max_value=50.0,
        value=20.0,
        step=1.0,
        help="设置目标广告投资回报率"
    )
    
    # 高级选项
    with st.sidebar.expander("🔧 高级选项"):
        enable_logging = st.checkbox("启用详细日志", value=True)
        analysis_mode = st.selectbox(
            "分析模式",
            ["标准分析", "深度分析", "快速分析"],
            index=0
        )
    
    # 加载数据
    data, data_type = load_data()
    
    if data is not None:
        # 显示数据信息
        st.subheader("📊 数据概览")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Campaign数量", len(data))
        with col2:
            st.metric("总预算", f"${data['daily_budget'].sum():.1f}")
        with col3:
            st.metric("平均ROAS", f"{data['roas'].mean():.1f}")
        with col4:
            data_status = "真实数据" if data_type == "real" else "演示数据"
            st.metric("数据类型", data_status)
        
        # 显示数据表格
        with st.expander("📋 查看详细数据", expanded=False):
            st.dataframe(data, use_container_width=True)
        
        # 分析按钮
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🚀 开始AI分析")
            st.markdown("点击下方按钮启动AI代理进行预算优化分析")
        
        with col2:
            analyze_button = st.button(
                "🤖 启动AI分析", 
                type="primary",
                use_container_width=True
            )
        
        if analyze_button:
            st.markdown('<div class="success-box">🚀 正在启动AI预算优化分析...</div>', unsafe_allow_html=True)
            
            if agent_available and agent:
                # 使用真实AI代理
                result, logs = run_real_agent_analysis(agent, daily_budget, target_roas)
                
                if result:
                    st.subheader("📋 AI分析结果")
                    st.markdown(result)
                    
                    # 显示日志文件内容
                    st.markdown("---")
                    display_log_files()
                    
                    # 提供下载选项
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📥 下载分析报告"):
                            report_content = f"""
AI预算分配优化报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
日预算: ${daily_budget}
目标ROAS: {target_roas}

{result}

执行日志:
{logs}
                            """
                            st.download_button(
                                label="下载完整报告",
                                data=report_content,
                                file_name=f"budget_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain"
                            )
                    
                    with col2:
                        if st.button("🔄 重新分析"):
                            st.rerun()
            else:
                # 使用模拟分析
                result = simulate_analysis_fallback(daily_budget, target_roas, data)
                st.subheader("📋 分析结果")
                st.markdown(result)
    
    else:
        st.error("❌ 无法加载数据，请检查数据文件")
    
    # 页面底部信息
    st.markdown("---")
    st.markdown("""
    ### 💡 系统说明
    
    #### 🤖 AI代理功能
    - **真实AI分析**: 使用Amazon Bedrock Claude模型进行智能分析
    - **数据处理**: 自动读取和分析CSV数据文件
    - **优化建议**: 基于目标ROAS生成具体的预算调整建议
    - **风险评估**: 为每个调整建议提供风险等级评估
    
    #### 📊 分析能力
    - **多维度分析**: ROAS、转化率、预算效率等多角度评估
    - **智能决策**: 基于历史数据和目标KPI的智能决策
    - **实时处理**: 快速响应参数调整，实时生成优化建议
    - **详细日志**: 完整记录AI思考和分析过程
    
    #### 🎯 使用场景
    - **日常优化**: 定期进行预算分配优化
    - **策略调整**: 根据市场变化调整投放策略
    - **效果评估**: 评估当前Campaign表现
    - **决策支持**: 为预算决策提供数据支撑
    """)
    
    # 技术信息
    with st.expander("🔧 技术信息", expanded=False):
        st.markdown("""
        **AI模型**: Amazon Bedrock Claude 3.5 Sonnet
        **数据处理**: Pandas + Python REPL
        **可视化**: Plotly + Streamlit
        **部署**: 本地Streamlit应用
        
        **系统状态**:
        - AI代理: """ + ("✅ 可用" if agent_available else "❌ 不可用") + """
        - 数据文件: """ + ("✅ 已加载" if data is not None else "❌ 未找到") + """
        - 分析模式: """ + analysis_mode + """
        """)

if __name__ == "__main__":
    main()