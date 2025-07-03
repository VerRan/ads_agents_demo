import streamlit as st
import pandas as pd
import os
import io
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI数据分析师演示",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .demo-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .analysis-status {
        background-color: #f0f8ff;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .code-execution {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .metric-compact {
        text-align: center;
        padding: 0.5rem;
        background-color: #f8f9fa;
        border-radius: 5px;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
    .status-row {
        background-color: #fafafa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_file_name' not in st.session_state:
    st.session_state.current_file_name = None

def load_default_data():
    """Load default Google Ads data"""
    try:
        data_path = "google.campaign_daily_geo_stats.csv"
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            if 'data_day' in df.columns:
                df['data_day'] = pd.to_datetime(df['data_day'])
            if 'fetch_time' in df.columns:
                df['fetch_time'] = pd.to_datetime(df['fetch_time'])
            return df, "google.campaign_daily_geo_stats.csv"
        return None, None
    except Exception as e:
        st.error(f"加载默认数据失败: {str(e)}")
        return None, None

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
        st.error(f"创建JSON报告失败: {str(e)}")
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
        st.error(f"创建CSV摘要失败: {str(e)}")
        return None

def create_history_export(analysis_history):
    """创建分析历史的导出文件"""
    try:
        export_data = {
            "export_time": datetime.now().isoformat(),
            "total_analyses": len(analysis_history),
            "analyses": []
        }
        
        for analysis in analysis_history:
            export_data["analyses"].append({
                "timestamp": analysis['timestamp'].isoformat(),
                "file_name": analysis.get('file_name', ''),
                "query": analysis['query'],
                "result": analysis['result']
            })
        
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"创建历史导出失败: {str(e)}")
        return None

def analyze_code_purpose(code):
    """分析代码的目的和功能"""
    code_lower = code.lower()
    
    if 'import' in code_lower:
        return "导入必要的库和模块"
    elif 'read_csv' in code_lower or 'pd.read' in code_lower:
        return "读取和加载数据文件"
    elif 'describe()' in code_lower:
        return "生成数据的描述性统计"
    elif 'info()' in code_lower:
        return "查看数据基本信息"
    elif 'head()' in code_lower or 'tail()' in code_lower:
        return "查看数据样本"
    elif 'isnull()' in code_lower or 'isna()' in code_lower:
        return "检查缺失值"
    elif 'groupby' in code_lower:
        return "按条件分组分析数据"
    elif 'plot' in code_lower or 'plt.' in code_lower:
        return "创建数据可视化图表"
    elif 'corr()' in code_lower:
        return "计算相关性分析"
    elif 'value_counts()' in code_lower:
        return "统计数值分布"
    elif 'mean()' in code_lower or 'sum()' in code_lower or 'count()' in code_lower:
        return "计算统计指标"
    elif 'merge' in code_lower or 'join' in code_lower:
        return "合并和连接数据"
    elif 'drop' in code_lower:
        return "删除不需要的数据"
    elif 'fillna' in code_lower:
        return "处理缺失值"
    else:
        return "执行数据分析操作"

def estimate_code_complexity(code):
    """估算代码复杂度"""
    lines = code.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    
    complexity_score = 0
    
    # 基础复杂度：行数
    complexity_score += len(non_empty_lines)
    
    # 循环和条件语句增加复杂度
    for line in non_empty_lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in ['for ', 'while ', 'if ', 'elif ', 'try:', 'except']):
            complexity_score += 2
        if any(keyword in line_lower for keyword in ['groupby', 'merge', 'join', 'pivot']):
            complexity_score += 3
        if any(keyword in line_lower for keyword in ['plot', 'figure', 'subplot']):
            complexity_score += 2
    
    if complexity_score <= 5:
        return "简单 🟢"
    elif complexity_score <= 15:
        return "中等 🟡"
    else:
        return "复杂 🔴"

def format_code_result(result, code):
    """格式化代码执行结果"""
    if not result:
        return "代码执行完成，无输出结果"
    
    result_str = str(result)
    
    # 如果结果太长，进行智能截断
    if len(result_str) > 1000:
        lines = result_str.split('\n')
        if len(lines) > 20:
            # 显示前10行和后5行
            truncated = '\n'.join(lines[:10]) + '\n\n... (省略中间部分) ...\n\n' + '\n'.join(lines[-5:])
            return f"```\n{truncated}\n```\n\n*完整结果共{len(lines)}行，已智能截断显示*"
        else:
            # 按字符截断
            return f"```\n{result_str[:500]}\n\n... (结果太长，已截断) ...\n\n{result_str[-200:]}\n```"
    else:
        return f"```\n{result_str}\n```"

def get_execution_time_estimate(code):
    """估算代码执行时间"""
    code_lower = code.lower()
    
    if any(keyword in code_lower for keyword in ['read_csv', 'read_excel', 'read_sql']):
        return "预计 2-5秒 (数据读取)"
    elif any(keyword in code_lower for keyword in ['groupby', 'merge', 'join']):
        return "预计 1-3秒 (数据处理)"
    elif any(keyword in code_lower for keyword in ['plot', 'figure', 'subplot']):
        return "预计 1-2秒 (图表生成)"
    elif any(keyword in code_lower for keyword in ['describe', 'info', 'head', 'tail']):
        return "预计 <1秒 (快速查看)"
    else:
        return "预计 1-2秒 (一般操作)"

def create_streaming_agent(content_placeholder, status_placeholder, code_stats_placeholder=None):
    """创建支持流式输出的代理"""
    
    def streaming_callback(**kwargs):
        try:
            # 打印所有回调信息用于调试
            print(f"🔔 Callback received: {list(kwargs.keys())}")
            for key, value in kwargs.items():
                print(f"  {key}: {str(value)[:100]}...")
            
            # 处理所有类型的回调
            for key, value in kwargs.items():
                # 处理文本数据
                if key in ['data', 'text'] and value:
                    if hasattr(streaming_callback, 'content'):
                        streaming_callback.content += str(value)
                    else:
                        streaming_callback.content = str(value)
                    
                    content_placeholder.markdown(streaming_callback.content)
                    
                    # 更新状态
                    preview = str(value).strip()[:50]
                    if preview:
                        status_placeholder.info(f"💬 AI输出: {preview}...")
                
                # 处理工具相关的回调
                elif 'tool' in key.lower() or 'python' in str(value).lower():
                    print(f"🔧 Tool-related callback: {key} = {value}")
                    
                    # 尝试解析工具信息
                    if isinstance(value, dict):
                        tool_name = value.get('name', value.get('tool', 'unknown'))
                        tool_input = value.get('input', value.get('tool_input', {}))
                        
                        if 'python' in tool_name.lower() or 'repl' in tool_name.lower():
                            # 处理Python代码执行
                            if isinstance(tool_input, dict) and 'code' in tool_input:
                                code = str(tool_input['code'])
                                
                                streaming_callback.code_execution_count += 1
                                code_purpose = analyze_code_purpose(code)
                                code_complexity = estimate_code_complexity(code)
                                time_estimate = get_execution_time_estimate(code)
                                
                                code_display = f"""
---
**🐍 正在执行Python代码 (第{streaming_callback.code_execution_count}步):**

📋 **代码信息:**
- 目的: {code_purpose}
- 复杂度: {code_complexity}
- 预计用时: {time_estimate}

```python
{code}
```

⏳ 执行中，请稍候...
"""
                                if hasattr(streaming_callback, 'content'):
                                    streaming_callback.content += code_display
                                else:
                                    streaming_callback.content = code_display
                                content_placeholder.markdown(streaming_callback.content)
                                
                                # 更新统计
                                if hasattr(streaming_callback, 'code_stats_placeholder') and streaming_callback.code_stats_placeholder:
                                    streaming_callback.code_stats_placeholder.markdown(f'<div class="analysis-status"><strong>🐍 第{streaming_callback.code_execution_count}步:</strong><br/>{code_purpose} ⏳</div>', unsafe_allow_html=True)
                                
                                status_placeholder.info(f"🐍 执行代码: {code.split(chr(10))[0][:50]}...")
                                streaming_callback.last_code_start = datetime.now()
                    
                    elif isinstance(value, str) and len(value) > 10:
                        # 可能是工具执行结果
                        result_display = f"""
**📊 执行结果:**

```
{value}
```

---
"""
                        if hasattr(streaming_callback, 'content'):
                            streaming_callback.content += result_display
                        else:
                            streaming_callback.content = result_display
                        content_placeholder.markdown(streaming_callback.content)
                        
                        # 更新统计
                        if hasattr(streaming_callback, 'code_stats_placeholder') and streaming_callback.code_stats_placeholder:
                            execution_time = (datetime.now() - streaming_callback.last_code_start).total_seconds() if hasattr(streaming_callback, 'last_code_start') else 0
                            streaming_callback.code_stats_placeholder.markdown(f'<div class="analysis-status"><strong>🐍 完成{streaming_callback.code_execution_count}步:</strong><br/>用时{execution_time:.1f}秒 ✅</div>', unsafe_allow_html=True)
                        
                        status_placeholder.success(f"✅ 执行完成: {str(value)[:50]}...")
                
                # 处理其他类型的回调
                else:
                    if st.session_state.get('debug_mode', False):
                        print(f"Other callback: {key} = {str(value)[:100]}...")
                    
        except Exception as e:
            error_msg = f"回调函数错误: {e}"
            print(error_msg)
            if st.session_state.get('debug_mode', False):
                st.error(error_msg)
    
    # 初始化内容和工具跟踪
    streaming_callback.content = ""
    streaming_callback.code_execution_count = 0
    streaming_callback.current_step = "准备中"
    streaming_callback.code_stats_placeholder = code_stats_placeholder
    
    # 动态导入agent组件
    try:
        from google_ads_anlyst_agent import get_llm
        from strands import Agent
        from strands_tools import file_read, python_repl
        
        # 创建流式代理 - 直接使用回调函数
        streaming_agent = Agent(
            model=get_llm(),
            system_prompt="""
作为一位专业的数据分析专家和Python编程专家，请帮我编写代码完成数据分析任务。

请详细说明分析过程，包括:
1. 数据加载和基本信息查看
2. 数据清洗和预处理步骤  
3. 逐步的分析过程，每步附有详细说明
4. 关键发现和洞察
5. 结论和建议

请确保分析过程清晰易懂，结果准确可靠。在执行每个步骤时，请详细解释你在做什么。
            """,
            tools=[file_read, python_repl],
            callback_handler=streaming_callback
        )
        
        return streaming_agent, streaming_callback
        
    except Exception as e:
        st.error(f"创建流式代理失败: {str(e)}")
        return None, None

def analyze_data_with_agent_streaming(query, data_file_name, content_placeholder, status_placeholder):
    """使用AI代理进行流式分析"""
    try:
        # 步骤1: 创建流式代理
        status_placeholder.info("🔧 正在创建AI分析代理...")
        streaming_agent, callback = create_streaming_agent(content_placeholder, status_placeholder)
        
        if streaming_agent is None:
            status_placeholder.warning("⚠️ 流式代理创建失败，切换到备用模式...")
            return analyze_data_fallback(query, data_file_name, content_placeholder, status_placeholder)
        
        # 步骤2: 构建查询
        status_placeholder.info("📝 正在构建分析查询...")
        full_query = f"当前目录{data_file_name}的文件，{query}"
        
        # 步骤3: 初始化显示
        status_placeholder.info("🚀 AI分析代理已启动，开始分析...")
        content_placeholder.markdown("**🤖 AI分析过程:**\n\n🔍 AI正在理解您的问题...\n")
        
        # 步骤4: 执行流式分析
        status_placeholder.info("🧠 AI正在思考和分析...")
        result = streaming_agent(full_query)
        
        # 步骤5: 处理结果
        status_placeholder.info("📊 正在整理分析结果...")
        final_content = callback.content if callback.content else str(result)
        
        # 如果没有流式内容，显示最终结果
        if not callback.content and result:
            final_content = f"**🎯 最终分析结果:**\n\n{str(result)}"
            content_placeholder.markdown(final_content)
        else:
            # 添加结束标记
            if hasattr(callback, 'content') and callback.content:
                callback.content += "\n\n---\n**✅ 分析完成**"
                content_placeholder.markdown(callback.content)
        
        return final_content
        
    except Exception as e:
        error_msg = f"流式分析失败: {str(e)}"
        print(error_msg)
        status_placeholder.warning("⚠️ 流式分析遇到问题，切换到备用模式...")
        return analyze_data_fallback(query, data_file_name, content_placeholder, status_placeholder)

def analyze_data_with_agent_streaming_with_progress(query, data_file_name, content_placeholder, status_placeholder, progress_placeholder, time_placeholder, code_stats_placeholder, start_time):
    """带进度显示的流式分析"""
    try:
        # 步骤1: 创建代理 (20%)
        progress_placeholder.progress(0.2)
        time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 - 创建AI代理")
        
        streaming_agent, callback = create_streaming_agent(content_placeholder, status_placeholder, code_stats_placeholder)
        
        if streaming_agent is None:
            return analyze_data_fallback_with_progress(query, data_file_name, content_placeholder, status_placeholder, progress_placeholder, time_placeholder, code_stats_placeholder, start_time)
        
        # 步骤2: 准备查询 (40%)
        progress_placeholder.progress(0.4)
        time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 - 准备查询")
        
        full_query = f"当前目录{data_file_name}的文件，{query}"
        content_placeholder.markdown("**🤖 AI分析过程:**\n\n🔍 AI正在理解您的问题...\n")
        
        # 步骤3: 执行分析 (60%-90%)
        progress_placeholder.progress(0.6)
        time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 - 执行分析")
        
        result = streaming_agent(full_query)
        
        # 步骤4: 完成 (100%)
        progress_placeholder.progress(1.0)
        time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 - 完成")
        
        final_content = callback.content if callback.content else str(result)
        
        if not callback.content and result:
            final_content = f"**🎯 最终分析结果:**\n\n{str(result)}"
            content_placeholder.markdown(final_content)
        else:
            if hasattr(callback, 'content') and callback.content:
                callback.content += "\n\n---\n**✅ 分析完成**"
                content_placeholder.markdown(callback.content)
        
        return final_content
        
    except Exception as e:
        error_msg = f"流式分析失败: {str(e)}"
        print(error_msg)
        return analyze_data_fallback_with_progress(query, data_file_name, content_placeholder, status_placeholder, progress_placeholder, time_placeholder, start_time)

def analyze_data_fallback(query, data_file_name, content_placeholder, status_placeholder):
    """备用的非流式分析方法"""
    try:
        # 步骤1: 导入AI代理
        status_placeholder.info("🔧 正在加载AI分析引擎（备用模式）...")
        content_placeholder.markdown("**🤖 备用分析模式启动**\n\n🔧 正在初始化AI分析引擎...")
        
        from google_ads_anlyst_agent import agent
        
        # 步骤2: 构建查询
        status_placeholder.info("� 正在准备分析查询（...")
        full_query = f"当前目录{data_file_name}的文件，{query}"
        content_placeholder.markdown("**🤖 备用分析模式启动**\n\n📝 查询已准备完成\n\n🧠 AI正在深度分析您的数据...")
        
        # 步骤3: 执行分析
        status_placeholder.info("🧠 AI正在深度分析数据，请耐心等待...")
        content_placeholder.markdown("**🤖 备用分析模式启动**\n\n📝 查询已准备完成\n\n🧠 AI正在深度分析您的数据...\n\n⏳ 这可能需要一些时间，请稍候...")
        
        result = agent(full_query)
        
        # 步骤4: 显示结果
        status_placeholder.info("📊 正在格式化分析结果...")
        final_content = f"**🎯 AI分析结果:**\n\n{str(result)}\n\n---\n**✅ 分析完成（备用模式）**"
        content_placeholder.markdown(final_content)
        
        return str(result)
        
    except Exception as e:
        error_msg = f"分析过程中出现错误: {str(e)}"
        status_placeholder.error(f"❌ {error_msg}")
        content_placeholder.error(f"**❌ 分析失败**\n\n{error_msg}\n\n💡 建议：\n- 检查数据文件是否存在\n- 确认网络连接正常\n- 尝试重新提问")
        return error_msg

def analyze_data_fallback_with_progress(query, data_file_name, content_placeholder, status_placeholder, progress_placeholder, time_placeholder, code_stats_placeholder, start_time):
    """带进度显示的备用分析方法"""
    try:
        # 步骤1: 加载AI引擎 (30%)
        progress_placeholder.progress(0.3)
        time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 - 加载AI引擎")
        
        content_placeholder.markdown("**🤖 备用分析模式启动**\n\n🔧 正在初始化AI分析引擎...")
        from google_ads_anlyst_agent import agent
        
        # 步骤2: 准备查询 (50%)
        progress_placeholder.progress(0.5)
        time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 - 准备查询")
        
        full_query = f"当前目录{data_file_name}的文件，{query}"
        content_placeholder.markdown("**🤖 备用分析模式启动**\n\n📝 查询已准备完成\n\n🧠 AI正在深度分析您的数据...")
        
        # 步骤3: 执行分析 (70%-90%)
        progress_placeholder.progress(0.7)
        time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 - 深度分析中")
        
        content_placeholder.markdown("**🤖 备用分析模式启动**\n\n📝 查询已准备完成\n\n🧠 AI正在深度分析您的数据...\n\n⏳ 这可能需要一些时间，请稍候...")
        
        result = agent(full_query)
        
        # 步骤4: 完成 (100%)
        progress_placeholder.progress(1.0)
        time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 - 完成")
        
        final_content = f"**🎯 AI分析结果:**\n\n{str(result)}\n\n---\n**✅ 分析完成（备用模式）**"
        content_placeholder.markdown(final_content)
        
        return str(result)
        
    except Exception as e:
        error_msg = f"分析过程中出现错误: {str(e)}"
        progress_placeholder.progress(0.0)
        time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 - 失败")
        status_placeholder.error(f"❌ {error_msg}")
        content_placeholder.error(f"**❌ 分析失败**\n\n{error_msg}\n\n💡 建议：\n- 检查数据文件是否存在\n- 确认网络连接正常\n- 尝试重新提问")
        return error_msg



def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI数据分析师演示</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📁 数据管理")
        
        # File upload
        uploaded_file = st.file_uploader(
            "上传CSV文件", 
            type=['csv'],
            help="支持CSV格式的数据文件"
        )
        
        if uploaded_file is not None:
            try:
                # Save uploaded file
                file_path = f"uploaded_{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load data
                df = pd.read_csv(file_path)
                st.session_state.data = df
                st.session_state.current_file_name = file_path
                st.success(f"✅ 文件上传成功！\n- 文件名: {uploaded_file.name}\n- 数据行数: {len(df)}\n- 列数: {len(df.columns)}")
                
            except Exception as e:
                st.error(f"文件上传失败: {str(e)}")
        
        # Load default data button
        if st.button("📊 加载示例数据"):
            df, filename = load_default_data()
            if df is not None:
                st.session_state.data = df
                st.session_state.current_file_name = filename
                st.success(f"✅ 示例数据加载成功！\n- 数据行数: {len(df)}\n- 列数: {len(df.columns)}")
        
        # Data info
        if st.session_state.data is not None:
            st.markdown("---")
            st.subheader("📋 当前数据信息")
            df = st.session_state.data
            st.write(f"**文件名:** {st.session_state.current_file_name}")
            st.write(f"**行数:** {len(df):,}")
            st.write(f"**列数:** {len(df.columns)}")
            st.write(f"**列名预览:**")
            st.write(", ".join(df.columns[:5].tolist()) + ("..." if len(df.columns) > 5 else ""))
            
            # 分析设置
            st.markdown("---")
            st.subheader("⚙️ 分析设置")
            
            # 流式输出开关
            enable_streaming = st.checkbox(
                "启用流式输出", 
                value=True, 
                help="实时显示分析过程，如果遇到问题可以关闭"
            )
            st.session_state.enable_streaming = enable_streaming
            
            # 调试模式开关
            debug_mode = st.checkbox(
                "调试模式", 
                value=False, 
                help="显示详细的调试信息"
            )
            st.session_state.debug_mode = debug_mode
            
            # 数据导出选项
            st.markdown("---")
            st.subheader("📤 数据导出")
            
            # 数据摘要下载
            csv_summary = create_csv_summary(df)
            if csv_summary:
                st.download_button(
                    label="📊 下载数据摘要",
                    data=csv_summary,
                    file_name=f"数据摘要_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # 原始数据下载
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8')
            st.download_button(
                label="📁 下载原始数据",
                data=csv_buffer.getvalue(),
                file_name=f"原始数据_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Main content
    if st.session_state.data is None:
        # Welcome screen
        st.markdown("""
        <div class="demo-card">
            <h3>👋 欢迎使用AI数据分析师演示</h3>
            <p>这是一个智能数据分析工具，可以帮助您：</p>
            <ul>
                <li>📊 自动分析数据结构和统计信息</li>
                <li>🔍 回答关于数据的各种问题</li>
                <li>📈 生成数据洞察和建议</li>
                <li>💡 提供专业的数据分析建议</li>
            </ul>
            <p><strong>开始使用：</strong>请在左侧上传CSV文件或加载示例数据</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Demo features
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 主要功能
            - **智能问答**: 用自然语言提问
            - **数据洞察**: 自动发现数据模式
            - **统计分析**: 专业的统计计算
            - **可视化建议**: 推荐合适的图表
            """)
        
        with col2:
            st.markdown("""
            ### 📝 示例问题
            - "这个数据集有多少行数据？"
            - "哪个广告系列效果最好？"
            - "不同设备的转化率如何？"
            - "数据中有缺失值吗？"
            """)
    
    else:
        # Data loaded - show analysis interface
        df = st.session_state.data
        
        # Data overview
        st.subheader("📊 数据概览")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总行数", f"{len(df):,}")
        with col2:
            st.metric("总列数", len(df.columns))
        with col3:
            # Calculate missing values
            missing_count = df.isnull().sum().sum()
            st.metric("缺失值", missing_count)
        with col4:
            # Calculate numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            st.metric("数值列", len(numeric_cols))
        
        # Sample data
        with st.expander("📋 查看数据样本", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Analysis section
        st.markdown("---")
        st.subheader("🤖 AI智能分析")
        
        # Predefined questions
        st.markdown("**💡 快速分析选项:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 数据基本统计"):
                st.session_state.selected_query = "请分析这个数据集的基本统计信息，包括数据规模、数据类型、缺失值情况等"
        
        with col2:
            if st.button("🔍 数据质量检查"):
                st.session_state.selected_query = "请检查数据质量，包括缺失值、重复值、异常值等问题"
        
        with col3:
            if st.button("📈 关键指标分析"):
                st.session_state.selected_query = "请分析数据中的关键业务指标，找出重要的数据洞察"
        
        # Custom query input
        st.markdown("**✍️ 自定义问题:**")
        user_query = st.text_area(
            "请输入您的问题:",
            placeholder="例如：帮我分析不同设备类型的转化率差异",
            height=100,
            key="user_query"
        )
        
        # Analysis button
        col1, col2 = st.columns([1, 4])
        with col1:
            analyze_button = st.button("🚀 开始分析", type="primary")
        
        # Handle analysis
        query_to_analyze = None
        if analyze_button and user_query.strip():
            query_to_analyze = user_query.strip()
        elif hasattr(st.session_state, 'selected_query'):
            query_to_analyze = st.session_state.selected_query
            delattr(st.session_state, 'selected_query')
        
        if query_to_analyze:
            st.markdown("---")
            st.subheader("📋 分析结果")
            
            # Show query
            st.markdown(f"**❓ 分析问题:** {query_to_analyze}")
            
            # 创建分析显示区域
            st.markdown("### 🔍 分析过程")
            
            # 状态栏
            st.markdown('<div class="status-row">', unsafe_allow_html=True)
            status_col1, status_col2, status_col3 = st.columns([2, 2, 2])
            
            with status_col1:
                status_placeholder = st.empty()
                status_placeholder.info("🚀 准备开始分析...")
            
            with status_col2:
                time_placeholder = st.empty()
                time_placeholder.markdown('<div class="analysis-status"><strong>⏱️ 分析时间:</strong> 准备中...</div>', unsafe_allow_html=True)
            
            with status_col3:
                code_stats_placeholder = st.empty()
                code_stats_placeholder.markdown('<div class="analysis-status"><strong>🐍 代码执行:</strong> 等待中...</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 进度条
            progress_placeholder = st.empty()
            progress_placeholder.progress(0.0)
            
            # 分析设置信息
            with st.expander("⚙️ 分析设置", expanded=False):
                setting_col1, setting_col2, setting_col3 = st.columns(3)
                with setting_col1:
                    st.write(f"**流式输出:** {'✅ 启用' if st.session_state.get('enable_streaming', True) else '❌ 禁用'}")
                with setting_col2:
                    st.write(f"**调试模式:** {'✅ 启用' if st.session_state.get('debug_mode', False) else '❌ 禁用'}")
                with setting_col3:
                    st.write(f"**数据文件:** `{st.session_state.current_file_name}`")
            
            # 主要内容显示区域
            st.markdown("### 📊 分析内容")
            content_container = st.container()
            with content_container:
                content_placeholder = st.empty()
                content_placeholder.markdown('<div class="code-execution"><strong>🚀 准备开始分析...</strong><br/>请稍候，AI正在准备分析您的数据</div>', unsafe_allow_html=True)
            
            # 分析开始时间
            start_time = datetime.now()
            
            try:
                # 显示开始状态
                status_placeholder.info("🚀 开始分析...")
                progress_placeholder.progress(0.1)
                time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒")
                
                # 根据用户设置选择分析方式
                if st.session_state.get('enable_streaming', True):
                    # 流式分析
                    progress_placeholder.progress(0.2)
                    time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 (流式模式)")
                    
                    result = analyze_data_with_agent_streaming_with_progress(
                        query_to_analyze, 
                        st.session_state.current_file_name,
                        content_placeholder,
                        status_placeholder,
                        progress_placeholder,
                        time_placeholder,
                        code_stats_placeholder,
                        start_time
                    )
                else:
                    # 非流式分析
                    progress_placeholder.progress(0.3)
                    time_placeholder.markdown(f"**⏱️ 分析时间:** {(datetime.now() - start_time).total_seconds():.1f}秒 (备用模式)")
                    
                    result = analyze_data_fallback_with_progress(
                        query_to_analyze,
                        st.session_state.current_file_name,
                        content_placeholder,
                        status_placeholder,
                        progress_placeholder,
                        time_placeholder,
                        code_stats_placeholder,
                        start_time
                    )
                
                # 计算分析时间
                end_time = datetime.now()
                analysis_duration = (end_time - start_time).total_seconds()
                
                # 显示完成状态
                progress_placeholder.progress(1.0)
                status_placeholder.success(f"✅ 分析完成！")
                time_placeholder.markdown(f"**⏱️ 总用时:** {analysis_duration:.1f}秒 ✅")
                
                # 显示分析统计
                st.markdown("---")
                
                # 紧凑的统计显示
                result_length = len(str(result)) if result else 0
                words_per_second = result_length / analysis_duration if analysis_duration > 0 else 0
                
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    st.metric("⏱️ 分析用时", f"{analysis_duration:.1f}秒")
                
                with stat_col2:
                    st.metric("🔄 分析模式", "流式" if st.session_state.get('enable_streaming', True) else "备用")
                
                with stat_col3:
                    st.metric("📝 结果长度", f"{result_length:,}字符")
                
                with stat_col4:
                    st.metric("⚡ 生成速度", f"{words_per_second:.0f}字符/秒")
                
                # 调试信息
                if st.session_state.get('debug_mode', False):
                    with st.expander("🔍 调试信息", expanded=False):
                        st.write(f"**分析统计:**")
                        st.write(f"- 开始时间: {start_time.strftime('%H:%M:%S')}")
                        st.write(f"- 结束时间: {end_time.strftime('%H:%M:%S')}")
                        st.write(f"- 分析用时: {analysis_duration:.2f}秒")
                        st.write(f"- 流式输出: {'启用' if st.session_state.get('enable_streaming', True) else '禁用'}")
                        st.write(f"- 结果长度: {len(str(result))} 字符")
                        st.write(f"- 数据文件: {st.session_state.current_file_name}")
                        
                        # 显示结果的前100个字符
                        if result:
                            st.write(f"**结果预览:**")
                            st.code(str(result)[:200] + "..." if len(str(result)) > 200 else str(result))
                
                # 分析过程时间线
                if st.session_state.get('debug_mode', False):
                    with st.expander("⏱️ 分析时间线", expanded=False):
                        timeline_data = [
                            {"步骤": "开始分析", "时间": start_time.strftime('%H:%M:%S.%f')[:-3], "状态": "✅"},
                            {"步骤": "创建AI代理", "时间": (start_time + pd.Timedelta(seconds=0.5)).strftime('%H:%M:%S.%f')[:-3], "状态": "✅"},
                            {"步骤": "准备查询", "时间": (start_time + pd.Timedelta(seconds=1.0)).strftime('%H:%M:%S.%f')[:-3], "状态": "✅"},
                            {"步骤": "执行分析", "时间": (start_time + pd.Timedelta(seconds=2.0)).strftime('%H:%M:%S.%f')[:-3], "状态": "✅"},
                            {"步骤": "完成分析", "时间": end_time.strftime('%H:%M:%S.%f')[:-3], "状态": "✅"}
                        ]
                        
                        timeline_df = pd.DataFrame(timeline_data)
                        st.dataframe(timeline_df, use_container_width=True)
                
                # Save to history
                st.session_state.analysis_history.append({
                    'timestamp': datetime.now(),
                    'query': query_to_analyze,
                    'result': result,
                    'file_name': st.session_state.current_file_name
                })
                
                # 添加下载按钮
                if result and len(result.strip()) > 0:
                    st.markdown("---")
                    st.subheader("📥 下载选项")
                    
                    col_download1, col_download2, col_download3 = st.columns(3)
                    
                    with col_download1:
                        # Markdown格式报告
                        markdown_report = create_analysis_report_text(
                            query_to_analyze, 
                            result, 
                            st.session_state.current_file_name
                        )
                        st.download_button(
                            label="📄 下载Markdown报告",
                            data=markdown_report,
                            file_name=f"分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col_download2:
                        # JSON格式报告
                        json_report = create_json_report({
                            'query': query_to_analyze,
                            'result': result,
                            'file_name': st.session_state.current_file_name
                        })
                        if json_report:
                            st.download_button(
                                label="📊 下载JSON报告",
                                data=json_report,
                                file_name=f"分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json",
                                use_container_width=True
                            )
                    
                    with col_download3:
                        # 数据摘要CSV
                        if st.session_state.data is not None:
                            csv_summary = create_csv_summary(st.session_state.data)
                            if csv_summary:
                                st.download_button(
                                    label="📈 下载数据摘要",
                                    data=csv_summary,
                                    file_name=f"数据摘要_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                    
                    # 继续分析按钮
                    if st.button("🔄 继续分析", use_container_width=True):
                        st.rerun()
                
            except Exception as e:
                status_placeholder.error(f"❌ 分析失败: {str(e)}")
        
        # Analysis history
        if st.session_state.analysis_history:
            st.markdown("---")
            st.subheader("📚 分析历史")
            
            # 历史记录操作按钮
            col_hist1, col_hist2, col_hist3 = st.columns(3)
            
            with col_hist1:
                # 导出所有历史记录
                history_export = create_history_export(st.session_state.analysis_history)
                if history_export:
                    st.download_button(
                        label="📥 导出全部历史",
                        data=history_export,
                        file_name=f"分析历史_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            with col_hist2:
                # 导出最近5条记录
                recent_history = st.session_state.analysis_history[-5:]
                recent_export = create_history_export(recent_history)
                if recent_export:
                    st.download_button(
                        label="📋 导出最近记录",
                        data=recent_export,
                        file_name=f"最近分析_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            with col_hist3:
                if st.button("🗑️ 清空历史", use_container_width=True):
                    st.session_state.analysis_history = []
                    st.success("历史记录已清空！")
                    st.rerun()
            
            # 显示历史记录
            for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):  # Show last 5
                with st.expander(f"🔍 {analysis['query'][:50]}..." if len(analysis['query']) > 50 else f"🔍 {analysis['query']}"):
                    st.write(f"**时间:** {analysis['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**文件:** {analysis['file_name']}")
                    st.write(f"**问题:** {analysis['query']}")
                    st.write(f"**结果:** {analysis['result']}")
                    
                    # 单个记录的下载按钮
                    col_single1, col_single2 = st.columns(2)
                    with col_single1:
                        single_report = create_analysis_report_text(
                            analysis['query'], 
                            analysis['result'], 
                            analysis['file_name']
                        )
                        st.download_button(
                            label="📄 下载此报告",
                            data=single_report,
                            file_name=f"单个分析_{analysis['timestamp'].strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown",
                            key=f"download_single_{i}",
                            use_container_width=True
                        )
                    
                    with col_single2:
                        single_json = create_json_report({
                            'query': analysis['query'],
                            'result': analysis['result'],
                            'file_name': analysis['file_name']
                        })
                        if single_json:
                            st.download_button(
                                label="📊 下载JSON",
                                data=single_json,
                                file_name=f"单个分析_{analysis['timestamp'].strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json",
                                key=f"download_json_{i}",
                                use_container_width=True
                            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 1rem;'>"
        "🤖 AI数据分析师演示 - 让数据分析变得简单高效"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()