#!/usr/bin/env python3
"""
预算分配Agent API服务启动脚本
"""

import argparse
import sys
import os
import time
import subprocess
from typing import Optional

def check_dependencies():
    """检查依赖是否安装"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'pandas',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print(f"请运行: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def start_api_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """启动API服务器"""
    try:
        import uvicorn
        from api_server import app
        
        print(f"🚀 启动预算分配Agent API服务器...")
        print(f"   地址: http://{host}:{port}")
        print(f"   API文档: http://{host}:{port}/docs")
        print(f"   重载模式: {'开启' if reload else '关闭'}")
        print(f"   按 Ctrl+C 停止服务")
        print("-" * 50)
        
        uvicorn.run(
            "api_server:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n⏹️ 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        return False
    
    return True

def test_api_connection(host: str = "localhost", port: int = 8000, timeout: int = 30):
    """测试API连接"""
    import requests
    import time
    
    url = f"http://{host}:{port}/health"
    print(f"🔍 测试API连接: {url}")
    
    for i in range(timeout):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ API服务器连接成功")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < timeout - 1:
            print(f"   等待服务器启动... ({i+1}/{timeout})")
            time.sleep(1)
    
    print(f"❌ API服务器连接失败")
    return False

def run_api_test():
    """运行API测试"""
    try:
        print("🧪 运行API测试...")
        from test_api import test_api
        test_api()
        return True
    except Exception as e:
        print(f"❌ API测试失败: {str(e)}")
        return False

def show_usage_examples():
    """显示使用示例"""
    print("\n📚 使用示例:")
    print("-" * 30)
    
    print("\n1️⃣ Python客户端使用:")
    print("""
from api_client import BudgetAllocationAPIClient

# 创建客户端
client = BudgetAllocationAPIClient("http://localhost:8000")

# 健康检查
health = client.health_check()
print(health)

# 预算分析
result = client.analyze_budget(
    daily_budget=500,
    target_roas=20,
    enable_logging=True
)
print(result)
""")
    
    print("\n2️⃣ cURL使用:")
    print("""
# 健康检查
curl http://localhost:8000/health

# 预算分析
curl -X POST http://localhost:8000/analyze/budget \\
  -H "Content-Type: application/json" \\
  -d '{
    "daily_budget": 500,
    "target_roas": 20,
    "enable_logging": true
  }'

# 快速分析
curl -X POST http://localhost:8000/analyze/quick \\
  -H "Content-Type: application/json" \\
  -d '{
    "analysis_type": "basic"
  }'
""")
    
    print("\n3️⃣ 浏览器访问:")
    print("   - API文档: http://localhost:8000/docs")
    print("   - 健康检查: http://localhost:8000/health")
    print("   - 文件列表: http://localhost:8000/files")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="预算分配Agent API服务启动脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python start_api.py                    # 启动API服务器
  python start_api.py --port 8080        # 指定端口
  python start_api.py --reload           # 开发模式（自动重载）
  python start_api.py --test             # 测试API连接
  python start_api.py --examples         # 显示使用示例
        """
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="服务器地址 (默认: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="服务器端口 (默认: 8000)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="开启自动重载模式（开发用）"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="测试API连接"
    )
    
    parser.add_argument(
        "--examples",
        action="store_true",
        help="显示使用示例"
    )
    
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="检查依赖包"
    )
    
    args = parser.parse_args()
    
    # 显示使用示例
    if args.examples:
        show_usage_examples()
        return
    
    # 检查依赖
    if args.check_deps:
        if check_dependencies():
            print("✅ 所有依赖包已安装")
        return
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 测试API连接
    if args.test:
        if test_api_connection(args.host, args.port):
            run_api_test()
        return
    
    # 启动API服务器
    print("🎯 预算分配Agent API服务")
    print("=" * 40)
    
    success = start_api_server(
        host=args.host,
        port=args.port,
        reload=args.reload
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()