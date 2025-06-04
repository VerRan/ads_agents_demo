# 视频分类助手

基于 Amazon Nova Pro 和 Streamlit 构建的视频分类应用，可以理解和分类视频内容。该应用使用先进的AI模型分析视频，并将其归类到预定义的278个类别中。

## 功能特点

- 上传视频文件（支持mp4, mov, avi格式）
- 通过URL下载并分析视频
- 使用 Amazon Nova Pro 理解视频内容
- 将视频自动分类到278个预定义类别中
- 显示详细的分类结果
- 用户友好的界面，支持视频预览

## 技术架构

- **前端**: Streamlit - 提供简洁直观的用户界面
- **AI模型**: Amazon Bedrock (Nova Pro) - 用于视频理解和内容分析
- **代理框架**: Strands - 用于构建和管理AI代理
- **AWS SDK**: Boto3 - 与AWS服务交互
- **视频处理**: ffmpeg-python - 处理视频文件
- **网络请求**: Requests - 用于从URL下载视频

## 安装步骤

1. 克隆仓库:
```bash
git clone <repository-url>
cd ads-videos-classify-agent
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 确保已配置 AWS 凭证:
```bash
aws configure
```

4. 确保您有权限访问 Amazon Bedrock 的 Nova Pro 模型

## 运行应用

```bash
streamlit run app.py
```

应用将在本地启动，通常可以通过浏览器访问 http://localhost:8501

## 使用方法

### 方法一：上传本地视频文件

1. 打开浏览器访问 Streamlit 应用（通常是 http://localhost:8501）
2. 选择"上传视频文件"选项卡
3. 上传视频文件（支持 mp4, mov, avi 格式）
4. 点击"分析上传的视频"按钮
5. 等待处理完成（处理时间取决于视频大小和复杂度）
6. 查看视频内容理解结果和分类结果

### 方法二：通过URL分析视频

1. 打开浏览器访问 Streamlit 应用
2. 选择"输入视频URL"选项卡
3. 输入视频的URL地址
4. 点击"分析URL视频"按钮
5. 系统会自动下载视频并进行分析
6. 查看视频内容理解结果和分类结果

## 分类类别

应用支持278个预定义类别，包括但不限于：
- 电子产品（手机、电脑、家电等）
- 服装鞋帽（T恤、裤子、鞋子等）
- 家居用品（家具、装饰品等）
- 美妆护肤（化妆品、护肤品等）
- 母婴产品（婴儿用品、玩具等）
- 宠物用品（宠物食品、玩具等）
- 运动户外（健身器材、运动服装等）
- 食品饮料（零食、饮料等）

完整类别列表可在应用中查看。

## 项目结构

```
ads-videos-classify-agent/
├── app.py                # Streamlit应用主文件
├── agent.py              # AI代理定义和工具函数
│   ├── video_understand  # 视频内容理解工具
│   ├── video_classify    # 视频分类工具
│   └── download_video    # 从URL下载视频工具
├── requirements.txt      # 项目依赖
├── README.md             # 项目说明
└── temp/                 # 临时文件存储目录（自动创建）
```

## 核心功能实现

### 视频内容理解

使用 Amazon Bedrock 的 Nova Pro 模型分析视频内容，理解视频中发生的事件、对象和场景。

### 视频分类

基于视频内容理解结果，使用 Nova Pro 模型将视频分类到预定义的278个类别中。

### 视频下载

支持从URL下载视频文件到本地进行分析，使用 requests 库实现高效下载。

## 注意事项

- 视频文件大小可能会影响处理时间
- 确保您的AWS账户有足够的权限访问Bedrock服务
- 处理大型视频文件可能会产生额外的AWS费用
- 从URL下载视频时，确保URL是公开可访问的

## 贡献指南

欢迎提交问题和改进建议！请通过以下方式参与：
1. Fork 项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件
