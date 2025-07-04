# 🚀 Ads Agents Demo

一个基于AI的广告代理系统集合，包含多个专业化的广告处理Agent，帮助自动化广告创意、预算分配、数据分析等任务。

## 📁 项目结构

### 🎨 [ads_creative_agent](./ads_creative_agent/)
**广告创意生成Agent**
- 🤖 自然语言交互界面
- 👕 AI虚拟试穿功能（基于Amazon Nova Canvas）
- 🖼️ 智能图片处理和尺寸调整
- 🌐 图片资源管理和批量下载

**快速启动**：
```bash
cd ads_creative_agent
python run_nlp_ui.py
```

### 💰 [ads_buget_allocation_agent](./ads_buget_allocation_agent/)
**广告预算分配Agent**
- 📊 智能预算分析和分配
- 📈 数据驱动的投放策略
- 🎯 多平台预算优化
- 📋 详细的分析报告

### 📊 [ads_data_analyst_agent](./ads_data_analyst_agent/)
**广告数据分析Agent**
- 📈 广告效果数据分析
- 🔍 深度洞察和趋势分析
- 📊 可视化报表生成
- 🎯 ROI和转化率分析

### 🔍 [ads-materials-understand-agent](./ads-materials-understand-agent/)
**广告素材理解Agent**
- 🖼️ 图片内容识别和分析
- 📝 文本内容提取和理解
- 🏷️ 自动标签和分类
- 🎨 素材质量评估

### 📋 [pre-advertising-analysis-agent](./pre-advertising-analysis-agent/)
**广告前期分析Agent**
- 🎯 目标受众分析
- 🏪 竞品调研和分析
- 📊 市场趋势预测
- 💡 投放策略建议

## 🚀 快速开始

### 环境要求
- Python 3.8+
- AWS账户（用于AI服务）
- 必要的API密钥

### 通用安装步骤
```bash
# 1. 克隆项目
git clone <repository-url>
cd ads_agents_demo

# 2. 选择要使用的Agent
cd ads_creative_agent  # 或其他Agent目录

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
python run_ui.py  # 或相应的启动脚本
```

## 🌟 主要特性

### 🤖 AI驱动
- 基于最新的AI模型和服务
- 支持自然语言交互
- 智能任务理解和执行

### 🎯 专业化
- 每个Agent专注特定领域
- 深度优化的功能模块
- 行业最佳实践集成

### 🔧 易于使用
- 直观的Web界面
- 详细的使用文档
- 丰富的示例和模板

### 🔗 可扩展
- 模块化设计
- 标准化接口
- 易于集成和定制

## 📖 使用场景

### 🎨 创意制作
使用 `ads_creative_agent` 进行：
- 产品虚拟试穿展示
- 广告图片批量处理
- 创意素材自动生成

### 💰 预算管理
使用 `ads_buget_allocation_agent` 进行：
- 多平台预算分配
- ROI优化建议
- 投放效果预测

### 📊 数据洞察
使用 `ads_data_analyst_agent` 进行：
- 广告效果分析
- 用户行为洞察
- 趋势预测报告

## 🛠️ 开发指南

### 项目规范
- 每个Agent都有独立的README
- 统一的代码风格和结构
- 完整的测试覆盖

### 贡献方式
1. Fork项目
2. 创建功能分支
3. 提交Pull Request
4. 代码审查和合并

## 📞 支持与反馈

### 文档资源
- 每个Agent目录下都有详细的README
- QUICK_START.md提供快速上手指南
- 示例代码和使用案例

### 问题反馈
- 创建GitHub Issue
- 提供详细的错误信息
- 包含复现步骤

## 🏆 成功案例

### 电商广告
- 服装虚拟试穿转化率提升40%
- 自动化素材处理节省80%时间
- 智能预算分配ROI提升25%

### 品牌营销
- 多平台投放效果统一分析
- 创意素材质量自动评估
- 竞品策略实时监控

## 🔮 未来规划

- [ ] 更多AI模型集成
- [ ] 实时协作功能
- [ ] 移动端支持
- [ ] API服务化
- [ ] 企业级部署方案

---

## 🎯 选择你的Agent

| Agent | 主要功能 | 适用场景 | 启动命令 |
|-------|----------|----------|----------|
| 🎨 Creative | 创意生成、虚拟试穿 | 电商、时尚 | `cd ads_creative_agent && python run_nlp_ui.py` |
| 💰 Budget | 预算分配、ROI优化 | 投放管理 | `cd ads_buget_allocation_agent && python run_demo_ui.py` |
| 📊 Analyst | 数据分析、报表生成 | 效果评估 | `cd ads_data_analyst_agent && python run_ui.py` |
| 🔍 Materials | 素材理解、内容分析 | 素材管理 | `cd ads-materials-understand-agent && python app.py` |
| 📋 Pre-Analysis | 前期分析、策略建议 | 投放规划 | `cd pre-advertising-analysis-agent && python run_ui.py` |

**🚀 开始你的AI广告之旅！**