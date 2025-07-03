#!/usr/bin/env python3
"""
AI数据分析师 REST API服务器
提供google_ads_anlyst_agent.py的API接口
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import pandas as pd
import json
import io
import os
import uuid
import asyncio
from datetime import datetime
import logging

# 导入现有的分析代理
from google_ads_anlyst_agent import agent, get_llm, filename as default_filename

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="AI数据分析师 API",
    description="基于AI的数据分析服务，支持自然语言查询和数据分析",
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
class AnalysisRequest(BaseModel):
    query: str
    file_name: Optional[str] = None
    stream: Optional[bool] = False

class AnalysisResponse(BaseModel):
    success: bool
    result: str
    execution_time: float
    timestamp: str
    file_name: Optional[str] = None

class FileUploadResponse(BaseModel):
    success: bool
    file_name: str
    file_size: int
    rows: int
    columns: int
    message: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# 全局变量存储上传的文件信息
uploaded_files: Dict[str, Dict[str, Any]] = {}

@app.get("/", response_model=Dict[str, str])
async def root():
    """根路径，返回API信息"""
    return {
        "message": "AI数据分析师 API服务",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
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
            message=f"文件上传成功，文件ID: {file_id}"
        )
        
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@app.get("/files")
async def list_files():
    """列出已上传的文件"""
    return {
        "uploaded_files": uploaded_files,
        "default_file": default_filename
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_data(request: AnalysisRequest):
    """分析数据"""
    try:
        start_time = datetime.now()
        
        # 确定要使用的文件
        if request.file_name:
            if request.file_name in uploaded_files:
                file_path = uploaded_files[request.file_name]["file_path"]
                query = f"当前目录{file_path}的文件，{request.query}"
            else:
                raise HTTPException(status_code=404, detail="文件未找到")
        else:
            # 使用默认文件
            query = f"当前目录{default_filename}的文件，{request.query}"
            request.file_name = default_filename
        
        # 执行分析
        result = agent(query)
        
        # 计算执行时间
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return AnalysisResponse(
            success=True,
            result=str(result),
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
            file_name=request.file_name
        )
        
    except Exception as e:
        logger.error(f"数据分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"数据分析失败: {str(e)}")

@app.post("/analyze/stream")
async def analyze_data_stream(request: AnalysisRequest):
    """流式分析数据"""
    try:
        # 确定要使用的文件
        if request.file_name:
            if request.file_name in uploaded_files:
                file_path = uploaded_files[request.file_name]["file_path"]
                query = f"当前目录{file_path}的文件，{request.query}"
            else:
                raise HTTPException(status_code=404, detail="文件未找到")
        else:
            query = f"当前目录{default_filename}的文件，{request.query}"
        
        async def generate_stream():
            """生成流式响应"""
            try:
                # 这里可以实现真正的流式处理
                # 目前先模拟分块返回结果
                yield f"data: {json.dumps({'type': 'start', 'message': '开始分析...'})}\n\n"
                
                result = agent(query)
                
                # 将结果分块发送
                result_str = str(result)
                chunk_size = 100
                for i in range(0, len(result_str), chunk_size):
                    chunk = result_str[i:i+chunk_size]
                    yield f"data: {json.dumps({'type': 'chunk', 'data': chunk})}\n\n"
                    await asyncio.sleep(0.1)  # 模拟流式延迟
                
                yield f"data: {json.dumps({'type': 'end', 'message': '分析完成'})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
        
    except Exception as e:
        logger.error(f"流式分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"流式分析失败: {str(e)}")

@app.get("/analyze/history")
async def get_analysis_history():
    """获取分析历史（简单实现）"""
    # 这里可以实现真正的历史记录存储
    return {
        "message": "分析历史功能待实现",
        "suggestion": "可以集成数据库存储历史记录"
    }

@app.post("/data/preview")
async def preview_data(file_name: Optional[str] = None, rows: int = 10):
    """预览数据"""
    try:
        if file_name and file_name in uploaded_files:
            file_path = uploaded_files[file_name]["file_path"]
        else:
            file_path = default_filename
        
        # 读取数据
        df = pd.read_csv(file_path)
        
        # 返回预览数据
        preview_data = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "sample_data": df.head(rows).to_dict(orient="records"),
            "missing_values": df.isnull().sum().to_dict(),
            "basic_stats": df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {}
        }
        
        return preview_data
        
    except Exception as e:
        logger.error(f"数据预览失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"数据预览失败: {str(e)}")

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """删除上传的文件"""
    try:
        if file_id not in uploaded_files:
            raise HTTPException(status_code=404, detail="文件未找到")
        
        # 删除物理文件
        file_path = uploaded_files[file_id]["file_path"]
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 从内存中删除记录
        del uploaded_files[file_id]
        
        return {"success": True, "message": f"文件 {file_id} 已删除"}
        
    except Exception as e:
        logger.error(f"文件删除失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件删除失败: {str(e)}")

# 预定义的分析模板
ANALYSIS_TEMPLATES = {
    "basic_stats": "请分析这个数据集的基本统计信息，包括数据规模、数据类型、缺失值情况等",
    "data_quality": "请检查数据质量，包括缺失值、重复值、异常值等问题",
    "key_metrics": "请分析数据中的关键业务指标，找出重要的数据洞察",
    "missing_values": "数据中有多少缺失值？",
    "data_shape": "这个数据集有多少行多少列？",
    "column_info": "请介绍一下数据集中各个列的含义和数据类型"
}

@app.get("/templates")
async def get_analysis_templates():
    """获取预定义的分析模板"""
    return {
        "templates": ANALYSIS_TEMPLATES,
        "usage": "使用模板key作为query参数，或者直接使用模板内容"
    }

@app.post("/analyze/template/{template_key}")
async def analyze_with_template(template_key: str, file_name: Optional[str] = None):
    """使用预定义模板进行分析"""
    if template_key not in ANALYSIS_TEMPLATES:
        raise HTTPException(status_code=404, detail="模板未找到")
    
    request = AnalysisRequest(
        query=ANALYSIS_TEMPLATES[template_key],
        file_name=file_name
    )
    
    return await analyze_data(request)

if __name__ == "__main__":
    import uvicorn
    
    # 启动服务器
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )