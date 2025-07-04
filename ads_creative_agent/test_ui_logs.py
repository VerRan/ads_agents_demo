#!/usr/bin/env python3
"""
Test script to verify UI logging functionality
"""

import streamlit as st
import time
from datetime import datetime

st.title("🧪 UI Logging Test")

# Test the logging functionality
if st.button("Test Logging"):
    log_container = st.container()
    progress_bar = st.progress(0)
    
    with log_container:
        st.subheader("📋 Test Log")
        log_placeholder = st.empty()
        
        log_messages = []
        
        def add_log(message):
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_messages.append(f"[{timestamp}] {message}")
            log_placeholder.text("\n".join(log_messages[-10:]))
        
        # Simulate processing steps
        steps = [
            (10, "🚀 Starting process..."),
            (25, "📷 Loading images..."),
            (40, "🔄 Preparing data..."),
            (60, "☁️ Sending to API..."),
            (80, "🎨 Processing..."),
            (95, "💾 Saving results..."),
            (100, "✅ Complete!")
        ]
        
        for progress, message in steps:
            add_log(message)
            progress_bar.progress(progress)
            time.sleep(0.5)  # Simulate processing time
        
        st.success("Test completed!")

st.markdown("---")
st.write("This test demonstrates the logging functionality that will be shown in the main UI.")