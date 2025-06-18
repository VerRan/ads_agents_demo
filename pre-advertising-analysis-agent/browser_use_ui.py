"""
Enhanced Browser Use UI with Remote Desktop Viewer

To use it, you'll need to install streamlit, and run with:
python -m streamlit run browser_use_ui.py

Features:
- Browser automation with AI agents
- Real-time remote desktop viewing via VNC
- Execution monitoring and logging
"""

import asyncio
import os
import sys
import time
import requests
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import streamlit.components.v1 as components

from browser_use import Agent
from browser_use.browser import BrowserSession
from browser_use.controller.service import Controller

if os.name == 'nt':
	asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import boto3
from botocore.config import Config
from langchain_aws import ChatBedrockConverse

from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession
from browser_use.controller.service import Controller
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="浏览器自动化 + 远程桌面",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .vnc-container {
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        background-color: #f9f9f9;
        margin: 10px 0;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online {
        background-color: #4CAF50;
    }
    .status-offline {
        background-color: #f44336;
    }
    .control-panel {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def check_vnc_server(host="localhost", port=6081):
    """Check if VNC server is accessible"""
    try:
        response = requests.get(f"http://{host}:{port}", timeout=3)
        return response.status_code == 200
    except:
        return False

def create_vnc_viewer(vnc_url, width=800, height=600):
    """Create VNC viewer component"""
    vnc_html = f"""
    <div class="vnc-container">
        <iframe 
            src="{vnc_url}" 
            width="{width}" 
            height="{height}"
            frameborder="0"
            scrolling="no"
            style="border-radius: 5px;">
        </iframe>
    </div>
    """
    return vnc_html

def get_llm():
	"""Initialize Bedrock LLM"""
	config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
	bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1', config=config)

	return ChatBedrockConverse(
		model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
		temperature=0.0,
		max_tokens=None,
		client=bedrock_client,
	)

def initialize_agent(query: str, provider: str, window_width=800, window_height=600):
	"""Initialize browser automation agent"""
	llm = get_llm()
	controller = Controller()
	browser_session = BrowserSession(window_size={'width': window_width, 'height': window_height})

	return Agent(
		task=query,
		llm=llm,
		controller=controller,
		browser_session=browser_session,
		use_vision=True,
		max_actions_per_step=1,
	), browser_session


# Main UI
st.markdown("""
<div class="main-header">
    <h1>🤖 浏览器自动化 + 远程桌面查看器</h1>
    <p>AI驱动的浏览器自动化，配备实时远程桌面监控</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent_running' not in st.session_state:
    st.session_state.agent_running = False
if 'browser_session' not in st.session_state:
    st.session_state.browser_session = None
if 'execution_results' not in st.session_state:
    st.session_state.execution_results = []

# Sidebar configuration
st.sidebar.header("🔧 配置选项")

# VNC Configuration
st.sidebar.subheader("🖥️ 远程桌面配置")
vnc_host = st.sidebar.text_input("VNC 主机", value="localhost")
vnc_port = st.sidebar.number_input("VNC 端口", value=6081, min_value=1000, max_value=65535)
vnc_url = f"http://{vnc_host}:{vnc_port}/vnc.html?host={vnc_host}&port={vnc_port}"

# Check VNC server status
vnc_status = check_vnc_server(vnc_host, vnc_port)
status_color = "status-online" if vnc_status else "status-offline"
status_text = "在线" if vnc_status else "离线"

st.sidebar.markdown(f"""
<div style="padding: 10px; background-color: {'#d4edda' if vnc_status else '#f8d7da'}; 
     border-radius: 5px; border: 1px solid {'#c3e6cb' if vnc_status else '#f5c6cb'};">
    <span class="status-indicator {status_color}"></span>
    VNC 服务器状态: <strong>{status_text}</strong>
</div>
""", unsafe_allow_html=True)

# Browser Configuration
st.sidebar.subheader("🌐 浏览器配置")
window_width = st.sidebar.slider("窗口宽度", 400, 1200, 800)
window_height = st.sidebar.slider("窗口高度", 300, 900, 600)
max_steps = st.sidebar.slider("最大执行步数", 5, 50, 25)

# Agent Configuration
st.sidebar.subheader("🤖 代理配置")
provider = st.sidebar.selectbox('LLM 提供商', ['Amazon Bedrock-claude-3.7'], index=0)
use_vision = st.sidebar.checkbox("启用视觉识别", value=True)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 任务配置")
    
    # Predefined tasks
    predefined_tasks = [
        "帮我给www.cupshe.com做一个完整的投前报告分析",
        "帮我查一下Amazon的股票价格",
        "搜索最新的AI技术新闻",
        "分析竞品网站的产品特点",
        "收集目标网站的联系信息"
    ]
    
    task_option = st.selectbox("选择预定义任务", ["自定义任务"] + predefined_tasks)
    
    if task_option == "自定义任务":
        query = st.text_area('输入自定义任务:', 
                           placeholder="请描述您希望浏览器执行的任务...",
                           height=100)
    else:
        query = task_option
        st.text_area('当前任务:', value=query, height=100, disabled=True)
    
    # Control buttons
    col1_1, col1_2, col1_3 = st.columns([1, 1, 1])
    
    with col1_1:
        start_button = st.button('🚀 启动代理', type="primary", disabled=st.session_state.agent_running)
    
    with col1_2:
        stop_button = st.button('⏹️ 停止执行', disabled=not st.session_state.agent_running)
    
    with col1_3:
        close_button = st.button('🔒 关闭浏览器')

with col2:
    st.subheader("🖥️ 远程桌面查看器")
    
    if vnc_status:
        # VNC viewer controls
        viewer_width = st.slider("查看器宽度", 400, 1000, 600, key="viewer_width")
        viewer_height = st.slider("查看器高度", 300, 800, 400, key="viewer_height")
        
        # Display VNC viewer
        vnc_html = create_vnc_viewer(vnc_url, viewer_width, viewer_height)
        components.html(vnc_html, height=viewer_height + 50)
        
        # VNC connection info
        st.info(f"🔗 VNC URL: {vnc_url}")
        
        # Refresh button for VNC
        if st.button("🔄 刷新远程桌面"):
            st.rerun()
    else:
        st.error(f"""
        ❌ **VNC 服务器未连接**
        
        请确保 VNC 服务器正在运行在 {vnc_host}:{vnc_port}
        
        **启动 VNC 服务器的常见方法:**
        - Docker: `docker run -d -p 6081:6081 vnc-server`
        - 本地安装: 启动 noVNC 服务
        - 远程服务器: 检查防火墙和端口转发
        """)
        
        if st.button("🔄 重新检测 VNC 服务器"):
            st.rerun()

# Execution area
st.markdown("---")
st.subheader("📊 执行监控")

# Handle button actions
if start_button and query:
    st.session_state.agent_running = True
    st.write('🔄 正在初始化代理...')
    
    try:
        agent, browser_session = initialize_agent(query, provider, window_width, window_height)
        st.session_state.browser_session = browser_session
        
        async def run_agent():
            execution_status = st.empty()
            execution_log = st.container()
            progress_bar = st.progress(0)
            
            try:
                with st.spinner('🤖 正在执行自动化任务...'):
                    execution_status.info("🚀 代理已启动，正在执行任务...")
                    
                    # Run the agent
                    result = await agent.run(max_steps=max_steps)
                    
                    progress_bar.progress(100)
                    execution_status.success("✅ 任务执行完成！")
                    
                    # Display results
                    with execution_log:
                        st.subheader("📋 执行结果")
                        result_text = result.final_result()
                        st.markdown(result_text)
                        
                        # Save to session state
                        st.session_state.execution_results.append({
                            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'task': query,
                            'result': result_text
                        })
                        
                        # Download option
                        st.download_button(
                            label="📥 下载执行结果",
                            data=result_text,
                            file_name=f"browser_automation_result_{int(time.time())}.txt",
                            mime="text/plain"
                        )
                
                st.session_state.agent_running = False
                
            except Exception as e:
                execution_status.error(f"❌ 执行过程中出现错误: {str(e)}")
                st.session_state.agent_running = False
                progress_bar.empty()
        
        # Run the async function
        asyncio.run(run_agent())
        
    except Exception as e:
        st.error(f'❌ 初始化代理失败: {str(e)}')
        st.session_state.agent_running = False

elif start_button and not query:
    st.warning("⚠️ 请输入要执行的任务")

if stop_button:
    st.session_state.agent_running = False
    st.warning("⏹️ 执行已停止")

if close_button and st.session_state.browser_session:
    async def close_browser():
        await st.session_state.browser_session.close()
    
    asyncio.run(close_browser())
    st.session_state.browser_session = None
    st.session_state.agent_running = False
    st.info("🔒 浏览器已关闭")

# Execution history
if st.session_state.execution_results:
    st.markdown("---")
    st.subheader("📚 执行历史")
    
    for i, result in enumerate(reversed(st.session_state.execution_results)):
        with st.expander(f"📋 任务 {len(st.session_state.execution_results) - i}: {result['task'][:50]}... ({result['timestamp']})"):
            st.markdown(f"**任务**: {result['task']}")
            st.markdown(f"**时间**: {result['timestamp']}")
            st.markdown("**结果**:")
            st.text(result['result'])

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    🤖 浏览器自动化工具 | 使用 Amazon Bedrock Claude 3.7 Sonnet 驱动
    <br>
    💡 提示: 确保 VNC 服务器正在运行以查看浏览器实时操作
</div>
""", unsafe_allow_html=True)
