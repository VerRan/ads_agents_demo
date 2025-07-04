# 🤖 预算分配Agent

基于AI的广告预算分配优化系统，支持数据分析、预算调整建议和完整的REST API接口。

## ✨ 核心功能

- 🧠 **AI预算优化** - 基于目标ROAS智能调整广告预算分配
- 📊 **数据分析** - 深度分析广告数据，提供专业洞察
- 📝 **完整日志** - 记录完整的分析过程，包括Python执行结果
- 🔗 **REST API** - 标准化API接口，支持系统集成和自动化
- 📋 **分析模板** - 预定义的分析模板，快速获得专业建议
- ⚡ **多种模式** - 支持命令行、API、批量处理等多种使用方式

## 🚀 快速开始

### 方法1: 命令行使用

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 直接运行预算分析
python buget_allocation_agent.py

# 3. 查看生成的日志文件
ls -la budget_analysis_complete_*.txt
```

### 方法2: REST API使用

```bash
# 1. 启动API服务器
python start_api.py

# 2. 访问API文档
# http://localhost:8000/docs

# 3. 使用Python客户端
python demo_api.py
```

### 方法3: 一键演示

```bash
# 自动启动服务器并运行演示
python run_demo.py
```

## 📱 使用方式

### 1. 命令行分析

```python
# 直接运行主程序
python buget_allocation_agent.py

# 输出示例:
# 🔧 工具 #1: file_read
# 🔧 工具 #2: python_repl
# 📊 数据分析结果...
# 💰 预算调整建议...
```

### 2. Python API客户端

```python
from api_client import BudgetAllocationAPIClient

# 创建客户端
client = BudgetAllocationAPIClient("http://localhost:8000")

# 预算分析
result = client.analyze_budget(
    daily_budget=500,
    target_roas=20,
    enable_logging=True
)

print(f"分析完成，耗时: {result['execution_time']:.2f}秒")
print(f"日志文件: {result['log_file']}")
print(result['result'])
```

### 3. REST API调用

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
```

### 4. 文件上传分析

```python
# 上传自定义数据文件
upload_result = client.upload_file("your_data.csv")
file_id = upload_result['file_name']

# 使用上传的文件进行分析
result = client.analyze_budget(
    daily_budget=500,
    target_roas=20,
    file_name=file_id
)
```

## 🏗️ 项目结构

```
ads_buget_allocation_agent/
├── buget_allocation_agent.py    # 主分析程序
├── custom_callback_handler.py   # 自定义回调处理器
├── api_server.py               # REST API服务器
├── api_client.py               # Python API客户端
├── start_api.py                # API启动脚本
├── test_api.py                 # API测试脚本
├── demo_api.py                 # API演示脚本
├── run_demo.py                 # 一键演示脚本
├── simple_test.py              # 简单功能测试
├── 2025-03-04_input.csv        # 示例数据文件
├── README.md                   # 项目说明
├── API_README.md               # API详细文档
└── LOGGING_GUIDE.md            # 日志功能指南
```

## 📊 主要API端点

| 端点 | 方法 | 说明 | 示例 |
|------|------|------|------|
| `/health` | GET | 健康检查 | `curl http://localhost:8000/health` |
| `/analyze/budget` | POST | 预算分析 | 日预算500，目标ROAS 20 |
| `/analyze/quick` | POST | 快速分析 | 基础数据统计 |
| `/analyze/templates` | GET | 分析模板 | 获取可用模板列表 |
| `/upload` | POST | 上传文件 | 上传CSV数据文件 |
| `/logs` | GET | 日志管理 | 查看分析日志 |

## 🎯 分析模板

### 1. 预算优化分析
```python
result = client.analyze_with_template(
    "budget_optimization",
    daily_budget=500,
    target_roas=20
)
```
**输出**: 详细的预算调整建议表格，包括每个Campaign的当前预算、建议预算、调整幅度、风险等级等。

### 2. 广告表现分析
```python
result = client.analyze_with_template("performance_analysis")
```
**输出**: 各Campaign的表现评估、ROAS分析、优化建议。

### 3. 风险评估分析
```python
result = client.analyze_with_template("risk_assessment")
```
**输出**: 投资风险评估、风险等级分类、风险控制建议。

### 4. 数据质量检查
```python
result = client.analyze_with_template("data_quality")
```
**输出**: 数据完整性检查、质量问题识别、数据清理建议。

## 📝 日志功能

### 完整日志记录
系统支持完整的日志记录功能，解决了"终端输出包含Python执行结果但文件中没有"的问题：

- 🔧 **工具调用记录** - 记录每个工具的使用情况
- 📊 **Python执行结果** - 完整记录数据框、统计信息、图表等
- 🤖 **Agent回复** - 记录AI的分析过程和建议
- ⏰ **时间戳** - 精确的执行时间记录

### 日志文件示例
```
=== 预算分配Agent完整执行日志 ===
开始时间: 2025-07-03 14:56:34
==================================================

[14:56:38] 🔧 工具 #1: file_read
----------------------------------------

[14:56:40] 🤖 Agent回复:
----------------------------------------
我会帮您分析广告数据并给出预算调整建议...
========================================

[14:56:47] 📊 Python执行结果:
----------------------------------------
数据形状: (18, 22)
数据前几行:
    adset_id campaign_id  daily_budget  purchase  roas
0  adse_1835   camp_4441          51.1       3.0  41.8
...

预算调整建议:
| Campaign ID | 当前预算 | 当前ROAS | 调整后预算 | 调整幅度 |
| ----------- | -------- | -------- | ---------- | -------- |
| camp_0296   | $24.5    | 48.9     | $35.87     | 46.39%   |
...
========================================
```

## 🧪 测试和演示

### 运行测试
```bash
# 完整API测试
python test_api.py

# 简单功能测试
python simple_test.py

# 启动脚本测试
python start_api.py --test
```

### 运行演示
```bash
# 一键演示（推荐）
python run_demo.py

# API功能演示
python demo_api.py

# 命令行演示
python buget_allocation_agent.py
```

## 🔧 配置选项

### API服务器配置
```bash
# 指定端口
python start_api.py --port 8080

# 开发模式（自动重载）
python start_api.py --reload

# 检查依赖
python start_api.py --check-deps

# 显示使用示例
python start_api.py --examples
```

### 日志配置
```python
# 启用完整日志记录
callback_handler = create_callback_handler(
    handler_type="complete",  # 推荐：完整捕获所有输出
    log_file=None  # 自动生成文件名
)
```

## 📈 性能特点

- ⚡ **快速分析** - 基础分析通常在5-10秒内完成
- 🔄 **流式处理** - 支持实时查看分析过程
- 📊 **完整记录** - 所有Python执行结果都被完整捕获
- 🎯 **精准建议** - 基于AI的专业预算优化建议
- 🔗 **易于集成** - 标准REST API，支持多种编程语言

## 🤝 集成示例

### 1. 定时任务集成
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
```

### 2. Web应用集成
```javascript
// React组件示例
const analyzeBudget = async () => {
  const response = await fetch('/api/analyze/budget', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      daily_budget: 500,
      target_roas: 20,
      enable_logging: true
    })
  });
  
  const result = await response.json();
  setAnalysisResult(result);
};
```

### 3. 批量处理集成
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

## 🐛 故障排除

### 常见问题

1. **API服务器启动失败**
   ```bash
   # 检查端口占用
   lsof -i :8000
   # 使用其他端口
   python start_api.py --port 8080
   ```

2. **依赖包缺失**
   ```bash
   # 检查依赖
   python start_api.py --check-deps
   # 安装依赖
   pip install fastapi uvicorn pydantic pandas requests
   ```

3. **Agent初始化失败**
   ```bash
   # 检查AWS凭证
   aws sts get-caller-identity
   # 检查Bedrock权限
   aws bedrock list-foundation-models
   ```

4. **日志文件问题**
   ```bash
   # 检查日志文件
   ls -la budget_analysis_complete_*.txt
   # 查看最新日志
   tail -f budget_analysis_complete_*.txt
   ```

### 获取帮助

- 📖 **API文档**: http://localhost:8000/docs
- 📚 **详细指南**: [API_README.md](API_README.md)
- 📝 **日志指南**: [LOGGING_GUIDE.md](LOGGING_GUIDE.md)
- 🧪 **测试脚本**: `python test_api.py`

## 🎉 主要特性

### ✅ 已解决的问题
1. **Python执行结果完整捕获** - 现在可以完整记录所有print输出、数据框显示、统计信息等
2. **终端和文件输出一致** - 解决了之前终端有内容但文件缺失的问题
3. **REST API支持** - 提供完整的API接口，支持系统集成
4. **多种使用方式** - 命令行、API、批量处理等多种模式

### 🎯 核心优势
- **专业分析** - 基于AI的专业预算优化建议
- **完整记录** - 所有分析过程都被详细记录
- **易于集成** - 标准REST API，支持多种编程语言
- **灵活配置** - 支持自定义参数和分析模板
- **实时反馈** - 流式处理，实时查看分析进度

## 🚀 快速体验

```bash
# 1. 一键启动演示
python run_demo.py

# 2. 选择"运行完整演示"
# 3. 查看生成的预算优化建议
# 4. 检查完整的日志文件

# 就这么简单！🎉
```

现在你的预算分配Agent不仅能提供专业的分析建议，还能通过REST API轻松集成到任何系统中！