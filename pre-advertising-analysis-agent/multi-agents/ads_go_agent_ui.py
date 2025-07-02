import streamlit as st
import sys
import os
import time
import io
from contextlib import redirect_stdout

# Import the necessary components from ads_go_agent_as_tool
from ads_go_agent_as_tool import coordinator_agent

def main():
    st.set_page_config(
        page_title="广告投前多智能体分析工具",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 广告投前多智能体分析工具")
    st.markdown("---")
    
    # 侧边栏配置
    st.sidebar.header("关于")
    st.sidebar.info(
        "这是一个使用多智能体协作的广告投前分析工具，可以帮助您对目标网站进行深度分析，"
        "为广告投放策略提供数据支持。多智能体分析提供了更全面、更深入的洞察。"
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
        start_analysis = st.button("开始多智能体分析", type="primary")
        
        # 创建结果区域的占位符
        result_placeholder = st.empty()
        
        # URL验证
        is_valid_url = False
        if website_url:
            if website_url.startswith(('http://', 'https://')):
                is_valid_url = True
            else:
                website_url = 'https://' + website_url
                is_valid_url = True
        
        if start_analysis and website_url and is_valid_url:
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
            
            if not selected_analyses:
                selected_analyses = ["产品分析", "竞品分析", "市场分析", "受众分析"]
            
            prompt += "、".join(selected_analyses) + """部分的详细分析，其余不要；

分析结果应包含量化数据指标和客观事实，竞品的品牌尽可能与此品牌产品的风格特征、细分赛道、体量规模、网站访问量、品牌知名度上均有一定程度的接近。
"""
            
            try:
                # 创建进度条和状态文本
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 创建智能体工作状态指示器
                agent_status_container = st.container()
                with agent_status_container:
                    st.subheader("智能体工作状态")
                    status_cols = st.columns(4)
                    
                    # 初始状态为等待中
                    coordinator_status = status_cols[0].empty()
                    coordinator_status.info("📊 协调者智能体: 等待中")
                    
                    product_status = status_cols[1].empty()
                    product_status.info("🔍 产品分析智能体: 等待中")
                    
                    competitor_status = status_cols[2].empty()
                    competitor_status.info("🏆 竞品分析智能体: 等待中")
                    
                    market_status = status_cols[3].empty()
                    market_status.info("📈 市场分析智能体: 等待中")
                
                # 显示详细分析进度
                progress_details = st.empty()
                
                # 模拟分析进度
                status_text.text("正在初始化多智能体协作系统...")
                progress_bar.progress(5)
                time.sleep(0.5)
                
                # 更新协调者状态
                coordinator_status.success("📊 协调者智能体: 活跃")
                progress_details.info("协调者智能体正在规划任务...")
                
                status_text.text("正在收集网站信息...")
                progress_bar.progress(15)
                time.sleep(0.7)
                
                # 更新产品分析状态
                if "产品分析" in analysis_options:
                    product_status.warning("🔍 产品分析智能体: 工作中")
                    progress_details.info("产品分析智能体正在提取产品特点和价值主张...")
                    status_text.text("产品分析智能体正在工作...")
                    progress_bar.progress(30)
                    time.sleep(0.7)
                    product_status.success("🔍 产品分析智能体: 完成")
                
                # 更新竞品分析状态
                if "竞品分析" in analysis_options:
                    competitor_status.warning("🏆 竞品分析智能体: 工作中")
                    progress_details.info("竞品分析智能体正在识别主要竞争对手和差异点...")
                    status_text.text("竞品分析智能体正在工作...")
                    progress_bar.progress(50)
                    time.sleep(0.7)
                    competitor_status.success("🏆 竞品分析智能体: 完成")
                
                # 更新市场分析状态
                if "市场分析" in analysis_options:
                    market_status.warning("📈 市场分析智能体: 工作中")
                    progress_details.info("市场分析智能体正在分析市场规模和增长趋势...")
                    status_text.text("市场分析智能体正在工作...")
                    progress_bar.progress(70)
                    time.sleep(0.7)
                    market_status.success("📈 市场分析智能体: 完成")
                
                # 更新协调者状态
                progress_details.info("协调者智能体正在整合各专业智能体的分析结果...")
                status_text.text("协调智能体正在整合分析结果...")
                progress_bar.progress(90)
                time.sleep(0.7)
                
                progress_details.success("所有智能体已完成分析任务，正在生成最终报告...")
                
                # 根据所选选项调整受众分析状态UI
                if "受众分析" in analysis_options:
                    audience_status = st.empty()
                    audience_status.warning("👥 受众分析智能体: 工作中")
                    progress_details.info("受众分析智能体正在分析目标人群特征和行为...")
                    time.sleep(0.7)
                    audience_status.success("👥 受众分析智能体: 完成")
                
                # 执行真实的分析
                try:
                    # 捕获输出
                    f = io.StringIO()
                    with redirect_stdout(f):
                        # 调用coordinator_agent函数进行分析
                        result = coordinator_agent(prompt)
                    
                    # 获取分析结果
                    output = f.getvalue()
                    if output and len(output.strip()) > 0:
                        st.session_state.result = output
                    elif hasattr(result, 'content') and result.content:
                        st.session_state.result = result.content
                    else:
                        st.session_state.result = str(result)
                except Exception as e:
                    st.error(f"调用分析函数时出错: {str(e)}")
                    st.session_state.result = f"分析过程中出现错误: {str(e)}，请稍后重试或联系管理员。"
                
                # 完成分析
                progress_bar.progress(100)
                status_text.text("分析完成！")
                time.sleep(0.5)
                
                # 清除进度显示
                progress_bar.empty()
                status_text.empty()
                
                # 显示成功消息
                st.success("🎉 分析成功完成！您可以在下方查看详细结果。")
                
                st.session_state.analysis_complete = True
                
            except Exception as e:
                # 详细的错误处理
                error_msg = str(e)
                st.error(f"分析过程中出现错误: {error_msg}")
                
                # 根据错误类型提供有用的反馈
                if "connection" in error_msg.lower():
                    st.warning("⚠️ 连接错误：请检查您的网络连接或尝试稍后重试。")
                elif "timeout" in error_msg.lower():
                    st.warning("⚠️ 请求超时：服务器响应时间过长，请稍后重试。")
                elif "api key" in error_msg.lower() or "authentication" in error_msg.lower():
                    st.warning("⚠️ 认证错误：API密钥可能无效或过期。")
                elif "url" in error_msg.lower():
                    st.warning("⚠️ URL错误：请确保输入的网址格式正确且可访问。")
                else:
                    st.warning("⚠️ 发生未知错误：请尝试重新运行分析或联系管理员。")
                    
                # 添加日志记录建议
                st.info("💡 提示：如果问题持续存在，请复制上述错误信息并联系技术支持。")
        elif not website_url and start_analysis:
            st.warning("⚠️ 请输入网站URL")
        elif website_url and not is_valid_url and start_analysis:
            st.warning("⚠️ 请输入有效的网站URL，包含 http:// 或 https://")
        
        # 显示分析结果
        if st.session_state.analysis_started:
            with result_placeholder.container():
                st.subheader("多智能体分析结果")
                
                if st.session_state.analysis_complete:
                    # 创建选项卡来分类显示结果
                    tab_titles = []
                    if "产品分析" in analysis_options:
                        tab_titles.append("产品分析")
                    if "竞品分析" in analysis_options:
                        tab_titles.append("竞品分析")  
                    if "市场分析" in analysis_options:
                        tab_titles.append("市场分析")
                    if "受众分析" in analysis_options:
                        tab_titles.append("受众分析")
                    tab_titles.append("完整报告")
                    
                    tabs = st.tabs(tab_titles)
                    
                    # 将结果解析为不同部分
                    result_content = st.session_state.result
                    
                    # 对于每个选项卡，显示相应部分的内容
                    tab_index = 0
                    if "产品分析" in analysis_options:
                        with tabs[tab_index]:
                            st.markdown("## 产品分析")
                            # 这里应该提取产品分析部分，但由于我们没有实际解析逻辑，显示完整结果
                            st.markdown(result_content)
                        tab_index += 1
                    
                    if "竞品分析" in analysis_options:
                        with tabs[tab_index]:
                            st.markdown("## 竞品分析")
                            # 这里应该提取竞品分析部分
                            st.markdown(result_content)
                        tab_index += 1
                        
                    if "市场分析" in analysis_options:
                        with tabs[tab_index]:
                            st.markdown("## 市场分析")
                            # 这里应该提取市场分析部分
                            st.markdown(result_content)
                        tab_index += 1
                        
                    if "受众分析" in analysis_options:
                        with tabs[tab_index]:
                            st.markdown("## 受众分析")
                            # 这里应该提取受众分析部分
                            st.markdown(result_content)
                        tab_index += 1
                    
                    # 完整报告选项卡
                    with tabs[-1]:
                        st.markdown("## 完整分析报告")
                        st.markdown(result_content)
                    
                    # 提供结果的下载选项
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="下载完整分析报告 (Markdown)",
                            data=result_content,
                            file_name=f"{website_url.replace('https://', '').replace('http://', '').replace('/', '_')}_多智能体分析报告.md",
                            mime="text/markdown"
                        )
                    
                    domain = website_url.replace('https://', '').replace('http://', '').split('/')[0]
                    with col2:
                        st.download_button(
                            label="下载完整分析报告 (TXT)",
                            data=result_content,
                            file_name=f"{domain}_多智能体分析报告.txt",
                            mime="text/plain"
                        )
                else:
                    st.info("多智能体分析正在进行中，请稍候...")
        else:
            with result_placeholder.container():
                st.info("点击开始分析按钮开始网站分析")
    
    with col2:
        st.subheader("多智能体分析说明")
        st.info(
            """
            **多智能体分析系统包含:**
            
            - **协调者智能体**: 统筹整个分析流程，整合各专业智能体的结果
            - **产品分析智能体**: 分析产品定位、特点、产品线、价格策略等
            - **竞品分析智能体**: 识别主要竞争对手，比较差异和优势
            - **市场分析智能体**: 分析市场规模、趋势和机会
            - **受众分析智能体**: 分析目标受众特征和行为
            
            多智能体协作分析提供更全面、更深入的洞察，帮助您制定更有效的广告投放策略。
            """
        )
        
        st.subheader("使用提示")
        st.warning(
            """
            - 请确保输入完整的网站URL，包括 http:// 或 https://
            - 多智能体分析过程可能需要较长时间，请耐心等待
            - 分析结果可以下载保存为Markdown格式
            """
        )

if __name__ == "__main__":
    main()