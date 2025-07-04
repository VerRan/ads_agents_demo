#!/usr/bin/env python3
"""
预算分配Agent演示Web应用
基于Streamlit的客户演示界面 - 演示模式
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime

# 演示数据
DEMO_DATA = {
    'campaigns': [
        {'id': 'camp_0296', 'budget': 24.5, 'roas': 48.9, 'purchases': 2, 'value': 1220.0},
        {'id': 'camp_5539', 'budget': 22.3, 'roas': 61.8, 'purchases': 4, 'value': 1378.1},
        {'id': 'camp_2002', 'budget': 34.6, 'roas': 34.8, 'purchases': 2, 'value': 942.4},
        {'id': 'camp_2164', 'budget': 38.0, 'roas': 31.5, 'purchases': 2, 'value': 1198.7},
        {'id': 'camp_4441', 'budget': 67.1, 'roas': 20.9, 'purchases': 3, 'value': 2136.8},
        {'id': 'camp_3525', 'budget': 104.0, 'roas': 15.25, 'purchases': 5, 'value': 1678.2},
        {'id': 'camp_3486', 'budget': 56.1, 'roas': 5.87, 'purchases': 1, 'value': 201.9},
        {'id': 'camp_6210', 'budget': 45.5, 'roas': 10.3, 'purchases': 2, 'value': 470.6},
        {'id': 'camp_0057', 'budget': 9.6, 'roas': 0.0, 'purchases': 0, 'value': 0.0},
    ]
}

# 页面配置
st.set_page_config(
    page_title="AI预算分配优化系统",
    page_icon="💰",
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'analysis_logs' not in st.session_state:
    st.session_state.analysis_logs = []



def show_header():
    """显示页面头部"""
    st.markdown('<h1 class="main-header">🤖 AI预算分配优化系统</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🎯 智能优化")
        st.write("基于AI的预算分配建议")
    with col2:
        st.markdown("### 📊 数据驱动")
        st.write("深度分析广告表现数据")
    with col3:
        st.markdown("### ⚡ 实时分析")
        st.write("快速获得专业建议")

def show_sidebar():
    """显示侧边栏"""
    st.sidebar.markdown("## 🎬 演示参数")
    
    # 分析参数设置
    daily_budget = st.sidebar.number_input(
        "日预算 ($)",
        min_value=100,
        max_value=10000,
        value=500,
        step=50,
        help="设置每日广告预算"
    )
    
    target_roas = st.sidebar.number_input(
        "目标ROAS",
        min_value=1.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
        help="设置目标投资回报率"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📊 演示说明")
    st.sidebar.info("""
    **演示模式特点:**
    - 模拟真实AI分析过程
    - 展示完整思考步骤
    - 生成专业预算建议
    - 无需API连接
    """)
    
    return daily_budget, target_roas

def show_demo_data():
    """显示演示数据"""
    st.markdown("## � 演示数据管")
    
    # 创建演示数据DataFrame
    df = pd.DataFrame(DEMO_DATA['campaigns'])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 当前广告数据")
        st.dataframe(df, use_container_width=True)
    
    with col2:
        st.markdown("### 数据概览")
        total_budget = df['budget'].sum()
        avg_roas = df['roas'].mean()
        total_purchases = df['purchases'].sum()
        total_value = df['value'].sum()
        
        st.metric("总预算", f"${total_budget:.1f}")
        st.metric("平均ROAS", f"{avg_roas:.1f}")
        st.metric("总购买数", f"{total_purchases}")
        st.metric("总价值", f"${total_value:.1f}")
        
        # 简单图表
        fig = px.bar(df, x='id', y='roas', title='各Campaign ROAS表现')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

def run_demo_analysis(daily_budget, target_roas):
    """运行演示分析（模拟实时过程）"""
    st.markdown("### 🎬 AI预算优化演示")
    
    # 清空之前的日志
    st.session_state.analysis_logs = []
    
    # 创建演示日志
    demo_logs = [
        {
            'type': 'tool_start',
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'message': '🔧 步骤 1: 读取广告数据文件...'
        },
        {
            'type': 'tool_result',
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'message': '📊 数据读取完成:\n- 共9个Campaign\n- 包含预算、ROAS、购买等关键指标'
        },
        {
            'type': 'agent_reply',
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'message': f'🤖 AI分析: 开始基于目标ROAS {target_roas} 和日预算 ${daily_budget} 进行优化分析...'
        },
        {
            'type': 'tool_start',
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'message': '🔧 步骤 2: 执行数据分析和预算优化算法...'
        },
        {
            'type': 'tool_result',
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'message': '📊 分析结果:\n- 高效Campaign: camp_5539 (ROAS: 61.8), camp_0296 (ROAS: 48.9)\n- 低效Campaign: camp_3486 (ROAS: 5.87), camp_0057 (ROAS: 0.0)'
        },
        {
            'type': 'agent_reply',
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'message': '🤖 AI分析: 基于表现数据生成预算调整建议，优化整体投资回报率...'
        }
    ]
    
    # 创建进度显示
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_display = st.empty()
    
    # 模拟实时分析过程
    for i, log_entry in enumerate(demo_logs):
        # 更新进度
        progress = (i + 1) / len(demo_logs)
        progress_bar.progress(progress)
        
        # 更新状态
        status_text.text(f"正在处理步骤 {i+1}/{len(demo_logs)}")
        
        # 添加到日志
        st.session_state.analysis_logs.append(log_entry)
        
        # 更新日志显示
        log_text = ""
        for log in st.session_state.analysis_logs:
            log_text += f"**[{log['timestamp']}]** {log['message']}\n\n"
        
        log_display.markdown(log_text)
        
        # 模拟处理时间
        time.sleep(1.2)
    
    # 完成分析
    progress_bar.progress(1.0)
    status_text.text("✅ 分析完成！")
    
    # 生成最终结果
    result_data = generate_demo_result(daily_budget, target_roas)
    st.session_state.analysis_result = result_data
    
    st.success(f"✅ 演示分析完成 (模拟耗时: 7.2秒)")
    show_analysis_results(result_data)

def generate_demo_result(daily_budget, target_roas):
    """生成演示结果"""
    # 基于演示数据生成优化建议
    campaigns = DEMO_DATA['campaigns']
    
    # 简单的预算优化逻辑
    optimized_campaigns = []
    for camp in campaigns:
        current_budget = camp['budget']
        current_roas = camp['roas']
        
        if current_roas >= target_roas:
            # 表现好的增加预算
            new_budget = min(current_budget * 1.3, daily_budget * 0.25)
            action = "增加"
            risk = "低"
        elif current_roas > 10:
            # 中等表现的微调
            new_budget = current_budget * 1.1
            action = "微增"
            risk = "中"
        elif current_roas > 0:
            # 表现差的减少预算
            new_budget = current_budget * 0.7
            action = "减少"
            risk = "高"
        else:
            # 无效的暂停
            new_budget = 0
            action = "暂停"
            risk = "高"
        
        change = new_budget - current_budget
        change_pct = (change / current_budget * 100) if current_budget > 0 else -100
        
        optimized_campaigns.append({
            'campaign_id': camp['id'],
            'current_budget': current_budget,
            'current_roas': current_roas,
            'new_budget': new_budget,
            'change': change,
            'change_pct': change_pct,
            'action': action,
            'risk': risk
        })
    
    return {
        'success': True,
        'campaigns': optimized_campaigns,
        'daily_budget': daily_budget,
        'target_roas': target_roas,
        'execution_time': 7.2
    }

def demo_section(daily_budget, target_roas):
    """演示区域"""
    col2 = st.columns(1)[0]
    
    with col2:
        if st.button("🚀 开始AI分析演示", use_container_width=True, type="primary"):
            run_demo_analysis(daily_budget, target_roas)

def show_analysis_results(result_data):
    """显示分析结果"""
    st.markdown("### 📊 AI分析结果")
    
    # 显示关键指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("分析耗时", f"{result_data['execution_time']:.1f}秒")
    with col2:
        st.metric("日预算", f"${result_data['daily_budget']}")
    with col3:
        st.metric("目标ROAS", f"{result_data['target_roas']}")
    with col4:
        total_campaigns = len(result_data['campaigns'])
        st.metric("Campaign数量", f"{total_campaigns}")
    
    # 显示预算调整表格
    st.markdown("#### 💰 预算调整建议")
    
    df = pd.DataFrame(result_data['campaigns'])
    
    # 格式化显示
    df_display = df.copy()
    df_display['当前预算'] = df_display['current_budget'].apply(lambda x: f"${x:.1f}")
    df_display['当前ROAS'] = df_display['current_roas'].apply(lambda x: f"{x:.1f}")
    df_display['调整后预算'] = df_display['new_budget'].apply(lambda x: f"${x:.1f}")
    df_display['调整金额'] = df_display['change'].apply(lambda x: f"${x:+.1f}")
    df_display['调整幅度'] = df_display['change_pct'].apply(lambda x: f"{x:+.1f}%")
    
    # 选择显示列
    display_columns = ['campaign_id', '当前预算', '当前ROAS', '调整后预算', '调整金额', '调整幅度', 'action', 'risk']
    column_names = ['Campaign ID', '当前预算', '当前ROAS', '调整后预算', '调整金额', '调整幅度', '动作', '风险等级']
    
    df_final = df_display[display_columns]
    df_final.columns = column_names
    
    st.dataframe(df_final, use_container_width=True)
    
    # 显示可视化图表
    show_demo_charts(result_data)

def show_demo_charts(result_data):
    """显示演示图表"""
    st.markdown("#### 📈 可视化分析")
    
    df = pd.DataFrame(result_data['campaigns'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ROAS对比图
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            name='当前ROAS',
            x=df['campaign_id'],
            y=df['current_roas'],
            marker_color='lightblue'
        ))
        fig1.add_hline(y=result_data['target_roas'], line_dash="dash", 
                      line_color="red", annotation_text=f"目标ROAS: {result_data['target_roas']}")
        fig1.update_layout(title='Campaign ROAS表现', xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True, key="roas_chart")
    
    with col2:
        # 预算调整图
        colors = ['green' if x > 0 else 'red' if x < 0 else 'gray' for x in df['change']]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df['campaign_id'],
            y=df['change'],
            marker_color=colors,
            name='预算调整'
        ))
        fig2.update_layout(title='预算调整金额', xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True, key="budget_change_chart")
    
    # 汇总统计
    st.markdown("#### 📋 优化汇总")
    
    increase_count = len(df[df['change'] > 0])
    decrease_count = len(df[df['change'] < 0])
    pause_count = len(df[df['new_budget'] == 0])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(f"🔺 增加预算: {increase_count} 个Campaign")
    with col2:
        st.warning(f"🔻 减少预算: {decrease_count} 个Campaign")
    with col3:
        st.error(f"⏸️ 暂停投放: {pause_count} 个Campaign")

def main():
    """主函数"""
    # 显示页面头部
    show_header()
    
    # 显示侧边栏并获取参数
    daily_budget, target_roas = show_sidebar()
    
    # 显示演示数据
    show_demo_data()
    
    # 显示演示区域
    demo_section(daily_budget, target_roas)
    
    # 如果有分析结果，显示结果
    if st.session_state.analysis_result:
        show_analysis_results(st.session_state.analysis_result)
    
    # 显示分析日志
    if st.session_state.analysis_logs:
        with st.expander("🔄 分析过程日志", expanded=False):
            for log in st.session_state.analysis_logs:
                st.markdown(f"**[{log['timestamp']}]** {log['message']}")

if __name__ == "__main__":
    main()