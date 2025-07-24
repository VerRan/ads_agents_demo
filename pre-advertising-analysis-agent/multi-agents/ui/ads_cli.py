#!/usr/bin/env python3
"""
Command Line Interface for Ads Analysis Agent
"""

import argparse
import json
import sys
import time
from datetime import datetime
from ads_go_agent_as_tool import coordinator_agent, run_agent_graph
import re

def validate_url(url):
    """Validate URL format"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   📊 广告投放前分析系统                        ║
    ║                  AI-Powered Ad Analysis Tool                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_progress(message, step=None, total=None):
    """Print progress message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if step and total:
        progress = f"[{step}/{total}]"
        print(f"[{timestamp}] {progress} {message}")
    else:
        print(f"[{timestamp}] {message}")

def save_results(results, url, mode, output_file=None):
    """Save analysis results to file"""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"analysis_results_{timestamp}.json"
    
    data = {
        "url": url,
        "analysis_time": datetime.now().isoformat(),
        "mode": mode,
        "results": str(results)
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 结果已保存到: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ 保存文件失败: {str(e)}")
        return None

def format_output(results, format_type="text"):
    """Format analysis results for display"""
    if format_type == "json":
        try:
            # Try to parse as JSON if possible
            if isinstance(results, str):
                return json.dumps({"analysis": results}, ensure_ascii=False, indent=2)
            else:
                return json.dumps(results, ensure_ascii=False, indent=2)
        except:
            return json.dumps({"analysis": str(results)}, ensure_ascii=False, indent=2)
    else:
        # Text format
        separator = "=" * 60
        return f"""
{separator}
📊 分析结果
{separator}

{str(results)}

{separator}
        """

def interactive_mode():
    """Run in interactive mode"""
    print_banner()
    print("🔄 进入交互模式 (输入 'quit' 退出)")
    print()
    
    while True:
        try:
            # Get URL input
            url = input("🔗 请输入产品URL: ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                print("👋 再见!")
                break
            
            if not url:
                print("❌ URL不能为空")
                continue
            
            if not validate_url(url):
                print("❌ 请输入有效的URL格式")
                continue
            
            # Get mode selection
            print("\n📋 选择分析模式:")
            print("1. 协调器模式 (Coordinator)")
            print("2. 图模式 (Agent Graph)")
            
            mode_choice = input("请选择 (1 或 2): ").strip()
            
            if mode_choice == "1":
                mode = "coordinator"
                mode_name = "协调器模式"
            elif mode_choice == "2":
                mode = "graph"
                mode_name = "图模式"
            else:
                print("❌ 无效选择，使用默认协调器模式")
                mode = "coordinator"
                mode_name = "协调器模式"
            
            # Run analysis
            print(f"\n🚀 开始分析 ({mode_name})...")
            print_progress("准备分析任务", 1, 4)
            
            task = f"分析一下{url}"
            
            print_progress("启动AI代理", 2, 4)
            start_time = time.time()
            
            try:
                if mode == "coordinator":
                    print_progress("执行协调器分析", 3, 4)
                    result = coordinator_agent(task)
                else:
                    print_progress("执行图模式分析", 3, 4)
                    result = run_agent_graph(task)
                
                end_time = time.time()
                duration = round(end_time - start_time, 2)
                
                print_progress("分析完成", 4, 4)
                print(f"⏱️  分析耗时: {duration}秒")
                
                # Display results
                print(format_output(result))
                
                # Ask if user wants to save
                save_choice = input("💾 是否保存结果到文件? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes', '是']:
                    save_results(result, url, mode_name)
                
            except Exception as e:
                print(f"❌ 分析失败: {str(e)}")
            
            print("\n" + "─" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出程序")
            break
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="广告投放前分析系统 - AI驱动的产品分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python ads_cli.py --url https://example.com
  python ads_cli.py --url https://example.com --mode graph --output results.json
  python ads_cli.py --interactive
        """
    )
    
    parser.add_argument(
        "--url", "-u",
        help="要分析的产品URL"
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=["coordinator", "graph"],
        default="coordinator",
        help="分析模式: coordinator (协调器) 或 graph (图模式)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径 (可选)"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="输出格式: text 或 json"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="启动交互模式"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，减少输出信息"
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        interactive_mode()
        return
    
    # Validate arguments
    if not args.url:
        print("❌ 错误: 请提供URL参数或使用 --interactive 模式")
        parser.print_help()
        sys.exit(1)
    
    if not validate_url(args.url):
        print("❌ 错误: 请提供有效的URL格式")
        sys.exit(1)
    
    # Print banner unless in quiet mode
    if not args.quiet:
        print_banner()
    
    # Prepare analysis
    task = f"分析一下{args.url}"
    mode_name = "协调器模式" if args.mode == "coordinator" else "图模式"
    
    if not args.quiet:
        print(f"🔗 分析URL: {args.url}")
        print(f"📋 分析模式: {mode_name}")
        print(f"📄 输出格式: {args.format}")
        print()
        print_progress("开始分析...", 1, 3)
    
    # Run analysis
    start_time = time.time()
    
    try:
        if args.mode == "coordinator":
            if not args.quiet:
                print_progress("执行协调器分析", 2, 3)
            result = coordinator_agent(task)
        else:
            if not args.quiet:
                print_progress("执行图模式分析", 2, 3)
            result = run_agent_graph(task)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        if not args.quiet:
            print_progress("分析完成", 3, 3)
            print(f"⏱️  分析耗时: {duration}秒")
            print()
        
        # Output results
        formatted_result = format_output(result, args.format)
        print(formatted_result)
        
        # Save to file if specified
        if args.output:
            save_results(result, args.url, mode_name, args.output)
        
    except Exception as e:
        print(f"❌ 分析失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
