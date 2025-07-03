# 🔗 AI数据分析师 REST API 文档

## 📋 概述

AI数据分析师REST API提供了与`google_ads_anlyst_agent.py`相同的分析能力，支持通过HTTP请求进行数据分析。

## 🚀 快速开始

### 启动服务

```bash
# 方式1: 只启动API服务
python api_server.py

# 方式2: 同时启动Web界面和API
python start_services.py

# 方式3: 使用Docker
docker-compose up
```

### 服务地址

- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **Redoc文档**: http://localhost:8000/redoc
- **Web界面**: http://localhost:8501 (如果启动)

## 📚 API端点

### 1. 健康检查

```http
GET /health
```

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "1.0.0"
}
```

### 2. 文件上传

```http
POST /upload
Content-Type: multipart/form-data

file: [CSV文件]
```

**响应示例**:
```json
{
  "success": true,
  "file_name": "uuid-generated-id",
  "file_size": 1024000,
  "rows": 10000,
  "columns": 32,
  "message": "文件上传成功，文件ID: uuid-generated-id"
}
```

### 3. 数据分析

```http
POST /analyze
Content-Type: application/json

{
  "query": "这个数据集有多少行数据？",
  "file_name": "uuid-generated-id"  // 可选，不提供则使用默认文件
}
```

**响应示例**:
```json
{
  "success": true,
  "result": "根据分析，这个数据集共有10,001行数据...",
  "execution_time": 2.5,
  "timestamp": "2024-01-01T12:00:00",
  "file_name": "uuid-generated-id"
}
```

### 4. 流式分析

```http
POST /analyze/stream
Content-Type: application/json

{
  "query": "请分析数据的基本统计信息",
  "file_name": "uuid-generated-id"
}
```

**响应格式**: Server-Sent Events (SSE)
```
data: {"type": "start", "message": "开始分析..."}

data: {"type": "chunk", "data": "正在读取数据文件..."}

data: {"type": "chunk", "data": "数据加载完成，共10000行..."}

data: {"type": "end", "message": "分析完成"}
```

### 5. 数据预览

```http
POST /data/preview?rows=10&file_name=uuid-generated-id
```

**响应示例**:
```json
{
  "rows": 10000,
  "columns": 32,
  "column_names": ["customer_name", "campaign_name", ...],
  "data_types": {"customer_name": "object", "clicks": "int64", ...},
  "sample_data": [
    {"customer_name": "客户A", "clicks": 100, ...},
    ...
  ],
  "missing_values": {"customer_name": 31, "country": 8},
  "basic_stats": {"clicks": {"mean": 150.5, "std": 89.2, ...}}
}
```

### 6. 分析模板

```http
GET /templates
```

**响应示例**:
```json
{
  "templates": {
    "basic_stats": "请分析这个数据集的基本统计信息...",
    "data_quality": "请检查数据质量，包括缺失值、重复值...",
    "key_metrics": "请分析数据中的关键业务指标...",
    ...
  },
  "usage": "使用模板key作为query参数，或者直接使用模板内容"
}
```

### 7. 使用模板分析

```http
POST /analyze/template/{template_key}?file_name=uuid-generated-id
```

**示例**:
```http
POST /analyze/template/basic_stats
```

### 8. 文件管理

```http
# 列出文件
GET /files

# 删除文件
DELETE /files/{file_id}
```

## 🐍 Python客户端使用

```python
from api_client import AIAnalystAPIClient

# 创建客户端
client = AIAnalystAPIClient("http://localhost:8000")

# 健康检查
health = client.health_check()
print(f"服务状态: {health['status']}")

# 上传文件
upload_result = client.upload_file("data.csv")
file_id = upload_result['file_name']

# 数据分析
result = client.analyze_data("这个数据集有多少行数据？", file_id)
print(f"分析结果: {result['result']}")

# 使用模板
template_result = client.analyze_with_template("basic_stats", file_id)
print(f"模板分析: {template_result['result']}")

# 流式分析
for chunk in client.analyze_data_stream("请分析数据质量", file_id):
    if chunk['type'] == 'chunk':
        print(f"接收: {chunk['data']}")
```

## 🌐 JavaScript/前端使用

```javascript
// 基本分析
async function analyzeData(query, fileId = null) {
    const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: query,
            file_name: fileId
        })
    });
    
    const result = await response.json();
    return result;
}

// 流式分析
async function streamAnalysis(query, fileId = null) {
    const response = await fetch('http://localhost:8000/analyze/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: query,
            file_name: fileId
        })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                console.log('接收数据:', data);
            }
        }
    }
}

// 使用示例
analyzeData("数据集有多少行？").then(result => {
    console.log('分析结果:', result.result);
});
```

## 🔧 cURL示例

```bash
# 健康检查
curl http://localhost:8000/health

# 上传文件
curl -X POST -F "file=@data.csv" http://localhost:8000/upload

# 数据分析
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "这个数据集有多少行数据？"}'

# 使用模板
curl -X POST http://localhost:8000/analyze/template/basic_stats

# 数据预览
curl -X POST "http://localhost:8000/data/preview?rows=5"
```

## 🚀 部署到AWS

API服务已集成到Docker和AWS部署配置中：

```bash
# 本地Docker测试
docker-compose up

# 部署到AWS ECS
./deploy.sh
```

部署后的访问地址：
- **Web界面**: http://your-alb-dns-name/
- **API服务**: http://your-alb-dns-name/api/
- **API文档**: http://your-alb-dns-name/api/docs

## 📊 性能特点

- **并发支持**: FastAPI异步处理，支持多并发请求
- **流式响应**: 支持Server-Sent Events，实时返回分析过程
- **文件管理**: 支持多文件上传和管理
- **模板系统**: 预定义分析模板，快速执行常用分析
- **错误处理**: 完善的错误处理和状态码

## 🔒 安全考虑

- **CORS配置**: 生产环境需要限制允许的域名
- **文件上传**: 限制文件大小和类型
- **输入验证**: 对所有输入进行验证
- **认证授权**: 生产环境建议添加API密钥或JWT认证

## 🐛 故障排除

### 常见问题

1. **连接失败**
   ```bash
   # 检查服务是否启动
   curl http://localhost:8000/health
   ```

2. **文件上传失败**
   - 检查文件格式是否为CSV
   - 检查文件大小是否过大

3. **分析超时**
   - 复杂查询可能需要更长时间
   - 考虑使用流式分析

### 调试模式

```bash
# 启动时启用调试日志
uvicorn api_server:app --host 0.0.0.0 --port 8000 --log-level debug
```

---

🎉 **现在你可以通过REST API享受与Web界面相同的AI数据分析能力！**