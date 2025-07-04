#!/usr/bin/env python3
"""
Demo script to showcase the UI functionality
"""

import streamlit as st
import os
from PIL import Image

# Simple demo page
st.set_page_config(
    page_title="Ads Creative Agent Demo",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Ads Creative Agent - Demo")
st.markdown("---")

# Show available functionality
st.header("🚀 Available Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👕 Virtual Try-On")
    st.write("• Upload person photo")
    st.write("• Upload/download garment image")
    st.write("• Generate AI try-on results")
    st.write("• Support multiple garment types")

with col2:
    st.subheader("🖼️ Image Processing")
    st.write("• Validate image requirements")
    st.write("• Auto-resize images")
    st.write("• Format conversion")
    st.write("• Quality optimization")

with col3:
    st.subheader("🔍 Path Resolver")
    st.write("• Handle local files")
    st.write("• Download from URLs")
    st.write("• Smart file finding")
    st.write("• Format validation")

st.markdown("---")

# Show current images
st.header("📁 Current Images")

current_images = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if current_images:
    cols = st.columns(min(len(current_images), 4))
    for i, img_file in enumerate(current_images):
        with cols[i % 4]:
            try:
                image = Image.open(img_file)
                st.image(image, caption=img_file, use_column_width=True)
                
                # Image info
                file_size = os.path.getsize(img_file) / 1024  # KB
                st.caption(f"📐 {image.size[0]}x{image.size[1]} | 💾 {file_size:.1f} KB")
            except Exception as e:
                st.error(f"Error loading {img_file}: {e}")
else:
    st.info("No images found in current directory")

# Instructions
st.markdown("---")
st.header("🎯 How to Use")

st.markdown("""
### 1. Virtual Try-On
1. Select **Virtual Try-On** from the sidebar
2. Choose your source image (person photo) - use `lht.jpg` as example
3. Choose reference image (garment) - use URL or upload
4. Select garment class (UPPER_BODY, LOWER_BODY, etc.)
5. Click **Generate Virtual Try-On**

### 2. Image Processing
1. Select **Image Processing** from the sidebar
2. Upload or specify an image
3. View current image specifications
4. Process if needed to meet requirements
5. Download the processed result

### 3. Path Resolver
1. Select **Image Path Resolver** from the sidebar
2. Enter a filename or URL
3. Click **Resolve Path** to test functionality
4. View resolved path and image preview

### 🔗 Example URLs to try:
- `https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg` (Shirt)
- `https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_.jpg` (Jacket)
- `https://fakestoreapi.com/img/71YAIFU48IL._AC_UL640_QL65_ML3_.jpg` (Dress)
""")

# Footer
st.markdown("---")
st.markdown("**🎨 Ads Creative Agent** - Powered by Amazon Nova Canvas & Streamlit")

if st.button("🚀 Launch Full UI", type="primary"):
    st.info("Run `python run_ui.py` in terminal to launch the full interactive UI!")