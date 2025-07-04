#!/usr/bin/env python3
"""
Test script to verify the UI state management fix
"""

import streamlit as st
import os
from image_handler import get_image_path

st.title("🧪 UI State Management Test")

# Initialize session state
if 'test_img_path' not in st.session_state:
    st.session_state.test_img_path = None

st.write("This test demonstrates the session state fix for image downloads.")

# Test URL input
test_url = st.text_input("Enter test URL:", 
                        value="https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg")

if st.button("Download Test Image"):
    with st.spinner("Downloading..."):
        result = get_image_path(test_url)
        if result["success"]:
            st.session_state.test_img_path = result["local_path"]
            st.success(f"Downloaded: {result['filename']}")
            st.rerun()  # Refresh to show the image
        else:
            st.error(f"Download failed: {result['error']}")
            st.session_state.test_img_path = None

# Show current state
st.write("**Current State:**")
if st.session_state.test_img_path:
    st.success(f"✅ Image path: {st.session_state.test_img_path}")
    if os.path.exists(st.session_state.test_img_path):
        from PIL import Image
        img = Image.open(st.session_state.test_img_path)
        st.image(img, caption="Downloaded Image", width=300)
    else:
        st.error("❌ File not found!")
else:
    st.warning("⚠️ No image downloaded yet")

# Test button that uses the state
if st.button("Test Process (uses session state)"):
    if st.session_state.test_img_path:
        st.success(f"✅ Would process: {os.path.basename(st.session_state.test_img_path)}")
    else:
        st.error("❌ No image to process!")

# Clear button
if st.button("Clear State"):
    st.session_state.test_img_path = None
    st.rerun()