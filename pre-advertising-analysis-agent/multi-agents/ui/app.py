#!/usr/bin/env python3
"""
Ads Go Agent REST API 启动脚本
简化的启动入口，包含欢迎信息和文档链接
"""

import os
import sys
from ads_go_agent_rest_api import app

def print_welcome():
    """打印欢迎信息和使用指南"""
    print("=" * 60)
    print("🚀 Ads Go Agent REST API 服务启动")
    print("=" * 60)
    print()
    print("📋 服务信息:")
    print("   • 服务地址: http://localhost:5000")
    print("   • API版本: v1.0.0")
    print("   • 状态检查: http://localhost:5000/health")
    print()
    print("📖 文档地址:")
    print("   • 交互式文档: http://localhost:5000/docs")
    print("   • JSON文档: http://localhost:5000/api/v1/docs")
    print()
    print("🔍 主要端点:")
    print("   • 综合分析: POST /api/v1/analyze")
    print("   • 产品分析: POST /api/v1/analyze/product")
    print("   • 竞品分析: POST /api/v1/analyze/competitor")
    print("   • 市场分析: POST /api/v1/analyze/market")
    print("   • 受众分析: POST /api/v1/analyze/audience")
    print("   • 批量分析: POST /api/v1/analyze/batch")
    print()
    print("🧪 测试命令:")
    print("   python test_api.py")
    print()
    print("💡 快速测试:")
    print('   curl -X GET http://localhost:5000/health')
    print()
    print("=" * 60)
    print("服务正在启动中...")
    print("=" * 60)

def main():
    """主函数"""
    print_welcome()
    
    # 检查依赖
    try:
        import flask
        import flask_cors
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements_api.txt")
        sys.exit(1)
    
    # 启动服务
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # 避免重复打印欢迎信息
        )
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
    except Exception as e:
        print(f"\n❌ 服务启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()