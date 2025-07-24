import streamlit as st
import json
import time
from datetime import datetime
import pandas as pd
from ads_go_agent_as_tool import coordinator_agent, run_agent_graph
import re

# Page configuration
st.set_page_config(
    page_title="广告投放前分析系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    .analysis-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def validate_url(url):
    """Validate URL format"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def parse_analysis_result(result):
    """Parse the analysis result and extract structured information"""
    try:
        # Try to extract JSON if present
        json_match = re.search(r'\{.*\}', str(result), re.DOTALL)
        if json_match:
            json_data = json.loads(json_match.group())
            return json_data
        else:
            # If no JSON, return the text result
            return {"analysis": str(result)}
    except:
        return {"analysis": str(result)}

def display_analysis_results(results):
    """Display analysis results in a structured format"""
    if isinstance(results, dict):
        if "analysis" in results:
            st.markdown("### 📋 分析结果")
            st.markdown(f'<div class="analysis-card">{results["analysis"]}</div>', unsafe_allow_html=True)
        
        # Display other structured data if available
        for key, value in results.items():
            if key != "analysis":
                st.markdown(f"### {key}")
                if isinstance(value, (dict, list)):
                    st.json(value)
                else:
                    st.write(value)
    else:
        st.markdown("### 📋 分析结果")
        st.markdown(f'<div class="analysis-card">{str(results)}</div>', unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<h1 class="main-header">📊 广告投放前分析系统</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("## ⚙️ 配置选项")
        
        # Analysis mode selection
        analysis_mode = st.selectbox(
            "选择分析模式",
            ["协调器模式 (Coordinator)", "图模式 (Agent Graph)"],
            help="选择不同的分析执行模式"
        )
        
        # Advanced options
        with st.expander("高级选项"):
            show_raw_output = st.checkbox("显示原始输出", value=False)
            save_results = st.checkbox("保存结果到文件", value=True)
        
        st.markdown("---")
        st.markdown("### 📖 使用说明")
        st.markdown("""
        1. 输入要分析的产品URL
        2. 选择分析模式
        3. 点击开始分析
        4. 查看详细分析报告
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔗 输入产品URL")
        url_input = st.text_input(
            "请输入要分析的产品网站URL:",
            placeholder="https://example.com",
            help="输入完整的产品网站URL，系统将自动分析产品特征、竞品、市场和受众信息"
        )
        
        # URL validation
        if url_input:
            if validate_url(url_input):
                st.success("✅ URL格式正确")
            else:
                st.error("❌ 请输入有效的URL格式 (例: https://example.com)")
    
    with col2:
        st.markdown("### 📊 分析状态")
        if 'analysis_running' not in st.session_state:
            st.session_state.analysis_running = False
        
        if st.session_state.analysis_running:
            st.info("🔄 分析进行中...")
        else:
            st.info("⏳ 等待开始分析")
    
    # Analysis button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 开始分析", type="primary", use_container_width=True):
            if not url_input:
                st.error("请先输入产品URL")
            elif not validate_url(url_input):
                st.error("请输入有效的URL格式")
            else:
                st.session_state.analysis_running = True
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Start analysis
                    status_text.text("🔍 开始分析产品...")
                    progress_bar.progress(10)
                    
                    # Prepare task
                    task = f"分析一下{url_input}"
                    
                    status_text.text("🤖 启动分析代理...")
                    progress_bar.progress(30)
                    
                    # Run analysis based on selected mode
                    if analysis_mode == "协调器模式 (Coordinator)":
                        status_text.text("📊 执行协调器分析...")
                        progress_bar.progress(50)
                        result = coordinator_agent(task)
                    else:
                        status_text.text("🕸️ 执行图模式分析...")
                        progress_bar.progress(50)
                        result = run_agent_graph(task)
                    
                    progress_bar.progress(80)
                    status_text.text("📝 处理分析结果...")
                    
                    # Store results in session state
                    st.session_state.analysis_results = result
                    st.session_state.analysis_url = url_input
                    st.session_state.analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    progress_bar.progress(100)
                    status_text.text("✅ 分析完成!")
                    
                    time.sleep(1)  # Brief pause to show completion
                    
                except Exception as e:
                    st.error(f"❌ 分析过程中出现错误: {str(e)}")
                finally:
                    st.session_state.analysis_running = False
                    progress_bar.empty()
                    status_text.empty()
    
    # Display results if available
    if 'analysis_results' in st.session_state:
        st.markdown("---")
        st.markdown("## 📈 分析报告")
        
        # Analysis metadata
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><strong>分析URL</strong><br>{st.session_state.analysis_url}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><strong>分析时间</strong><br>{st.session_state.analysis_time}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><strong>分析模式</strong><br>{analysis_mode}</div>', unsafe_allow_html=True)
        
        # Display results
        parsed_results = parse_analysis_result(st.session_state.analysis_results)
        display_analysis_results(parsed_results)
        
        # Raw output option
        if show_raw_output:
            with st.expander("🔍 原始输出"):
                st.text(str(st.session_state.analysis_results))
        
        # Download results
        if save_results:
            st.markdown("### 💾 下载结果")
            col1, col2 = st.columns(2)
            
            with col1:
                # JSON download
                json_data = {
                    "url": st.session_state.analysis_url,
                    "analysis_time": st.session_state.analysis_time,
                    "mode": analysis_mode,
                    "results": parsed_results
                }
                st.download_button(
                    label="📄 下载JSON格式",
                    data=json.dumps(json_data, ensure_ascii=False, indent=2),
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with col2:
                # Text download
                text_data = f"""广告投放前分析报告
================
URL: {st.session_state.analysis_url}
分析时间: {st.session_state.analysis_time}
分析模式: {analysis_mode}

分析结果:
{str(st.session_state.analysis_results)}
"""
                st.download_button(
                    label="📝 下载文本格式",
                    data=text_data,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
        <p>🤖 广告投放前分析系统 | 基于AI多代理协作技术</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
