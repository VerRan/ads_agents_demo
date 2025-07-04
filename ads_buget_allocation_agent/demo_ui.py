#!/usr/bin/env python3
"""
预算分配Agent演示UI
基于Streamlit的简单操作界面
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="AI预算分配优化系统演示",
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
        margin: 0.5rem 0;
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

def load_demo_data():
    """加载演示数据"""
    try:
        # 尝试加载实际数据文件
        if os.path.exists("2025-03-04_input.csv"):
            df = pd.read_csv("2025-03-04_input.csv")
            return df
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
            return pd.DataFrame(demo_data)
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        return None

def simulate_ai_analysis(daily_budget, target_roas, data):
    """模拟AI分析过程"""
    
    # 创建进度条和状态显示
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_container = st.container()
    
    # 模拟分析步骤
    steps = [
        ("🔍 正在读取数据文件...", 0.1),
        ("📊 分析数据结构和质量...", 0.2),
        ("🧮 计算当前ROAS表现...", 0.4),
        ("💡 生成优化策略...", 0.6),
        ("📈 计算预算调整建议...", 0.8),
        ("✅ 生成最终报告...", 1.0)
    ]
    
    with log_container:
        st.subheader("🤖 AI分析过程")
        log_text = st.empty()
        
        analysis_log = []
        
        for step_text, progress in steps:
            status_text.text(step_text)
            progress_bar.progress(progress)
            
            # 添加到日志
            timestamp = datetime.now().strftime("%H:%M:%S")
            analysis_log.append(f"[{timestamp}] {step_text}")
            log_text.text("\n".join(analysis_log))
            
            time.sleep(1)  # 模拟处理时间
    
    status_text.text("✅ 分析完成！")
    
    # 生成优化建议
    recommendations = generate_recommendations(data, daily_budget, target_roas)
    
    return recommendations

def generate_recommendations(data, daily_budget, target_roas):
    """生成预算优化建议"""
    recommendations = []
    
    for _, row in data.iterrows():
        campaign_id = row['campaign_id']
        current_budget = row['daily_budget']
        current_roas = row['roas']
        
        # 简单的优化逻辑
        if current_roas >= target_roas * 1.5:  # 高效Campaign
            new_budget = current_budget * 1.3
            action = "增加"
            risk_level = "低"
            reason = f"ROAS ({current_roas:.1f}) 远超目标，建议增加投入"
        elif current_roas >= target_roas:  # 达标Campaign
            new_budget = current_budget * 1.1
            action = "小幅增加"
            risk_level = "低"
            reason = f"ROAS ({current_roas:.1f}) 达标，适度增加投入"
        elif current_roas >= target_roas * 0.5:  # 中等表现
            new_budget = current_budget * 0.9
            action = "小幅减少"
            risk_level = "中"
            reason = f"ROAS ({current_roas:.1f}) 低于目标，适度减少投入"
        elif current_roas > 0:  # 低效但有转化
            new_budget = current_budget * 0.7
            action = "大幅减少"
            risk_level = "高"
            reason = f"ROAS ({current_roas:.1f}) 过低，大幅减少投入"
        else:  # 无效Campaign
            new_budget = 0
            action = "暂停"
            risk_level = "高"
            reason = "无转化数据，建议暂停投放"
        
        adjustment_amount = new_budget - current_budget
        adjustment_percentage = (adjustment_amount / current_budget * 100) if current_budget > 0 else 0
        
        recommendations.append({
            'campaign_id': campaign_id,
            'current_budget': current_budget,
            'current_roas': current_roas,
            'new_budget': new_budget,
            'adjustment_amount': adjustment_amount,
            'adjustment_percentage': adjustment_percentage,
            'action_type': action,
            'reason': reason,
            'risk_level': risk_level
        })
    
    return recommendations

def display_recommendations(recommendations):
    """显示优化建议"""
    st.subheader("💰 预算优化建议")
    
    # 转换为DataFrame便于显示
    df_rec = pd.DataFrame(recommendations)
    
    # 汇总统计
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_current = df_rec['current_budget'].sum()
        st.metric("当前总预算", f"${total_current:.1f}")
    
    with col2:
        total_new = df_rec['new_budget'].sum()
        st.metric("建议总预算", f"${total_new:.1f}")
    
    with col3:
        total_change = total_new - total_current
        st.metric("预算变化", f"${total_change:.1f}")
    
    with col4:
        avg_roas = df_rec['current_roas'].mean()
        st.metric("平均ROAS", f"{avg_roas:.1f}")
    
    # 详细建议表格
    st.subheader("📋 详细调整建议")
    
    # 格式化显示
    display_df = df_rec.copy()
    display_df['current_budget'] = display_df['current_budget'].apply(lambda x: f"${x:.1f}")
    display_df['new_budget'] = display_df['new_budget'].apply(lambda x: f"${x:.1f}")
    display_df['adjustment_amount'] = display_df['adjustment_amount'].apply(lambda x: f"${x:.1f}")
    display_df['adjustment_percentage'] = display_df['adjustment_percentage'].apply(lambda x: f"{x:.1f}%")
    display_df['current_roas'] = display_df['current_roas'].apply(lambda x: f"{x:.1f}")
    
    # 重命名列
    display_df = display_df.rename(columns={
        'campaign_id': 'Campaign ID',
        'current_budget': '当前预算',
        'current_roas': '当前ROAS',
        'new_budget': '建议预算',
        'adjustment_amount': '调整金额',
        'adjustment_percentage': '调整幅度',
        'action_type': '动作类型',
        'reason': '调整原因',
        'risk_level': '风险等级'
    })
    
    st.dataframe(display_df, use_container_width=True)
    
    # 可视化图表
    create_charts(df_rec)

def create_charts(df_rec):
    """创建可视化图表"""
    st.subheader("📊 可视化分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ROAS表现图
        fig_roas = px.bar(
            df_rec, 
            x='campaign_id', 
            y='current_roas',
            title='各Campaign ROAS表现',
            labels={'current_roas': 'ROAS', 'campaign_id': 'Campaign ID'}
        )
        fig_roas.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_roas, use_container_width=True)
    
    with col2:
        # 预算调整图
        fig_budget = px.bar(
            df_rec, 
            x='campaign_id', 
            y='adjustment_amount',
            title='预算调整金额',
            labels={'adjustment_amount': '调整金额 ($)', 'campaign_id': 'Campaign ID'},
            color='adjustment_amount',
            color_continuous_scale='RdYlGn'
        )
        fig_budget.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_budget, use_container_width=True)

def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-header">💰 AI预算分配优化系统演示</h1>', unsafe_allow_html=True)
    
    # 侧边栏参数设置
    st.sidebar.header("🎛️ 参数设置")
    
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
    
    # 加载数据
    data = load_demo_data()
    
    if data is not None:
        # 显示当前数据概览
        st.subheader("📊 当前Campaign数据")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Campaign数量", len(data))
        with col2:
            st.metric("总预算", f"${data['daily_budget'].sum():.1f}")
        with col3:
            st.metric("平均ROAS", f"{data['roas'].mean():.1f}")
        
        # 显示数据表格
        st.dataframe(data, use_container_width=True)
        
        # 分析按钮
        if st.button("🚀 开始AI预算优化分析", type="primary"):
            st.markdown('<div class="success-box">正在启动AI分析引擎...</div>', unsafe_allow_html=True)
            
            # 执行分析
            recommendations = simulate_ai_analysis(daily_budget, target_roas, data)
            
            # 显示结果
            display_recommendations(recommendations)
            
            # 下载建议
            if st.button("📥 下载优化建议"):
                csv = pd.DataFrame(recommendations).to_csv(index=False)
                st.download_button(
                    label="下载CSV文件",
                    data=csv,
                    file_name=f"budget_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    else:
        st.error("无法加载数据，请检查数据文件是否存在")
    
    # 页面底部信息
    st.markdown("---")
    st.markdown("""
    ### 💡 使用说明
    1. **调整参数**: 在左侧设置日预算和目标ROAS
    2. **查看数据**: 检查当前Campaign的表现数据
    3. **开始分析**: 点击分析按钮启动AI优化
    4. **查看建议**: 获得详细的预算调整建议和可视化图表
    5. **下载结果**: 将优化建议导出为CSV文件
    
    ### 🎯 系统特点
    - 🤖 **AI驱动**: 基于机器学习的智能预算优化
    - 📊 **数据可视化**: 直观的图表展示分析结果
    - 💰 **ROI优化**: 专注于提升广告投资回报率
    - 🔄 **实时分析**: 快速响应参数调整
    """)

if __name__ == "__main__":
    main()