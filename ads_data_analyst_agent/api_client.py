#!/usr/bin/env python3
"""
AI数据分析师 API客户端
用于调用REST API服务
"""

import requests
import json
import time
from typing import Optional, Dict, Any
import pandas as pd

class AIAnalystAPIClient:
    """AI数据分析师API客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """上传CSV文件"""
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'text/csv')}
            response = self.session.post(f"{self.base_url}/upload", files=files)
        response.raise_for_status()
        return response.json()
    
    def list_files(self) -> Dict[str, Any]:
        """列出已上传的文件"""
        response = self.session.get(f"{self.base_url}/files")
        response.raise_for_status()
        return response.json()
    
    def analyze_data(self, query: str, file_name: Optional[str] = None) -> Dict[str, Any]:
        """分析数据"""
        data = {
            "query": query,
            "file_name": file_name
        }
        response = self.session.post(f"{self.base_url}/analyze", json=data)
        response.raise_for_status()
        return response.json()
    
    def analyze_data_stream(self, query: str, file_name: Optional[str] = None):
        """流式分析数据"""
        data = {
            "query": query,
            "file_name": file_name,
            "stream": True
        }
        response = self.session.post(f"{self.base_url}/analyze/stream", json=data, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])  # 去掉 'data: ' 前缀
                        yield data
                    except json.JSONDecodeError:
                        continue
    
    def preview_data(self, file_name: Optional[str] = None, rows: int = 10) -> Dict[str, Any]:
        """预览数据"""
        params = {"rows": rows}
        if file_name:
            params["file_name"] = file_name
        
        response = self.session.post(f"{self.base_url}/data/preview", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_templates(self) -> Dict[str, Any]:
        """获取分析模板"""
        response = self.session.get(f"{self.base_url}/templates")
        response.raise_for_status()
        return response.json()
    
    def analyze_with_template(self, template_key: str, file_name: Optional[str] = None) -> Dict[str, Any]:
        """使用模板分析"""
        params = {}
        if file_name:
            params["file_name"] = file_name
        
        response = self.session.post(f"{self.base_url}/analyze/template/{template_key}", params=params)
        response.raise_for_status()
        return response.json()
    
    def delete_file(self, file_id: str) -> Dict[str, Any]:
        """删除文件"""
        response = self.session.delete(f"{self.base_url}/files/{file_id}")
        response.raise_for_status()
        return response.json()

# 使用示例
def example_usage():
    """API使用示例"""
    client = AIAnalystAPIClient()
    
    print("🚀 AI数据分析师 API客户端示例")
    print("=" * 50)
    
    try:
        # 1. 健康检查
        print("1. 健康检查...")
        health = client.health_check()
        print(f"   状态: {health['status']}")
        
        # 2. 获取分析模板
        print("\n2. 获取分析模板...")
        templates = client.get_templates()
        print(f"   可用模板: {list(templates['templates'].keys())}")
        
        # 3. 预览默认数据
        print("\n3. 预览默认数据...")
        preview = client.preview_data(rows=5)
        print(f"   数据形状: {preview['rows']} 行 x {preview['columns']} 列")
        print(f"   列名: {preview['column_names'][:5]}...")
        
        # 4. 使用模板分析
        print("\n4. 使用模板分析...")
        result = client.analyze_with_template("basic_stats")
        print(f"   分析结果: {result['result'][:200]}...")
        print(f"   执行时间: {result['execution_time']:.2f}秒")
        
        # 5. 自定义查询
        print("\n5. 自定义查询...")
        custom_result = client.analyze_data("这个数据集有多少行数据？")
        print(f"   查询结果: {custom_result['result']}")
        
        # 6. 流式分析示例
        print("\n6. 流式分析示例...")
        print("   开始流式分析...")
        for chunk in client.analyze_data_stream("请简单介绍一下这个数据集"):
            if chunk['type'] == 'start':
                print(f"   {chunk['message']}")
            elif chunk['type'] == 'chunk':
                print(f"   接收数据块: {len(chunk['data'])} 字符")
            elif chunk['type'] == 'end':
                print(f"   {chunk['message']}")
            elif chunk['type'] == 'error':
                print(f"   错误: {chunk['message']}")
                break
        
        print("\n✅ API测试完成！")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API请求失败: {e}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    example_usage()