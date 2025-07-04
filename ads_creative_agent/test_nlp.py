#!/usr/bin/env python3
"""
Test natural language processing functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui import parse_natural_language_task

def test_nlp():
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
    test_nlp()