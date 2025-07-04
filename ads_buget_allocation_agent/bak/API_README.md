# 🚀 预算分配Agent REST API

基于AI的广告预算分配优化服务，提供完整的REST API接口，支持数据分析、预算优化和日志记录。

## ✨ 核心功能

- 🧠 **AI预算优化** - 基于目标ROAS智能调整广告预算分配
- 📊 **数据分析** - 支持CSV文件上传和多种分析模式
- 📝 **完整日志** - 记录完整的分析过程，包括Python执行结果
- 🔗 **REST API** - 标准化API接口，支持系统集成
- 📋 **分析模板** - 预定义的分析模板，快速获得专业建议
- ⚡ **快速分析** - 支持基础、详细、自定义等多种分析模式

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install fastapi uvicorn pydantic pandas requests
```

### 2. 启动API服务器

```bash
# 方法1: 使用启动脚本（推荐）
python start_api.py

# 方法2: 直接启动
python api_server.py

# 方法3: 使用uvicorn
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### 3. 访问API文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 📱 使用方式

### 1. Python客户端使用

```python
from api_client import BudgetAllocationAPIClient

# 创建客户端
client = BudgetAllocationAPIClient("http://localhost:8000")

# 健康检查
health = client.health_check()
print(f"服务状态: {health['status']}")

# 预算分析
result = client.analyze_budget(
    daily_budget=500,
    target_roas=20,
    enable_logging=True
)

if result['success']:
    print(f"分析完成，耗时: {result['execution_time']:.2f}秒")
    print(f"日志文件: {result['log_file']}")
    print(result['result'])
else:
    print(f"分析失败: {result['error']}")
```

### 2. cURL使用

```bash
# 健康检查
curl http://localhost:8000/health

# 预算分析
curl -X POST http://localhost:8000/analyze/budget \
  -H "Content-Type: application/json" \
  -d '{
    "daily_budget": 500,
    "target_roas": 20,
    "enable_logging": true
  }'

# 快速分析
curl -X POST http://localhost:8000/analyze/quick \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "detailed"
  }'

# 上传文件
curl -X POST http://localhost:8000/upload \
  -F "file=@your_data.csv"
```

### 3. JavaScript/Fetch使用

```javascript
// 预算分析
const response = await fetch('http://localhost:8000/analyze/budget', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    daily_budget: 500,
    target_roas: 20,
    enable_logging: true
  })
});

const result = await response.json();
console.log(result);
```

## 📊 主要API端点

| 端点 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/health` | GET | 健康检查 | - |
| `/upload` | POST | 上传CSV文件 | file |
| `/files` | GET | 列出文件 | - |
| `/analyze/budget` | POST | 预算分析 | daily_budget, target_roas, file_name?, custom_query?, enable_logging? |
| `/analyze/quick` | POST | 快速分析 | file_name?, analysis_type |
| `/analyze/templates` | GET | 获取分析模板 | - |
| `/analyze/template/{name}` | POST | 使用模板分析 | template参数 |
| `/logs` | GET | 列出日志文件 | - |
| `/logs/{filename}` | GET | 获取日志内容 | - |

## 🎯 分析模板

### 1. 预算优化分析 (`budget_optimization`)

```python
result = client.analyze_with_template(
    "budget_optimization",
    daily_budget=500,
    target_roas=20
)
```

**功能**: 基于目标ROAS进行预算分配优化
**输出**: 详细的预算调整建议表格

### 2. 广告表现分析 (`performance_analysis`)

```python
result = client.analyze_with_template("performance_analysis")
```

**功能**: 分析各Campaign的表现和效果
**输出**: 表现评估和优化建议

### 3. 风险评估分析 (`risk_assessment`)

```python
result = client.analyze_with_template("risk_assessment")
```

**功能**: 评估各Campaign的投资风险
**输出**: 风险等级和风险控制建议

### 4. 数据质量检查 (`data_quality`)

```python
result = client.analyze_with_template("data_quality")
```

**功能**: 检查数据完整性和质量问题
**输出**: 数据质量报告和改进建议

## 📝 日志功能

### 完整日志记录

API支持完整的日志记录功能，包括：

- 🔧 **工具调用记录** - 记录每个工具的使用情况
- 📊 **Python执行结果** - 完整记录数据框、统计信息、图表等
- 🤖 **Agent回复** - 记录AI的分析过程和建议
- ⏰ **时间戳** - 精确的执行时间记录

### 日志文件管理

```python
# 列出日志文件
logs = client.list_log_files()
print(f"共有 {logs['total_files']} 个日志文件")

# 获取最新日志
latest_log = logs['log_files'][0]['filename']
log_content = client.get_log_file(latest_log)
print(log_content['content'])
```

## 🔧 配置选项

### 启动参数

```bash
# 指定端口
python start_api.py --port 8080

# 开发模式（自动重载）
python start_api.py --reload

# 指定主机地址
python start_api.py --host 127.0.0.1

# 检查依赖
python start_api.py --check-deps

# 显示使用示例
python start_api.py --examples
```

### 环境变量

```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export ENABLE_CORS=true
```

## 🧪 测试

### 运行测试

```bash
# 启动API服务器（另一个终端）
python start_api.py

# 运行测试
python test_api.py

# 或者使用启动脚本测试
python start_api.py --test
```

### 测试内容

- ✅ 健康检查
- ✅ 文件管理
- ✅ 快速分析
- ✅ 预算分析
- ✅ 模板分析
- ✅ 日志管理
- ✅ 错误处理
- ✅ 性能测试

## 📈 性能优化

### 1. 缓存策略

```python
# 客户端可以缓存分析结果
import hashlib

def get_cache_key(daily_budget, target_roas, file_name):
    data = f"{daily_budget}_{target_roas}_{file_name}"
    return hashlib.md5(data.encode()).hexdigest()
```

### 2. 异步处理

```python
import asyncio
import aiohttp

async def async_analyze():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:8000/analyze/budget',
            json={'daily_budget': 500, 'target_roas': 20}
        ) as response:
            return await response.json()
```

### 3. 批量处理

```python
# 批量分析多个场景
scenarios = [
    {'daily_budget': 500, 'target_roas': 15},
    {'daily_budget': 500, 'target_roas': 20},
    {'daily_budget': 500, 'target_roas': 25},
]

results = []
for scenario in scenarios:
    result = client.analyze_budget(**scenario)
    results.append(result)
```

## 🔒 安全考虑

### 1. 生产环境配置

```python
# 限制CORS域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 不要使用 "*"
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 2. 文件上传限制

```python
# 限制文件大小和类型
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = ['.csv']
```

### 3. 速率限制

```bash
# 使用nginx或其他反向代理添加速率限制
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
```

## 🐛 故障排除

### 常见问题

1. **端口占用**
   ```bash
   # 检查端口使用情况
   lsof -i :8000
   # 或使用其他端口
   python start_api.py --port 8080
   ```

2. **依赖缺失**
   ```bash
   # 检查依赖
   python start_api.py --check-deps
   # 安装缺失依赖
   pip install fastapi uvicorn pydantic pandas requests
   ```

3. **Agent初始化失败**
   ```bash
   # 检查AWS凭证
   aws sts get-caller-identity
   # 检查Bedrock权限
   aws bedrock list-foundation-models
   ```

4. **文件路径问题**
   ```bash
   # 确保数据文件存在
   ls -la 2025-03-04_input.csv
   # 检查文件权限
   chmod 644 2025-03-04_input.csv
   ```

### 日志调试

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看API日志
tail -f api_server.log
```

## 🤝 集成示例

### 1. 与现有系统集成

```python
class BudgetOptimizer:
    def __init__(self, api_url="http://localhost:8000"):
        self.client = BudgetAllocationAPIClient(api_url)
    
    def optimize_campaign_budgets(self, campaigns_data, target_roas):
        # 上传数据
        upload_result = self.client.upload_file(campaigns_data)
        file_id = upload_result['file_name']
        
        # 执行优化
        result = self.client.analyze_budget(
            daily_budget=sum(c['budget'] for c in campaigns_data),
            target_roas=target_roas,
            file_name=file_id
        )
        
        return result
```

### 2. 定时任务集成

```python
import schedule
import time

def daily_budget_optimization():
    client = BudgetAllocationAPIClient()
    result = client.analyze_budget(
        daily_budget=500,
        target_roas=20,
        enable_logging=True
    )
    
    # 发送结果到邮件或Slack
    send_notification(result)

# 每天早上9点执行
schedule.every().day.at("09:00").do(daily_budget_optimization)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 3. Web应用集成

```javascript
// React组件示例
const BudgetAnalyzer = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const analyzeBudget = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/analyze/budget', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          daily_budget: 500,
          target_roas: 20,
          enable_logging: true
        })
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('分析失败:', error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      <button onClick={analyzeBudget} disabled={loading}>
        {loading ? '分析中...' : '开始预算分析'}
      </button>
      {result && <pre>{result.result}</pre>}
    </div>
  );
};
```

## 📚 更多资源

- [完整日志指南](LOGGING_GUIDE.md)
- [API测试脚本](test_api.py)
- [Python客户端](api_client.py)
- [启动脚本](start_api.py)

## 🎉 总结

预算分配Agent REST API提供了完整的广告预算优化解决方案：

1. ✅ **易于集成** - 标准REST API，支持多种编程语言
2. ✅ **功能完整** - 从数据上传到结果分析的完整流程
3. ✅ **日志详细** - 完整记录分析过程，便于审计和调试
4. ✅ **模板丰富** - 多种预定义分析模板，快速获得专业建议
5. ✅ **性能优秀** - 支持异步处理和批量分析
6. ✅ **文档完善** - 详细的API文档和使用示例

现在你可以轻松地将AI预算优化能力集成到任何系统中！🚀