import sys
import os
import time
import io
import asyncio
import re
import boto3
from contextlib import redirect_stdout
from pathlib import Path

# Import streamlit first
import streamlit as st

# Set page configuration - THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="AI广告分析套件",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import required modules for ads analysis
from strands import Agent, tool
from strands_tools import file_read, file_write, editor
from exa_py import Exa

# Import required modules for browser automation
from dotenv import load_dotenv
load_dotenv()

# Import browser automation modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'ads_agents_demo', 'ads_analysis'))
try:
    from browser_use import Agent as BrowserAgent
    from browser_use.browser import BrowserSession
    from browser_use.controller.service import Controller
    from botocore.config import Config
    from langchain_aws import ChatBedrockConverse
    BROWSER_USE_AVAILABLE = True
except ImportError:
    BROWSER_USE_AVAILABLE = False
    # Warning moved after page config
    st.warning("Browser automation features not available. Please install browser-use dependencies.")

# # Import video analysis modules
# sys.path.append(os.path.join(os.path.dirname(__file__), 'ads_agents_demo', 'ads-videos-classify-agent'))
# try:
#     from agent import video_understand, video_classify, download_video
#     VIDEO_ANALYSIS_AVAILABLE = True
# except ImportError:
    VIDEO_ANALYSIS_AVAILABLE = False
#     # Warning moved after page config
#     st.warning("Video analysis features not available. Please check video analysis dependencies.")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .status-container {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #2196f3;
    }
    .result-container {
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        max-height: 400px;
        overflow-y: auto;
    }
    .video-container {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚀 AI广告分析套件</h1>
    <p>集成落地页分析、广告投前分析和视频分类的一站式广告分析解决方案</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# Sidebar navigation
st.sidebar.title("🎯 功能导航")
# analysis_mode = st.sidebar.selectbox(
#     "选择分析模式",
#     ["广告投前分析","落地页深度分析", "视频内容分析", "综合分析报告", "智能聊天助手"]
# )

analysis_mode = st.sidebar.selectbox(
    "选择分析模式",
    ["广告投前分析","落地页深度分析"]
)

# Environment setup check
st.sidebar.markdown("### 🔧 环境配置")
api_key_status = "✅" if os.environ.get('EXA_API_KEY') else "❌"
st.sidebar.markdown(f"EXA API Key: {api_key_status}")
# st.sidebar.markdown(f"AWS 配置: {aws_status}")

if not os.environ.get('EXA_API_KEY'):
    st.sidebar.error("请设置 EXA_API_KEY 环境变量")
# if not os.environ.get('AWS_ACCESS_KEY_ID'):
#     st.sidebar.error("请设置 AWS 凭证")

# Tool definitions for ads analysis
API_KEY = os.environ.get('EXA_API_KEY')

@tool
def exa_search(search_text) -> str:
    """Search web content using Exa API"""
    try:
        exa = Exa(api_key=API_KEY)
        result = exa.search_and_contents(
            search_text,
            text={"max_characters": 1000}
        )
        return str(result)
    except Exception as e:
        return f"搜索错误: {str(e)}"

# Helper functions
def get_bedrock_llm():
    """Get Bedrock LLM for browser automation"""
    try:
        config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
        bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1', config=config)
        return ChatBedrockConverse(
            model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
            temperature=0.0,
            max_tokens=None,
            client=bedrock_client,
        )
    except Exception as e:
        st.error(f"初始化 Bedrock LLM 失败: {e}")
        return None

def initialize_browser_agent(query: str, cdp_url: str = "http://localhost:9222"):
    """Initialize browser automation agent"""
    if not BROWSER_USE_AVAILABLE:
        return None, None
    
    try:
        llm = get_bedrock_llm()
        if not llm:
            return None, None
            
        controller = Controller()
        
        # 使用用户提供的CDP URL
        browser_session = BrowserSession(cdp_url=cdp_url)
        
        agent = BrowserAgent(
            task=query,
            llm=llm,
            controller=controller,
            browser_session=browser_session,
            use_vision=True,
            max_actions_per_step=1,
        )
        return agent, browser_session
    except Exception as e:
        st.error(f"初始化浏览器代理失败: {e}")
        return None, None

def ads_analysis_agent(prompt):
    """Execute ads analysis using Strands agent"""
    try:
        f = io.StringIO()
        with redirect_stdout(f):
            agent = Agent(
                system_prompt="你是一名资深的广告分析师，专门进行网站和市场分析",
                tools=[exa_search]
            )
            response = agent(prompt)
        
        output = f.getvalue()
        if output and len(output.strip()) > 0:
            return output
        elif hasattr(response, 'content') and response.content:
            return response.content
        else:
            return "分析正在进行中，请稍后查看结果。"
    except Exception as e:
        return f"分析过程中出现错误: {str(e)}"

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temp directory"""
    try:
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"文件保存失败: {e}")
        return None

def process_video_analysis(file_path):
    """Process video analysis using video classification agent"""
    if not VIDEO_ANALYSIS_AVAILABLE:
        return {"error": "视频分析功能不可用"}
    
    try:
        # Video understanding
        understanding = video_understand(file_path)
        
        # Video classification
        classification = video_classify(understanding)
        
        # Parse classification result
        class_id = classification.strip()
        if ":" in class_id:
            class_id, class_name = class_id.split(":", 1)
            return {
                "understanding": understanding,
                "class_id": class_id,
                "class_name": class_name
            }
        else:
            return {
                "understanding": understanding,
                "class_id": class_id,
                "class_name": "未知类别"
            }
    except Exception as e:
        return {"error": f"视频分析失败: {str(e)}"}

def is_url(text):
    """Check if text contains URL"""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return bool(url_pattern.search(text))

def extract_url(text):
    """Extract URL from text"""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    match = url_pattern.search(text)
    return match.group(0) if match else None

# Main content based on selected analysis mode
if analysis_mode == "落地页深度分析":
    st.header("📊 落地页深度分析")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("落地页分析配置")
        website_url = st.text_input(
            "请输入要分析的网站URL:", 
            "https://www.kreadoai.com/", 
            key="website_url"
        )
        
        analysis_options = st.multiselect(
            "选择分析内容:",
            ["产品分析", "竞品分析", "市场分析", "受众分析"],
            default=["产品分析", "竞品分析", "市场分析", "受众分析"],
            key="analysis_options"
        )
        
        start_analysis = st.button("🚀 开始深度分析", type="primary")
        
        if start_analysis and website_url:
            # Build analysis prompt
            prompt = f"""为 {website_url} 在Facebook ads、Google ads等广告平台上创建具有竞争力的广告；因此需要对此网站链接进行深度的投前分析，并产出报告供我全面了解产品自身、竞品、市场情况，辅助我制定最佳的投放策略；因此需要你需要对此网站链接进行"""
            
            selected_analyses = []
            if "产品分析" in analysis_options:
                selected_analyses.append("产品分析")
            if "竞品分析" in analysis_options:
                selected_analyses.append("竞品分析")
            if "市场分析" in analysis_options:
                selected_analyses.append("市场分析")
            if "受众分析" in analysis_options:
                selected_analyses.append("受众分析")
            
            prompt += "、".join(selected_analyses) + "部分的详细分析，其余不要；"
            
            prompt += """你应该保证报告中尽可能存在量化数据指标（需有客观事实的数据来源佐证）,且竞品的品牌尽可能的与此品牌产品的风格特征、细分赛道、体量规模、网站访问量、品牌知名度上均有一定程度的接近，否则将造成竞品过大或过小，对比无任何意义；并按照以下结构分析输出："""
            
            if "产品分析" in analysis_options:
                prompt += """
1.产品分析
- 产品定位和特点
- 产品线情况分析
- 价格策略研究
- 产品质量和用户评价
- 销售渠道分析
- 品牌故事和价值主张"""
            
            if "竞品分析" in analysis_options:
                prompt += """
2.竞品分析
- 找出主要竞争对手
- 竞品定位和差异对比
- 竞品价格策略比较
- 竞品营销手段和渠道分析
- 竞品市场份额和增长趋势
- SWOT分析"""
            
            if "市场分析" in analysis_options:
                prompt += """
3.市场分析
- 全球市场规模和增长趋势
- 市场细分和目标市场分析
- 市场发展的推动和阻碍因素
- 行业趋势和创新动态
- 季节性变化和地域差异
- 市场机会和挑战"""
            
            if "受众分析" in analysis_options:
                prompt += """
4.受众分析
- 目标受众的人口特征
- 消费者行为和购买决策过程
- 受众喜好和需求分析
- 社交媒体参与度及影响因素
- 用户忠诚度和复购率分析
- 受众细分和个性化营销机会"""
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔍 正在收集网站信息...")
            progress_bar.progress(20)
            time.sleep(1)
            
            status_text.text("📊 正在分析产品特点...")
            progress_bar.progress(40)
            time.sleep(1)
            
            status_text.text("🏢 正在识别竞争对手...")
            progress_bar.progress(60)
            time.sleep(1)
            
            status_text.text("📈 正在分析市场趋势...")
            progress_bar.progress(80)
            time.sleep(1)
            
            status_text.text("🎯 正在研究目标受众...")
            progress_bar.progress(90)
            
            # Execute analysis
            result = ads_analysis_agent(prompt)
            st.session_state.analysis_results['website_analysis'] = result
            
            progress_bar.progress(100)
            status_text.text("✅ 分析完成！")
            time.sleep(1)
            
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.subheader("📋 分析结果")
            st.markdown(result)
            
            # Download option
            if result:
                st.download_button(
                    label="📥 下载分析报告",
                    data=result,
                    file_name=f"{website_url.replace('https://', '').replace('http://', '').replace('/', '_')}_分析报告.md",
                    mime="text/markdown"
                )
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 分析说明</h4>
            <ul>
                <li><strong>产品分析</strong>: 深入了解产品定位、特点、产品线、价格策略等</li>
                <li><strong>竞品分析</strong>: 识别主要竞争对手，比较差异和优势</li>
                <li><strong>市场分析</strong>: 了解市场规模、趋势和机会</li>
                <li><strong>受众分析</strong>: 分析目标受众特征和行为</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>💡 使用提示</h4>
            <ul>
                <li>请确保输入完整的网站URL</li>
                <li>分析过程可能需要几分钟时间</li>
                <li>分析结果可以下载保存</li>
                <li>支持量化数据和客观事实</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif analysis_mode == "广告投前分析":
    st.header("🤖 广告投前分析")
    
    if not BROWSER_USE_AVAILABLE:
        st.error("广告投前分析功能不可用，请安装相关依赖包")
    else:
        # 创建左右布局
        left_col, right_col = st.columns([1, 1])
        
        # 左侧：任务执行区域
        with left_col:
            st.markdown("""
            <div class="feature-card">
                <h4>🎯 自动化任务执行</h4>
                <p>使用AI驱动的广告投前分析来执行复杂的落地页分析任务</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 使用表单来收集所有输入并一次性提交
            with st.form("task_form"):
                query = st.text_area(
                    "请描述您希望执行的任务:",  # 这是标签
                    height=150
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    max_steps = st.slider("最大执行步数", 5, 50, 25)
                with col2:
                    cdp_url = st.text_input("CDP URL", "http://localhost:9222", help="Chrome DevTools Protocol URL")
                
                # 表单提交按钮
                submitted = st.form_submit_button("🚀 启动自动化任务", type="primary")
            
            # 表单提交后的处理
            if submitted:
                # 设置显示浏览器查看器
                st.session_state.show_browser_viewer = True
                
                st.markdown("### 🔄 执行状态")
                execution_status = st.empty()
                execution_log = st.container()
                
                with st.spinner('正在初始化浏览器代理...'):
                    # 使用用户提供的CDP URL
                    agent, browser_session = initialize_browser_agent(query, cdp_url=cdp_url)
                    
                    if agent and browser_session:
                        async def run_browser_agent():
                            try:
                                with st.spinner('正在执行自动化任务...'):
                                    result = await agent.run(max_steps=max_steps)
                                
                                with execution_log:
                                    st.subheader("📊 执行结果")
                                    st.markdown(result.final_result())
                                    st.session_state.analysis_results['browser_automation'] = result.final_result()
                                
                                st.success('🎉 任务执行完成！')
                                
                                # Close browser button
                                if st.button('🔒 关闭浏览器'):
                                    await browser_session.close()
                                    st.info("浏览器已关闭")
                            
                            except Exception as e:
                                st.error(f"执行过程中出现错误: {str(e)}")
                        
                        # Run the async function
                        if os.name == 'nt':
                            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                        asyncio.run(run_browser_agent())
                    else:
                        st.error("无法初始化浏览器代理，请检查配置")
        
        # 右侧：CDP/VNC显示区域
        with right_col:
            st.markdown("""
            <div class="feature-card">
                <h4>🖥️ 浏览器操作实时查看</h4>
                <p>通过远程桌面查看广告投前分析操作过程</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 使用session_state来控制是否显示浏览器查看器
            if "show_browser_viewer" not in st.session_state:
                st.session_state.show_browser_viewer = False
            
            # 只有当show_browser_viewer为True时才显示iframe
            if True:
                # 添加VNC查看器iframe，设置高度为100%以填充右侧列，移除可能的蒙版和模糊效果 border: 1px solid #ddd; border-radius: 8px; overflow: hidden; 
                st.markdown("""
                <div style="height: 600px;">
                    <iframe src="http://localhost:6081/vnc.html?host=localhost&port=6081&autoconnect=true&resize=scale&quality=9&compression=0&view_only=0&password=123456&autoconnect=true" width="100%" height="100%" frameborder="0" style="background: transparent; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;"></iframe>
                </div>
                """, unsafe_allow_html=True)
            # else:
            #     # 显示占位符
            #     st.markdown("""
            #     <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden; height: 600px; display: flex; justify-content: center; align-items: center; background-color: #f8f9fa;">
            #         <div style="text-align: center;">
            #             <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#6c757d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            #                 <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            #                 <line x1="8" y1="21" x2="16" y2="21"></line>
            #                 <line x1="12" y1="17" x2="12" y2="21"></line>
            #             </svg>
            #             <p style="margin-top: 10px; color: #6c757d;">点击"启动自动化任务"按钮后显示浏览器操作</p>
            #         </div>
            #     </div>
            #     """, unsafe_allow_html=True)
            
            # 添加VNC连接说明
            with st.expander("📌 远程连接说明"):
                st.markdown("""
                - VNC查看器连接到 `localhost:6081`
                - 如果无法显示，请确保VNC服务已启动
                - 可以通过命令 `docker run -p 6081:6081 -p 5901:5901 -d --name vnc-browser dorowu/ubuntu-desktop-lxde-vnc` 启动VNC服务
                - 或者直接在新标签页打开 [http://localhost:6081/vnc.html?host=localhost&port=6081](http://localhost:6081/vnc.html?host=localhost&port=6081&password=123456&autoconnect=true)
                """)
                
                st.markdown("""
                **CDP连接说明**:
                - 确保Chrome浏览器已使用`--remote-debugging-port=9222`参数启动
                - 可以通过访问 [http://localhost:9222](http://localhost:9222) 查看可用页面
                - 如需更改CDP URL，请在左侧输入框中修改
                """)
                
                # 添加刷新按钮
                if st.button("🔄 刷新远程视图"):
                    st.rerun()

elif analysis_mode == "视频内容分析":
    st.header("🎬 视频内容分析")
    
    if not VIDEO_ANALYSIS_AVAILABLE:
        st.error("视频分析功能不可用，请检查相关依赖")
    else:
        tab1, tab2, tab3 = st.tabs(["📁 上传视频", "🔗 视频URL", "💬 智能分析"])
        
        with tab1:
            st.subheader("上传视频文件")
            uploaded_file = st.file_uploader(
                "选择视频文件", 
                type=["mp4", "mov", "avi", "mkv"],
                help="支持 MP4, MOV, AVI, MKV 格式"
            )
            
            if uploaded_file is not None:
                file_path = save_uploaded_file(uploaded_file)
                
                if file_path:
                    # Display video
                    st.video(file_path)
                    
                    if st.button("🔍 分析上传的视频", type="primary"):
                        with st.spinner("正在分析视频内容..."):
                            result = process_video_analysis(file_path)
                        
                        if "error" not in result:
                            st.subheader("📊 视频内容理解")
                            st.markdown(f"""
                            <div class="result-container">
                                {result["understanding"]}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.subheader("🏷️ 视频分类结果")
                            st.success(f"**分类ID**: {result['class_id']}")
                            if result.get('class_name'):
                                st.success(f"**分类名称**: {result['class_name']}")
                            
                            st.session_state.analysis_results['video_analysis'] = result
                        else:
                            st.error(f"分析失败: {result['error']}")
        
        with tab2:
            st.subheader("输入视频URL")
            video_url = st.text_input(
                "视频URL", 
                placeholder="https://example.com/video.mp4"
            )
            
            if video_url and st.button("🔍 分析URL视频", type="primary"):
                try:
                    with st.spinner("正在下载视频..."):
                        file_path = download_video(video_url)
                    
                    st.video(file_path)
                    
                    with st.spinner("正在分析视频内容..."):
                        result = process_video_analysis(file_path)
                    
                    if "error" not in result:
                        st.subheader("📊 视频内容理解")
                        st.markdown(f"""
                        <div class="result-container">
                            {result["understanding"]}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.subheader("🏷️ 视频分类结果")
                        st.success(f"**分类ID**: {result['class_id']}")
                        if result.get('class_name'):
                            st.success(f"**分类名称**: {result['class_name']}")
                        
                        st.session_state.analysis_results['video_analysis'] = result
                    else:
                        st.error(f"分析失败: {result['error']}")
                
                except Exception as e:
                    st.error(f"处理视频时出错: {e}")
        
        with tab3:
            st.subheader("智能视频分析对话")
            
            # Initialize chat messages for video analysis
            if "video_chat_messages" not in st.session_state:
                st.session_state.video_chat_messages = [
                    {"role": "assistant", "content": "你好！我是视频分析助手。你可以上传视频、提供视频URL或直接询问我关于视频分析的问题。"}
                ]
            
            # Display chat messages
            for message in st.session_state.video_chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if message.get("video_path"):
                        st.video(message["video_path"])
            
            # Chat input
            if prompt := st.chat_input("输入消息..."):
                st.session_state.video_chat_messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    if is_url(prompt):
                        url = extract_url(prompt)
                        st.markdown("🔍 发现视频URL，正在下载并分析...")
                        
                        try:
                            file_path = download_video(url)
                            st.video(file_path)
                            
                            result = process_video_analysis(file_path)
                            
                            if "error" not in result:
                                response = f"""
                                ✅ **视频分析完成**
                                
                                **内容理解**: {result['understanding']}
                                
                                **分类结果**: 
                                - 分类ID: {result['class_id']}
                                - 分类名称: {result.get('class_name', '未知')}
                                """
                            else:
                                response = f"❌ 分析失败: {result['error']}"
                            
                            st.markdown(response)
                            st.session_state.video_chat_messages.append({
                                "role": "assistant", 
                                "content": response, 
                                "video_path": file_path
                            })
                        
                        except Exception as e:
                            response = f"❌ 处理视频时出错: {str(e)}"
                            st.markdown(response)
                            st.session_state.video_chat_messages.append({
                                "role": "assistant", 
                                "content": response
                            })
                    else:
                        response = "我是视频分析助手，可以帮你分析视频内容并进行分类。请提供视频URL或上传视频文件。"
                        st.markdown(response)
                        st.session_state.video_chat_messages.append({
                            "role": "assistant", 
                            "content": response
                        })

elif analysis_mode == "综合分析报告":
    st.header("📈 综合分析报告")
    
    if not st.session_state.analysis_results:
        st.info("🔍 还没有分析结果。请先使用其他分析功能生成数据。")
    else:
        st.markdown("### 📊 已完成的分析")
        
        for analysis_type, result in st.session_state.analysis_results.items():
            with st.expander(f"📋 {analysis_type.replace('_', ' ').title()}", expanded=True):
                if isinstance(result, dict):
                    for key, value in result.items():
                        st.markdown(f"**{key}**: {value}")
                else:
                    st.markdown(result)
        
        # Generate comprehensive report
        if st.button("📝 生成综合报告", type="primary"):
            comprehensive_prompt = """
            基于以下分析结果，生成一份综合的广告投放策略报告：
            
            """
            
            for analysis_type, result in st.session_state.analysis_results.items():
                comprehensive_prompt += f"\n### {analysis_type}:\n{str(result)}\n"
            
            comprehensive_prompt += """
            
            请基于以上信息，提供：
            1. 综合市场洞察
            2. 广告投放建议
            3. 目标受众策略
            4. 创意内容建议
            5. 预算分配建议
            6. 效果监测指标
            """
            
            with st.spinner("正在生成综合报告..."):
                comprehensive_report = ads_analysis_agent(comprehensive_prompt)
            
            st.subheader("📋 综合分析报告")
            st.markdown(comprehensive_report)
            
            # Download comprehensive report
            st.download_button(
                label="📥 下载综合报告",
                data=comprehensive_report,
                file_name="comprehensive_ads_analysis_report.md",
                mime="text/markdown"
            )

elif analysis_mode == "智能聊天助手":
    st.header("💬 智能聊天助手")
    
    # Initialize chat messages
    if "main_chat_messages" not in st.session_state:
        st.session_state.main_chat_messages = [
            {
                "role": "assistant", 
                "content": """
                👋 你好！我是AI广告分析助手，可以帮你：
                
                🔍 **落地页分析**: 分析任何网站的产品、竞品、市场和受众
                🤖 **广告投前分析**: 执行复杂的落地页分析任务
                🎬 **视频分析**: 理解和分类视频内容
                📊 **综合报告**: 生成完整的广告投放策略
                
                请告诉我你需要什么帮助！
                """
            }
        ]
    
    # Display chat messages
    for message in st.session_state.main_chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("请输入您的问题或需求..."):
        st.session_state.main_chat_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Analyze user intent and provide appropriate response
            if any(keyword in prompt.lower() for keyword in ["网站", "分析", "竞品", "市场"]):
                response = """
                🔍 **落地页分析功能**
                
                我可以帮你进行深度的落地页分析，包括：
                - 产品分析：了解产品定位、特点、价格策略
                - 竞品分析：识别竞争对手，比较优劣势
                - 市场分析：分析市场规模、趋势和机会
                - 受众分析：研究目标用户特征和行为
                
                请切换到"落地页深度分析"模式，或直接提供网站URL让我开始分析！
                """
            elif any(keyword in prompt.lower() for keyword in ["视频", "分类", "内容"]):
                response = """
                🎬 **视频分析功能**
                
                我可以帮你分析视频内容：
                - 理解视频内容和主题
                - 将视频分类到278个预定义类别中
                - 支持上传文件或提供URL
                
                请切换到"视频内容分析"模式开始使用！
                """
            elif any(keyword in prompt.lower() for keyword in ["浏览器", "自动化", "爬取"]):
                response = """
                🤖 **广告投前分析功能**
                
                我可以使用AI驱动的广告投前分析来：
                - 自动访问和分析网站
                - 收集竞品信息
                - 执行复杂的数据收集任务
                
                请切换到"广告投前分析"模式来使用这个功能！
                """
            else:
                # Use the ads analysis agent for general questions
                response = ads_analysis_agent(f"作为广告分析专家，请回答：{prompt}")
            
            st.markdown(response)
            st.session_state.main_chat_messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    🚀 AI广告分析套件 | 使用 Amazon Nova Pro、Strands 和 EXA API 构建
</div>
""", unsafe_allow_html=True)

# Display video classification categories in sidebar
with st.sidebar.expander("🏷️ 视频分类类别"):
    st.markdown("""
    <div style="max-height: 200px; overflow-y: auto; font-size: 0.8em;">
    1:3D Printing; 2:AR/VR Glasses; 3:DIY Toys; 4:T-Shirts; 5:Professional Lighting; 
    6:Professional Equipment - Others; 7:Stockings/Socks; 8:Personal Care Tools; 
    9:Personal Care Products - Others; 10:Musical Instruments and Accessories; 
    11:Books; 12:Dairy Products; 13:Transportation - Others; 14:Parent-Child Sets; 
    15:Leisure Snacks; 16:Water/Heating Accessories; 17:Wigs; 18:Wigs/Headwear - Others; 
    19:Health Detection Equipment; 20:Fitness Equipment; 21:Hobbies and Entertainment - Others;
    ... (278 categories total)
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Create temp directory if it doesn't exist
    if not os.path.exists("temp"):
        os.makedirs("temp")
