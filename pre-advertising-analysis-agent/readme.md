# 🚀 广告分析模块 (Ads Analysis Module)

## 概述

广告分析模块是AI广告分析套件的核心组件，专注于提供全面的网站分析和广告策略开发功能。该模块结合了先进的AI技术和数据分析能力，帮助营销人员和广告专业人士做出数据驱动的决策。

## 主要功能

### 1. 网站深度分析
- **产品分析**: 深入了解产品定位、特点、产品线和价格策略
- **竞品分析**: 识别主要竞争对手，比较差异和优势
- **市场分析**: 分析市场规模、趋势和机会
- **受众分析**: 研究目标受众特征和行为

### 2. 浏览器自动化
- **AI驱动**: 使用Amazon Bedrock Claude模型控制浏览器
- **实时可视化**: 通过VNC/CDP查看浏览器操作过程
- **灵活配置**: 可调整执行步数和连接参数
- **自动报告**: 生成结构化分析报告

### 3. 综合UI界面
- **统一入口**: 集成网站分析和视频分类功能
- **多模式切换**: 在不同分析模式间无缝切换
- **结果整合**: 汇总多种分析结果生成综合报告
- **智能助手**: 提供基于对话的分析支持

## 技术架构

### 核心组件
- **Streamlit**: 提供交互式Web界面
- **Strands Agent**: 实现AI代理功能
- **Exa API**: 用于网站内容搜索和分析
- **Browser-Use**: 实现浏览器自动化
- **AWS Bedrock**: 提供Claude 3.7 Sonnet模型支持

### 文件结构
```
ads_analysis/
├── combined_ads_ui.py         # 综合UI界面实现
├── ads_analysis_agent.py      # 广告分析代理实现
├── browser_use/               # 浏览器自动化相关模块
│   ├── browser.py            # 浏览器控制核心
│   └── controller/           # 浏览器控制器
├── requirements.txt           # 基本依赖项
└── combined_requirements.txt  # 综合UI的完整依赖项
```

## 安装指南

### 环境要求
- Python 3.8+
- Chrome/Chromium浏览器 (用于浏览器自动化)
- FFmpeg (用于视频处理，如与视频分析模块集成)

### 依赖安装
```bash
# 安装基本依赖
pip install -r requirements.txt

# 安装综合UI的完整依赖
pip install -r combined_requirements.txt

# 安装Chrome/Chromium (Amazon Linux 2023)
sudo dnf install chromium

# 或使用Flatpak安装
sudo dnf install flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.chromium.Chromium
```

### 环境变量配置
```bash
# EXA API配置
export API_KEY="your-exa-api-key"

# AWS配置
export AWS_ACCESS_KEY_ID="your-aws-access-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

## 使用指南

### 启动综合UI
```bash
# 直接运行Streamlit应用
streamlit run combined_ads_ui.py

# 或使用启动脚本
python run_combined_ui.py
```

### 浏览器自动化设置
1. 启动带有CDP支持的Chrome/Chromium:
```bash
# 本地Chrome
google-chrome --remote-debugging-port=9222

# Flatpak安装的Chromium
flatpak run org.chromium.Chromium --remote-debugging-port=9222

# 无头模式
flatpak run org.chromium.Chromium --headless --remote-debugging-port=9222
```

2. 设置VNC服务器(可选，用于远程查看):
```bash
docker run -p 6081:6081 -p 5901:5901 -d --name vnc-browser dorowu/ubuntu-desktop-lxde-vnc
```

### 网站分析示例
```python
from ads_analysis.ads_analysis_agent import Agent

# 创建分析代理
agent = Agent(system_prompt="你是一名资深的广告分析师")

# 执行网站分析
analysis = agent.analyze("https://example.com")
print(analysis)
```

## 最新更新

### 综合UI改进
- 添加了表单提交功能，提高用户体验
- 实现了条件性VNC查看器显示，优化资源使用
- 改进了浏览器自动化界面，采用左右布局
- 增强了CDP连接配置选项

### 浏览器自动化增强
- 支持自定义CDP URL配置
- 添加了浏览器操作实时查看功能
- 优化了任务执行流程和状态反馈

## 故障排除

### 常见问题

1. **浏览器连接失败**
   - 确保Chrome/Chromium已启动并开启了远程调试端口
   - 验证CDP URL是否正确(默认为http://localhost:9222)
   - 检查网络连接和防火墙设置

2. **VNC查看器不显示**
   - 确保VNC服务器已启动并正常运行
   - 验证端口映射是否正确(默认6081)
   - 尝试在新标签页直接访问VNC URL

3. **API认证错误**
   - 确保已正确设置EXA_API_KEY环境变量
   - 验证AWS凭证是否有效且具有必要权限

## 未来计划

- [ ] 添加更多数据可视化组件
- [ ] 支持多语言分析和报告
- [ ] 集成更多广告平台数据源
- [ ] 开发API接口供外部系统调用

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 开发环境设置
```bash
git clone https://github.com/VerRan/ads_agents_demo.git
cd ads_agents_demo/ads_analysis
pip install -r combined_requirements.txt
```

### 代码规范
- 遵循Python PEP 8编码规范
- 添加适当的注释和文档字符串
- 确保所有功能都有错误处理

---

📊 **使用广告分析模块，让数据驱动您的广告决策！**
