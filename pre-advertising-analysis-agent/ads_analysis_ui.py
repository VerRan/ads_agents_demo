import streamlit as st
import sys
import os
from strands import Agent, tool
from exa_py import Exa
from strands_tools import file_read, file_write, editor

API_KEY = "00a01fd0-0483-4bba-91b6-1a719838238a"
@tool
def exa_search(search_text) -> str:
    exa = Exa(api_key = API_KEY)
    result = exa.search_and_contents(
        search_text,
        text = { "max_characters": 1000 }
    )
    return str(result)


def create_streaming_agent(content_placeholder, status_placeholder):
    """创建支持流式输出的代理"""
    
    def streaming_callback(**kwargs):
        try:
            if "data" in kwargs:
                # 实时更新内容
                if hasattr(streaming_callback, 'content'):
                    streaming_callback.content += kwargs["data"]
                else:
                    streaming_callback.content = kwargs["data"]
                
                # 更新显示
                with content_placeholder.container():
                    st.markdown(streaming_callback.content)
            
            elif "current_tool_use" in kwargs:
                current_tool_use = kwargs["current_tool_use"]
                
                # 检查 current_tool_use 是否是字典类型
                if isinstance(current_tool_use, dict) and current_tool_use.get("name"):
                    tool_name = current_tool_use["name"]
                    tool_args = current_tool_use.get("input", {})
                    
                    # 生成工具使用的唯一标识
                    tool_id = f"{tool_name}_{str(tool_args)}"
                    
                    # 检查是否已经显示过这个工具使用
                    if not hasattr(streaming_callback, 'shown_tools'):
                        streaming_callback.shown_tools = set()
                    
                    if tool_id not in streaming_callback.shown_tools:
                        streaming_callback.shown_tools.add(tool_id)
                        
                        # 只在状态栏显示工具使用状态，不添加到内容中
                        if tool_name == "exa_search":
                            search_query = tool_args.get("search_text", "") if isinstance(tool_args, dict) else ""
                            status_text = f"� 正在在搜索: {search_query[:50]}..."
                        else:
                            status_text = f"⚙️ 正在使用工具: {tool_name}"
                        
                        # 使用带有旋转图标的状态显示
                        status_placeholder.info(f"⏳ {status_text}")
                    
                elif isinstance(current_tool_use, str):
                    # 如果是字符串，检查是否已经显示过
                    if not hasattr(streaming_callback, 'shown_tools'):
                        streaming_callback.shown_tools = set()
                    
                    if current_tool_use not in streaming_callback.shown_tools:
                        streaming_callback.shown_tools.add(current_tool_use)
                        
                        status_text = f"⚙️ 正在使用工具: {current_tool_use}"
                        status_placeholder.info(f"⏳ {status_text}")
                    
        except Exception as e:
            # 如果回调函数出错，记录但不中断主流程
            st.error(f"流式输出回调错误: {str(e)}")
            print(f"Callback error: {e}, kwargs: {kwargs}")
    
    # 初始化内容和工具跟踪
    streaming_callback.content = ""
    streaming_callback.shown_tools = set()
    
    return Agent(
        system_prompt="你是一名资深的广告分析师，专门进行广告投放前的深度分析。请提供详细、专业的分析报告。",
        tools=[exa_search],
        callback_handler=streaming_callback
    ), streaming_callback

def main():
    st.set_page_config(
        page_title="广告投前站点分析工具",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 广告投前站点分析工具")
    st.markdown("---")
    
    # 侧边栏配置
    st.sidebar.header("关于")
    st.sidebar.info(
        "这是一个广告投前站点分析工具，可以帮助您对目标网站进行深度分析，"
        "为广告投放策略提供数据支持。"
    )
    
    # 初始化会话状态
    if 'analysis_started' not in st.session_state:
        st.session_state.analysis_started = False
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'result' not in st.session_state:
        st.session_state.result = ""
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("网站分析")
        website_url = st.text_input("请输入要分析的网站URL:", "https://www.kreadoai.com/", key="website_url")
        
        analysis_options = st.multiselect(
            "选择分析内容:",
            ["产品分析", "竞品分析", "市场分析", "受众分析"],
            default=["产品分析", "竞品分析", "市场分析", "受众分析"],
            key="analysis_options"
        )
        
        # 创建分析按钮
        start_analysis = st.button("开始分析", type="primary")
        
        # 创建结果区域的占位符
        status_placeholder = st.empty()
        content_placeholder = st.empty()
        
        if start_analysis and website_url:
            st.session_state.analysis_started = True
            st.session_state.analysis_complete = False
            st.session_state.result = ""
            
            # 构建分析提示词
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

## 1. 产品分析
- 产品定位和特点
- 产品线情况分析
- 价格策略研究
- 产品质量和用户评价
- 销售渠道分析
- 品牌故事和价值主张"""
            
            if "竞品分析" in analysis_options:
                prompt += """

## 2. 竞品分析
- 找出主要竞争对手
- 竞品定位和差异对比
- 竞品价格策略比较
- 竞品营销手段和渠道分析
- 竞品市场份额和增长趋势
- SWOT分析"""
            
            if "市场分析" in analysis_options:
                prompt += """

## 3. 市场分析
- 全球市场规模和增长趋势
- 市场细分和目标市场分析
- 市场发展的推动和阻碍因素
- 行业趋势和创新动态
- 季节性变化和地域差异
- 市场机会和挑战"""
            
            if "受众分析" in analysis_options:
                prompt += """

## 4. 受众分析
- 目标受众的人口特征
- 消费者行为和购买决策过程
- 受众喜好和需求分析
- 社交媒体参与度及影响因素
- 用户忠诚度和复购率分析
- 受众细分和个性化营销机会"""
            
            try:
                # 显示开始状态
                status_placeholder.info("🚀 开始分析，请稍候...")
                
                # 创建流式代理
                streaming_agent, callback = create_streaming_agent(content_placeholder, status_placeholder)
                
                # 执行分析（流式输出）
                response = streaming_agent(prompt)
                
                # 保存最终结果
                st.session_state.result = callback.content
                st.session_state.analysis_complete = True
                
                # 显示完成状态
                status_placeholder.success("✅ 分析完成！")
                
            except Exception as e:
                status_placeholder.error(f"❌ 分析过程中出现错误: {str(e)}")
                st.error(f"详细错误信息: {str(e)}")
        elif not website_url and start_analysis:
            st.warning("请输入有效的网站URL")
        
        # 显示下载按钮（如果分析完成）
        if st.session_state.analysis_complete and st.session_state.result:
            st.markdown("---")
            col_download1, col_download2 = st.columns([1, 1])
            with col_download1:
                st.download_button(
                    label="📥 下载分析报告 (Markdown)",
                    data=st.session_state.result,
                    file_name=f"{website_url.replace('https://', '').replace('http://', '').replace('/', '_')}_分析报告.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col_download2:
                # 重新分析按钮
                if st.button("🔄 重新分析", use_container_width=True):
                    st.session_state.analysis_started = False
                    st.session_state.analysis_complete = False
                    st.session_state.result = ""
                    st.rerun()
        
        # 如果还没开始分析，显示提示
        if not st.session_state.analysis_started:
            st.info("👆 点击开始分析按钮开始网站分析")
    
    with col2:
        st.subheader("分析说明")
        st.info(
            """
            **分析内容说明:**
            
            - **产品分析**: 深入了解产品定位、特点、产品线、价格策略等
            - **竞品分析**: 识别主要竞争对手，比较差异和优势
            - **市场分析**: 了解市场规模、趋势和机会
            - **受众分析**: 分析目标受众特征和行为
            
            分析结果将包含量化数据和客观事实，帮助您制定更有效的广告投放策略。
            """
        )
        
        st.subheader("使用提示")
        st.warning(
            """
            - 请确保输入完整的网站URL，包括 http:// 或 https://
            - 分析过程可能需要几分钟时间，请耐心等待
            - 分析结果可以下载保存为Markdown格式
            """
        )

if __name__ == "__main__":
    main()
