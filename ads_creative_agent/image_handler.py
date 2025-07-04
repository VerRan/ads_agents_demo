#!/usr/bin/env python3
"""
Image handler tool for processing local images and downloading from URLs.
"""

import os
import requests
import uuid
from urllib.parse import urlparse, unquote
from pathlib import Path
import mimetypes

class ImageHandler:
    """Handles image path resolution and URL downloads."""
    
    def __init__(self, download_dir="downloaded_images"):
        """Initialize with download directory."""
        self.download_dir = download_dir
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        
        # Create download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def is_url(self, path_or_url):
        """Check if the input is a URL."""
        try:
            result = urlparse(path_or_url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def get_file_extension_from_url(self, url):
        """Extract file extension from URL."""
        parsed_url = urlparse(url)
        path = unquote(parsed_url.path)
        
        # Try to get extension from path
        _, ext = os.path.splitext(path)
        if ext.lower() in self.supported_extensions:
            return ext.lower()
        
        # If no extension in path, try to guess from content-type
        try:
            response = requests.head(url, timeout=10)
            content_type = response.headers.get('content-type', '')
            ext = mimetypes.guess_extension(content_type.split(';')[0])
            if ext and ext.lower() in self.supported_extensions:
                return ext.lower()
        except:
            pass
        
        # Default to .jpg if can't determine
        return '.jpg'
    
    def download_image(self, url):
        """Download image from URL and return local path."""
        try:
            # Get file extension
            ext = self.get_file_extension_from_url(url)
            
            # Generate unique filename
            filename = f"img_{uuid.uuid4().hex[:8]}{ext}"
            local_path = os.path.join(self.download_dir, filename)
            
            # Download the image
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save to local file
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return {
                "success": True,
                "local_path": local_path,
                "original_url": url,
                "filename": filename,
                "size_bytes": os.path.getsize(local_path)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original_url": url
            }
    
    def find_local_image(self, image_name):
        """Find local image file by name."""
        # Check current directory first
        if os.path.exists(image_name):
            return {
                "success": True,
                "local_path": os.path.abspath(image_name),
                "found_in": "current_directory"
            }
        
        # Check download directory
        download_path = os.path.join(self.download_dir, image_name)
        if os.path.exists(download_path):
            return {
                "success": True,
                "local_path": os.path.abspath(download_path),
                "found_in": "download_directory"
            }
        
        # Try to find similar names (case insensitive)
        current_files = [f for f in os.listdir('.') if f.lower().endswith(tuple(self.supported_extensions))]
        download_files = []
        if os.path.exists(self.download_dir):
            download_files = [f for f in os.listdir(self.download_dir) if f.lower().endswith(tuple(self.supported_extensions))]
        
        # Look for case-insensitive match
        image_name_lower = image_name.lower()
        for file in current_files:
            if file.lower() == image_name_lower:
                return {
                    "success": True,
                    "local_path": os.path.abspath(file),
                    "found_in": "current_directory",
                    "note": "Found with case-insensitive match"
                }
        
        for file in download_files:
            if file.lower() == image_name_lower:
                return {
                    "success": True,
                    "local_path": os.path.abspath(os.path.join(self.download_dir, file)),
                    "found_in": "download_directory",
                    "note": "Found with case-insensitive match"
                }
        
        return {
            "success": False,
            "error": f"Image '{image_name}' not found",
            "available_images": {
                "current_directory": current_files,
                "download_directory": download_files
            }
        }
    
    def get_image_path(self, image_input):
        """
        Main function to get local image path from name or URL.
        
        Args:
            image_input: Image name or URL
            
        Returns:
            dict: Result with local_path or error information
        """
        if self.is_url(image_input):
            # It's a URL, download it
            result = self.download_image(image_input)
            if result["success"]:
                return {
                    "success": True,
                    "local_path": result["local_path"],
                    "source": "downloaded",
                    "original_url": image_input,
                    "filename": result["filename"],
                    "size_bytes": result["size_bytes"]
                }
            else:
                return result
        else:
            # It's a local file name, find it
            return self.find_local_image(image_input)


# Convenience function for tool integration
def get_image_path(image_input, download_dir="downloaded_images"):
    """
    Get local path for an image (download if URL, find if local name).
    
    Args:
        image_input: Image filename or URL
        download_dir: Directory to save downloaded images
        
    Returns:
        dict: Result with local_path or error information
    """
    handler = ImageHandler(download_dir)
    return handler.get_image_path(image_input)


def main():
    """Test the image handler."""
    handler = ImageHandler()
    
    # Test cases
    test_cases = [
        "lht.jpg",  # Local file
        "nonexistent.png",  # Non-existent file
        "https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg",  # URL
    ]
    
    for test_input in test_cases:
        print(f"\n🔍 Testing: {test_input}")
        print("-" * 50)
        result = handler.get_image_path(test_input)
        
        if result["success"]:
            print(f"✅ Success!")
            print(f"📁 Local path: {result['local_path']}")
            if "source" in result:
                print(f"📥 Source: {result['source']}")
            if "original_url" in result:
                print(f"🌐 Original URL: {result['original_url']}")
        else:
            print(f"❌ Failed: {result['error']}")
            if "available_images" in result:
                print("📋 Available images:")
                for location, files in result["available_images"].items():
                    if files:
                        print(f"  {location}: {', '.join(files)}")


if __name__ == "__main__":
    main()