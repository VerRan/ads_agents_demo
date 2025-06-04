import streamlit as st
import sys
import os
import time
import io
from contextlib import redirect_stdout
from strands import tool
from exa_py import Exa
from strands import Agent, tool
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

def agent(PROMPT):
    # 创建一个StringIO对象来捕获输出
    f = io.StringIO()
    with redirect_stdout(f):
        ads_analysis_agent = Agent(
            system_prompt=(
            "你是一名资深的广告分析师"
            ),
            tools=[exa_search]
        )
        
        response = ads_analysis_agent(PROMPT)
    
    # 获取捕获的输出
    output = f.getvalue()
    
    # 如果有输出，则返回输出，否则尝试从响应中获取内容
    if output and len(output.strip()) > 0:
        return output
    elif hasattr(response, 'content') and response.content:
        return response.content
    else:
        return "# 分析报告\n\n正在生成分析结果，请稍后刷新页面查看。"

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
        result_placeholder = st.empty()
        
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
            
            try:
                # 创建进度条
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 模拟流式输出
                status_text.text("正在收集网站信息...")
                progress_bar.progress(10)
                time.sleep(1)
                
                status_text.text("正在分析产品特点...")
                progress_bar.progress(25)
                time.sleep(1)
                
                status_text.text("正在识别竞争对手...")
                progress_bar.progress(40)
                time.sleep(1)
                
                status_text.text("正在分析市场趋势...")
                progress_bar.progress(60)
                time.sleep(1)
                
                status_text.text("正在研究目标受众...")
                progress_bar.progress(80)
                time.sleep(1)
                
                status_text.text("正在生成分析报告...")
                progress_bar.progress(95)
                
                # 调用分析代理
                result = agent(prompt)
                st.session_state.result = result
                
                # 完成分析
                progress_bar.progress(100)
                status_text.text("分析完成！")
                time.sleep(1)
                
                # 清除进度显示
                progress_bar.empty()
                status_text.empty()
                
                st.session_state.analysis_complete = True
                
            except Exception as e:
                st.error(f"分析过程中出现错误: {str(e)}")
        elif not website_url and start_analysis:
            st.warning("请输入有效的网站URL")
        
        # 显示分析结果
        if st.session_state.analysis_started:
            with result_placeholder.container():
                st.subheader("分析结果")
                
                if st.session_state.analysis_complete:
                    st.markdown(st.session_state.result)
                    
                    # 提供下载选项
                    if st.session_state.result:  # 确保结果不为None
                        st.download_button(
                            label="下载分析报告",
                            data=st.session_state.result,
                            file_name=f"{website_url.replace('https://', '').replace('http://', '').replace('/', '_')}_分析报告.md",
                        mime="text/markdown"
                    )
                else:
                    st.info("分析正在进行中，请稍候...")
        else:
            with result_placeholder.container():
                st.info("点击开始分析按钮开始网站分析")
    
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
