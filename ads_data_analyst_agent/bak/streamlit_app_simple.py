import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Google Ads Data Analyst - Simple",
    page_icon="📊",
    layout="wide"
)

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

def main():
    st.title("🚀 Google Ads Data Analyst - Simple Version")
    
    # Test basic functionality
    st.write("Testing basic Streamlit functionality...")
    
    # Load data
    st.write("Loading data...")
    df = load_data()
    
    if df is not None:
        st.success(f"✅ Data loaded successfully! {len(df)} records")
        
        # Show basic info
        st.subheader("📊 Data Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Date Range", f"{(df['data_day'].max() - df['data_day'].min()).days} days")
        
        # Show sample data
        st.subheader("📋 Sample Data")
        st.dataframe(df.head())
        
        # Basic statistics
        st.subheader("📈 Basic Statistics")
        numeric_cols = ['clicks', 'impressions', 'cost', 'conversions']
        if all(col in df.columns for col in numeric_cols):
            st.dataframe(df[numeric_cols].describe())
        
    else:
        st.error("❌ Failed to load data")
    
    # Test agent import
    st.subheader("🤖 Testing Agent Import")
    try:
        st.write("Attempting to import agent...")
        from google_ads_anlyst_agent import agent, get_llm
        st.success("✅ Agent imported successfully!")
        
        # Test simple query
        if st.button("Test Simple Query"):
            try:
                with st.spinner("Testing agent..."):
                    result = agent("请简单介绍一下你的功能")
                    st.success("✅ Agent test successful!")
                    st.write("Agent response:", result)
            except Exception as e:
                st.error(f"❌ Agent test failed: {str(e)}")
                
    except Exception as e:
        st.error(f"❌ Failed to import agent: {str(e)}")

if __name__ == "__main__":
    main()