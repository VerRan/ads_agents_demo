#!/usr/bin/env python3
"""
Streamlit UI for Ads Creative Agent
"""

import streamlit as st
import os
import sys
from PIL import Image
import base64
from io import BytesIO
import time
import logging
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_handler import get_image_path
from nova_VTO import try_on_nova
from resize_images import ImageProcessor
import re
from urllib.parse import urlparse

# Page configuration
st.set_page_config(
    page_title="Ads Creative Agent",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e8b57;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def display_image_with_info(image_path, title="Image"):
    """Display image with information."""
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption=title, use_container_width=True)
        
        # Image info
        file_size = os.path.getsize(image_path) / 1024  # KB
        st.caption(f"📁 {os.path.basename(image_path)} | 📐 {image.size[0]}x{image.size[1]} | 💾 {file_size:.1f} KB")
    else:
        st.error(f"Image not found: {image_path}")

def parse_natural_language_task(task_text):
    """Parse natural language task and extract actions."""
    task_lower = task_text.lower()
    actions = []
    
    # Extract URLs
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, task_text)
    
    # Extract file names
    file_pattern = r'\b(\w+\.(jpg|jpeg|png|gif|bmp|webp))\b'
    file_matches = re.findall(file_pattern, task_text, re.IGNORECASE)
    files = [match[0] for match in file_matches]
    
    # Determine action type
    if any(word in task_lower for word in ['试穿', 'try on', 'vto', 'virtual try-on', '换衣服', '穿上']):
        actions.append({
            'type': 'virtual_tryon',
            'description': '虚拟试穿',
            'urls': urls,
            'files': files
        })
    
    if any(word in task_lower for word in ['处理', 'process', 'resize', '调整', '压缩']):
        actions.append({
            'type': 'image_processing',
            'description': '图片处理',
            'urls': urls,
            'files': files
        })
    
    if any(word in task_lower for word in ['下载', 'download', '获取', 'get']):
        actions.append({
            'type': 'download',
            'description': '下载图片',
            'urls': urls,
            'files': files
        })
    
    # Extract garment class
    garment_class = "UPPER_BODY"  # default
    if any(word in task_lower for word in ['裤子', 'pants', 'trousers', '下装', 'lower']):
        garment_class = "LOWER_BODY"
    elif any(word in task_lower for word in ['全身', 'full body', 'dress', '连衣裙']):
        garment_class = "FULL_BODY"
    elif any(word in task_lower for word in ['配饰', 'accessories', '帽子', 'hat', '眼镜', 'glasses']):
        garment_class = "ACCESSORIES"
    
    return {
        'actions': actions,
        'garment_class': garment_class,
        'urls': urls,
        'files': files,
        'original_text': task_text
    }

def execute_natural_language_task(parsed_task):
    """Execute the parsed natural language task."""
    results = []
    
    for action in parsed_task['actions']:
        if action['type'] == 'download':
            for url in action['urls']:
                result = get_image_path(url)
                results.append({
                    'action': 'download',
                    'url': url,
                    'result': result
                })
        
        elif action['type'] == 'virtual_tryon':
            # This will be handled in the UI with session state
            results.append({
                'action': 'virtual_tryon_prepared',
                'garment_class': parsed_task['garment_class']
            })
        
        elif action['type'] == 'image_processing':
            # This will be handled in the UI
            results.append({
                'action': 'image_processing_prepared'
            })
    
    return results

def execute_task_from_input(task_input):
    """Execute task from natural language input."""
    st.subheader("🔄 任务执行")
    
    # Parse the task
    parsed_task = parse_natural_language_task(task_input)
    
    # Show parsing results
    with st.expander("📊 任务解析结果", expanded=True):
        st.write("**识别的动作:**")
        for action in parsed_task['actions']:
            st.write(f"• {action['description']} ({action['type']})")
        
        if parsed_task['urls']:
            st.write("**发现的URL:**")
            for url in parsed_task['urls']:
                st.write(f"• {url}")
        
        if parsed_task['files']:
            st.write("**发现的文件:**")
            for file in parsed_task['files']:
                st.write(f"• {file}")
        
        st.write(f"**服装类型:** {parsed_task['garment_class']}")
    
    # Execute the task
    progress_bar = st.progress(0)
    log_placeholder = st.empty()
    log_messages = []
    
    def add_log(message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_messages.append(f"[{timestamp}] {message}")
        log_placeholder.text("\n".join(log_messages[-8:]))
    
    try:
        add_log("🚀 开始执行任务...")
        progress_bar.progress(10)
        
        # Collect all available images
        all_images = []
        
        # First, handle local files (existing files)
        for file in parsed_task['files']:
            result = get_image_path(file)
            if result["success"]:
                all_images.append(result["local_path"])
                add_log(f"✅ 找到本地文件: {file}")
            else:
                add_log(f"⚠️ 本地文件未找到，将尝试从URL下载: {file}")
        
        progress_bar.progress(30)
        
        # Then, download from URLs
        for i, url in enumerate(parsed_task['urls']):
            add_log(f"📥 下载图片 {i+1}/{len(parsed_task['urls'])}: {url[:50]}...")
            result = get_image_path(url)
            if result["success"]:
                all_images.append(result["local_path"])
                add_log(f"✅ 下载成功: {result['filename']}")
            else:
                add_log(f"❌ 下载失败: {result['error']}")
        
        progress_bar.progress(60)
        
        # Show collected images
        add_log(f"📋 共收集到 {len(all_images)} 张图片")
        for i, img_path in enumerate(all_images):
            add_log(f"  {i+1}. {os.path.basename(img_path)}")
        progress_bar.progress(70)
        
        # Auto-assign images for virtual try-on
        if any(action['type'] == 'virtual_tryon' for action in parsed_task['actions']):
            if len(all_images) >= 2:
                # Smart assignment: try to identify person vs garment
                # For now, use simple logic: first image as source, second as reference
                st.session_state.src_img_path = all_images[0]
                st.session_state.ref_img_path = all_images[1]
                add_log(f"📷 设置源图片: {os.path.basename(all_images[0])}")
                add_log(f"👔 设置参考图片: {os.path.basename(all_images[1])}")
                
                # Auto-execute virtual try-on
                add_log("🎨 开始虚拟试穿...")
                result = try_on_nova(st.session_state.src_img_path, st.session_state.ref_img_path, parsed_task['garment_class'])
                
                if result.get("success"):
                    add_log("✅ 虚拟试穿完成!")
                    progress_bar.progress(100)
                    
                    # Show results
                    st.success("🎉 任务执行成功!")
                    
                    for i, filename in enumerate(result["saved_files"]):
                        if os.path.exists(filename):
                            st.markdown(f"**生成的图片 {i+1}:**")
                            display_image_with_info(filename, f"虚拟试穿结果 {i+1}")
                            
                            # Download button
                            with open(filename, "rb") as file:
                                st.download_button(
                                    label=f"📥 下载 {os.path.basename(filename)}",
                                    data=file.read(),
                                    file_name=os.path.basename(filename),
                                    mime="image/png",
                                    key=f"auto_download_{i}"
                                )
                else:
                    add_log(f"❌ 虚拟试穿失败: {result.get('error', '未知错误')}")
                    st.error("虚拟试穿失败")
            elif len(all_images) == 1:
                # Only one image available, set it and ask user to provide another
                downloaded_img = all_images[0]
                if 'lht.jpg' in downloaded_img.lower() or 'person' in downloaded_img.lower():
                    st.session_state.src_img_path = downloaded_img
                    add_log(f"📷 设置源图片: {os.path.basename(downloaded_img)}")
                    add_log("⚠️ 请提供参考图片（衣服图片）以完成虚拟试穿")
                    st.warning("已设置源图片，请在界面中添加参考图片（衣服图片）以完成虚拟试穿")
                else:
                    st.session_state.ref_img_path = downloaded_img
                    add_log(f"👔 设置参考图片: {os.path.basename(downloaded_img)}")
                    add_log("⚠️ 请提供源图片（人物照片）以完成虚拟试穿")
                    st.warning("已设置参考图片，请在界面中添加源图片（人物照片）以完成虚拟试穿")
            else:
                add_log("⚠️ 虚拟试穿需要至少1张图片")
                st.warning("虚拟试穿需要至少1张图片，请提供图片URL或文件名")
        
        # Show collected images
        if all_images and not any(action['type'] == 'virtual_tryon' for action in parsed_task['actions']):
            st.subheader("📷 收集到的图片")
            cols = st.columns(min(len(all_images), 3))
            for i, img_path in enumerate(all_images):
                with cols[i % 3]:
                    display_image_with_info(img_path, f"图片 {i+1}")
        
        progress_bar.progress(100)
        add_log("🎯 任务执行完成!")
        
        # Show final status
        if all_images:
            st.info(f"✅ 任务完成！共处理 {len(all_images)} 张图片")
        else:
            st.warning("⚠️ 未找到任何图片")
        
    except Exception as e:
        add_log(f"💥 执行出错: {str(e)}")
        st.error(f"任务执行失败: {str(e)}")
        progress_bar.progress(100)

def show_task_analysis(task_input):
    """Show task analysis without execution."""
    st.subheader("🔍 任务分析")
    
    parsed_task = parse_natural_language_task(task_input)
    
    st.json({
        "识别的动作": [action['description'] for action in parsed_task['actions']],
        "URL列表": parsed_task['urls'],
        "文件列表": parsed_task['files'],
        "服装类型": parsed_task['garment_class'],
        "原始文本": parsed_task['original_text']
    })

def show_example_tasks():
    """Show example tasks."""
    st.subheader("💡 任务示例")
    
    examples = [
        {
            "title": "🎯 虚拟试穿",
            "task": "用lht.jpg作为源图片，下载这个衣服图片并进行虚拟试穿：https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg",
            "description": "使用本地人物照片和网络衣服图片进行虚拟试穿"
        },
        {
            "title": "📥 批量下载",
            "task": "下载这些图片：https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_.jpg 和 https://fakestoreapi.com/img/71YAIFU48IL._AC_UL640_QL65_ML3_.jpg",
            "description": "从URL批量下载图片到本地"
        },
        {
            "title": "👗 连衣裙试穿",
            "task": "用lht.jpg试穿这个连衣裙：https://fakestoreapi.com/img/71YAIFU48IL._AC_UL640_QL65_ML3_.jpg",
            "description": "指定服装类型为连衣裙的虚拟试穿"
        },
        {
            "title": "🔧 图片处理",
            "task": "处理和调整这个图片的尺寸：https://example.com/large-image.jpg",
            "description": "下载并处理图片使其符合平台要求"
        }
    ]
    
    for example in examples:
        with st.expander(example["title"]):
            st.write(f"**描述:** {example['description']}")
            st.code(example["task"])
            if st.button(f"使用此示例", key=f"use_{example['title']}"):
                st.session_state.example_task = example["task"]
                st.rerun()

def main():
    # Header
    st.markdown('<div class="main-header">🎨 Ads Creative Agent</div>', unsafe_allow_html=True)
    
    # Natural Language Task Input
    st.markdown('<div class="section-header">💬 自然语言任务输入</div>', unsafe_allow_html=True)
    
    # Initialize session state for example task
    if 'example_task' not in st.session_state:
        st.session_state.example_task = ""
    
    # Task input area
    task_input = st.text_area(
        "描述你想要做的任务:",
        value=st.session_state.example_task,
        placeholder="例如：用lht.jpg作为源图片，下载这个URL的衣服图片并进行虚拟试穿：https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg",
        height=100,
        help="你可以用自然语言描述任务，支持中英文。例如：下载图片、虚拟试穿、图片处理等"
    )
    
    # Clear example task after use
    if st.session_state.example_task:
        st.session_state.example_task = ""
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🚀 执行任务", type="primary", disabled=not task_input.strip()):
            execute_task_from_input(task_input)
    
    with col2:
        if st.button("📋 解析任务", disabled=not task_input.strip()):
            show_task_analysis(task_input)
    
    with col3:
        if st.button("💡 示例任务"):
            show_example_tasks()
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Tools")
        
        # Tool selection
        tool_option = st.selectbox(
            "Choose a tool:",
            ["Virtual Try-On", "Image Processing", "Image Path Resolver"]
        )
        
        st.markdown("---")
        
        # Available images
        st.subheader("📁 Available Images")
        current_images = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        downloaded_dir = "downloaded_images"
        downloaded_images = []
        if os.path.exists(downloaded_dir):
            downloaded_images = [f for f in os.listdir(downloaded_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if current_images:
            st.write("**Current Directory:**")
            for img in current_images:
                st.write(f"• {img}")
        
        if downloaded_images:
            st.write("**Downloaded Images:**")
            for img in downloaded_images:
                st.write(f"• {img}")
    
    # Main content based on tool selection
    if tool_option == "Virtual Try-On":
        virtual_tryon_ui()
    elif tool_option == "Image Processing":
        image_processing_ui()
    elif tool_option == "Image Path Resolver":
        image_path_resolver_ui()

def virtual_tryon_ui():
    """Virtual Try-On interface."""
    st.markdown('<div class="section-header">👕 Virtual Try-On</div>', unsafe_allow_html=True)
    
    # Initialize session state for image paths
    if 'src_img_path' not in st.session_state:
        st.session_state.src_img_path = None
    if 'ref_img_path' not in st.session_state:
        st.session_state.ref_img_path = None
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Source Image (Person)")
        
        # Source image input options
        src_input_type = st.radio("Source input type:", ["Local File", "URL", "Upload"], key="src_type")
        
        if src_input_type == "Local File":
            src_img_name = st.text_input("Enter image filename:", value="lht.jpg", key="src_local")
            if src_img_name:
                result = get_image_path(src_img_name)
                if result["success"]:
                    st.session_state.src_img_path = result["local_path"]
                    display_image_with_info(st.session_state.src_img_path, "Source Image")
                else:
                    st.error(f"Error: {result['error']}")
                    st.session_state.src_img_path = None
        
        elif src_input_type == "URL":
            src_url = st.text_input("Enter image URL:", key="src_url")
            if src_url and st.button("Download Source Image", key="download_src"):
                with st.spinner("Downloading image..."):
                    result = get_image_path(src_url)
                    if result["success"]:
                        st.session_state.src_img_path = result["local_path"]
                        st.success(f"Downloaded: {result['filename']}")
                        st.rerun()  # Refresh to show the image
                    else:
                        st.error(f"Download failed: {result['error']}")
                        st.session_state.src_img_path = None
            
            # Display downloaded image if exists
            if st.session_state.src_img_path and os.path.exists(st.session_state.src_img_path):
                display_image_with_info(st.session_state.src_img_path, "Source Image")
        
        elif src_input_type == "Upload":
            uploaded_src = st.file_uploader("Upload source image", type=['png', 'jpg', 'jpeg'], key="upload_src")
            if uploaded_src:
                # Save uploaded file
                src_img_path = f"uploaded_src_{uploaded_src.name}"
                with open(src_img_path, "wb") as f:
                    f.write(uploaded_src.getbuffer())
                st.session_state.src_img_path = src_img_path
                display_image_with_info(st.session_state.src_img_path, "Source Image")
    
    with col2:
        st.subheader("👔 Reference Image (Garment)")
        
        # Reference image input options
        ref_input_type = st.radio("Reference input type:", ["Local File", "URL", "Upload"], key="ref_type")
        
        if ref_input_type == "Local File":
            ref_img_name = st.text_input("Enter image filename:", key="ref_local")
            if ref_img_name:
                result = get_image_path(ref_img_name)
                if result["success"]:
                    st.session_state.ref_img_path = result["local_path"]
                    display_image_with_info(st.session_state.ref_img_path, "Reference Image")
                else:
                    st.error(f"Error: {result['error']}")
                    st.session_state.ref_img_path = None
        
        elif ref_input_type == "URL":
            ref_url = st.text_input("Enter image URL:", 
                                  value="https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg", 
                                  key="ref_url")
            if ref_url and st.button("Download Reference Image", key="download_ref"):
                with st.spinner("Downloading image..."):
                    result = get_image_path(ref_url)
                    if result["success"]:
                        st.session_state.ref_img_path = result["local_path"]
                        st.success(f"Downloaded: {result['filename']}")
                        st.rerun()  # Refresh to show the image
                    else:
                        st.error(f"Download failed: {result['error']}")
                        st.session_state.ref_img_path = None
            
            # Display downloaded image if exists
            if st.session_state.ref_img_path and os.path.exists(st.session_state.ref_img_path):
                display_image_with_info(st.session_state.ref_img_path, "Reference Image")
        
        elif ref_input_type == "Upload":
            uploaded_ref = st.file_uploader("Upload reference image", type=['png', 'jpg', 'jpeg'], key="upload_ref")
            if uploaded_ref:
                # Save uploaded file
                ref_img_path = f"uploaded_ref_{uploaded_ref.name}"
                with open(ref_img_path, "wb") as f:
                    f.write(uploaded_ref.getbuffer())
                st.session_state.ref_img_path = ref_img_path
                display_image_with_info(st.session_state.ref_img_path, "Reference Image")
    
    # Garment class selection
    st.subheader("⚙️ Settings")
    garment_class = st.selectbox(
        "Garment Class:",
        ["UPPER_BODY", "LOWER_BODY", "FULL_BODY", "ACCESSORIES"],
        index=0
    )
    
    # Show current status
    st.subheader("📋 Current Status")
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        if st.session_state.src_img_path:
            st.success(f"✅ Source: {os.path.basename(st.session_state.src_img_path)}")
        else:
            st.warning("⚠️ No source image selected")
    with col2:
        if st.session_state.ref_img_path:
            st.success(f"✅ Reference: {os.path.basename(st.session_state.ref_img_path)}")
        else:
            st.warning("⚠️ No reference image selected")
    with col3:
        if st.button("🗑️ Clear All", help="Clear all selected images"):
            st.session_state.src_img_path = None
            st.session_state.ref_img_path = None
            st.rerun()
    
    # Virtual Try-On button
    if st.button("🎨 Generate Virtual Try-On", type="primary", use_container_width=True):
        if st.session_state.src_img_path and st.session_state.ref_img_path:
            # Create log container
            log_container = st.container()
            status_container = st.empty()
            progress_bar = st.progress(0)
            
            with log_container:
                st.subheader("📋 Processing Log")
                log_placeholder = st.empty()
                
                # Initialize log
                log_messages = []
                
                def add_log(message):
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    log_messages.append(f"[{timestamp}] {message}")
                    log_placeholder.text("\n".join(log_messages[-10:]))  # Show last 10 messages
                
                try:
                    add_log("🚀 Starting virtual try-on process...")
                    progress_bar.progress(10)
                    
                    add_log(f"📷 Source image: {os.path.basename(st.session_state.src_img_path)}")
                    add_log(f"👔 Reference image: {os.path.basename(st.session_state.ref_img_path)}")
                    add_log(f"⚙️ Garment class: {garment_class}")
                    progress_bar.progress(20)
                    
                    add_log("🔄 Preparing images for processing...")
                    progress_bar.progress(30)
                    
                    add_log("☁️ Sending request to Amazon Nova Canvas...")
                    progress_bar.progress(50)
                    
                    status_container.info("🎨 Generating virtual try-on... This may take a few moments.")
                    
                    result = try_on_nova(st.session_state.src_img_path, st.session_state.ref_img_path, garment_class)
                    progress_bar.progress(90)
                    
                    if result.get("success"):
                        add_log("✅ Virtual try-on completed successfully!")
                        add_log(f"📁 Generated {result['images_generated']} image(s)")
                        add_log(f"💾 Saved to: {result.get('output_directory', 'output')}/")
                        progress_bar.progress(100)
                        
                        status_container.success("🎉 Virtual try-on completed!")
                        
                        st.markdown('<div class="success-box">✅ Virtual try-on completed successfully!</div>', 
                                  unsafe_allow_html=True)
                        
                        # Display results
                        st.subheader("🎉 Results")
                        
                        # Show batch information
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Images Generated", result['images_generated'])
                        with col2:
                            st.metric("Timestamp", result.get('timestamp', 'Unknown'))
                        with col3:
                            st.metric("Batch ID", result.get('batch_id', 'Unknown')[:8])
                        
                        # Show generated images
                        for i, filename in enumerate(result["saved_files"]):
                            if os.path.exists(filename):
                                st.markdown(f"**Generated Image {i+1}:**")
                                display_image_with_info(filename, f"Virtual Try-On Result {i+1}")
                                
                                # Download button with original filename
                                original_filename = os.path.basename(filename)
                                with open(filename, "rb") as file:
                                    st.download_button(
                                        label=f"📥 Download {original_filename}",
                                        data=file.read(),
                                        file_name=original_filename,
                                        mime="image/png",
                                        key=f"download_{i}"
                                    )
                                
                                add_log(f"📄 Saved: {original_filename}")
                    else:
                        add_log(f"❌ Virtual try-on failed: {result.get('error', 'Unknown error')}")
                        progress_bar.progress(100)
                        status_container.error("❌ Virtual try-on failed!")
                        
                        st.markdown(f'<div class="error-box">❌ Virtual try-on failed: {result.get("error", "Unknown error")}</div>', 
                                  unsafe_allow_html=True)
                        
                except Exception as e:
                    add_log(f"💥 Exception occurred: {str(e)}")
                    progress_bar.progress(100)
                    status_container.error(f"❌ Error: {str(e)}")
                    st.error(f"Error during virtual try-on: {str(e)}")
        else:
            st.warning("Please provide both source and reference images.")

def image_processing_ui():
    """Image processing interface."""
    st.markdown('<div class="section-header">🖼️ Image Processing</div>', unsafe_allow_html=True)
    
    # Image input
    st.subheader("📤 Input Image")
    input_type = st.radio("Input type:", ["Local File", "URL", "Upload"])
    
    input_img_path = None
    if input_type == "Local File":
        img_name = st.text_input("Enter image filename:")
        if img_name:
            result = get_image_path(img_name)
            if result["success"]:
                input_img_path = result["local_path"]
                display_image_with_info(input_img_path, "Input Image")
            else:
                st.error(f"Error: {result['error']}")
    
    elif input_type == "URL":
        img_url = st.text_input("Enter image URL:")
        if img_url and st.button("Download Image"):
            with st.spinner("Downloading image..."):
                result = get_image_path(img_url)
                if result["success"]:
                    input_img_path = result["local_path"]
                    st.success(f"Downloaded: {result['filename']}")
                    display_image_with_info(input_img_path, "Input Image")
                else:
                    st.error(f"Download failed: {result['error']}")
    
    elif input_type == "Upload":
        uploaded_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            input_img_path = f"uploaded_{uploaded_file.name}"
            with open(input_img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            display_image_with_info(input_img_path, "Input Image")
    
    # Processing options
    if input_img_path:
        st.subheader("⚙️ Processing Options")
        
        processor = ImageProcessor()
        
        # Check current image status
        is_valid, errors = processor.validate_image_requirements(input_img_path)
        info = processor.get_image_info(input_img_path)
        
        # Display current image info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Resolution", f"{info['resolution_mp']:.2f} MP")
        with col2:
            st.metric("Dimensions", f"{info['width']}x{info['height']}")
        with col3:
            st.metric("Aspect Ratio", f"{info['aspect_ratio']:.2f}")
        
        # Validation status
        if is_valid:
            st.success("✅ Image meets all requirements!")
        else:
            st.warning("⚠️ Image needs processing:")
            for error in errors:
                st.write(f"• {error}")
        
        # Process button
        if st.button("🔧 Process Image", type="primary"):
            # Create log container for image processing
            log_container = st.container()
            progress_bar = st.progress(0)
            
            with log_container:
                st.subheader("📋 Processing Log")
                log_placeholder = st.empty()
                
                log_messages = []
                
                def add_log(message):
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    log_messages.append(f"[{timestamp}] {message}")
                    log_placeholder.text("\n".join(log_messages[-8:]))  # Show last 8 messages
                
                try:
                    add_log("🚀 Starting image processing...")
                    progress_bar.progress(10)
                    
                    add_log(f"📷 Input image: {os.path.basename(input_img_path)}")
                    add_log("🔍 Analyzing image requirements...")
                    progress_bar.progress(30)
                    
                    result = processor.process_image(input_img_path)
                    progress_bar.progress(80)
                    
                    if result["success"]:
                        if result["processed_info"] != result["original_info"]:
                            add_log("✅ Image processed successfully!")
                            add_log(f"📐 Original: {result['original_info']['width']}x{result['original_info']['height']}")
                            add_log(f"📐 Processed: {result['processed_info']['width']}x{result['processed_info']['height']}")
                            progress_bar.progress(100)
                            
                            st.success("✅ Image processed successfully!")
                            
                            # Show processed image
                            st.subheader("📤 Processed Image")
                            display_image_with_info(result["output_path"], "Processed Image")
                            
                            # Download button
                            with open(result["output_path"], "rb") as file:
                                st.download_button(
                                    label="📥 Download Processed Image",
                                    data=file.read(),
                                    file_name=os.path.basename(result["output_path"]),
                                    mime="image/png"
                                )
                        else:
                            add_log("ℹ️ No processing needed - image already meets requirements!")
                            progress_bar.progress(100)
                            st.info("ℹ️ No processing needed - image already meets requirements!")
                    else:
                        add_log(f"❌ Processing failed: {', '.join(result['errors'])}")
                        progress_bar.progress(100)
                        st.error(f"❌ Processing failed: {', '.join(result['errors'])}")
                        
                except Exception as e:
                    add_log(f"💥 Exception occurred: {str(e)}")
                    progress_bar.progress(100)
                    st.error(f"Error during processing: {str(e)}")

def image_path_resolver_ui():
    """Image path resolver interface."""
    st.markdown('<div class="section-header">🔍 Image Path Resolver</div>', unsafe_allow_html=True)
    
    st.write("Test the image path resolution functionality:")
    
    # Input
    image_input = st.text_input(
        "Enter image name or URL:",
        placeholder="e.g., lht.jpg or https://example.com/image.jpg"
    )
    
    if st.button("🔍 Resolve Path") and image_input:
        # Create log container for path resolution
        log_container = st.container()
        progress_bar = st.progress(0)
        
        with log_container:
            st.subheader("📋 Resolution Log")
            log_placeholder = st.empty()
            
            log_messages = []
            
            def add_log(message):
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_messages.append(f"[{timestamp}] {message}")
                log_placeholder.text("\n".join(log_messages[-6:]))  # Show last 6 messages
            
            try:
                add_log("🚀 Starting path resolution...")
                add_log(f"🔍 Input: {image_input}")
                progress_bar.progress(20)
                
                # Check if it's a URL
                from urllib.parse import urlparse
                parsed = urlparse(image_input)
                if parsed.scheme and parsed.netloc:
                    add_log("🌐 Detected URL - preparing to download...")
                else:
                    add_log("📁 Detected local filename - searching...")
                
                progress_bar.progress(50)
                
                result = get_image_path(image_input)
                progress_bar.progress(90)
                
                if result["success"]:
                    add_log("✅ Image resolved successfully!")
                    if "source" in result:
                        add_log(f"📥 Source: {result['source']}")
                    if "filename" in result:
                        add_log(f"📄 Filename: {result['filename']}")
                    progress_bar.progress(100)
                    
                    st.success("✅ Image resolved successfully!")
                    
                    # Display result info in expandable section
                    with st.expander("📊 Detailed Result Information"):
                        st.json(result)
                    
                    # Display image if available
                    if "local_path" in result:
                        st.subheader("📷 Resolved Image")
                        display_image_with_info(result["local_path"], "Resolved Image")
                else:
                    add_log(f"❌ Resolution failed: {result['error']}")
                    progress_bar.progress(100)
                    
                    st.error(f"❌ Resolution failed: {result['error']}")
                    
                    # Show available images if provided
                    if "available_images" in result:
                        st.subheader("📋 Available Images")
                        for location, files in result["available_images"].items():
                            if files:
                                st.write(f"**{location.replace('_', ' ').title()}:**")
                                for file in files:
                                    st.write(f"• {file}")
                                    
            except Exception as e:
                add_log(f"💥 Exception occurred: {str(e)}")
                progress_bar.progress(100)
                st.error(f"Error during resolution: {str(e)}")

if __name__ == "__main__":
    main()