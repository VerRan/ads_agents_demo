#!/usr/bin/env python3
"""
Natural language parser for ads creative tasks (standalone)
"""

import re
from urllib.parse import urlparse

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

def main():
    """Test natural language parsing."""
    
    test_cases = [
        "用lht.jpg作为源图片，下载这个衣服图片并进行虚拟试穿：https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg",
        "Download this shirt and try it on: https://example.com/shirt.jpg with my photo lht.jpg",
        "处理这个图片：test.png，调整尺寸",
        "下载这些图片：https://site1.com/img1.jpg 和 https://site2.com/img2.png",
        "用我的照片试穿这个连衣裙：https://example.com/dress.jpg",
        "Try on these pants with lht.jpg: https://example.com/pants.jpg"
    ]
    
    print("🧪 自然语言处理测试")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 测试案例 {i}:")
        print(f"输入: {test_case}")
        print("-" * 40)
        
        result = parse_natural_language_task(test_case)
        
        print(f"动作: {[action['description'] for action in result['actions']]}")
        print(f"URLs: {result['urls']}")
        print(f"文件: {result['files']}")
        print(f"服装类型: {result['garment_class']}")

if __name__ == "__main__":
    main()