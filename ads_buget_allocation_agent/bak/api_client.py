#!/usr/bin/env python3
"""
预算分配Agent API客户端
提供简单易用的Python客户端接口
"""

import requests
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
import os

class BudgetAllocationAPIClient:
    """预算分配Agent API客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        初始化API客户端
        
        Args:
            base_url: API服务器地址
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        上传CSV文件
        
        Args:
            file_path: 本地CSV文件路径
            
        Returns:
            上传结果，包含文件ID
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'text/csv')}
                response = self.session.post(f"{self.base_url}/upload", files=files)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_files(self) -> Dict[str, Any]:
        """列出已上传的文件"""
        try:
            response = self.session.get(f"{self.base_url}/files")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_budget(
        self,
        daily_budget: float,
        target_roas: float,
        file_name: Optional[str] = None,
        custom_query: Optional[str] = None,
        enable_logging: bool = True
    ) -> Dict[str, Any]:
        """
        预算分配分析
        
        Args:
            daily_budget: 日预算
            target_roas: 目标ROAS
            file_name: 文件ID（可选，不提供则使用默认文件）
            custom_query: 自定义查询（可选）
            enable_logging: 是否启用日志记录
            
        Returns:
            分析结果
        """
        try:
            data = {
                "daily_budget": daily_budget,
                "target_roas": target_roas,
                "enable_logging": enable_logging
            }
            
            if file_name:
                data["file_name"] = file_name
            if custom_query:
                data["custom_query"] = custom_query
            
            response = self.session.post(
                f"{self.base_url}/analyze/budget",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def quick_analysis(
        self,
        file_name: Optional[str] = None,
        analysis_type: str = "basic"
    ) -> Dict[str, Any]:
        """
        快速分析
        
        Args:
            file_name: 文件ID（可选）
            analysis_type: 分析类型 (basic, detailed, custom)
            
        Returns:
            分析结果
        """
        try:
            data = {"analysis_type": analysis_type}
            if file_name:
                data["file_name"] = file_name
            
            response = self.session.post(
                f"{self.base_url}/analyze/quick",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_analysis_templates(self) -> Dict[str, Any]:
        """获取分析模板"""
        try:
            response = self.session.get(f"{self.base_url}/analyze/templates")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_with_template(
        self,
        template_name: str,
        daily_budget: Optional[float] = None,
        target_roas: Optional[float] = None,
        file_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        使用模板进行分析
        
        Args:
            template_name: 模板名称
            daily_budget: 日预算（预算优化模板需要）
            target_roas: 目标ROAS（预算优化模板需要）
            file_name: 文件ID（可选）
            
        Returns:
            分析结果
        """
        try:
            params = {}
            if daily_budget is not None:
                params["daily_budget"] = daily_budget
            if target_roas is not None:
                params["target_roas"] = target_roas
            if file_name:
                params["file_name"] = file_name
            
            response = self.session.post(
                f"{self.base_url}/analyze/template/{template_name}",
                params=params
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_log_files(self) -> Dict[str, Any]:
        """列出日志文件"""
        try:
            response = self.session.get(f"{self.base_url}/logs")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_log_file(self, filename: str) -> Dict[str, Any]:
        """
        获取日志文件内容
        
        Args:
            filename: 日志文件名
            
        Returns:
            日志文件内容
        """
        try:
            response = self.session.get(f"{self.base_url}/logs/{filename}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# 便捷函数
def create_client(base_url: str = "http://localhost:8000") -> BudgetAllocationAPIClient:
    """创建API客户端实例"""
    return BudgetAllocationAPIClient(base_url)

# 使用示例
if __name__ == "__main__":
    # 创建客户端
    client = create_client()
    
    # 健康检查
    print("🔍 健康检查...")
    health = client.health_check()
    print(f"服务状态: {health}")
    
    # 列出文件
    print("\n📁 列出文件...")
    files = client.list_files()
    print(f"可用文件: {files}")
    
    # 快速分析
    print("\n⚡ 快速分析...")
    quick_result = client.quick_analysis(analysis_type="basic")
    if quick_result.get("success"):
        print(f"分析完成，耗时: {quick_result['execution_time']:.2f}秒")
        print(f"结果预览: {quick_result['result'][:200]}...")
    else:
        print(f"分析失败: {quick_result.get('error')}")
    
    # 预算分析
    print("\n💰 预算分析...")
    budget_result = client.analyze_budget(
        daily_budget=500,
        target_roas=20,
        enable_logging=True
    )
    if budget_result.get("success"):
        print(f"预算分析完成，耗时: {budget_result['execution_time']:.2f}秒")
        print(f"日志文件: {budget_result.get('log_file')}")
        print(f"结果预览: {budget_result['result'][:200]}...")
    else:
        print(f"预算分析失败: {budget_result.get('error')}")
    
    # 获取分析模板
    print("\n📋 分析模板...")
    templates = client.get_analysis_templates()
    if "templates" in templates:
        print("可用模板:")
        for name, info in templates["templates"].items():
            print(f"  - {name}: {info['description']}")
    
    # 列出日志文件
    print("\n📝 日志文件...")
    logs = client.list_log_files()
    if "log_files" in logs:
        print(f"共有 {logs['total_files']} 个日志文件")
        for log in logs["log_files"][:3]:  # 显示最新的3个
            print(f"  - {log['filename']} ({log['size']} bytes)")