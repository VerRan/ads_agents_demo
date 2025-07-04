#!/usr/bin/env python3
"""
预算分配Agent REST API服务器
提供buget_allocation_agent.py的API接口
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
import pandas as pd
import json
import io
import os
import uuid
import asyncio
from datetime import datetime
import logging

# 导入现有的预算分配代理
from buget_allocation_agent import Agent, get_llm, PROMPT
from strands_tools import file_read, python_repl
from custom_callback_handler import create_callback_handler

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="预算分配Agent API",
    description="基于AI的广告预算分配优化服务，支持数据分析和预算调整建议",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class BudgetAnalysisRequest(BaseModel):
    daily_budget: float
    target_roas: float
    file_name: Optional[str] = None
    custom_query: Optional[str] = None
    enable_logging: Optional[bool] = True

class BudgetAnalysisResponse(BaseModel):
    success: bool
    result: str
    execution_time: float
    timestamp: str
    file_name: Optional[str] = None
    log_file: Optional[str] = None
    summary: Optional[Dict[str, Any]] = None

class FileUploadResponse(BaseModel):
    success: bool
    file_name: str
    file_size: int
    rows: int
    columns: int
    message: str
    preview: Optional[List[Dict]] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    agent_status: str

class QuickAnalysisRequest(BaseModel):
    file_name: Optional[str] = None
    analysis_type: str = "basic"  # basic, detailed, custom

class BudgetSummary(BaseModel):
    total_campaigns: int
    current_total_budget: float
    recommended_total_budget: float
    budget_change: float
    budget_change_percentage: float
    campaigns_to_increase: int
    campaigns_to_decrease: int
    campaigns_to_pause: int
    risk_distribution: Dict[str, float]

# 全局变量存储上传的文件信息和Agent实例
uploaded_files: Dict[str, Dict[str, Any]] = {}
agent_instance = None

def get_agent_instance(enable_logging: bool = True):
    """获取Agent实例"""
    global agent_instance
    
    if enable_logging:
        callback_handler = create_callback_handler(
            handler_type="complete",
            log_file=None  # 自动生成文件名
        )
    else:
        callback_handler = None
    
    return Agent(
        model=get_llm(),
        system_prompt=PROMPT,
        tools=[file_read, python_repl],
        callback_handler=callback_handler
    )

@app.get("/", response_model=Dict[str, str])
async def root():
    """根路径，返回API信息"""
    return {
        "message": "预算分配Agent API服务",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "description": "基于AI的广告预算分配优化服务"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    try:
        # 测试Agent是否正常工作
        test_agent = get_agent_instance(enable_logging=False)
        agent_status = "healthy" if test_agent else "error"
    except Exception as e:
        agent_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        agent_status=agent_status
    )

@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """上传CSV文件"""
    try:
        # 检查文件类型
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="只支持CSV文件")
        
        # 读取文件内容
        content = await file.read()
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        file_path = f"uploaded_{file_id}_{file.filename}"
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 读取并分析文件
        df = pd.read_csv(file_path)
        
        # 生成预览数据
        preview = df.head(5).to_dict('records') if len(df) > 0 else []
        
        # 存储文件信息
        uploaded_files[file_id] = {
            "original_name": file.filename,
            "file_path": file_path,
            "upload_time": datetime.now().isoformat(),
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist()
        }
        
        return FileUploadResponse(
            success=True,
            file_name=file_id,
            file_size=len(content),
            rows=len(df),
            columns=len(df.columns),
            message=f"文件上传成功，文件ID: {file_id}",
            preview=preview
        )
        
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@app.get("/files")
async def list_files():
    """列出已上传的文件"""
    return {
        "uploaded_files": uploaded_files,
        "default_file": "2025-03-04_input.csv",
        "total_files": len(uploaded_files)
    }

@app.post("/analyze/budget", response_model=BudgetAnalysisResponse)
async def analyze_budget(request: BudgetAnalysisRequest):
    """预算分配分析"""
    try:
        start_time = datetime.now()
        
        # 确定要使用的文件
        if request.file_name:
            if request.file_name in uploaded_files:
                file_path = uploaded_files[request.file_name]["file_path"]
                filename = file_path
            else:
                raise HTTPException(status_code=404, detail="文件未找到")
        else:
            # 使用默认文件
            filename = "2025-03-04_input.csv"
        
        # 构建查询
        if request.custom_query:
            query = request.custom_query
        else:
            query = f"""你必须在用户的日预算{request.daily_budget}
            及目标KPI{request.target_roas}的基础上，对用户提供的广告数据{filename}进行深度分析，后给出预算调整建议。"""
        
        # 创建Agent实例
        agent = get_agent_instance(enable_logging=request.enable_logging)
        
        # 执行分析
        result = agent(query)
        
        # 计算执行时间
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # 生成日志文件名（如果启用了日志）
        log_file = None
        if request.enable_logging:
            # 查找最新的日志文件
            import glob
            log_files = glob.glob("budget_analysis_complete_*.txt")
            if log_files:
                log_file = max(log_files, key=os.path.getctime)
        
        # 尝试解析结果生成摘要
        summary = None
        try:
            summary = parse_budget_analysis_summary(str(result))
        except Exception as e:
            logger.warning(f"无法生成摘要: {str(e)}")
        
        return BudgetAnalysisResponse(
            success=True,
            result=str(result),
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
            file_name=request.file_name or filename,
            log_file=log_file,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"预算分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"预算分析失败: {str(e)}")

@app.post("/analyze/quick", response_model=BudgetAnalysisResponse)
async def quick_analysis(request: QuickAnalysisRequest):
    """快速分析"""
    try:
        start_time = datetime.now()
        
        # 确定要使用的文件
        if request.file_name:
            if request.file_name in uploaded_files:
                file_path = uploaded_files[request.file_name]["file_path"]
                filename = file_path
            else:
                raise HTTPException(status_code=404, detail="文件未找到")
        else:
            filename = "2025-03-04_input.csv"
        
        # 根据分析类型构建查询
        if request.analysis_type == "basic":
            query = f"请分析{filename}文件的基本统计信息，包括数据行数、列数、主要指标概览。"
        elif request.analysis_type == "detailed":
            query = f"请详细分析{filename}文件中的广告数据，包括各Campaign的表现、ROAS分布、预算使用情况。"
        else:
            query = f"请分析{filename}文件中的数据质量和完整性。"
        
        # 创建Agent实例（快速分析不启用日志）
        agent = get_agent_instance(enable_logging=False)
        
        # 执行分析
        result = agent(query)
        
        # 计算执行时间
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return BudgetAnalysisResponse(
            success=True,
            result=str(result),
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
            file_name=request.file_name or filename,
            log_file=None
        )
        
    except Exception as e:
        logger.error(f"快速分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"快速分析失败: {str(e)}")

@app.get("/analyze/templates")
async def get_analysis_templates():
    """获取分析模板"""
    return {
        "templates": {
            "budget_optimization": {
                "name": "预算优化分析",
                "description": "基于目标ROAS进行预算分配优化",
                "required_params": ["daily_budget", "target_roas"],
                "example": {
                    "daily_budget": 500,
                    "target_roas": 20
                }
            },
            "performance_analysis": {
                "name": "广告表现分析",
                "description": "分析各Campaign的表现和效果",
                "required_params": [],
                "example": {}
            },
            "risk_assessment": {
                "name": "风险评估分析",
                "description": "评估各Campaign的投资风险",
                "required_params": [],
                "example": {}
            },
            "data_quality": {
                "name": "数据质量检查",
                "description": "检查数据完整性和质量问题",
                "required_params": [],
                "example": {}
            }
        }
    }

@app.post("/analyze/template/{template_name}")
async def analyze_with_template(
    template_name: str,
    daily_budget: Optional[float] = None,
    target_roas: Optional[float] = None,
    file_name: Optional[str] = None
):
    """使用模板进行分析"""
    try:
        # 确定要使用的文件
        if file_name:
            if file_name in uploaded_files:
                file_path = uploaded_files[file_name]["file_path"]
                filename = file_path
            else:
                raise HTTPException(status_code=404, detail="文件未找到")
        else:
            filename = "2025-03-04_input.csv"
        
        # 根据模板构建查询
        if template_name == "budget_optimization":
            if not daily_budget or not target_roas:
                raise HTTPException(status_code=400, detail="预算优化分析需要daily_budget和target_roas参数")
            
            request = BudgetAnalysisRequest(
                daily_budget=daily_budget,
                target_roas=target_roas,
                file_name=file_name,
                enable_logging=True
            )
            return await analyze_budget(request)
            
        elif template_name == "performance_analysis":
            request = QuickAnalysisRequest(
                file_name=file_name,
                analysis_type="detailed"
            )
            return await quick_analysis(request)
            
        elif template_name == "risk_assessment":
            query = f"请分析{filename}文件中各Campaign的投资风险，包括ROAS稳定性、预算使用效率、表现波动性等。"
            
        elif template_name == "data_quality":
            request = QuickAnalysisRequest(
                file_name=file_name,
                analysis_type="custom"
            )
            return await quick_analysis(request)
            
        else:
            raise HTTPException(status_code=404, detail="模板未找到")
        
        # 执行自定义查询
        start_time = datetime.now()
        agent = get_agent_instance(enable_logging=False)
        result = agent(query)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return BudgetAnalysisResponse(
            success=True,
            result=str(result),
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
            file_name=file_name or filename,
            log_file=None
        )
        
    except Exception as e:
        logger.error(f"模板分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"模板分析失败: {str(e)}")

@app.get("/logs")
async def list_log_files():
    """列出日志文件"""
    try:
        import glob
        log_files = []
        
        # 查找所有日志文件
        for pattern in ["budget_analysis_complete_*.txt", "simple_test.log"]:
            files = glob.glob(pattern)
            for file in files:
                stat = os.stat(file)
                log_files.append({
                    "filename": file,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        # 按创建时间排序
        log_files.sort(key=lambda x: x["created"], reverse=True)
        
        return {
            "log_files": log_files,
            "total_files": len(log_files)
        }
        
    except Exception as e:
        logger.error(f"获取日志文件列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取日志文件列表失败: {str(e)}")

@app.get("/logs/{filename}")
async def get_log_file(filename: str):
    """获取日志文件内容"""
    try:
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="日志文件未找到")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "filename": filename,
            "content": content,
            "size": len(content),
            "lines": len(content.splitlines())
        }
        
    except Exception as e:
        logger.error(f"读取日志文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"读取日志文件失败: {str(e)}")

def parse_budget_analysis_summary(result_text: str) -> Dict[str, Any]:
    """解析预算分析结果，生成摘要"""
    try:
        # 这里可以实现更复杂的解析逻辑
        # 目前返回基本信息
        lines = result_text.split('\n')
        
        summary = {
            "analysis_type": "budget_optimization",
            "total_lines": len(lines),
            "contains_table": "Campaign ID" in result_text,
            "contains_recommendations": "建议" in result_text or "调整" in result_text,
            "risk_analysis": "风险" in result_text,
            "generated_at": datetime.now().isoformat()
        }
        
        return summary
        
    except Exception as e:
        logger.warning(f"解析摘要失败: {str(e)}")
        return {}

# 启动服务器的函数
def start_server(host: str = "0.0.0.0", port: int = 8000):
    """启动API服务器"""
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()