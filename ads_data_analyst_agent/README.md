# 🤖 AI数据分析师演示平台

一个基于AI的智能数据分析平台，支持自然语言查询、实时流式输出和REST API集成。

## ✨ 核心功能

- 🧠 **AI智能分析** - 使用自然语言提问，获得专业数据分析结果
- 🔄 **实时流式输出** - 观看AI分析过程，包括代码执行和结果生成
- 📊 **可视化界面** - 直观的Web界面，支持文件上传和历史管理
- 🔗 **REST API** - 完整的API接口，支持系统集成和自动化
- 📥 **多格式导出** - 支持Markdown、JSON、CSV等格式的报告下载
- ☁️ **云端部署** - 一键部署到AWS，支持高可用和自动扩缩容

## 🚀 快速开始

### 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务 (Web界面 + API)
python start_services.py

# 3. 访问应用
# Web界面: http://localhost:8501
# REST API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### Docker运行

```bash
# 构建并启动
docker-compose up

# 后台运行
docker-compose up -d
```

### AWS部署

```bash
# 一键部署到AWS ECS Fargate
./deploy.sh
```

## 📱 使用方式

### 1. Web界面使用

1. **上传数据** - 支持CSV文件上传或使用示例数据
2. **自然语言提问** - 例如："这个数据集有多少行？"、"哪个广告系列效果最好？"
3. **观看分析过程** - 实时查看AI执行的Python代码和结果
4. **下载报告** - 多种格式的分析报告下载

### 2. REST API使用

```python
from api_client import AIAnalystAPIClient

# 创建客户端
client = AIAnalystAPIClient("http://localhost:8000")

# 上传文件
result = client.upload_file("data.csv")
file_id = result['file_name']

# 数据分析
analysis = client.analyze_data("请分析数据的基本统计信息", file_id)
print(analysis['result'])

# 流式分析
for chunk in client.analyze_data_stream("数据质量如何？", file_id):
    print(chunk)
```

### 3. cURL示例

```bash
# 健康检查
curl http://localhost:8000/health

# 数据分析
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "这个数据集有多少行数据？"}'

# 使用分析模板
curl -X POST http://localhost:8000/analyze/template/basic_stats
```

## 🏗️ 架构概览

```
┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │
│   Web界面       │    │    REST API     │
│   :8501         │    │    :8000        │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌─────────────────┐
         │ AI分析引擎       │
         │ (Bedrock)       │
         └─────────────────┘
```

## 📊 主要API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/upload` | POST | 上传CSV文件 |
| `/analyze` | POST | 数据分析 |
| `/analyze/stream` | POST | 流式分析 |
| `/analyze/template/{key}` | POST | 模板分析 |
| `/data/preview` | POST | 数据预览 |
| `/files` | GET | 文件列表 |

## �️ 开发 指南

### 项目结构

```
ads_data_analyst_agent/
├── demo_app.py              # Streamlit Web应用
├── api_server.py            # FastAPI REST服务
├── google_ads_anlyst_agent.py # AI分析核心
├── api_client.py            # Python客户端
├── start_services.py        # 服务启动器
├── requirements.txt         # Python依赖
├── Dockerfile              # Docker配置
├── docker-compose.yml      # Docker Compose
├── deploy.sh               # AWS部署脚本
└── terraform/              # AWS基础设施代码
```

### 启动选项

```bash
# 启动所有服务
python start_services.py

# 只启动Web界面
python start_services.py --streamlit

# 只启动API服务
python start_services.py --api

# 显示帮助
python start_services.py --help
```

### 测试

```bash
# API功能测试
python test_api.py

# 本地Web界面测试
streamlit run demo_app.py
```

## ☁️ AWS部署

### 部署架构

- **ECS Fargate** - 无服务器容器运行
- **Application Load Balancer** - 负载均衡和路由
- **CloudFront** - CDN加速
- **ECR** - 容器镜像仓库
- **CloudWatch** - 监控和日志

### 部署步骤

```bash
# 1. 配置AWS凭证
aws configure

# 2. 一键部署
./deploy.sh

# 3. 访问应用
# Web界面: http://your-alb-dns/
# API服务: http://your-alb-dns/api/
```

### 成本估算

- **基础配置**: ~$70-85/月
- **包含**: 2个Fargate任务、ALB、CloudFront、日志存储

## 🔧 配置说明

### 环境变量

```bash
AWS_DEFAULT_REGION=us-east-1    # AWS区域
STREAMLIT_SERVER_HEADLESS=true  # Streamlit无头模式
```

### 自定义配置

- **修改端口**: 编辑`start_services.py`中的端口配置
- **调整资源**: 修改`terraform/variables.tf`中的CPU/内存配置
- **更换模型**: 在`google_ads_anlyst_agent.py`中配置不同的AI模型

## 📚 详细文档

- [API详细文档](docs/API_DOCUMENTATION.md)
- [AWS部署指南](docs/AWS_DEPLOYMENT_GUIDE.md)
- [REST API集成说明](docs/REST_API_INTEGRATION.md)

## 🐛 故障排除

### 常见问题

1. **端口占用**
   ```bash
   # 检查端口使用情况
   lsof -i :8501
   lsof -i :8000
   ```

2. **依赖安装失败**
   ```bash
   # 升级pip并重新安装
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **AWS部署失败**
   ```bash
   # 检查AWS凭证
   aws sts get-caller-identity
   
   # 查看详细错误
   ./deploy.sh --help
   ```

### 获取帮助

- 查看日志: `docker-compose logs`
- API状态: `curl http://localhost:8000/health`
- Web状态: 访问 `http://localhost:8501`

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

---

🚀 **开始你的AI数据分析之旅吧！**