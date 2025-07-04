#!/usr/bin/env python3
"""
Simple test script for virtual try-on functionality.
This bypasses the agent to avoid context length issues.
"""

from nova_VTO import try_on_nova
import os

def test_virtual_tryon():
    """Test the virtual try-on functionality directly."""
    
    # Check if source image exists
    src_img = "lht.jpg"
    if not os.path.exists(src_img):
        print(f"❌ Source image {src_img} not found")
        return
    
    # For testing, let's use a downloaded image
    ref_img = "downloaded_images/img_5d28d4a1.jpg"  # Use the downloaded shirt image
    if not os.path.exists(ref_img):
        print(f"❌ Reference image {ref_img} not found")
        print("Available images:")
        for file in os.listdir("."):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"  - {file}")
        return
    
    print(f"🔍 Testing virtual try-on:")
    print(f"  Source: {src_img}")
    print(f"  Reference: {ref_img}")
    print(f"  Garment Class: UPPER_BODY (default)")
    print("-" * 50)
    
    try:
        result = try_on_nova(src_img, ref_img, "UPPER_BODY")
        
        if result.get("success"):
            print("✅ Virtual try-on completed successfully!")
            print(f"📁 Generated {result['images_generated']} image(s)")
            print("📄 Saved files:")
            for file in result['saved_files']:
                print(f"  - {file}")
        else:
            print("❌ Virtual try-on failed:")
            print(f"  Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    test_virtual_tryon()