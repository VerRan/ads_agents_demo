#!/usr/bin/env python3
"""
Simplified Ads Creative Agent with better context management.
"""

from strands import Agent, tool
from strands_tools import file_read
from strands.handlers.callback_handler import PrintingCallbackHandler
from nova_VTO import try_on_nova
from image_handler import get_image_path
import os
import logging

# Configure logging
logging.getLogger("strands").setLevel(logging.WARNING)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

@tool
def get_image_local_path(image_input):
    """Get local path for an image (handles URLs and local files)."""
    return get_image_path(image_input)

@tool
def vto_nova(src_img, ref_img, garmentClass="UPPER_BODY"):
    """
    Perform virtual try-on using Nova VTO.
    
    Args:
        src_img: Path to source image (person photo) or URL
        ref_img: Path to reference image (garment) or URL
        garmentClass: Type of garment (default: UPPER_BODY)
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
        result = try_on_nova(src_result["local_path"], ref_result["local_path"], garmentClass)
        return result
    except Exception as e:
        return f"Error in VTO processing: {str(e)}"

@tool
def list_images():
    """List available image files in the current directory."""
    image_files = []
    for file in os.listdir("."):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_files.append(file)
    return {"available_images": image_files}

def main():
    """Run the simplified ads creative agent."""
    
    # Create agent with minimal system prompt
    agent = Agent(
        system_prompt="""You are an Ads Creative Agent. You can:
1. List available images with list_images()
2. Perform virtual try-on with vto_nova(src_img, ref_img, garmentClass)

Keep responses concise and focused.""",
        tools=[list_images, get_image_local_path, vto_nova],
        callback_handler=PrintingCallbackHandler()
    )
    
    # Simple test with URL
    task = "请用lht.jpg作为源图片，用这个URL的衬衣图片进行虚拟试穿：https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg"
    
    try:
        result = agent(task)
        print("\n✅ Task completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()