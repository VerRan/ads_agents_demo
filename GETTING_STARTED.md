# 🚀 Getting Started - Ads Agents Demo

## 选择你的第一个Agent

### 🎨 推荐：从创意Agent开始
如果你是第一次使用，推荐从**广告创意Agent**开始：

```bash
cd ads_creative_agent
pip install -r requirements.txt
python run_nlp_ui.py
```

然后在浏览器中访问 http://localhost:8503

### 💬 试试自然语言交互
在界面顶部输入：
```
用lht.jpg试穿这个衣服：https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg
```

点击"🚀 执行任务"，看看AI如何理解并执行你的指令！

## 🎯 各Agent特色功能

### 🎨 Creative Agent - 最受欢迎
**特色**：自然语言交互 + AI虚拟试穿
```bash
cd ads_creative_agent
python run_nlp_ui.py
```
**试试这个**：
- "用我的照片试穿这件衣服：[URL]"
- "下载并处理这些图片：[URLs]"

### 💰 Budget Agent - 数据驱动
**特色**：智能预算分配 + ROI优化
```bash
cd ads_buget_allocation_agent
python run_demo_ui.py
```
**试试这个**：
- 上传广告数据CSV文件
- 查看智能预算分配建议

### 📊 Data Analyst - 深度洞察
**特色**：广告效果分析 + 可视化报表
```bash
cd ads_data_analyst_agent
python run_ui.py
```

### 🔍 Materials Understanding - 内容识别
**特色**：图片内容分析 + 自动标签
```bash
cd ads-materials-understand-agent
python app.py
```

### 📋 Pre-Analysis - 策略规划
**特色**：市场分析 + 投放建议
```bash
cd pre-advertising-analysis-agent
python run_ui.py
```

## ⚡ 5分钟体验流程

### 步骤1：环境准备（1分钟）
```bash
# 确保Python 3.8+已安装
python --version

# 配置AWS（如果使用AI功能）
aws configure  # 可选，某些功能需要
```

### 步骤2：选择Agent（1分钟）
```bash
# 推荐从创意Agent开始
cd ads_creative_agent
```

### 步骤3：安装依赖（2分钟）
```bash
pip install -r requirements.txt
```

### 步骤4：启动体验（1分钟）
```bash
python run_nlp_ui.py
```

浏览器自动打开，开始体验！

## 🎪 Demo场景

### 场景1：电商服装试穿
1. 准备一张人物照片
2. 找一个服装商品URL
3. 输入："用[照片]试穿这个衣服：[URL]"
4. 查看AI生成的试穿效果

### 场景2：广告素材批量处理
1. 收集多个商品图片URL
2. 输入："下载并处理这些图片：[URLs]"
3. 获得符合平台要求的处理后图片

### 场景3：预算智能分配
1. 准备广告投放数据
2. 上传到预算分配Agent
3. 获得数据驱动的预算建议

## 🔧 常见问题

### Q: 需要什么技术背景？
A: 不需要！界面友好，支持自然语言交互

### Q: 需要付费API吗？
A: 部分AI功能需要AWS账户，但有免费额度

### Q: 可以离线使用吗？
A: 基础功能可以，AI功能需要网络连接

### Q: 支持哪些图片格式？
A: PNG, JPEG, JPG等常见格式

### Q: 如何获得帮助？
A: 每个Agent都有详细README和示例

## 🎯 下一步

### 深入学习
- 查看各Agent的详细README
- 尝试不同的任务类型
- 探索高级功能

### 定制开发
- 修改界面和功能
- 集成到现有系统
- 开发新的Agent

### 分享反馈
- 创建Issue报告问题
- 分享使用心得
- 贡献代码改进

---

**🎉 开始探索AI广告的无限可能！**