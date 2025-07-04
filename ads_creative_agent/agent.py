from strands import tool
from exa_py import Exa
from strands import Agent, tool
from strands_tools import file_read, file_write, editor, http_request,generate_image,python_repl
from strands.handlers.callback_handler import PrintingCallbackHandler

import json
import boto3
import os
import sys
import ffmpeg
import argparse
import requests
import uuid
from urllib.parse import urlparse
from resize_images import ImageProcessor 
from image_handler import ImageHandler
from nova_VTO import try_on_nova
from image_handler import get_image_path
import logging


os.environ['DEV'] = 'true'

# def task_to_code(task):
# Enables Strands debug log level
logging.getLogger("strands").setLevel(logging.DEBUG)
# Sets the logging format and streams logs to stderr
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

@tool
def get_image_local_path(image_input):
    """
    Get local path for an image. Can handle both local filenames and URLs.
    
    Args:
        image_input: Image filename or URL
        
    Returns:
        dict: Result with local_path or error information
    """
    return get_image_path(image_input)

@tool
def vto_nova(src_img, ref_img, garmentClass="UPPER_BODY"):
    """
    Use this tool to try on nova VTO (Virtual Try-On).
    
    Args:
        src_img: Path to source image (person photo) or URL
        ref_img: Path to reference image (garment) or URL
        garmentClass: Type of garment (default: UPPER_BODY)
    
    Returns:
        Response from VTO processing
    """
    try:
        # Get local paths for both images
        src_result = get_image_path(src_img)
        if not src_result["success"]:
            return f"Error with source image: {src_result['error']}"
        
        ref_result = get_image_path(ref_img)
        if not ref_result["success"]:
            return f"Error with reference image: {ref_result['error']}"
        
        # Use local paths for VTO
        response = try_on_nova(src_result["local_path"], ref_result["local_path"], garmentClass)
        return response
    except Exception as e:
        return f"Error in VTO processing: {str(e)}"
            # "1. you can create images with generate_image "
            # "2. you can create new ads images with source image and ref image for example ,you can create a new image with my photo and a t-shit image, le me try on it  "



def agent(task):
    SYS_PROMPT = """
    You are an Ads Creative Agent that helps create advertising images using AI tools.

    Your capabilities:
    1. Search and download images from the internet using http_request
    2. Apply virtual try-on effects using vto_nova tool
    3. Read and process local image files

    Keep responses concise and focused on the task. When processing images, work efficiently to avoid context length issues.
    """
    ads_video_classify_agent = Agent(
        system_prompt=SYS_PROMPT,
        tools=[file_read, get_image_local_path, vto_nova, http_request],
        callback_handler=PrintingCallbackHandler()
    )
    
    try:
        result = ads_video_classify_agent(task)
        print("Task completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Try with a shorter, more specific request.")

if __name__ == "__main__":
        # Simple test task
    url="https://cbu01.alicdn.com/img/ibank/8904729072_509441886.jpg"
    task = f"请帮我用lht.jpg作为源图片，帮我换上{url}"
    agent(task)