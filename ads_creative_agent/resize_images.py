"""
Image resizing utility for ads creative agent.
Handles image validation and resizing according to platform requirements.
"""

from PIL import Image
import os
from typing import Tuple, Optional
import math


class ImageProcessor:
    """Handles image validation and resizing for ad creatives."""
    
    # Constants based on requirements
    MAX_RESOLUTION_MP = 4.19  # Maximum resolution in megapixels
    MAX_DIMENSION = 4096      # Maximum height or width in pixels
    MIN_DIMENSION = 320       # Minimum width requirement
    MIN_ASPECT_RATIO = 1/4    # 1:4 aspect ratio
    MAX_ASPECT_RATIO = 4/1    # 4:1 aspect ratio
    SUPPORTED_FORMATS = {'PNG', 'JPEG', 'JPG'}
    
    def __init__(self):
        pass
    
    def validate_file_format(self, file_path: str) -> bool:
        """Validate if the file format is supported."""
        try:
            with Image.open(file_path) as img:
                return img.format in self.SUPPORTED_FORMATS
        except Exception:
            return False
    
    def get_image_info(self, file_path: str) -> dict:
        """Get comprehensive image information."""
        with Image.open(file_path) as img:
            width, height = img.size
            resolution_mp = (width * height) / 1_000_000
            aspect_ratio = width / height
            
            return {
                'width': width,
                'height': height,
                'resolution_mp': resolution_mp,
                'aspect_ratio': aspect_ratio,
                'format': img.format,
                'mode': img.mode
            }
    
    def validate_image_requirements(self, file_path: str) -> Tuple[bool, list]:
        """Validate image against all requirements."""
        errors = []
        
        # Check file format
        if not self.validate_file_format(file_path):
            errors.append(f"Unsupported format. Only {', '.join(self.SUPPORTED_FORMATS)} are allowed.")
            return False, errors
        
        info = self.get_image_info(file_path)
        
        # Check resolution
        if info['resolution_mp'] > self.MAX_RESOLUTION_MP:
            errors.append(f"Resolution too high: {info['resolution_mp']:.2f}MP > {self.MAX_RESOLUTION_MP}MP")
        
        # Check dimensions
        if info['width'] > self.MAX_DIMENSION or info['height'] > self.MAX_DIMENSION:
            errors.append(f"Dimensions too large: {info['width']}x{info['height']} (max: {self.MAX_DIMENSION}px)")
        
        # Check minimum width requirement
        if info['width'] < self.MIN_DIMENSION:
            errors.append(f"Width too small: {info['width']}px (min: {self.MIN_DIMENSION}px)")
        
        # Check aspect ratio
        if not (self.MIN_ASPECT_RATIO <= info['aspect_ratio'] <= self.MAX_ASPECT_RATIO):
            errors.append(f"Invalid aspect ratio: {info['aspect_ratio']:.2f} (must be between {self.MIN_ASPECT_RATIO} and {self.MAX_ASPECT_RATIO})")
        
        return len(errors) == 0, errors    

    def calculate_resize_dimensions(self, current_width: int, current_height: int) -> Tuple[int, int]:
        """Calculate optimal resize dimensions while maintaining aspect ratio."""
        aspect_ratio = current_width / current_height
        
        # Ensure aspect ratio is within bounds
        if aspect_ratio < self.MIN_ASPECT_RATIO:
            aspect_ratio = self.MIN_ASPECT_RATIO
        elif aspect_ratio > self.MAX_ASPECT_RATIO:
            aspect_ratio = self.MAX_ASPECT_RATIO
        
        # Calculate max dimensions based on resolution limit
        max_pixels = self.MAX_RESOLUTION_MP * 1_000_000
        max_width_from_resolution = int(math.sqrt(max_pixels * aspect_ratio))
        max_height_from_resolution = int(math.sqrt(max_pixels / aspect_ratio))
        
        # Apply dimension constraints
        target_width = min(max_width_from_resolution, self.MAX_DIMENSION)
        target_height = min(max_height_from_resolution, self.MAX_DIMENSION)
        
        # Ensure minimum width requirement
        if target_width < self.MIN_DIMENSION:
            target_width = self.MIN_DIMENSION
            target_height = int(target_width / aspect_ratio)
        
        # Ensure we maintain the aspect ratio
        if target_width / target_height > aspect_ratio:
            target_width = int(target_height * aspect_ratio)
        else:
            target_height = int(target_width / aspect_ratio)
        
        # Final check to ensure minimum width
        if target_width < self.MIN_DIMENSION:
            target_width = self.MIN_DIMENSION
            target_height = int(target_width / aspect_ratio)
        
        return target_width, target_height
    
    def resize_image(self, input_path: str, output_path: str, quality: int = 95) -> bool:
        """Resize image to meet requirements."""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary (for JPEG output)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                current_width, current_height = img.size
                target_width, target_height = self.calculate_resize_dimensions(current_width, current_height)
                
                # Resize using high-quality resampling
                resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                
                # Determine output format
                output_format = 'JPEG' if output_path.lower().endswith(('.jpg', '.jpeg')) else 'PNG'
                
                # Save with appropriate settings
                if output_format == 'JPEG':
                    resized_img.save(output_path, format=output_format, quality=quality, optimize=True)
                else:
                    resized_img.save(output_path, format=output_format, optimize=True)
                
                return True
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
    
    def process_image(self, input_path: str, output_path: Optional[str] = None) -> dict:
        """Complete image processing workflow."""
        result = {
            'success': False,
            'original_info': None,
            'processed_info': None,
            'errors': [],
            'output_path': None
        }
        
        try:
            # Validate input file exists
            if not os.path.exists(input_path):
                result['errors'].append("Input file does not exist")
                return result
            
            # Get original image info
            result['original_info'] = self.get_image_info(input_path)
            
            # Validate requirements
            is_valid, errors = self.validate_image_requirements(input_path)
            
            if is_valid:
                # Image already meets requirements
                result['success'] = True
                result['processed_info'] = result['original_info']
                result['output_path'] = input_path
                return result
            
            # Need to resize - generate output path if not provided
            if output_path is None:
                base, ext = os.path.splitext(input_path)
                output_path = f"{base}_resized{ext}"
            
            # Resize image
            if self.resize_image(input_path, output_path):
                result['processed_info'] = self.get_image_info(output_path)
                result['success'] = True
                result['output_path'] = output_path
            else:
                result['errors'].append("Failed to resize image")
        
        except Exception as e:
            result['errors'].append(f"Processing error: {str(e)}")
        
        return result


def main():
    """Example usage of the ImageProcessor."""
    processor = ImageProcessor()
    
    # Example usage
    # input_file = "coats.png"  # Replace with actual file path
    input_file = "coats-2.png"  # Replace with actual file path
    if os.path.exists(input_file):
        result = processor.process_image(input_file)
        
        if result['success']:
            print("✅ Image processed successfully!")
            print(f"Output: {result['output_path']}")
            print(f"Original: {result['original_info']['width']}x{result['original_info']['height']} ({result['original_info']['resolution_mp']:.2f}MP)")
            if result['processed_info'] != result['original_info']:
                print(f"Resized: {result['processed_info']['width']}x{result['processed_info']['height']} ({result['processed_info']['resolution_mp']:.2f}MP)")
        else:
            print("❌ Image processing failed:")
            for error in result['errors']:
                print(f"  - {error}")
    else:
        print("Please provide a valid image file path")


if __name__ == "__main__":
    main()