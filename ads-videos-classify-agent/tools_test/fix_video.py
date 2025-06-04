#!/usr/bin/env python3
"""
视频修复工具 - 解决ffmpeg视频处理错误
"""

import os
import sys
import ffmpeg
import argparse

def fix_video(input_path, output_path=None, width=480):
    """
    修复视频文件，确保宽度和高度都是偶数，以便与libx264编码器兼容
    
    参数:
        input_path: 输入视频文件路径
        output_path: 输出视频文件路径（如果为None，则使用input_path_fixed.mp4）
        width: 目标宽度（将自动调整为偶数）
    
    返回:
        输出视频文件路径
    """
    if not os.path.exists(input_path):
        print(f"错误: 输入文件 '{input_path}' 不存在")
        return None
    
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_fixed{ext}"
    
    try:
        # 获取视频信息
        probe = ffmpeg.probe(input_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        
        if not video_stream:
            print("错误: 无法找到视频流")
            return None
        
        original_width = int(video_stream['width'])
        original_height = int(video_stream['height'])
        print(f"原始视频尺寸: {original_width}x{original_height}")
        
        # 确保宽度是偶数
        width = width if width % 2 == 0 else width - 1
        
        print(f"处理视频: {input_path} -> {output_path}")
        print(f"目标宽度: {width}（确保为偶数）")
        
        # 使用-2参数确保高度也是偶数
        ffmpeg.input(input_path).filter("scale", width, -2).output(
            output_path, 
            pix_fmt='yuv420p',  # 确保像素格式兼容
            vcodec='libx264',   # 明确指定编码器
            preset='medium'     # 编码速度和质量的平衡
        ).run(overwrite_output=True)
        
        # 验证输出
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"成功: 视频已修复并保存到 {output_path}")
            
            # 验证新视频的尺寸
            new_probe = ffmpeg.probe(output_path)
            new_video_stream = next((stream for stream in new_probe['streams'] if stream['codec_type'] == 'video'), None)
            new_width = int(new_video_stream['width'])
            new_height = int(new_video_stream['height'])
            print(f"新视频尺寸: {new_width}x{new_height}")
            
            return output_path
        else:
            print("错误: 输出文件不存在或为空")
            return None
            
    except Exception as e:
        print(f"错误: 处理视频时出错: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='修复视频文件，确保宽度和高度都是偶数')
    parser.add_argument('input', help='输入视频文件路径')
    parser.add_argument('-o', '--output', help='输出视频文件路径')
    parser.add_argument('-w', '--width', type=int, default=480, help='目标宽度（默认480）')
    
    args = parser.parse_args()
    
    fix_video(args.input, args.output, args.width)

if __name__ == "__main__":
    main()
