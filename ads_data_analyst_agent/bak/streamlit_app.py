import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import os
import sys
import io
import contextlib

# Import agent components
try:
    from google_ads_anlyst_agent import agent, get_llm, filename
except Exception as e:
    st.error(f"Error importing agent: {str(e)}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Google Ads Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

def load_data():
    """Load the Google Ads data"""
    try:
        data_path = "google.campaign_daily_geo_stats.csv"
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            # Convert date columns
            df['data_day'] = pd.to_datetime(df['data_day'])
            df['fetch_time'] = pd.to_datetime(df['fetch_time'])
            return df
        else:
            st.error(f"Data file not found: {data_path}")
            return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def run_agent_analysis(query):
    """Run analysis using the Google Ads analyst agent"""
    try:
        # Add the filename context to the query
        full_query = f"当前目录{filename}的文件，{query}"
        
        # Capture stdout to get the agent's response
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            result = agent(full_query)
        
        output = f.getvalue()
        
        # Store in history
        st.session_state.analysis_history.append({
            'timestamp': datetime.now(),
            'query': query,
            'result': str(result),
            'output': output
        })
        
        return result, output
    except Exception as e:
        st.error(f"Error running analysis: {str(e)}")
        return None, str(e)

def display_data_overview(df):
    """Display data overview and basic statistics"""
    st.subheader("📋 Data Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Date Range", f"{(df['data_day'].max() - df['data_day'].min()).days} days")
    with col3:
        st.metric("Campaigns", df['campaign_name'].nunique())
    with col4:
        st.metric("Countries", df['country'].nunique())
    
    # Data sample
    st.subheader("📊 Data Sample")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Basic statistics
    st.subheader("📈 Key Metrics Summary")
    numeric_cols = ['clicks', 'impressions', 'cost', 'conversions', 'all_conversions']
    summary_stats = df[numeric_cols].describe()
    st.dataframe(summary_stats, use_container_width=True)

def create_performance_charts(df):
    """Create performance visualization charts"""
    st.subheader("📊 Performance Analytics")
    
    # Time series analysis
    daily_performance = df.groupby('data_day').agg({
        'clicks': 'sum',
        'impressions': 'sum',
        'cost': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Daily Clicks', 'Daily Impressions', 'Daily Cost', 'Daily Conversions'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Add traces
    fig.add_trace(
        go.Scatter(x=daily_performance['data_day'], y=daily_performance['clicks'],
                  name='Clicks', line=dict(color='blue')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=daily_performance['data_day'], y=daily_performance['impressions'],
                  name='Impressions', line=dict(color='green')),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=daily_performance['data_day'], y=daily_performance['cost'],
                  name='Cost', line=dict(color='red')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=daily_performance['data_day'], y=daily_performance['conversions'],
                  name='Conversions', line=dict(color='orange')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Performance Trends Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Device and Country performance
    col1, col2 = st.columns(2)
    
    with col1:
        device_performance = df.groupby('device')['clicks'].sum().reset_index()
        fig_device = px.pie(device_performance, values='clicks', names='device', 
                           title='Clicks by Device Type')
        st.plotly_chart(fig_device, use_container_width=True)
    
    with col2:
        country_performance = df.groupby('country')['clicks'].sum().reset_index()
        country_performance = country_performance.sort_values('clicks', ascending=False).head(10)
        fig_country = px.bar(country_performance, x='country', y='clicks',
                            title='Top 10 Countries by Clicks')
        st.plotly_chart(fig_country, use_container_width=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Google Ads Data Analyst</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Data loading
        if st.button("🔄 Load/Refresh Data", type="primary"):
            with st.spinner("Loading data..."):
                st.session_state.data = load_data()
                if st.session_state.data is not None:
                    st.success(f"Data loaded successfully! {len(st.session_state.data)} records")
        
        # File upload option
        st.subheader("📁 Upload Custom Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            try:
                st.session_state.data = pd.read_csv(uploaded_file)
                st.success("Custom data uploaded successfully!")
            except Exception as e:
                st.error(f"Error uploading file: {str(e)}")
        
        # Analysis options
        st.subheader("🎯 Quick Analysis")
        quick_analyses = [
            "统计文件中有多少个缺失值？",
            "分析每个设备类型的点击率和转化率",
            "找出表现最好的前10个广告系列",
            "分析不同国家的广告效果差异",
            "计算每月的广告支出趋势"
        ]
        
        selected_analysis = st.selectbox("Select quick analysis:", ["Custom"] + quick_analyses)
        
        if st.button("🚀 Run Analysis"):
            if st.session_state.data is not None:
                query = selected_analysis if selected_analysis != "Custom" else "请分析数据的基本统计信息"
                with st.spinner("Running analysis..."):
                    result, output = run_agent_analysis(query)
                    st.success("Analysis completed!")
            else:
                st.warning("Please load data first!")
    
    # Main content
    if st.session_state.data is None:
        st.info("👆 Please load data using the sidebar to get started!")
        st.session_state.data = load_data()  # Try to load default data
    
    if st.session_state.data is not None:
        df = st.session_state.data
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Analytics", "🤖 AI Analysis", "📋 History"])
        
        with tab1:
            display_data_overview(df)
        
        with tab2:
            create_performance_charts(df)
        
        with tab3:
            st.subheader("🤖 AI-Powered Analysis")
            st.write("Ask questions about your Google Ads data in natural language!")
            
            # Custom query input
            user_query = st.text_area(
                "Enter your analysis question:",
                placeholder="例如：帮我分析哪个设备类型的转化率最高？",
                height=100
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("🔍 Analyze", type="primary"):
                    if user_query.strip():
                        with st.spinner("AI is analyzing your data..."):
                            result, output = run_agent_analysis(user_query)
                            
                            if result:
                                st.success("Analysis completed!")
                                
                                # Display results
                                st.subheader("📊 Analysis Results")
                                st.write(result)
                                
                                if output:
                                    with st.expander("🔍 Detailed Output"):
                                        st.code(output)
                    else:
                        st.warning("Please enter a question!")
            
            # Display recent analysis if available
            if st.session_state.analysis_history:
                st.subheader("🕒 Recent Analysis")
                latest = st.session_state.analysis_history[-1]
                st.write(f"**Query:** {latest['query']}")
                st.write(f"**Result:** {latest['result']}")
                st.write(f"**Time:** {latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        with tab4:
            st.subheader("📋 Analysis History")
            
            if st.session_state.analysis_history:
                for i, analysis in enumerate(reversed(st.session_state.analysis_history)):
                    with st.expander(f"Analysis #{len(st.session_state.analysis_history)-i}: {analysis['query'][:50]}..."):
                        st.write(f"**Time:** {analysis['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                        st.write(f"**Query:** {analysis['query']}")
                        st.write(f"**Result:** {analysis['result']}")
                        if analysis['output']:
                            st.code(analysis['output'])
                
                if st.button("🗑️ Clear History"):
                    st.session_state.analysis_history = []
                    st.success("History cleared!")
            else:
                st.info("No analysis history yet. Run some analyses to see them here!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🚀 Google Ads Data Analyst - Powered by AI Agent & Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
